"""
Step 3 (plumbing) regression tests: the three extraction refactors that
must not change observable behavior, and the new speed plumb.

Covers, per spec docs/pssr_window_narrowing_design_v5.md:
    section 5.3 - PSSR_Auto(return_speeds=False) is byte-identical to the
                  pre-change output; return_speeds=True adds exactly the
                  four documented speed keys, parallel to the existing
                  position lists.
    section 5.4 - calc_planets_labelled_speeds keeps xx[3] alongside
                  xx[0]; positions/labels match calc_planets_labelled;
                  the existing function is untouched.
    section 5.5 - the orb literals in find_pssr_swiss_aspects are now
                  named constants with unchanged values and semantics.

The golden files (test_techniques_golden.py) are the authoritative
byte-identical regression for PSSR_Auto's default path; the tests here
pin the new surface and the orb semantics directly.
"""

from datetime import datetime

import julian
import swisseph as swe
import pytest

from topo_astro.core.aspects import (
    PSSR_MOON_ORB_DEG,
    PSSR_PLANET_ORB_DEG,
    find_pssr_swiss_aspects,
)
from topo_astro.core.constants import (
    PLANETS,
    calc_planets_labelled,
    calc_planets_labelled_speeds,
)
from topo_astro.techniques.pssr import PSSR_Auto, exclude_planets

from tests.fixtures.fixture_manifest import BIRTH_DATA_DIR, PEOPLE

PERSON = next(iter(PEOPLE))


@pytest.fixture(scope="module")
def pssr_case():
    """One real (person, candidate, event) case for the PSSR plumbing."""
    import json
    import os

    birth = json.load(open(os.path.join(BIRTH_DATA_DIR, f"{PERSON}.json"), encoding="utf-8"))
    person_cfg = PEOPLE[PERSON]
    radix_dt = datetime.fromisoformat(next(iter(person_cfg["candidates"].values())))
    events_by_dt = {e["datetime"]: e for e in birth["list_of_events"]}
    event_dt_str = person_cfg["event_datetimes"][0]
    dt_event = datetime.fromisoformat(events_by_dt[event_dt_str]["datetime"])
    return radix_dt, dt_event, birth["geopos_natal"]


# --- section 5.4: calc_planets_labelled_speeds --------------------------------

def test_speeds_match_labelled_positions():
    jd = julian.to_jd(datetime(1980, 6, 1, 12, 0, 0))
    pos = calc_planets_labelled(jd, "(dp)")
    spd = calc_planets_labelled_speeds(jd, "(dp)")
    assert len(spd) == len(pos) == len(PLANETS)
    for (p_name, p_long, p_label), (s_name, s_long, s_speed, s_label) in zip(pos, spd):
        assert s_name == p_name
        assert s_long == p_long
        assert s_label == p_label
        assert isinstance(s_speed, float)


def test_speeds_match_swe_calc_ut_directly():
    jd = julian.to_jd(datetime(1980, 6, 1, 12, 0, 0))
    spd = calc_planets_labelled_speeds(jd, "(dp)")
    for index, (name, _long, speed, _label) in enumerate(spd):
        xx, _ = swe.calc_ut(jd, index)
        assert name == PLANETS[index]
        assert speed == xx[3]


def test_speed_sanity_moon_and_venus():
    jd = julian.to_jd(datetime(1980, 6, 1, 12, 0, 0))
    spd = calc_planets_labelled_speeds(jd, "(dp)")
    speeds = dict((name, abs(speed)) for name, _l, speed, _t in spd)
    assert 11.7 <= speeds["Moon"] <= 15.5
    # Venus can be near station (~0) or fast (~1.25'/day max); it must
    # never be a retrograde-like large magnitude.
    assert 0.0 <= speeds["Venus"] <= 1.5


def test_calc_planets_labelled_untouched_shape():
    jd = julian.to_jd(datetime(1980, 6, 1, 12, 0, 0))
    for entry in calc_planets_labelled(jd, "(dp)"):
        assert len(entry) == 3


# --- section 5.5: named orb constants, unchanged semantics --------------------

def test_orb_constant_values():
    assert PSSR_PLANET_ORB_DEG == 12 / 60
    assert PSSR_MOON_ORB_DEG == 32 / 60


def test_finder_moon_conj_opp_uses_32_arcmin():
    # A Moon conjunction at ~25.2' fires (32' orb), even though it is far
    # beyond the 12' fast-to-slow orb.
    radix = [("Sun", 100.0, "(r)")]
    direct = [("Moon", 100.42, "(dp)")]
    out = find_pssr_swiss_aspects(radix, direct)
    assert "conjunction" in out


