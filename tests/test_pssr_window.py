"""
Step 4 tests: sweep and per-point stage evaluation kinematics (spec v5
sections 3.2-3.7, execution-plan Step 4).

The relevance gates are stubbed open in Step 4, so these tests exercise
pure kinematics: the grid sweep, point-set membership (no fast-to-fast in
stage 1, no Sun/POF/angles anywhere), the 12'/18'/32' orb boundaries,
majors-only behavior (a 45-degree semisquare just inside orb never fires),
the speed gate on the side the fast point actually sits, and per-tuple
interval building with per-stage per-event unions.

The synthetic tests feed exact longitudes/speeds to the stage evaluators
(deterministic, no ephemeris). Two real-ephemeris tests on the beyonce
fixture verify the integrated sweep: every real stage-1 hit stays inside
the 12' orb, and a real in-orb episode demonstrably ends at the 12'
boundary (the "computed candidate time ... only within 12' on either
side" checklist item).

Step 5 tests (relevance wiring) and Step 6 tests (ranges, consensus,
margin, report - sections 3.7-3.10, incl. the narrow_birth_time_window
entry point) live in the same file. The Step 6 consensus/margin/tier
tests are pure synthetic interval tests on the pass functions; one
real-ephemeris test drives the full entry point end to end.
"""

import json
import os
from datetime import datetime, timedelta

import julian
import pytest

from topo_astro.batch import pssr_window as pw
from topo_astro.batch import pssr_window_config as cfg
from topo_astro.core.aspects import calculate_aspect
from topo_astro.core.constants import calc_planets_labelled
from topo_astro.significators.rules_data import EventType
from topo_astro.techniques.pssr import PSSR_Auto

from tests.fixtures.fixture_manifest import BIRTH_DATA_DIR, PEOPLE

FAST = {"Mercury", "Venus", "Mars"}
SLOW = {"Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Mean_Node"}
SPEED_FLOOR_DEG = cfg.SPEED_FLOOR_ARC_MIN_PER_DAY / 60.0


def stage1(prog, radix, prog_speeds=None, radix_speeds=None, event_id=EventType.SUCCESS_ELECTED, compendium=None):
    """Thin convenience wrapper: stage-1 evaluation on sparse synthetic
    point sets (missing speeds default to a fast/typical value)."""
    prog_speeds = prog_speeds or {name: 1.2 for name in prog}
    radix_speeds = radix_speeds or {name: 1.0 for name in radix}
    return pw.stage1_hits(0.0, "dp", prog, prog_speeds, radix, radix_speeds, event_id, compendium)


def stage2(prog, radix, prog_speeds=None, radix_speeds=None, event_id=EventType.SUCCESS_ELECTED, compendium=None):
    prog_speeds = prog_speeds or {name: 1.2 for name in prog}
    radix_speeds = radix_speeds or {name: 1.0 for name in radix}
    return pw.stage2_hits(0.0, "dp", prog, prog_speeds, radix, radix_speeds, event_id, compendium)


# --- the sweep (section 3.2) -------------------------------------------------

def test_sweep_jds_inclusive_of_both_endpoints():
    start = datetime(2000, 1, 1, 0, 0, 0)
    end = datetime(2000, 1, 1, 0, 5, 0)
    points = list(pw.sweep_jds(start, end, 60))
    assert len(points) == 6
    assert points[0] == julian.to_jd(start)
    assert points[-1] == julian.to_jd(end)
    step = points[1] - points[0]
    assert step == pytest.approx(60.0 / 86400.0)
    for a, b in zip(points, points[1:]):
        assert b - a == pytest.approx(step)


# --- stage 1 (section 3.5) ---------------------------------------------------

def test_stage1_exact_conjunction_fires_case_a():
    hits, misses = stage1({"Mercury": 100.0}, {"Jupiter": 100.0})
    assert len(hits) == 1
    hit = hits[0]
    assert hit["stage"] == 1
    assert hit["arm"] == "fast_to_slow"
    assert hit["variant"] == "dp"
    assert hit["progressed_point"] == "Mercury"
    assert hit["radix_point"] == "Jupiter"
    assert hit["aspect"] == "conjunction"
    assert hit["separation_deg"] == 0.0
    assert hit["progressed_speed"] == 1.2
    assert hit["radix_speed"] == 1.0


def test_stage1_flags_only_within_12_arcmin():
    # Separation sweep across the 12' = 0.2 deg boundary: in-orb below and
    # at 0.2 deg (within float precision), silent just beyond. The exact
    # 0.2 boundary is a float-representation edge (100.0 + 0.2 lands a few
    # ulps past the orb), so the sweep uses 0.19/0.21 margins.
    for separation in (0.0, 0.1, 0.19):
        hits, _ = stage1({"Mercury": 100.0 + separation}, {"Jupiter": 100.0})
        assert len(hits) == 1, f"expected hit at separation {separation}"
    for separation in (0.21, 0.25, 0.35):
        hits, misses = stage1({"Mercury": 100.0 + separation}, {"Jupiter": 100.0})
        assert len(hits) == 0, f"expected no hit at separation {separation}"
        assert misses == []


