"""
batch/pssr_window.py - the PSSR window-narrowing pipeline.

Architectural layer: batch/ (new for this feature). This module implements
the algorithm contract: the grid sweep (spec v5 section 3.2), the point-set
membership rules (section 3.3), majors-only aspect evaluation over raw
degrees with the 12'/18'/32' orb rules (section 3.4), stage 1 fast-to-slow
(section 3.5), stage 2 moon-to-slow + fast-to-fast (section 3.6), per-tuple
interval building with per-stage per-event unions (section 3.7), the coarse
pass / consensus / margin (section 3.8), the fine pass (section 3.9), the
confidence tiers and the report (section 3.10), and the batch entry point
narrow_birth_time_window (section 3.1).

Phase note (Step 6): the pipeline is complete. The relevance gates are
wired to the compendium lookups (sections 4.1/4.2) - the entry point loads
a Compendium by default; passing compendium=None to the stage/evaluation
functions keeps the gates OPEN (the Step-4 kinematics mode used by the
isolated stage tests). See the spec's section 9 future-research register
for what is deliberately outside this feature.

Single-event consensus semantics (contract resolution): sections 3.8/3.9
fail the coarse/fine consensus pass open to the full input window when
fewer than 2 events contribute, but section 3.10's "1 (any stage)" tier row
and the section 7 checklist ("single-event <= 60 min vs > 60 min") require
the single corroborating event's own contribution range to become the
final window - otherwise that tier is unreachable. Resolution: the
consensus machinery never narrows below the input window on its own; the
final-window selection uses the single contributor's range (C2 if non-empty
else C1), pre-margin, and tiers it against SINGLE_EVENT_FINE_RANGE_MINUTES.

All decisions read from `pssr_window_config`; there are no hardcoded
business values in this module. Pure functions, no globals. Point names
are the codebase's PLANETS names ('Mercury', ..., 'Mean_Node'); the
config's Planet codes are the same strings; the compendium lookups map
them via to_compendium_symbol.
"""

import julian

from topo_astro.core.aspects import calculate_aspect, MAJOR_ASPECTS
from topo_astro.core.constants import calc_planets_labelled, calc_planets_labelled_speeds
from topo_astro.significators.compendium import Compendium, to_compendium_symbol
from topo_astro.techniques.pssr import PSSR_Auto
from topo_astro.batch import pssr_window_config as config


# The spec's section 3.1 signature names the parameter `config`; the module
# alias above stays available to default it when the caller passes nothing.
_CONFIG_MODULE = config


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


# --- interval algebra (spec sections 3.7-3.9) ---------------------------------

def _point_in_intervals(jd, intervals):
    return any(lo <= jd <= hi for lo, hi in intervals)


def _clip_intervals(intervals, lo, hi):
    """Intersect interval lists with a single (lo, hi) range; preserves
    order; empty pieces dropped."""
    out = []
    for s, e in intervals:
        s2, e2 = max(s, lo), min(e, hi)
        if s2 <= e2:
            out.append((s2, e2))
    return out


def _intersect_two(a, b):
    """Pointwise interval intersection of two sorted interval lists."""
    out = []
    i = j = 0
    while i < len(a) and j < len(b):
        start = max(a[i][0], b[j][0])
        end = min(a[i][1], b[j][1])
        if start <= end:
            out.append((start, end))
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return out


def intersect_intervals(interval_lists):
    """Section 3.8/3.9: the literal interval intersection across the given
    per-event interval lists. Events with empty lists contribute nothing
    (callers pre-filter contributors). Returns [] when it is empty."""
    non_empty = [iv for iv in interval_lists if iv]
    if not non_empty:
        return []
    result = non_empty[0]
    for ivs in non_empty[1:]:
        result = _intersect_two(result, ivs)
        if not result:
            break
    return result


def _max_cardinality_subset(events_intervals, tie_break="earliest_start"):
    """Section 3.8/3.9 partial-consensus fallback: the largest subset of
    contributing events whose interval sets mutually intersect, ties broken
    by earliest window start (CONSENSUS_TIE_BREAK). Returns
    (subset_events, (start, end)) or None when no subset of >= 2 events
    has a common point.

    Any subset with a non-empty intersection has a common point, so the
    maximum-overlap point over all interval endpoints yields a
    maximum-cardinality subset (and the subset is exact, not greedy)."""
    events = [e for e, _ in events_intervals]
    ivs = [iv for _, iv in events_intervals]
    candidates = []
    for iv in ivs:
        for lo, hi in iv:
            candidates.append(lo)
            candidates.append(hi)
    best_count = 0
    best = None
    for t in candidates:
        members = [e for e, iv in zip(events, ivs) if _point_in_intervals(t, iv)]
        count = len(members)
        if count < best_count or count < 2:
            continue
        window = _window_span(intersect_intervals(
            [iv for e, iv in zip(events, ivs) if e in members]))
        if count > best_count:
            best_count = count
            best = (members, window)
        elif count == best_count and tie_break == "earliest_start" and window[0] < best[1][0]:
            best = (members, window)
    if best is None:
        return None
    subset, window = best
    return subset, window


