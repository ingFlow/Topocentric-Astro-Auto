"""
Golden-master generator for the Phase 2 characterization test suite.

THIS SCRIPT ACTUALLY IMPORTS AND RUNS THE REAL APPLICATION CODE.
It reproduces, function-for-function, the exact setup-and-dispatch sequence
that `app.py`'s `update_content()` route uses to build each technique object,
so the captured output is genuine end-to-end application behavior rather
than a hand-rolled approximation of it.

Run this once against the pre-refactor (or any refactor-in-progress) tree to
(re)produce the golden JSON files under fixtures/golden/. The pytest test
modules in tests/ then load those golden files and assert new runs still
match them exactly - they do NOT re-derive expected values themselves.

--------------------------------------------------------------------------
IMPORTANT - ephemeris precision caveat, please read before trusting these
numbers as final:

The source repository calls `swe.set_ephe_path('/usr/share/swisseph/ephe')`,
which does not exist in the environment this script was first run in. In
that case pyswisseph silently falls back to its built-in Moshier analytical
ephemeris instead of erroring. Moshier does not need external data files and
is accurate to a small fraction of an arcsecond for the Sun and a few
arcseconds for the outer planets across the date range this project uses,
which is generally far finer than the orbs this system checks aspects
against. But it is *not* guaranteed to be bit-identical to the full
file-based Swiss Ephemeris your original/production environment may have
been using at that path.

Recommendation: re-run this script once in an environment that has the real
ephemeris files at that path (or wherever you've relocated it to), and treat
its output as the authoritative golden set. Until then, treat the golden
files produced here as a correct-and-useful first draft, not a bit-exact
match to a from-file Swiss Ephemeris run. Every golden JSON file records
which mode was actually used (see the "ephemeris_flag" field) so this is
never ambiguous later.
--------------------------------------------------------------------------
"""

import json
import os
import sys
from datetime import datetime

import julian
import swisseph as swe

FIXTURES_DIR = os.path.dirname(os.path.abspath(__file__))
GOLDEN_DIR = os.path.join(FIXTURES_DIR, "golden")

# --------------------------------------------------------------------
# Point this at wherever the real source currently lives. During Phase 2
# this is still the flat, pre-Phase-4 tree; update SOURCE_ROOT once the
# Phase 4 package move has happened and re-run to confirm golden files
# are unaffected (they should be - Phase 4 is import-path-only).
# --------------------------------------------------------------------
SOURCE_ROOT = os.environ.get("TOPO_ASTRO_SOURCE_ROOT", "/home/claude/repo_extracted")
sys.path.insert(0, SOURCE_ROOT)

import constants  # noqa: E402
import aspects_base  # noqa: E402
import pd_automate  # noqa: E402
import secondary_automate  # noqa: E402
import pssr_swiss_auto  # noqa: E402
import transit_swiss_auto  # noqa: E402
import sra_auto  # noqa: E402
import harmonics_auto  # noqa: E402
import lunar_auto  # noqa: E402

from tests.fixtures.fixture_manifest import PEOPLE  # noqa: E402

EPHE_PATH = "/usr/share/swisseph/ephe"
swe.set_ephe_path(EPHE_PATH)


def ephemeris_mode_flag():
    """Probe which ephemeris backend swe is actually using right now, so
    every golden file can honestly record it (see module docstring)."""
    _, flag = swe.calc_ut(2451545.0, swe.SUN)
    if flag & swe.FLG_MOSEPH:
        return "moseph (Moshier analytical fallback - no ephemeris files found at EPHE_PATH)"
    if flag & swe.FLG_SWIEPH:
        return "swieph (file-based Swiss Ephemeris - EPHE_PATH files were found and used)"
    return f"unknown (raw flag={flag})"


def apply_house_label_substitution(s):
    """Exactly reproduces the four re.sub() calls app.py runs on every
    aspect string before display, so golden output matches what a person
    actually sees, not just the raw technique-object return value."""
    import re
    s = re.sub(r"H10,", "MC,", s)
    s = re.sub(r"H1,", "AS,", s)
    s = re.sub(r"H7,", "DS,", s)
    s = re.sub(r"H4,", "IC,", s)
    return s


