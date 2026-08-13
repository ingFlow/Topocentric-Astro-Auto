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


def stage1(prog, radix, prog_speeds=None, radix_speeds=None, event_id=EventType.SUCCESS_ELECTED):
    """Thin convenience wrapper: stage-1 evaluation on sparse synthetic
    point sets (missing speeds default to a fast/typical value)."""
    prog_speeds = prog_speeds or {name: 1.2 for name in prog}
    radix_speeds = radix_speeds or {name: 1.0 for name in radix}
    return pw.stage1_hits(0.0, "dp", prog, prog_speeds, radix, radix_speeds, event_id)


def stage2(prog, radix, prog_speeds=None, radix_speeds=None, event_id=EventType.SUCCESS_ELECTED):
    prog_speeds = prog_speeds or {name: 1.2 for name in prog}
    radix_speeds = radix_speeds or {name: 1.0 for name in radix}
    return pw.stage2_hits(0.0, "dp", prog, prog_speeds, radix, radix_speeds, event_id)


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