def test_stage1_case_b_slow_progressed_fast_radix():
    hits, _ = stage1({"Jupiter": 100.0}, {"Mercury": 100.0})
    assert len(hits) == 1
    assert hits[0]["progressed_point"] == "Jupiter"
    assert hits[0]["radix_point"] == "Mercury"


def test_stage1_never_fast_to_fast():
    # Mercury-Venus, Venus-Moon and Moon-Mars exact conjunctions must never
    # be produced by stage 1 (D6) - regardless of which side each sits on.
    for pair in (("Mercury", "Venus"), ("Venus", "Moon"), ("Moon", "Mars")):
        hits, misses = stage1({pair[0]: 100.0}, {pair[1]: 100.0})
        assert hits == [], f"{pair} produced a stage-1 hit"
        assert misses == []


def test_stage1_membership_excludes_sun_pof_angles():
    radix = {"Sun": 100.0, "POF": 100.0, "H10": 100.0, "Jupiter": 100.0}
    hits, misses = stage1({"Mercury": 100.0}, radix)
    assert len(hits) == 1
    assert hits[0]["radix_point"] == "Jupiter"
    assert not any(h["radix_point"] in {"Sun", "POF", "H10"} for h in hits)
    assert not any(h["progressed_point"] in {"Sun", "POF"} for h in hits)


def test_stage1_speed_gate_progressed_side_below_floor():
    hits, misses = stage1({"Mercury": 100.0}, {"Jupiter": 100.0}, prog_speeds={"Mercury": 0.3})
    assert hits == []
    assert len(misses) == 1
    miss = misses[0]
    assert miss["kind"] == "speed_below_floor"
    assert miss["speed_deg_per_day"] == 0.3
    assert miss["aspect"] is None


def test_stage1_speed_gate_radix_side_below_floor():
    hits, misses = stage1({"Jupiter": 100.0}, {"Mercury": 100.0}, radix_speeds={"Mercury": 0.2})
    assert hits == []
    assert len(misses) == 1
    assert misses[0]["kind"] == "speed_below_floor"
    assert misses[0]["speed_deg_per_day"] == 0.2


def test_stage1_speed_gate_retrograde_passes_on_magnitude():
    hits, _ = stage1({"Mercury": 100.0}, {"Jupiter": 100.0}, prog_speeds={"Mercury": -1.2})
    assert len(hits) == 1
    assert hits[0]["progressed_speed"] == -1.2


def test_stage1_exact_floor_boundary():
    # |speed| exactly at the floor passes; just under it fails.
    hits, _ = stage1({"Mercury": 100.0}, {"Jupiter": 100.0}, prog_speeds={"Mercury": SPEED_FLOOR_DEG})
    assert len(hits) == 1
    hits, misses = stage1({"Mercury": 100.0}, {"Jupiter": 100.0}, prog_speeds={"Mercury": SPEED_FLOOR_DEG - 1e-9})
    assert hits == []
    assert misses and misses[0]["kind"] == "speed_below_floor"


# --- stage 2 (section 3.6) ---------------------------------------------------

def test_stage2_arm1_moon_conj_opp_32_arcmin():
    # Moon-to-slow conjunction: 32' orb.
    hits, _ = stage2({"Moon": 100.5}, {"Jupiter": 100.0}, prog_speeds={"Moon": 13.0})
    assert len(hits) == 1
    assert hits[0]["stage"] == 2
    assert hits[0]["arm"] == "moon_to_slow"
    assert hits[0]["aspect"] == "conjunction"
    hits, _ = stage2({"Moon": 100.55}, {"Jupiter": 100.0}, prog_speeds={"Moon": 13.0})
    assert hits == []


def test_stage2_arm1_moon_general_18_arcmin():
    # Moon-to-slow square: 18' general orb (not the 32' conj/opp orb).
    hits, _ = stage2({"Moon": 90.25}, {"Jupiter": 0.0}, prog_speeds={"Moon": 13.0})
    assert len(hits) == 1
    assert hits[0]["aspect"] == "square"
    hits, _ = stage2({"Moon": 90.4}, {"Jupiter": 0.0}, prog_speeds={"Moon": 13.0})
    assert hits == []


def test_stage2_arm1_opposition_uses_32_arcmin():
    hits, _ = stage2({"Moon": 180.5}, {"Jupiter": 0.0}, prog_speeds={"Moon": 13.0})
    assert len(hits) == 1
    assert hits[0]["aspect"] == "opposition"