def run_all_techniques_for(geo_pos_natal, jd_radix, dt_event, event_geopos):
    """Reproduces app.py's update_content() setup-and-dispatch sequence
    exactly, for every technique, against one (radix, event) pair."""
    jd_event = julian.to_jd(dt_event)
    e = aspects_base.calculate_obliquity(jd_event)

    rad_houses_info = swe.houses(jd_radix, geo_pos_natal[0], geo_pos_natal[1], b'T')
    rad_planets_equatorial = pd_automate.calc_rad_planets_equatorial(jd_radix)
    rad_planets_pof_houses_labelled = constants.calc_planets_pof_houses_labelled(jd_radix, geo_pos_natal)

    out = {}

    # --- Primary Direction ---
    pd_obj = pd_automate.PD_Automate(
        jd_radix, jd_event, geo_pos_natal,
        rad_planets_pof_houses_labelled, rad_planets_equatorial, rad_houses_info, e,
    )
    dir_a, conv_a = pd_obj.get_aspects_str()
    out["PRIMARY_DIRECT"] = {
        "direct": apply_house_label_substitution(dir_a),
        "converse": apply_house_label_substitution(conv_a),
        "info": stringify_info(pd_obj.get_extended_information()),
        "mdos_natal": stringify_info(pd_obj.get_mdos_natal()),
    }

    # --- Secondary Progressions ---
    sec_obj = secondary_automate.Secondary_Auto(
        jd_radix, jd_event, geo_pos_natal[0], geo_pos_natal[1], e,
        rad_houses_info[1][2], rad_planets_pof_houses_labelled,
    )
    prog_a, reg_a = sec_obj.get_str_aspects()
    out["SECONDARY_DIRECT"] = {
        "direct": apply_house_label_substitution(prog_a),
        "converse": apply_house_label_substitution(reg_a),
        "info": stringify_info(sec_obj.get_dict_info()),
    }

    # --- PSSR ---
    pssr_obj = pssr_swiss_auto.PSSR_Auto(
        julian.from_jd(jd_radix), dt_event, rad_planets_pof_houses_labelled,
    )
    pssr_dir, pssr_conv = pssr_obj.get_str_aspects()
    out["PSSR"] = {
        "direct": apply_house_label_substitution(pssr_dir),
        "converse": apply_house_label_substitution(pssr_conv),
        "info": stringify_info(pssr_obj.get_dict_info()),
    }

    # --- Transit ---
    trans_obj = transit_swiss_auto.Transit_Auto(
        jd_radix, jd_event, event_geopos, rad_planets_pof_houses_labelled,
    )
    trans_dir, trans_conv = trans_obj.get_str_aspects()
    out["TRANSIT"] = {
        "direct": apply_house_label_substitution(trans_dir),
        "converse": apply_house_label_substitution(trans_conv),
        "info": stringify_info(trans_obj.get_dict_info()),
    }

    # --- SRA ---
    sra_obj = sra_auto.SRA_Auto(
        julian.from_jd(jd_radix), dt_event, geo_pos_natal, rad_planets_pof_houses_labelled,
    )
    sra_dir, sra_conv = sra_obj.get_str_aspects()
    sra_all = (sra_dir + sra_conv)
    sra_all = apply_house_label_substitution(sra_all).replace(")(", ")\n(")
    out["SRA"] = {
        "combined": sra_all,
        "info": stringify_info(sra_obj.get_info()),
    }

    # --- Lunar ---
    lunar_obj = lunar_auto.Lunar_Auto(
        julian.from_jd(jd_radix), dt_event, event_geopos, geo_pos_natal, 1,
    )
    all_charts = lunar_obj.get_all_lunars()
    str_all = lunar_auto.get_str_labelled_aspects_from_array(all_charts)
    str_all_sub = apply_house_label_substitution(str_all)
    counts = lunar_auto.count_each_planet_lunars(str_all_sub)
    str_counts = lunar_auto.get_str_planet_counts(counts)
    mal_count, ben_count = lunar_auto.count_mal_ben_from_str_aspects(str_all_sub)
    out["LUNAR"] = {
        "labelled_aspects": str_all_sub,
        "info": stringify_info(lunar_obj.get_info()),
        "planet_counts": str_counts,
        "malefic_count": mal_count,
        "benefic_count": ben_count,
    }

    # --- Harmonics ---
    harm_obj = harmonics_auto.Harmonics_Auto(
        jd_radix, jd_event, geo_pos_natal, rad_planets_pof_houses_labelled,
    )
    harm_str = harm_obj.get_str_aspects()
    out["HARMONICS"] = {
        "combined": apply_house_label_substitution(harm_str),
        "info": stringify_info(harm_obj.get_dict_info()),
    }

    # --- Natal (not a technique object - app.py just lists the radix planets) ---
    natal_str = ""
    for p in rad_planets_pof_houses_labelled:
        natal_str += f"{p}\n"
    out["NATAL"] = {"combined": apply_house_label_substitution(natal_str)}

    return out


