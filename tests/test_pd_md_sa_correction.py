"""
Primary Directions: the MD > SA quadrant-shift correction in PD_Base.

This is "Bug #1" territory per the Developer Manual - a documented,
historically-tricky edge case in the spherical-trig core. Rather than
construct a synthetic fixture for it, this file exercises a real,
naturally-occurring trigger found by instrumenting PD_Base against the
full real event lists of all four fixture people (2,706 individual
planet-direction checks searched): Richard Wagner's dt_radix_start
candidate (1813-05-22T02:00:00, distinct from his dt_actual_dob of
1813-05-22T02:53:28) puts Pluto in house 12 in a configuration where
MD > SA on the first check, forcing the quadrant-shift retry.

Scope note: the correction succeeds on its first retry for this case (no
second/third escalation, no log_md_sa.txt write). A search of all four
people's complete real event lists found no naturally-occurring case that
forces the deeper escalation path (pd_base.py lines ~25-37) - that deeper
path remains uncharacterized by real data. Flagged here explicitly rather
than fabricated, per the same standard the rest of this suite follows.
"""

import os

import julian
import swisseph as swe
from datetime import datetime

import pd_base
import pd_automate
import aspects_base
from constants import PLANETS


WAGNER_GEOPOS = [51.33333333333333, 12.38333333333333, 113.0]
WAGNER_RADIX_START = "1813-05-22T02:00:00"  # the trigger candidate - see module docstring
WAGNER_EVENT = "1836-07-07T12:00:00"


def _instrument_and_run(radix_str, event_str, geopos):
    """Runs calc_directed_pd_planets with calc_md_to_oa_data instrumented
    to record every (MD, SA) pair where MD > SA on the pre-correction
    check, tagged with which planet triggered it."""
    original = pd_base.calc_md_to_oa_data
    fires = []
    current_planet = {"name": None}

    def wrapped(RA, RAMC, quadrant, GEO_LAT, DECL, ac, long):
        result = original(RA, RAMC, quadrant, GEO_LAT, DECL, ac, long)
        MD, AD, SA, phi, ADP, OA_OD, FLAG_ASCEN = result
        if MD > SA:
            fires.append({"planet": current_planet["name"], "MD": MD, "SA": SA, "quadrant": quadrant})
        return result

    pd_base.calc_md_to_oa_data = wrapped
    try:
        jd_radix = julian.to_jd(datetime.fromisoformat(radix_str))
        jd_event = julian.to_jd(datetime.fromisoformat(event_str))
        e = aspects_base.calculate_obliquity(jd_event)
        rad_houses_info = swe.houses(jd_radix, geopos[0], geopos[1], b'T')
        rad_planets_equatorial = pd_automate.calc_rad_planets_equatorial(jd_radix)

        results = {}
        for idx, planet_name in enumerate(PLANETS):
            current_planet["name"] = planet_name
            fires_before = len(fires)
            long, ra, decl = rad_planets_equatorial[idx]
            cusps = rad_houses_info[0]
            p_house = pd_base.get_housepos_manual(long, cusps)
            ac, mc, ramc = pd_automate.calc_radix_ac_mc_ramc(rad_houses_info)

            direct_obj = pd_base.PD_Base(jd_radix, jd_event, geopos[0], decl, ra, ramc, mc, True, p_house, ac, long, e)
            conv_obj = pd_base.PD_Base(jd_radix, jd_event, geopos[0], decl, ra, ramc, mc, False, p_house, ac, long, e)

            results[planet_name] = {
                "house": p_house,
                "triggered_correction": len(fires) > fires_before,
                "direct_long": direct_obj.get_long_directed(),
                "converse_long": conv_obj.get_long_directed(),
                "final_MD": direct_obj.MD,
                "final_SA": direct_obj.SA,
                "final_MDO": direct_obj.MDO,
            }
        return results, fires
    finally:
        pd_base.calc_md_to_oa_data = original


class TestMdSaQuadrantCorrection:
    def test_pluto_triggers_correction_for_wagner_radix_start(self):
        results, fires = _instrument_and_run(WAGNER_RADIX_START, WAGNER_EVENT, WAGNER_GEOPOS)
        assert results["Pluto"]["triggered_correction"] is True
        assert results["Pluto"]["house"] == 12

    def test_only_pluto_triggers_it_for_this_fixture_not_other_planets(self):
        """Confirms the trigger is specific (Pluto/house 12 for this exact
        radix), not a sign that every planet in this chart is broken -
        an important distinction when this test is read later."""
        results, fires = _instrument_and_run(WAGNER_RADIX_START, WAGNER_EVENT, WAGNER_GEOPOS)
        triggered = [p for p, r in results.items() if r["triggered_correction"]]
        assert triggered == ["Pluto"]

    def test_correction_resolves_after_one_retry_no_log_file(self, tmp_path, monkeypatch):
        """The correction succeeds on its first attempt here - MD ends up
        < SA (post-correction) and no log_md_sa.txt entry is written. If
        this ever starts writing to the log file, that means the deeper,
        currently-uncharacterized escalation path (see module docstring)
        has started firing for this fixture, which is itself worth
        knowing about even though it isn't what this test is checking for."""
        monkeypatch.chdir(tmp_path)  # log_md_sa.txt, if written, lands here, not in the source tree
        results, fires = _instrument_and_run(WAGNER_RADIX_START, WAGNER_EVENT, WAGNER_GEOPOS)

        assert results["Pluto"]["final_MD"] < results["Pluto"]["final_SA"], (
            "post-correction MD should be < SA; if this fails, the single retry "
            "no longer resolves the case and log_md_sa.txt should exist"
        )
        assert not os.path.exists("log_md_sa.txt")

    def test_final_directed_longitudes_are_valid_degrees(self):
        """The corrected calculation must still produce a normal, in-range
        directed longitude - the correction existing at all doesn't mean
        much if it silently produces nonsense output."""
        results, fires = _instrument_and_run(WAGNER_RADIX_START, WAGNER_EVENT, WAGNER_GEOPOS)
        pluto = results["Pluto"]
        assert 0.0 <= pluto["direct_long"] < 360.0
        assert 0.0 <= pluto["converse_long"] < 360.0
        assert round(pluto["final_MDO"], 4) == round((pluto["final_MD"] / pluto["final_SA"]) * 90, 4)

    def test_wagners_actual_dob_candidate_does_not_trigger_it(self):
        """Cross-check: the correction is specific to dt_radix_start, not a
        general property of Wagner's chart - his dt_actual_dob candidate
        (53 minutes later) does not trigger it for any planet."""
        results, fires = _instrument_and_run("1813-05-22T02:53:28", WAGNER_EVENT, WAGNER_GEOPOS)
        assert not any(r["triggered_correction"] for r in results.values())