def _window_span(intervals):
    """Collapse an interval list (possibly several disjoint pieces) to its
    span - the coarse/fine window is the consensus range."""
    return (intervals[0][0], intervals[-1][1])


def _apply_margin(window, margin_minutes, full_start, full_end):
    """Section 3.8/3.9: pad the window by SAFETY_MARGIN_MINUTES on both
    ends, clamped to the input window (never wider)."""
    lo, hi = window
    pad = float(margin_minutes) / 1440.0
    return (max(full_start, lo - pad), min(full_end, hi + pad))


# --- MAX_ASPECTS_PER_EVENT (spec section 3.7) ---------------------------------

def _restrict_to_single_aspect(result):
    """MAX_ASPECTS_PER_EVENT == "1": reproduce the book's single-aspect
    practice - per stage keep only the representative tuple, the one with
    the widest interval, and within it the hit nearest the interval center
    (i.e. the smallest orb at the center of its widest interval)."""
    kept_tuples = []
    kept_hits = []
    for stage in (1, 2):
        stage_tuples = [(k, iv) for k, iv in result["tuples"] if k[0] == stage]
        if not stage_tuples:
            continue
        widest = max(stage_tuples, key=lambda kv: max(e - s for s, e in kv[1]))
        kept_tuples.append(widest)
        key, intervals = widest
        center = (max(e for _, e in intervals) + min(s for s, _ in intervals)) / 2.0
        members = [h for h in result["hits"] if _tuple_key(h) == key]
        kept_hits.append(min(members, key=lambda h: abs(h["jd"] - center)))
    return {"event": result["event"], "tuples": kept_tuples,
            "c1": per_stage_union(kept_tuples, 1),
            "c2": per_stage_union(kept_tuples, 2),
            "hits": kept_hits, "near_misses": result["near_misses"]}


# --- coarse / fine passes and the final window (spec sections 3.8-3.10) -------

def coarse_pass(results, full_start, full_end, cfg):
    """Section 3.8. Returns the coarse pass outcome: consensus type
    ("full" | "partial" | "none"), the pre-margin coarse window (full
    input window when consensus is none), the corroboration count, and the
    subset/dropped events for partial consensus."""
    contributors = [r for r in results if r["c1"]]
    base = {"corroboration": len(contributors), "margin_minutes": cfg.SAFETY_MARGIN_MINUTES}
    if len(contributors) < 2:
        return {**base, "consensus": "none", "window_jd": (full_start, full_end),
                "subset_members": [], "dropped_events": []}
    intersection = intersect_intervals([r["c1"] for r in contributors])
    if intersection:
        return {**base, "consensus": "full", "window_jd": _window_span(intersection),
                "subset_members": [r["event"] for r in contributors], "dropped_events": []}
    if not cfg.CONSENSUS_MAX_CARDINALITY:
        return {**base, "consensus": "none", "window_jd": (full_start, full_end),
                "subset_members": [], "dropped_events": [r["event"] for r in contributors]}
    found = _max_cardinality_subset([(r["event"], r["c1"]) for r in contributors], cfg.CONSENSUS_TIE_BREAK)
    if found is None:
        return {**base, "consensus": "none", "window_jd": (full_start, full_end),
                "subset_members": [], "dropped_events": [r["event"] for r in contributors]}
    subset, window = found
    return {**base, "consensus": "partial", "window_jd": window,
            "subset_members": list(subset),
            "dropped_events": [r["event"] for r in contributors if r["event"] not in subset]}


