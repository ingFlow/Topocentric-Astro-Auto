"""
batch/pssr_window.py - the PSSR window-narrowing pipeline: sweep and
per-point stage evaluation.

Architectural layer: batch/ (new for this feature). This module
implements the kinematics of the algorithm contract - the grid sweep
(spec v5 section 3.2), the point-set membership rules (section 3.3),
majors-only aspect evaluation over raw degrees with the 12'/18'/32' orb
rules (section 3.4), stage 1 fast-to-slow (section 3.5), stage 2
moon-to-slow + fast-to-fast (section 3.6), and per-tuple interval
building with per-stage per-event unions (section 3.7).

Phase note (Step 5): the relevance gates are wired to the compendium
lookups (sections 4.1/4.2) - pass a `Compendium` into the stage/evaluation
functions (the Step-6 entry point loads one by default). With
`compendium=None` the gates stay OPEN (the Step-4 kinematics mode used by
the isolated stage tests). The range/consensus/margin/report machinery
(sections 3.8-3.10) and the batch entry point narrow_birth_time_window
land in Step 6. See the spec's section 9 future-research register for
what is deliberately outside this feature.

All decisions read from `pssr_window_config`; there are no hardcoded
business values in this module. Pure functions, no globals. Point names
are the codebase's PLANETS names ('Mercury', ..., 'Mean_Node'); the
config's Planet codes are the same strings; the compendium lookups map
them via to_compendium_symbol.
"""

import julian

from topo_astro.core.aspects import calculate_aspect, MAJOR_ASPECTS
from topo_astro.core.constants import calc_planets_labelled, calc_planets_labelled_speeds
from topo_astro.significators.compendium import to_compendium_symbol
from topo_astro.techniques.pssr import PSSR_Auto
from topo_astro.batch import pssr_window_config as config


# --- relevance gates (Step 5: wired to the compendium; None = Step-4 mode) ---

def _pair_relevance(compendium, event_id, point_a, point_b):
    """Section 4.1 wiring: the unordered pair (fast, slow), mapped to
    compendium symbols, resolves against the Juan Combos pairwise table.
    Returns (tier, no_data): tier in {"strong", "weak", "excluded",
    "absent"}; no_data is True when the event has no compendium event at
    all, or its event is one of the three marked-none events (its stage-1
    contribution is reported as `no_data`, never silently absent).
    With compendium=None (Step-4 kinematics mode) every pair reads as
    ("strong", False)."""
    if compendium is None:
        return "strong", False
    if compendium.event_title_for(event_id) is None:
        return "absent", True
    if not compendium.has_pair_data(event_id):
        return "absent", True
    strength = compendium.pair_strength(
        event_id, to_compendium_symbol(point_a), to_compendium_symbol(point_b)
    )
    return ("absent" if strength is None else strength), False


def _tier_for(compendium, event_id, symbol):
    """Section 4.2 wiring: the slow point's tier_score from the scoring
    JSON. Returns (tier_score | None, no_data); the caller compares
    against STAGE2_TIER_FLOOR and an absent key fails closed. With
    compendium=None (Step-4 kinematics mode) the gate reads as open."""
    if compendium is None:
        return 10, False
    if compendium.event_title_for(event_id) is None:
        return None, True
    return compendium.tier_score(event_id, to_compendium_symbol(symbol)), False


# --- sweep (spec section 3.2) ------------------------------------------------

def sweep_jds(dt_radix_start, dt_radix_end, step_seconds=None):
    """The section-3.2 grid: candidate radix times from dt_radix_start to
    dt_radix_end inclusive, `step_seconds` apart (default = STEP_SECONDS).
    Yields Julian dates."""
    if step_seconds is None:
        step_seconds = config.STEP_SECONDS
    start_jd = julian.to_jd(dt_radix_start)
    end_jd = julian.to_jd(dt_radix_end)
    step_jd = float(step_seconds) / 86400.0
    count = int(round((end_jd - start_jd) / step_jd))
    for i in range(count + 1):
        yield start_jd + i * step_jd


# --- aspect evaluation (spec section 3.4) ------------------------------------