def test_stage2_arm2_fast_to_fast_fires():
    hits, _ = stage2({"Mercury": 100.0}, {"Venus": 100.0})
    assert len(hits) == 1
    assert hits[0]["stage"] == 2
    assert hits[0]["arm"] == "fast_to_fast"
    assert hits[0]["progressed_point"] == "Mercury"
    assert hits[0]["radix_point"] == "Venus"


def test_stage2_arm2_moon_party_orbs():
    # Moon is a party in arm 2: conj/opp get 32', other aspects 18'.
    hits, _ = stage2({"Moon": 100.5}, {"Mercury": 100.0}, prog_speeds={"Moon": 13.0})
    assert len(hits) == 1 and hits[0]["aspect"] == "conjunction"
    hits, _ = stage2({"Moon": 90.25}, {"Mercury": 0.0}, prog_speeds={"Moon": 13.0})
    assert len(hits) == 1 and hits[0]["aspect"] == "square"
    hits, _ = stage2({"Moon": 90.4}, {"Mercury": 0.0}, prog_speeds={"Moon": 13.0})
    assert hits == []


def test_stage2_arm2_speed_gate_both_points():
    # Stalled progressed point: excluded, speed recorded.
    hits, misses = stage2({"Mercury": 100.0}, {"Venus": 100.0}, prog_speeds={"Mercury": 0.3})
    assert hits == []
    assert any(m["kind"] == "speed_below_floor" and m["speed_deg_per_day"] == 0.3 for m in misses)
    # Stalled radix point: excluded, speed recorded.
    hits, misses = stage2({"Mercury": 100.0}, {"Venus": 100.0}, radix_speeds={"Venus": 0.4})
    assert hits == []
    assert any(m["kind"] == "speed_below_floor" and m["speed_deg_per_day"] == 0.4 for m in misses)
    # Moon clears the floor trivially (no special-casing).
    hits, _ = stage2({"Moon": 100.0}, {"Mercury": 100.0}, prog_speeds={"Moon": 11.0}, radix_speeds={"Mercury": 1.2})
    assert len(hits) == 1


# --- majors only (section 3.4) -----------------------------------------------

def test_minor_semisquare_never_gates_but_is_recorded():
    # A 45-degree semisquare just inside orb: the majors-only check finds
    # nothing, so there is no hit; the minor is recorded in the near-miss
    # ledger (never gating).
    hits, misses = stage1({"Mercury": 45.1}, {"Jupiter": 0.0})
    assert hits == []
    minor_misses = [m for m in misses if m["kind"] == "minor_aspect"]
    assert len(minor_misses) == 1
    assert minor_misses[0]["aspect"] == "45-semisquare"
    assert minor_misses[0]["separation_deg"] == pytest.approx(0.1)


# --- intervals and per-stage unions (section 3.7) ----------------------------

STEP = 60.0 / 86400.0  # one 60-second grid step, in days - the fake jd's
# below are spaced consistently with build_intervals(step_seconds=60).


def _fake_hits(jd_steps, stage=1, arm="fast_to_slow", aspect="conjunction",
               prog="Mercury", radix="Jupiter"):
    return [pw._hit(k * STEP, stage, arm, "dp", prog, radix, aspect, 0.1, 1.2, 1.0)
            for k in jd_steps]


def test_interval_building_splits_gaps_and_merges_runs():
    # Three consecutive hits, a real out-of-orb gap (10+ steps), then two
    # more hits: two intervals for the same tuple.
    hits = _fake_hits([1, 2, 3, 10, 11])
    grouped = pw.group_hits_by_tuple(hits)
    assert len(grouped) == 1
    intervals = pw.build_intervals(grouped, 60)
    assert intervals[0][1] == [(1 * STEP, 3 * STEP), (10 * STEP, 11 * STEP)]


def test_interval_building_distinct_tuples_kept_separate():
    conj = _fake_hits([1, 2], aspect="conjunction")
    sextile = _fake_hits([2, 3], aspect="sextile")
    grouped = pw.group_hits_by_tuple(conj + sextile)
    assert len(grouped) == 2
    intervals = pw.build_intervals(grouped, 60)
    by_key = dict(intervals)
    assert by_key[(1, "fast_to_slow", "dp", "Mercury", "Jupiter", "conjunction")] == [(1 * STEP, 2 * STEP)]
    assert by_key[(1, "fast_to_slow", "dp", "Mercury", "Jupiter", "sextile")] == [(2 * STEP, 3 * STEP)]


def test_merge_intervals():
    assert pw.merge_intervals([(1, 3), (2, 5), (8, 9)]) == [(1, 5), (8, 9)]
    assert pw.merge_intervals([(5, 6), (1, 2), (2.5, 4)]) == [(1, 2), (2.5, 4), (5, 6)]
    assert pw.merge_intervals([]) == []