def fine_pass(results, margined_coarse, cfg):
    """Section 3.9. Stage-2 hits outside the margined coarse window are
    recorded in the fine-outside-coarse ledger (never silently discarded);
    C2(e) is clipped to the scan region for consensus. Returns the fine
    pass outcome plus the ledger."""
    ms, me = margined_coarse
    fine_outside = []
    for r in results:
        outside = [h for h in r["hits"] if h["stage"] == 2 and not (ms <= h["jd"] <= me)]
        for hit in outside:
            fine_outside.append({"event": r["event"], "hit": hit})
        r["c2_fine"] = _clip_intervals(r["c2"], ms, me)
    contributors = [r for r in results if r["c2_fine"]]
    base = {"corroboration": len(contributors), "fine_outside_coarse": fine_outside,
            "margined_coarse_window_jd": margined_coarse,
            "margin_minutes": cfg.SAFETY_MARGIN_MINUTES}
    if len(contributors) < 2:
        return {**base, "consensus": "none", "window_jd": None,
                "subset_members": [], "dropped_events": []}
    intersection = intersect_intervals([r["c2_fine"] for r in contributors])
    if intersection:
        return {**base, "consensus": "full", "window_jd": _window_span(intersection),
                "subset_members": [r["event"] for r in contributors], "dropped_events": []}
    if not cfg.CONSENSUS_MAX_CARDINALITY:
        return {**base, "consensus": "none", "window_jd": None,
                "subset_members": [], "dropped_events": [r["event"] for r in contributors]}
    found = _max_cardinality_subset([(r["event"], r["c2_fine"]) for r in contributors], cfg.CONSENSUS_TIE_BREAK)
    if found is None:
        return {**base, "consensus": "none", "window_jd": None,
                "subset_members": [], "dropped_events": [r["event"] for r in contributors]}
    subset, window = found
    return {**base, "consensus": "partial", "window_jd": window,
            "subset_members": list(subset),
            "dropped_events": [r["event"] for r in contributors if r["event"] not in subset]}


def _select_final_window(results, coarse, fine, full_start, full_end, cfg):
    """Section 3.10: the final pre-margin window, its tier, and the reason.
    Exactly one corroborating event -> that event's own contribution range
    (C2 if non-empty else C1), tiered against SINGLE_EVENT_FINE_RANGE_MINUTES
    (see the module docstring for the contract resolution). Zero -> none.
    Two or more -> the fine consensus if present, else the coarse consensus
    if present, else fail-open to the full input window (disjoint
    everything -> `none` tier)."""
    corroborators = [r for r in results if r["c1"] or r["c2"]]
    n = len(corroborators)
    if n == 0:
        return (full_start, full_end), "none", "no_contributors"
    if n == 1:
        r = corroborators[0]
        window = _window_span(r["c2"] or r["c1"])
        width_min = (window[1] - window[0]) * 1440.0
        tier = "usable" if width_min <= cfg.SINGLE_EVENT_FINE_RANGE_MINUTES else "weak"
        return window, tier, "single_event"
    if fine["consensus"] in ("full", "partial"):
        return fine["window_jd"], "usable", "fine_" + fine["consensus"]
    if coarse["consensus"] in ("full", "partial"):
        return coarse["window_jd"], "usable", "coarse_" + coarse["consensus"]
    return (full_start, full_end), "none", "no_consensus"


# --- the report (spec section 3.10) -------------------------------------------

def _relevance_wording(compendium, event_id, hit):
    """The relevance source + wording for a hit: the pairwise table for
    stage 1 / arm 2, the tier table for arm 1. Kinematics mode
    (compendium=None) reports the open-gate values."""
    if hit["arm"] == "moon_to_slow":
        if compendium is None:
            wording = "tier_score >= floor (kinematics mode: gate open)"
            tier = None
        else:
            tier = compendium.tier_score(event_id, to_compendium_symbol(hit["radix_point"]))
            wording = "tier_score %s >= STAGE2_TIER_FLOOR %s" % (
                tier if tier is not None else "absent", config.STAGE2_TIER_FLOOR)
        return "compendium_scoring_export_v2.json", wording
    a = to_compendium_symbol(hit["progressed_point"])
    b = to_compendium_symbol(hit["radix_point"])
    if compendium is None:
        strength = "strong"
        title = "(no compendium)"
    else:
        strength = compendium.pair_strength(event_id, a, b) or "strong"
        title = compendium.event_title_for(event_id) or "(no compendium)"
    return ("juan_combos_pairs_v1.json",
            "'%s:%s' -> %s for %s" % (a, b, strength, title))