def _moon_aspect(progressed_long, radix_long):
    """Major aspect where the Moon is a party (section 3.4): the 32'
    conj/opp orb applies to conjunction and opposition ONLY; every other
    major uses the general 18' orb. (calculate_aspect evaluates all majors
    within the orb it is given, so the wider attempt must be name-gated.)"""
    aspect = calculate_aspect(progressed_long, radix_long, config.ORB_MOON_CONJ_OPP_DEG, True)
    if aspect and aspect[0] in ("conjunction", "opposition"):
        return aspect
    aspect = calculate_aspect(progressed_long, radix_long, config.ORB_MOON_GENERAL_ARC_MIN / 60.0, True)
    if aspect and aspect[0] not in ("conjunction", "opposition"):
        return aspect
    return None


def _aspect_pair(progressed_long, radix_long, moon_party):
    """Major aspect between two longitudes with the section-3.4 orb rules.
    Returns (aspect_name, separation_deg) or None. The Moon gets 32' for
    conjunction/opposition and the general 18' orb otherwise; non-Moon
    pairs get the flat 12' orb."""
    if moon_party:
        return _moon_aspect(progressed_long, radix_long)
    return calculate_aspect(progressed_long, radix_long, config.ORB_FAST_SLOW_DEG, True)


def _minor_near_miss(progressed_long, radix_long, moon_party):
    """If the major check found nothing, look for a minor aspect inside the
    applicable orb (the non-conj/opp orb). Returns (aspect_name,
    separation_deg) or None. Minors are recorded in the near-miss ledger,
    never gating."""
    if moon_party:
        orb = config.ORB_MOON_GENERAL_ARC_MIN / 60.0
    else:
        orb = config.ORB_FAST_SLOW_DEG
    aspect = calculate_aspect(progressed_long, radix_long, orb, False)
    if aspect and aspect[0] not in MAJOR_ASPECTS:
        return aspect
    return None


def _speed_ok(speed):
    """Section 3.5/3.6 speed gate: |daily motion| >= the floor (30'/day;
    retrograde handled by magnitude - SPEED_FLOOR_USE_ABSOLUTE)."""
    floor = config.SPEED_FLOOR_ARC_MIN_PER_DAY / 60.0
    if config.SPEED_FLOOR_USE_ABSOLUTE:
        return abs(speed) >= floor
    return speed >= floor


# --- stage evaluations (spec sections 3.5, 3.6) ------------------------------

def _hit(jd, stage, arm, variant, progressed_point, radix_point, aspect, separation, prog_speed, radix_speed):
    return {
        "jd": jd,
        "stage": stage,
        "arm": arm,
        "variant": variant,
        "progressed_point": progressed_point,
        "radix_point": radix_point,
        "aspect": aspect,
        "separation_deg": separation,
        "progressed_speed": prog_speed,
        "radix_speed": radix_speed,
    }


def _near_miss(jd, stage, arm, variant, progressed_point, radix_point, kind, **extra):
    entry = {
        "jd": jd,
        "stage": stage,
        "arm": arm,
        "variant": variant,
        "progressed_point": progressed_point,
        "radix_point": radix_point,
        "kind": kind,
    }
    entry.update(extra)
    return entry