def test_per_stage_union():
    # One stage-1 tuple and one stage-2 tuple: the union per stage merges
    # only that stage's intervals.
    s1a = _fake_hits([1, 2], stage=1)
    s1b = _fake_hits([2, 3], stage=1, aspect="sextile")
    s2 = _fake_hits([5, 6], stage=2, arm="moon_to_slow")
    grouped = pw.group_hits_by_tuple(s1a + s1b + s2)
    intervals = pw.build_intervals(grouped, 60)
    c1 = pw.per_stage_union(intervals, 1)
    c2 = pw.per_stage_union(intervals, 2)
    assert c1 == [(1 * STEP, 3 * STEP)]
    assert c2 == [(5 * STEP, 6 * STEP)]


# --- real-ephemeris integration ----------------------------------------------

@pytest.fixture(scope="module")
def beyonce_case():
    birth = json.load(open(os.path.join(BIRTH_DATA_DIR, "beyonce.json"), encoding="utf-8"))
    radix_dt = datetime.fromisoformat(PEOPLE["beyonce"]["candidates"]["actual_dob"])
    event = {
        "datetime": datetime(2004, 2, 8, 12, 0, 0),
        "event_type": EventType.SUCCESS_ELECTED,
    }
    return radix_dt, event, birth["geopos_natal"]


def test_real_sweep_invariants(beyonce_case):
    radix_dt, event, geopos = beyonce_case
    points = list(pw.sweep_jds(radix_dt - timedelta(hours=6), radix_dt + timedelta(hours=6), 600))
    result = pw.collect_event_hits(points, [event], geopos)[0]

    assert result["hits"], "expected at least some stage activity on a real chart"
    assert result["c1"] and result["c2"], "expected both per-stage unions to be non-empty"
    for start, end in result["c1"] + result["c2"]:
        assert points[0] <= start <= end <= points[-1]

    max_orb = 32.0 / 60.0 + 1e-9
    for hit in result["hits"]:
        if hit["stage"] == 1:
            assert hit["separation_deg"] <= 12.0 / 60.0 + 1e-9
            assert (hit["progressed_point"] in FAST and hit["radix_point"] in SLOW) or \
                   (hit["progressed_point"] in SLOW and hit["radix_point"] in FAST)
        else:
            assert hit["separation_deg"] <= max_orb
        assert hit["progressed_point"] not in {"Sun", "POF"}
        assert hit["radix_point"] not in {"Sun", "POF"}
        assert "H" not in hit["progressed_point"] and "H" not in hit["radix_point"]

    kinds = {m["kind"] for m in result["near_misses"]}
    assert kinds <= {"speed_below_floor", "minor_aspect"}


def _longitudes_at(jd, event, variant, prog_point, radix_point):
    """Progressed + radix longitudes of one pair at an arbitrary jd,
    recomputed through the same machinery the sweep uses."""
    radix_planets = calc_planets_labelled(jd, "(r)")
    radix_pos = {name: long for name, long, _ in radix_planets}
    info = PSSR_Auto(julian.from_jd(jd), event["datetime"], rad_planets=radix_planets,
                     return_speeds=True).get_dict_info()
    direct = info["direct_planets"]
    converse = info["converse_planets"]
    variants = {
        "dp": {p: l for p, l, _ in direct[:10]},
        "dr": {p: l for p, l, _ in direct[10:]},
        "cp": {p: l for p, l, _ in converse[:10]},
        "cr": {p: l for p, l, _ in converse[10:]},
    }
    return variants[variant][prog_point], radix_pos[radix_point]


def test_real_sweep_in_orb_episode_ends_at_12_arcmin(beyonce_case):
    """The checklist centerpiece: a real in-orb stage-1 episode must be
    bounded by the 12' orb - walk outward from the tightest stage-1 hit
    (sorted by separation) and confirm the pair leaves orb exactly where
    the boundary says it should."""
    radix_dt, event, geopos = beyonce_case
    points = list(pw.sweep_jds(radix_dt - timedelta(hours=24), radix_dt + timedelta(hours=24), 600))
    step_seconds = (points[1] - points[0]) * 86400.0
    result = pw.collect_event_hits(points, [event], geopos)[0]

    stage1_hits = sorted(
        [h for h in result["hits"] if h["stage"] == 1],
        key=lambda h: h["separation_deg"],
    )
    assert stage1_hits, "expected stage-1 hits on a real chart over 48h"

    tried = set()
    for hit in stage1_hits:
        key = (hit["variant"], hit["progressed_point"], hit["radix_point"])
        if key in tried:
            continue
        tried.add(key)
        step = step_seconds / 86400.0
        out_of_orb_at = None
        for k in range(1, 61):
            jd = hit["jd"] + k * step
            prog_long, radix_long = _longitudes_at(jd, event, *key)
            if calculate_aspect(prog_long, radix_long, cfg.ORB_FAST_SLOW_DEG, True) is None:
                out_of_orb_at = k
                break
        if out_of_orb_at is None:
            # Pairs whose relative motion is near zero stay in orb for the
            # whole window (or beyond the walk budget) - skip to a faster pair.
            continue
        jd_in = hit["jd"] + (out_of_orb_at - 1) * step
        prog_in, radix_in = _longitudes_at(jd_in, event, *key)
        assert calculate_aspect(prog_in, radix_in, cfg.ORB_FAST_SLOW_DEG, True) is not None
        assert hit["separation_deg"] <= 12.0 / 60.0 + 1e-9
        assert out_of_orb_at >= 1
        break
    else:
        pytest.fail("no stage-1 pair with a measurable in-orb episode found on the real chart")