def _hit_context(compendium, result):
    """Per-hit report context: the containing interval, the orb at the
    interval center (the separation of the tuple hit nearest the center),
    and the relevance source/wording."""
    by_key = {}
    for key, intervals in result["tuples"]:
        by_key[key] = intervals
    members_by_key = {}
    for hit in result["hits"]:
        members_by_key.setdefault(_tuple_key(hit), []).append(hit)
    out = []
    event_id = result["event"]["event_type"]
    for hit in result["hits"]:
        entry = dict(hit)
        intervals = by_key.get(_tuple_key(hit), [])
        containing = next(((lo, hi) for lo, hi in intervals if lo <= hit["jd"] <= hi), None)
        if containing:
            center = (containing[0] + containing[1]) / 2.0
            nearest = min(members_by_key.get(_tuple_key(hit), [hit]),
                          key=lambda h: abs(h["jd"] - center))
            entry["interval_jd"] = containing
            entry["orb_arcmin_at_interval_center"] = nearest["separation_deg"] * 60.0
        source, wording = _relevance_wording(compendium, event_id, hit)
        entry["relevance_source"] = source
        entry["relevance_wording"] = wording
        out.append(entry)
    return out


def _parameters_used(cfg):
    return {
        "step_seconds": cfg.STEP_SECONDS,
        "aspect_classes": sorted(cfg.ASPECT_CLASSES),
        "orb_fast_slow_deg": cfg.ORB_FAST_SLOW_DEG,
        "orb_moon_conj_opp_deg": cfg.ORB_MOON_CONJ_OPP_DEG,
        "orb_moon_general_arc_min": cfg.ORB_MOON_GENERAL_ARC_MIN,
        "speed_floor_arc_min_per_day": cfg.SPEED_FLOOR_ARC_MIN_PER_DAY,
        "speed_floor_use_absolute": cfg.SPEED_FLOOR_USE_ABSOLUTE,
        "fast_set": sorted(cfg.FAST_SET),
        "slow_set": sorted(cfg.SLOW_SET),
        "fast_fast_set": sorted(cfg.FAST_FAST_SET),
        "pair_relevance_min": cfg.PAIR_RELEVANCE_MIN,
        "stage2_tier_floor": cfg.STAGE2_TIER_FLOOR,
        "safety_margin_minutes": cfg.SAFETY_MARGIN_MINUTES,
        "single_event_fine_range_minutes": cfg.SINGLE_EVENT_FINE_RANGE_MINUTES,
        "max_aspects_per_event": cfg.MAX_ASPECTS_PER_EVENT,
        "consensus_max_cardinality": cfg.CONSENSUS_MAX_CARDINALITY,
        "consensus_tie_break": cfg.CONSENSUS_TIE_BREAK,
    }


def _signed_distance_minutes(dt_dob, jd_lo, jd_hi):
    """Signed distance of dt_actual_dob from the final window, in minutes:
    0.0 inside, negative before the start, positive after the end."""
    jd = julian.to_jd(dt_dob)
    if jd_lo <= jd <= jd_hi:
        return 0.0
    if jd < jd_lo:
        return (jd - jd_lo) * 1440.0
    return (jd - jd_hi) * 1440.0


# --- the batch entry point (spec section 3.1) ---------------------------------

def narrow_birth_time_window(dt_radix_start, dt_radix_end, dt_actual_dob,
                             geopos_natal, events, config=None, compendium=None):
    """Section 3.1: run the full window-narrowing pipeline over
    [dt_radix_start, dt_radix_end] and return the PSSRWindowReport dict.

    `config` defaults to the resolved pssr_window_config module (any
    object exposing the same constants works; tests pass a small override
    namespace). `compendium` defaults to a loaded Compendium (production
    mode); pass one explicitly for determinism. The report schema is
    documented in the function's output below and in the section 3.10
    checklist. Callable directly - no CLI until Phase 10 of the migration.
    """
    cfg = _CONFIG_MODULE if config is None else config
    if compendium is None:
        compendium = Compendium.load()

    jd_start = julian.to_jd(dt_radix_start)
    jd_end = julian.to_jd(dt_radix_end)

    def _degraded(errors):
        """Fail-open (manual Step 6 item 4): on any internal error the
        window remains the full input range, the error is surfaced in the
        report, and the pipeline returns rather than raises - a narrowed
        window is never silently produced from broken data."""
        return {
            "dt_radix_start": dt_radix_start,
            "dt_radix_end": dt_radix_end,
            "dt_actual_dob": dt_actual_dob,
            "input_window_jd": (jd_start, jd_end),
            "coarse": {"consensus": "none", "window_jd": (jd_start, jd_end),
                       "corroboration": 0, "events_with_data": 0,
                       "margin_minutes": cfg.SAFETY_MARGIN_MINUTES,
                       "subset_members": [], "dropped_events": []},
            "fine": {"consensus": "none", "window_jd": None, "corroboration": 0,
                     "margined_coarse_window_jd": (jd_start, jd_end),
                     "margin_minutes": cfg.SAFETY_MARGIN_MINUTES,
                     "subset_members": [], "dropped_events": []},
            "final_window_pre_margin_jd": (jd_start, jd_end),
            "final_window_jd": (jd_start, jd_end),
            "tier": "none",
            "tier_reason": "internal_error",
            "signed_distance_from_window_minutes": _signed_distance_minutes(
                dt_actual_dob, jd_start, jd_end),
            "events": [],
            "near_miss_ledger": [],
            "parameters": _parameters_used(cfg),
            "errors": errors,
        }

    try:
        return _narrow_birth_time_window_impl(
            dt_radix_start, dt_radix_end, dt_actual_dob, geopos_natal, events,
            cfg, compendium, jd_start, jd_end)
    except Exception as exc:  # noqa: BLE001 - fail-open by design
        return _degraded([{"type": type(exc).__name__, "message": str(exc)}])