def stage1_hits(jd, variant, progressed, progressed_speeds, radix, radix_speeds, event_id, compendium=None):
    """Section 3.5: one point from FAST_SET, the other from SLOW_SET, either
    side progressed or radix (Case A: fast progressed / Case B: fast radix).
    Orb 12' (no Moon by construction). Speed gate on the fast point, measured
    on the side it sits (progressed-side -> progressed speed, radix-side ->
    natal speed). Relevance gate per section 4.1 (strong only; weak /
    excluded / absent / no-data go to the near-miss ledger). Returns
    (hits, near_misses)."""
    hits, misses = [], []
    floor_kind = "speed_below_floor"

    def check(prog_name, prog_long, rad_name, rad_long, fast_name, fast_speed):
        if not _speed_ok(fast_speed):
            misses.append(_near_miss(
                jd, 1, "fast_to_slow", variant, prog_name, rad_name, floor_kind,
                speed_deg_per_day=fast_speed, aspect=None,
            ))
            return
        aspect = _aspect_pair(prog_long, rad_long, moon_party=False)
        if not aspect:
            minor = _minor_near_miss(prog_long, rad_long, moon_party=False)
            if minor:
                misses.append(_near_miss(
                    jd, 1, "fast_to_slow", variant, prog_name, rad_name, "minor_aspect",
                    aspect=minor[0], separation_deg=minor[1],
                ))
            return
        aspect_name, separation = aspect
        relevance, no_data = _pair_relevance(compendium, event_id, prog_name, rad_name)
        if no_data:
            misses.append(_near_miss(
                jd, 1, "fast_to_slow", variant, prog_name, rad_name, "no_data",
                aspect=aspect_name, separation_deg=separation,
            ))
        elif relevance == config.PAIR_RELEVANCE_MIN:
            hits.append(_hit(
                jd, 1, "fast_to_slow", variant, prog_name, rad_name,
                aspect_name, separation, progressed_speeds.get(prog_name), radix_speeds.get(rad_name),
            ))
        else:
            misses.append(_near_miss(
                jd, 1, "fast_to_slow", variant, prog_name, rad_name,
                f"{relevance}_relevance", aspect=aspect_name, separation_deg=separation,
            ))

    for prog_name, prog_long in progressed.items():
        if prog_name not in config.FAST_SET:
            continue
        for rad_name, rad_long in radix.items():
            if rad_name not in config.SLOW_SET:
                continue
            check(prog_name, prog_long, rad_name, rad_long, prog_name, progressed_speeds[prog_name])

    for prog_name, prog_long in progressed.items():
        if prog_name not in config.SLOW_SET:
            continue
        for rad_name, rad_long in radix.items():
            if rad_name not in config.FAST_SET:
                continue
            check(prog_name, prog_long, rad_name, rad_long, rad_name, radix_speeds[rad_name])

    return hits, misses


def stage2_hits(jd, variant, progressed, progressed_speeds, radix, radix_speeds, event_id, compendium=None):
    """Section 3.6. Arm 1: progressed Moon vs one SLOW_SET target (no speed
    gate - the Moon's minimum motion makes it vacuous; relevance = the slow
    point's tier_score >= STAGE2_TIER_FLOOR, absent key fails closed).
    Arm 2: both points from FAST_FAST_SET, one per side, both points
    individually clearing the speed floor; Moon party -> 18'/32' orbs.
    Returns (hits, near_misses)."""
    hits, misses = [], []

    if config.MOON in progressed:
        moon_long = progressed[config.MOON]
        for rad_name, rad_long in radix.items():
            if rad_name not in config.SLOW_SET:
                continue
            aspect = _aspect_pair(moon_long, rad_long, moon_party=True)
            if not aspect:
                minor = _minor_near_miss(moon_long, rad_long, moon_party=True)
                if minor:
                    misses.append(_near_miss(
                        jd, 2, "moon_to_slow", variant, config.MOON, rad_name, "minor_aspect",
                        aspect=minor[0], separation_deg=minor[1],
                    ))
                continue
            aspect_name, separation = aspect
            tier, no_data = _tier_for(compendium, event_id, rad_name)
            if no_data:
                misses.append(_near_miss(
                    jd, 2, "moon_to_slow", variant, config.MOON, rad_name, "no_data",
                    aspect=aspect_name, separation_deg=separation,
                ))
                continue
            if tier is None or tier < config.STAGE2_TIER_FLOOR:
                misses.append(_near_miss(
                    jd, 2, "moon_to_slow", variant, config.MOON, rad_name, "tier_below_floor",
                    aspect=aspect_name, separation_deg=separation, tier=tier,
                ))
                continue
            hits.append(_hit(
                jd, 2, "moon_to_slow", variant, config.MOON, rad_name,
                aspect_name, separation, progressed_speeds[config.MOON], radix_speeds.get(rad_name),
            ))

    for prog_name, prog_long in progressed.items():
        if prog_name not in config.FAST_FAST_SET:
            continue
        if not _speed_ok(progressed_speeds[prog_name]):
            misses.append(_near_miss(
                jd, 2, "fast_to_fast", variant, prog_name, None, "speed_below_floor",
                speed_deg_per_day=progressed_speeds[prog_name], aspect=None,
            ))
            continue
        for rad_name, rad_long in radix.items():
            if rad_name not in config.FAST_FAST_SET:
                continue
            if not _speed_ok(radix_speeds[rad_name]):
                misses.append(_near_miss(
                    jd, 2, "fast_to_fast", variant, prog_name, rad_name, "speed_below_floor",
                    speed_deg_per_day=radix_speeds[rad_name], aspect=None,
                ))
                continue
            moon_party = prog_name == config.MOON or rad_name == config.MOON
            aspect = _aspect_pair(prog_long, rad_long, moon_party=moon_party)
            if not aspect:
                minor = _minor_near_miss(prog_long, rad_long, moon_party=moon_party)
                if minor:
                    misses.append(_near_miss(
                        jd, 2, "fast_to_fast", variant, prog_name, rad_name, "minor_aspect",
                        aspect=minor[0], separation_deg=minor[1],
                    ))
                continue
            aspect_name, separation = aspect
            relevance, no_data = _pair_relevance(compendium, event_id, prog_name, rad_name)
            if no_data:
                misses.append(_near_miss(
                    jd, 2, "fast_to_fast", variant, prog_name, rad_name, "no_data",
                    aspect=aspect_name, separation_deg=separation,
                ))
            elif relevance == config.PAIR_RELEVANCE_MIN:
                hits.append(_hit(
                    jd, 2, "fast_to_fast", variant, prog_name, rad_name,
                    aspect_name, separation, progressed_speeds[prog_name], radix_speeds[rad_name],
                ))
            else:
                misses.append(_near_miss(
                    jd, 2, "fast_to_fast", variant, prog_name, rad_name,
                    f"{relevance}_relevance", aspect=aspect_name, separation_deg=separation,
                ))

    return hits, misses