def test_finder_non_moon_uses_12_arcmin():
    # A Sun->Mars conjunction at ~25.2' is beyond the 12' orb: no aspect.
    radix = [("Sun", 100.0, "(r)")]
    direct = [("Mars", 100.42, "(dp)")]
    assert find_pssr_swiss_aspects(radix, direct) == ""
    # But at 9' it fires.
    radix = [("Sun", 100.0, "(r)")]
    direct = [("Mars", 100.15, "(dp)")]
    assert "conjunction" in find_pssr_swiss_aspects(radix, direct)


def test_finder_moon_non_conj_opp_18_arcmin_filter():
    # Moon square at ~25.2': within the 32' orb, but beyond the 18'
    # general-Moon filter, so it is suppressed.
    radix = [("Sun", 100.0, "(r)")]
    direct = [("Moon", 100.42 + 90.0, "(dp)")]
    assert find_pssr_swiss_aspects(radix, direct) == ""
    # Moon square at ~15': within the 18' filter, so it fires.
    radix = [("Sun", 100.0, "(r)")]
    direct = [("Moon", 100.25 + 90.0, "(dp)")]
    assert "square" in find_pssr_swiss_aspects(radix, direct)


# --- section 5.3: PSSR_Auto return_speeds -------------------------------------

def test_default_and_explicit_false_identical(pssr_case):
    radix_dt, dt_event, geopos = pssr_case
    base = PSSR_Auto(radix_dt, dt_event, geopos=geopos)
    explicit = PSSR_Auto(radix_dt, dt_event, geopos=geopos, return_speeds=False)
    assert base.get_dict_info() == explicit.get_dict_info()


def test_return_speeds_adds_exactly_four_keys(pssr_case):
    radix_dt, dt_event, geopos = pssr_case
    base = PSSR_Auto(radix_dt, dt_event, geopos=geopos).get_dict_info()
    sped = PSSR_Auto(radix_dt, dt_event, geopos=geopos, return_speeds=True).get_dict_info()
    added = set(sped.keys()) - set(base.keys())
    assert added == {
        "prog_dir_speeds", "reg_dir_speeds", "prog_conv_speeds", "reg_conv_speeds",
    }


def test_speed_lists_parallel_to_position_lists(pssr_case):
    radix_dt, dt_event, geopos = pssr_case
    info = PSSR_Auto(radix_dt, dt_event, geopos=geopos, return_speeds=True).get_dict_info()
    # direct/converse_planets are each prog+reg concatenated, so the prog
    # speed list is parallel to the first half and the reg speed list to
    # the second half.
    for speeds_key, planets_key in [
        ("prog_dir_speeds", "direct_planets"),
        ("reg_dir_speeds", "direct_planets"),
        ("prog_conv_speeds", "converse_planets"),
        ("reg_conv_speeds", "converse_planets"),
    ]:
        speeds = info[speeds_key]
        planets = info[planets_key]
        assert len(planets) == 2 * len(speeds)
        half = len(speeds)
        if speeds_key.startswith("prog"):
            aligned = planets[:half]
        else:
            aligned = planets[half:]
        for (s_name, s_long, s_speed, s_label), (p_name, p_long, p_label) in zip(speeds, aligned):
            assert s_name == p_name
            assert s_label == p_label
            assert s_long == p_long
            assert isinstance(s_speed, float)


def test_speed_lists_match_recomputed_from_exposed_datetimes(pssr_case):
    radix_dt, dt_event, geopos = pssr_case
    info = PSSR_Auto(radix_dt, dt_event, geopos=geopos, return_speeds=True).get_dict_info()
    for jd_key, speeds_key in [
        ("dt_prog_pssr_direct", "prog_dir_speeds"),
        ("dt_reg_pssr_direct", "reg_dir_speeds"),
        ("dt_prog_pssr_converse", "prog_conv_speeds"),
        ("dt_reg_pssr_converse", "reg_conv_speeds"),
    ]:
        # Round-tripping the JD through the exposed datetime loses a little
        # float precision, so compare element-wise with approx tolerance.
        jd = julian.to_jd(info[jd_key])
        label = info[speeds_key][0][3]
        expected = exclude_planets(calc_planets_labelled_speeds(jd, label), ["Sun"])
        assert [e[0] for e in expected] == [s[0] for s in info[speeds_key]]
        assert [e[3] for e in expected] == [s[3] for s in info[speeds_key]]
        for (e_name, e_long, e_speed, e_label), (s_name, s_long, s_speed, s_label) in zip(
            expected, info[speeds_key]
        ):
            assert e_name == s_name and e_label == s_label
            assert e_long == pytest.approx(s_long, abs=1e-5)
            assert e_speed == pytest.approx(s_speed, abs=1e-5)