# --- Step 5: relevance wiring (sections 4.1/4.2) -----------------------------

@pytest.fixture(scope="module")
def compendium():
    from topo_astro.significators.compendium import Compendium
    return Compendium.load()


def test_stage1_strong_pair_passes_with_compendium(compendium):
    # Birth of Son MERCURY:JUPITER is strong in the pairwise table.
    hits, misses = stage1({"Mercury": 100.0}, {"Jupiter": 100.0}, event_id=EventType.BIRTH_SON, compendium=compendium)
    assert len(hits) == 1
    assert misses == []


def test_stage1_excluded_pair_does_not_pass(compendium):
    # Birth of Son MARS:PLUTO is excluded ("only occasional exception").
    hits, misses = stage1({"Mars": 100.0}, {"Pluto": 100.0}, event_id=EventType.BIRTH_SON, compendium=compendium)
    assert hits == []
    assert len(misses) == 1
    assert misses[0]["kind"] == "excluded_relevance"
    assert misses[0]["progressed_point"] == "Mars"
    assert misses[0]["radix_point"] == "Pluto"


def test_stage1_absent_pair_does_not_pass(compendium):
    # Birth of Son MERCURY:NEPTUNE is not catalogued (absent != excluded).
    hits, misses = stage1({"Mercury": 100.0}, {"Neptune": 100.0}, event_id=EventType.BIRTH_SON, compendium=compendium)
    assert hits == []
    assert len(misses) == 1
    assert misses[0]["kind"] == "absent_relevance"


def test_stage1_weak_pair_goes_to_near_miss_ledger(compendium):
    # Birth of Son JUPITER:VENUS is weak - never gating (D3).
    hits, misses = stage1({"Venus": 100.0}, {"Jupiter": 100.0}, event_id=EventType.BIRTH_SON, compendium=compendium)
    assert hits == []
    assert len(misses) == 1
    assert misses[0]["kind"] == "weak_relevance"


def test_stage1_unordered_lookup_same_outcome(compendium):
    # Case A and Case B of the same unordered pair both pass (strong).
    hits_a, _ = stage1({"Mercury": 100.0}, {"Jupiter": 100.0}, event_id=EventType.BIRTH_SON, compendium=compendium)
    hits_b, _ = stage1({"Jupiter": 100.0}, {"Mercury": 100.0}, event_id=EventType.BIRTH_SON, compendium=compendium)
    assert len(hits_a) == 1
    assert len(hits_b) == 1


def test_stage2_arm1_tier_floor_boundaries(compendium):
    # Birth of Son: JUPITER tier 8 (pass), URANUS tier 6 (pass at floor),
    # PLUTO tier 4 (fail), SATURN tier 2 (fail).
    for slow, tier, expect_hit in [("Jupiter", 8, True), ("Uranus", 6, True),
                                   ("Pluto", 4, False), ("Saturn", 2, False)]:
        hits, misses = stage2({"Moon": 100.0}, {slow: 100.0},
                              prog_speeds={"Moon": 13.0}, radix_speeds={slow: 0.1},
                              event_id=EventType.BIRTH_SON, compendium=compendium)
        if expect_hit:
            assert len(hits) == 1, f"expected tier {tier} to pass"
        else:
            assert hits == [], f"expected tier {tier} to fail"
            floor_misses = [m for m in misses if m["kind"] == "tier_below_floor"]
            assert len(floor_misses) == 1
            assert floor_misses[0]["tier"] == tier


def test_stage2_arm1_absent_tier_fails_closed(compendium):
    # Birth of Brother has no SATURN tier data - the gate fails closed
    # (no data is never credit).
    hits, misses = stage2({"Moon": 100.0}, {"Saturn": 100.0},
                          prog_speeds={"Moon": 13.0}, radix_speeds={"Saturn": 0.1},
                          event_id=EventType.BIRTH_BROTHER, compendium=compendium)
    assert hits == []
    floor_misses = [m for m in misses if m["kind"] == "tier_below_floor"]
    assert len(floor_misses) == 1
    assert floor_misses[0]["tier"] is None