def _narrow_birth_time_window_impl(dt_radix_start, dt_radix_end, dt_actual_dob,
                                   geopos_natal, events, cfg, compendium,
                                   jd_start, jd_end):
    """The non-fail-open body of narrow_birth_time_window (the wrapper
    catches internal errors per manual Step 6 item 4)."""
    points = list(sweep_jds(dt_radix_start, dt_radix_end, cfg.STEP_SECONDS))
    if len(points) < 2:
        raise ValueError("window is too short for the configured STEP_SECONDS")
    step_seconds = (points[1] - points[0]) * 86400.0

    results = collect_event_hits(points, events, geopos_natal,
                                 step_seconds=step_seconds, compendium=compendium)
    if cfg.MAX_ASPECTS_PER_EVENT == "1":
        results = [_restrict_to_single_aspect(r) for r in results]

    coarse = coarse_pass(results, jd_start, jd_end, cfg)
    margined_coarse = _apply_margin(coarse["window_jd"], cfg.SAFETY_MARGIN_MINUTES,
                                    jd_start, jd_end)
    fine = fine_pass(results, margined_coarse, cfg)

    final_pre, tier, reason = _select_final_window(
        results, coarse, fine, jd_start, jd_end, cfg)
    final_jd = _apply_margin(final_pre, cfg.SAFETY_MARGIN_MINUTES, jd_start, jd_end)

    events_with_data = 0
    for e in events:
        if compendium.event_title_for(e["event_type"]) is not None:
            events_with_data += 1

    per_event = [{
        "event": r["event"],
        "c1": r["c1"],
        "c2": r["c2"],
        "hits": _hit_context(compendium, r),
        "near_misses": [dict(m, event=r["event"]) for m in r["near_misses"]],
    } for r in results]

    ledger = [m for r in results for m in
              [dict(m, event=r["event"]) for m in r["near_misses"]]]
    ledger.extend(fine["fine_outside_coarse"])

    return {
        "dt_radix_start": dt_radix_start,
        "dt_radix_end": dt_radix_end,
        "dt_actual_dob": dt_actual_dob,
        "input_window_jd": (jd_start, jd_end),
        "coarse": {
            "consensus": coarse["consensus"],
            "window_jd": coarse["window_jd"],
            "corroboration": coarse["corroboration"],
            "events_with_data": events_with_data,
            "margin_minutes": coarse["margin_minutes"],
            "subset_members": coarse["subset_members"],
            "dropped_events": coarse["dropped_events"],
        },
        "fine": {
            "consensus": fine["consensus"],
            "window_jd": fine["window_jd"],
            "corroboration": fine["corroboration"],
            "margined_coarse_window_jd": fine["margined_coarse_window_jd"],
            "margin_minutes": fine["margin_minutes"],
            "subset_members": fine["subset_members"],
            "dropped_events": fine["dropped_events"],
        },
        "final_window_pre_margin_jd": final_pre,
        "final_window_jd": final_jd,
        "tier": tier,
        "tier_reason": reason,
        "signed_distance_from_window_minutes": _signed_distance_minutes(
            dt_actual_dob, final_jd[0], final_jd[1]),
        "events": per_event,
        "near_miss_ledger": ledger,
        "parameters": _parameters_used(cfg),
        "errors": [],
    }