def stringify_info(info):
    """Info dicts/tuples can contain floats, tuples, datetimes, or nested
    structures that aren't natively JSON-safe (e.g. tuple keys, datetime
    values). Converts to a JSON-safe structure while preserving every
    value exactly (datetimes become ISO strings, round-trippable with
    datetime.fromisoformat)."""
    if isinstance(info, datetime):
        return {"__datetime__": info.isoformat()}
    if isinstance(info, dict):
        return {str(k): stringify_info(v) for k, v in info.items()}
    if isinstance(info, (list, tuple)):
        return [stringify_info(v) for v in info]
    return info


def generate_for_person(person_key, person_cfg):
    with open(person_cfg["file"]) as f:
        birth_data = json.load(f)

    geo_pos_natal = birth_data["geopos_natal"]
    events_by_dt = {e["datetime"]: e for e in birth_data["list_of_events"]}

    result = {
        "person": person_key,
        "timezone_scenario": person_cfg["timezone_scenario"],
        "ephemeris_mode": ephemeris_mode_flag(),
        "geo_pos_natal": geo_pos_natal,
        "candidates": {},
    }

    for cand_label, cand_dt_str in person_cfg["candidates"].items():
        radix_dt = datetime.fromisoformat(cand_dt_str)
        jd_radix = julian.to_jd(radix_dt)

        cand_result = {"radix_datetime": cand_dt_str, "jd_radix": jd_radix, "events": {}}

        for event_dt_str in person_cfg["event_datetimes"]:
            event = events_by_dt.get(event_dt_str)
            if event is None:
                raise KeyError(
                    f"{person_key}: no event with datetime {event_dt_str} in {person_cfg['file']}"
                )
            dt_event = datetime.fromisoformat(event["datetime"])
            event_geopos = event.get("geopos", geo_pos_natal)

            techniques_out = run_all_techniques_for(geo_pos_natal, jd_radix, dt_event, event_geopos)

            cand_result["events"][event_dt_str] = {
                "event_type": event["event_type"],
                "event_geopos": event_geopos,
                "techniques": techniques_out,
            }

        result["candidates"][cand_label] = cand_result

    return result


def main():
    os.makedirs(GOLDEN_DIR, exist_ok=True)
    print(f"Ephemeris mode in use: {ephemeris_mode_flag()}")
    for person_key, person_cfg in PEOPLE.items():
        print(f"Generating golden data for {person_key} ...")
        result = generate_for_person(person_key, person_cfg)
        out_path = os.path.join(GOLDEN_DIR, f"{person_key}_techniques.json")
        with open(out_path, "w") as f:
            json.dump(result, f, indent=2, sort_keys=False)
        print(f"  wrote {out_path}")
    print("Done.")


if __name__ == "__main__":
    main()