def test_no_data_event_type_zero_stage1_hits_and_reported(compendium):
    # POSITIVE_AC_MC has no compendium event at all - cannot contribute
    # any stage, and its non-contribution is reported (no_data ledger).
    hits, misses = stage1({"Mercury": 100.0}, {"Jupiter": 100.0},
                          event_id=EventType.POSITIVE_AC_MC, compendium=compendium)
    assert hits == []
    no_data = [m for m in misses if m["kind"] == "no_data"]
    assert len(no_data) == 1
    hits, misses = stage2({"Moon": 100.0}, {"Jupiter": 100.0},
                          prog_speeds={"Moon": 13.0}, radix_speeds={"Jupiter": 0.1},
                          event_id=EventType.POSITIVE_AC_MC, compendium=compendium)
    assert hits == []
    assert any(m["kind"] == "no_data" for m in misses)


def test_marked_none_event_stage1_zero_but_arm1_can_contribute(compendium):
    # Demobilization or Release is marked-none for the pairwise table
    # (zero stage-1 hits) but has tier data - arm 1 can still contribute
    # per section 3.7 (JUPITER tier 8; SATURN tier absent fails closed).
    hits, misses = stage1({"Mercury": 100.0}, {"Jupiter": 100.0},
                          event_id=EventType.DEMOBILIZATION_RELEASE, compendium=compendium)
    assert hits == []
    assert any(m["kind"] == "no_data" for m in misses)
    hits, _ = stage2({"Moon": 100.0}, {"Jupiter": 100.0},
                     prog_speeds={"Moon": 13.0}, radix_speeds={"Jupiter": 0.1},
                     event_id=EventType.DEMOBILIZATION_RELEASE, compendium=compendium)
    assert len(hits) == 1
    hits, misses = stage2({"Moon": 100.0}, {"Saturn": 100.0},
                          prog_speeds={"Moon": 13.0}, radix_speeds={"Saturn": 0.1},
                          event_id=EventType.DEMOBILIZATION_RELEASE, compendium=compendium)
    assert hits == []
    assert any(m["kind"] == "tier_below_floor" and m["tier"] is None for m in misses)


def test_real_sweep_hits_all_relevant_with_compendium(beyonce_case, compendium):
    # With the compendium wired, every stage-1 hit the sweep produces for
    # SUCCESS_ELECTED must resolve to strong in the pairwise table.
    radix_dt, event, geopos = beyonce_case
    points = list(pw.sweep_jds(radix_dt - timedelta(hours=6), radix_dt + timedelta(hours=6), 600))
    result = pw.collect_event_hits(points, [event], geopos, compendium=compendium)[0]
    from topo_astro.significators.compendium import to_compendium_symbol
    for hit in result["hits"]:
        if hit["stage"] != 1:
            continue
        strength = compendium.pair_strength(
            EventType.SUCCESS_ELECTED,
            to_compendium_symbol(hit["progressed_point"]),
            to_compendium_symbol(hit["radix_point"]),
        )
        assert strength == "strong", hit


# --- Step 6: ranges, consensus, margin, report (sections 3.7-3.10) -----------

B = 2451545.0


def fake_result(event_id, c1=(), c2=(), hits=()):
    """A minimal per-event result dict for the pass functions (real
    collect_event_hits output has the same shape)."""
    return {"event": {"datetime": datetime(2000, 1, 1), "event_type": event_id},
            "tuples": [], "c1": list(c1), "c2": list(c2),
            "hits": list(hits), "near_misses": []}


def fake_hit(jd, stage, arm="fast_to_slow", variant="dp", prog="Mercury",
             radix="Jupiter", aspect="conjunction", sep=0.1):
    return {"jd": jd, "stage": stage, "arm": arm, "variant": variant,
            "progressed_point": prog, "radix_point": radix, "aspect": aspect,
            "separation_deg": sep, "progressed_speed": 1.0, "radix_speed": 1.0}


def make_cfg(**overrides):
    """A config namespace: the resolved config module plus overrides (the
    spec's section 3.1 `config` parameter accepts any object exposing the
    same constants)."""
    from types import SimpleNamespace
    base = {k: v for k, v in vars(cfg).items() if not k.startswith("_")}
    base.update(overrides)
    return SimpleNamespace(**base)


def test_coarse_full_consensus_narrows():
    results = [
        fake_result(1, c1=[(B + 1, B + 9)]),
        fake_result(2, c1=[(B + 3, B + 12)]),
        fake_result(3, c1=[(B + 5, B + 15)]),
    ]
    out = pw.coarse_pass(results, B, B + 24, cfg)
    assert out["consensus"] == "full"
    assert out["window_jd"] == (B + 5, B + 9)
    assert out["corroboration"] == 3
    assert out["dropped_events"] == []