# --- per-point evaluation (spec section 3.2) ---------------------------------

def _variants(info):
    """The four equal-weight channels (direct/converse SSR x
    direct/converse progression), each a (name, longitude) dict plus a
    (name, speed) dict, Sun already excluded by PSSR_Auto."""
    direct = info["direct_planets"]
    converse = info["converse_planets"]
    return [
        {"variant": "dp", "planets": {p: l for p, l, _ in direct[:10]},
         "speeds": {p: s for p, _l, s, _ in info["prog_dir_speeds"]}},
        {"variant": "dr", "planets": {p: l for p, l, _ in direct[10:]},
         "speeds": {p: s for p, _l, s, _ in info["reg_dir_speeds"]}},
        {"variant": "cp", "planets": {p: l for p, l, _ in converse[:10]},
         "speeds": {p: s for p, _l, s, _ in info["prog_conv_speeds"]}},
        {"variant": "cr", "planets": {p: l for p, l, _ in converse[10:]},
         "speeds": {p: s for p, _l, s, _ in info["reg_conv_speeds"]}},
    ]


def evaluate_point(jd_t, events, geopos_natal, compendium=None):
    """Section 3.2 steps 1-3: recompute the candidate radix once per grid
    point (shared across events), construct PSSR_Auto per (point, event)
    with return_speeds=True, and evaluate stages 1 and 2 against the
    candidate radix positions. Returns a list, one dict per event:
    {"event": <event>, "hits": [...], "near_misses": [...]}.
    `compendium` feeds the relevance gates (Step 5); None leaves them open
    (Step-4 kinematics mode)."""
    radix_planets = calc_planets_labelled(jd_t, "(r)")
    radix_speeds = dict((name, speed) for name, _l, speed, _t in calc_planets_labelled_speeds(jd_t, "(r)"))
    radix_positions = {name: long for name, long, _l in radix_planets}
    dt_t = julian.from_jd(jd_t)

    per_event = []
    for event in events:
        event_id = event["event_type"]
        pssr = PSSR_Auto(dt_t, event["datetime"], rad_planets=radix_planets, return_speeds=True)
        info = pssr.get_dict_info()
        hits, misses = [], []
        for variant in _variants(info):
            s1, m1 = stage1_hits(jd_t, variant["variant"], variant["planets"], variant["speeds"],
                                 radix_positions, radix_speeds, event_id, compendium)
            s2, m2 = stage2_hits(jd_t, variant["variant"], variant["planets"], variant["speeds"],
                                 radix_positions, radix_speeds, event_id, compendium)
            hits.extend(s1 + s2)
            misses.extend(m1 + m2)
        per_event.append({"event": event, "hits": hits, "near_misses": misses})

    return per_event