def test_coarse_partial_consensus_max_cardinality():
    # A and C intersect; B (20-30) intersects neither span. The
    # max-cardinality subset is {A, C} and the dropped event is visible.
    results = [
        fake_result(1, c1=[(B + 0, B + 10)]),
        fake_result(2, c1=[(B + 20, B + 30)]),
        fake_result(3, c1=[(B + 5, B + 15)]),
    ]
    out = pw.coarse_pass(results, B, B + 40, cfg)
    assert out["consensus"] == "partial"
    assert out["window_jd"] == (B + 5, B + 10)
    assert {e["event_type"] for e in out["subset_members"]} == {1, 3}
    assert [e["event_type"] for e in out["dropped_events"]] == [2]


def test_coarse_partial_consensus_disabled_by_knob():
    results = [
        fake_result(1, c1=[(B + 0, B + 10)]),
        fake_result(2, c1=[(B + 20, B + 30)]),
        fake_result(3, c1=[(B + 5, B + 15)]),
    ]
    out = pw.coarse_pass(results, B, B + 40, make_cfg(CONSENSUS_MAX_CARDINALITY=False))
    assert out["consensus"] == "none"
    assert out["window_jd"] == (B, B + 40)


def test_coarse_disjoint_fails_open_to_full_window():
    results = [
        fake_result(1, c1=[(B + 0, B + 2)]),
        fake_result(2, c1=[(B + 10, B + 12)]),
        fake_result(3, c1=[(B + 20, B + 22)]),
    ]
    out = pw.coarse_pass(results, B, B + 24, cfg)
    assert out["consensus"] == "none"
    assert out["window_jd"] == (B, B + 24)
    window, tier, reason = pw._select_final_window(
        results, out, {"consensus": "none", "window_jd": None}, B, B + 24, cfg)
    assert window == (B, B + 24)
    assert tier == "none"


def test_coarse_fewer_than_two_contributors_fails_open():
    results = [fake_result(1, c1=[(B + 1, B + 2)]), fake_result(2)]
    out = pw.coarse_pass(results, B, B + 24, cfg)
    assert out["consensus"] == "none"
    assert out["window_jd"] == (B, B + 24)
    assert out["corroboration"] == 1


def test_fine_narrows_within_coarse_window():
    results = [
        fake_result(1, c2=[(B + 10, B + 20)]),
        fake_result(2, c2=[(B + 12, B + 25)]),
    ]
    coarse = {"consensus": "full", "window_jd": (B + 5, B + 30), "corroboration": 0}
    margined = pw._apply_margin(coarse["window_jd"], 0, B, B + 40)
    fine = pw.fine_pass(results, margined, make_cfg(SAFETY_MARGIN_MINUTES=0))
    assert fine["consensus"] == "full"
    assert fine["window_jd"] == (B + 12, B + 20)


def test_empty_fine_consensus_returns_coarse_window():
    results = [
        fake_result(1, c2=[(B + 0, B + 1)]),
        fake_result(2, c2=[(B + 5, B + 6)]),
    ]
    coarse = {"consensus": "full", "window_jd": (B + 2, B + 4), "corroboration": 0}
    margined = pw._apply_margin(coarse["window_jd"], 0, B, B + 40)
    fine = pw.fine_pass(results, margined, make_cfg(SAFETY_MARGIN_MINUTES=0))
    assert fine["consensus"] == "none"
    window, tier, reason = pw._select_final_window(results, coarse, fine, B, B + 40, cfg)
    assert window == (B + 2, B + 4)
    assert tier == "usable"
    assert reason == "coarse_full"


def test_margin_applies_and_clamps_to_input_window():
    full = (B, B + 100)
    pad = 30.0 / 1440.0
    assert pw._apply_margin((B + 5, B + 10), 30, *full) == (B + 5 - pad, B + 10 + pad)
    assert pw._apply_margin((B, B + 2), 30, *full) == (B, B + 2 + pad)
    assert pw._apply_margin((B + 1, B + 100), 30, *full) == (B + 1 - pad, B + 100)
    assert pw._apply_margin((B - 5, B + 2), 30, *full) == (B, B + 2 + pad)
    assert pw._apply_margin((B - 5, B + 200), 30, *full) == full


def test_fine_outside_coarse_ledger_and_c2_clip():
    coarse = {"consensus": "full", "window_jd": (B + 5, B + 15), "corroboration": 0}
    margined = pw._apply_margin(coarse["window_jd"], 0, B, B + 40)
    results = [
        fake_result(1, c2=[(B + 8, B + 12)],
                    hits=[fake_hit(B + 9, 2), fake_hit(B + 30, 2)]),
        fake_result(2, c2=[(B + 9, B + 11)], hits=[fake_hit(B + 10, 2)]),
    ]
    fine = pw.fine_pass(results, margined, make_cfg(SAFETY_MARGIN_MINUTES=0))
    assert len(fine["fine_outside_coarse"]) == 1
    assert fine["fine_outside_coarse"][0]["hit"]["jd"] == B + 30
    assert results[0]["c2_fine"] == [(B + 8, B + 12)]


def test_tier_two_events_usable():
    results = [
        fake_result(1, c1=[(B + 1, B + 3)]),
        fake_result(2, c1=[(B + 2, B + 4)]),
    ]
    coarse = pw.coarse_pass(results, B, B + 24, cfg)
    fine = pw.fine_pass(results, coarse["window_jd"], cfg)
    window, tier, reason = pw._select_final_window(results, coarse, fine, B, B + 24, cfg)
    assert tier == "usable"
    assert reason == "coarse_full"
    assert window == (B + 2, B + 3)


def test_tier_single_event_usable_under_60_minutes():
    results = [fake_result(1, c2=[(B, B + 30.0 / 1440.0)])]
    coarse = pw.coarse_pass(results, B, B + 24, cfg)
    fine = pw.fine_pass(results, coarse["window_jd"], cfg)
    window, tier, reason = pw._select_final_window(results, coarse, fine, B, B + 24, cfg)
    assert tier == "usable"
    assert reason == "single_event"
    assert window == (B, B + 30.0 / 1440.0)


def test_tier_single_event_weak_over_60_minutes():
    results = [fake_result(1, c2=[(B, B + 120.0 / 1440.0)])]
    coarse = pw.coarse_pass(results, B, B + 24, cfg)
    fine = pw.fine_pass(results, coarse["window_jd"], cfg)
    window, tier, reason = pw._select_final_window(results, coarse, fine, B, B + 24, cfg)
    assert tier == "weak"
    assert window == (B, B + 120.0 / 1440.0)


def test_tier_none_zero_contributors():
    results = [fake_result(1), fake_result(2)]
    coarse = pw.coarse_pass(results, B, B + 24, cfg)
    fine = pw.fine_pass(results, coarse["window_jd"], cfg)
    window, tier, reason = pw._select_final_window(results, coarse, fine, B, B + 24, cfg)
    assert tier == "none"
    assert window == (B, B + 24)


def test_narrow_birth_time_window_end_to_end(beyonce_case, compendium):
    """The full entry point on a real chart: completes, final window is
    inside the input window, and the report carries every section-3.10
    field. A coarse STEP_SECONDS keeps the test sweep small."""
    radix_dt, event, geopos = beyonce_case
    cfg2 = make_cfg(STEP_SECONDS=900, SAFETY_MARGIN_MINUTES=15)
    report = pw.narrow_birth_time_window(
        radix_dt - timedelta(hours=1.5), radix_dt + timedelta(hours=1.5),
        radix_dt, geopos, [event], config=cfg2, compendium=compendium)
    assert report["tier"] in ("usable", "weak", "none")
    jd_lo, jd_hi = report["input_window_jd"]
    assert report["final_window_jd"][0] >= jd_lo
    assert report["final_window_jd"][1] <= jd_hi
    assert report["final_window_pre_margin_jd"] == report["final_window_jd"] or \
        report["final_window_pre_margin_jd"][0] >= report["final_window_jd"][0]
    assert isinstance(report["signed_distance_from_window_minutes"], float)
    assert report["errors"] == []
    assert len(report["events"]) == 1
    assert report["events"][0]["event"]["event_type"] == EventType.SUCCESS_ELECTED
    assert set(report["coarse"]) >= {"consensus", "window_jd", "corroboration",
                                     "events_with_data", "margin_minutes",
                                     "subset_members", "dropped_events"}
    assert "parameters" in report
    assert report["parameters"]["step_seconds"] == 900


def test_internal_error_fails_open_to_full_window(beyonce_case, compendium, monkeypatch):
    """Manual Step 6 item 4: on an internal error the pipeline returns the
    full window with tier none and surfaces the error - it never raises."""
    radix_dt, event, geopos = beyonce_case
    cfg2 = make_cfg(STEP_SECONDS=900)

    def boom(*args, **kwargs):
        raise RuntimeError("boom")
    monkeypatch.setattr(pw, "calc_planets_labelled", boom)
    report = pw.narrow_birth_time_window(
        radix_dt - timedelta(hours=1), radix_dt + timedelta(hours=1),
        radix_dt, geopos, [event], config=cfg2, compendium=compendium)
    assert report["tier"] == "none"
    assert report["tier_reason"] == "internal_error"
    assert report["final_window_jd"] == report["input_window_jd"]
    assert len(report["errors"]) == 1
    assert report["errors"][0]["type"] == "RuntimeError"