# --- per-tuple intervals and per-stage unions (spec section 3.7) -------------

def _tuple_key(hit):
    return (hit["stage"], hit["arm"], hit["variant"],
            hit["progressed_point"], hit["radix_point"], hit["aspect"])


def group_hits_by_tuple(hits):
    """Group hits by their qualifying tuple (stage, arm, variant,
    progressed point, radix point, aspect class) - section 3.7. Preserves
    first-seen order of the tuple keys."""
    groups = {}
    order = []
    for hit in hits:
        key = _tuple_key(hit)
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(hit)
    return [(key, groups[key]) for key in order]


def build_intervals(grouped_hits, step_seconds):
    """Per-tuple contiguous in-orb intervals. Each group's hit jd's are
    sorted; consecutive hits closer than 1.5 grid steps belong to the same
    in-orb episode (a pair can come into orb, leave it and - near a mutual
    station - return; each run becomes its own interval). Returns a list of
    [(start_jd, end_jd), ...] per group, in input group order. `step_seconds`
    must be the sweep step the hits came from (a mismatch fragments every
    run into singletons)."""
    step_jd = float(step_seconds) / 86400.0
    gap_jd = 1.5 * step_jd
    results = []
    for key, hits in grouped_hits:
        jds = sorted(hit["jd"] for hit in hits)
        intervals = []
        if jds:
            start = prev = jds[0]
            for jd in jds[1:]:
                if jd - prev > gap_jd:
                    intervals.append((start, prev))
                    start = jd
                prev = jd
            intervals.append((start, prev))
        results.append((key, intervals))
    return results


def merge_intervals(intervals):
    """Union of (start_jd, end_jd) intervals, sorted and overlap-merged."""
    if not intervals:
        return []
    ordered = sorted(intervals)
    merged = [list(ordered[0])]
    for start, end in ordered[1:]:
        if start <= merged[-1][1]:
            if end > merged[-1][1]:
                merged[-1][1] = end
        else:
            merged.append([start, end])
    return [(start, end) for start, end in merged]


def per_stage_union(grouped_intervals, stage):
    """C1(e) / C2(e): the union of the event's stage-1 (resp. stage-2) hits'
    intervals - section 3.7. Each event is counted once per stage no matter
    how many hits it has."""
    stage_intervals = []
    for key, intervals in grouped_intervals:
        if key[0] == stage:
            stage_intervals.extend(intervals)
    return merge_intervals(stage_intervals)


def collect_event_hits(jd_points, events, geopos_natal, step_seconds=None, compendium=None):
    """Run the sweep over `jd_points` and group every event's hits into
    per-tuple intervals plus the per-stage unions C1(e)/C2(e). Returns one
    dict per event:
    {"event": ..., "tuples": [(key, [(start, end), ...]), ...],
     "c1": [...], "c2": [...], "hits": [...], "near_misses": [...]}.

    `step_seconds` defaults to the actual spacing of `jd_points` (derived
    from the first two points), so the interval builder cannot drift from
    the sweep that produced the hits. `compendium` feeds the relevance
    gates (Step 5)."""
    if step_seconds is None:
        if len(jd_points) < 2:
            raise ValueError("collect_event_hits needs at least two jd_points "
                             "to derive the sweep step; pass step_seconds explicitly otherwise")
        step_seconds = (jd_points[1] - jd_points[0]) * 86400.0
    per_event = {id(e): {"event": e, "hits": [], "near_misses": []} for e in events}
    for jd_t in jd_points:
        for result in evaluate_point(jd_t, events, geopos_natal, compendium):
            bucket = per_event[id(result["event"])]
            bucket["hits"].extend(result["hits"])
            bucket["near_misses"].extend(result["near_misses"])

    results = []
    for bucket in per_event.values():
        grouped = group_hits_by_tuple(bucket["hits"])
        intervals = build_intervals(grouped, step_seconds)
        results.append({
            "event": bucket["event"],
            "tuples": intervals,
            "c1": per_stage_union(intervals, 1),
            "c2": per_stage_union(intervals, 2),
            "hits": bucket["hits"],
            "near_misses": bucket["near_misses"],
        })
    return results
