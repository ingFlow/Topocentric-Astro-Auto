"""
The centerpiece of the Phase 2 characterization suite: re-runs every
technique, for every (person, candidate, event) combination in the golden
files, and asserts the live output still matches exactly.

Deliberately imports and reuses run_all_techniques_for from
fixtures/generate_golden_files.py rather than re-implementing the
setup-and-dispatch sequence a second time here - if this file and the
generator ever computed that sequence differently, a mismatch between them
would look like a false "regression" (or worse, a false "all clear") that
had nothing to do with the actual application code. There must be exactly
one place that knows how to call each of the seven techniques.

If any test in this file fails after a refactor phase, that phase changed
observable behavior and must not proceed until the difference is understood
and either fixed (if accidental) or the golden file is deliberately
regenerated and re-reviewed (if the change was intended).
"""

import json
import os

import pytest

from tests.fixtures.generate_golden_files import run_all_techniques_for, stringify_info
from tests.fixtures.fixture_manifest import PEOPLE, GOLDEN_DIR, BIRTH_DATA_DIR


def _load_golden(person_key):
    with open(os.path.join(GOLDEN_DIR, f"{person_key}_techniques.json")) as f:
        return json.load(f)


def _load_birth_data(person_key):
    with open(os.path.join(BIRTH_DATA_DIR, f"{person_key}.json")) as f:
        return json.load(f)


def _iter_all_cases():
    """Yields (person_key, candidate_label, event_datetime_str) for every
    combination captured in the golden files, so pytest can report each
    one as its own separately-collected, separately-failable test case
    rather than one monolithic all-or-nothing test."""
    for person_key, person_cfg in PEOPLE.items():
        for candidate_label in person_cfg["candidates"]:
            for event_dt_str in person_cfg["event_datetimes"]:
                yield (person_key, candidate_label, event_dt_str)


ALL_CASES = list(_iter_all_cases())
ALL_CASE_IDS = [f"{p}-{c}-{e}" for p, c, e in ALL_CASES]


@pytest.mark.parametrize("person_key,candidate_label,event_dt_str", ALL_CASES, ids=ALL_CASE_IDS)
def test_all_techniques_match_golden(person_key, candidate_label, event_dt_str):
    import julian
    from datetime import datetime

    golden = _load_golden(person_key)
    birth_data = _load_birth_data(person_key)
    geo_pos_natal = birth_data["geopos_natal"]
    events_by_dt = {e["datetime"]: e for e in birth_data["list_of_events"]}

    cand_golden = golden["candidates"][candidate_label]
    radix_dt = datetime.fromisoformat(cand_golden["radix_datetime"])
    jd_radix = julian.to_jd(radix_dt)

    event = events_by_dt[event_dt_str]
    dt_event = datetime.fromisoformat(event["datetime"])
    event_geopos = event.get("geopos", geo_pos_natal)

    live = run_all_techniques_for(geo_pos_natal, jd_radix, dt_event, event_geopos)
    live_json_safe = json.loads(json.dumps(stringify_info(live)))

    expected = cand_golden["events"][event_dt_str]["techniques"]

    assert live_json_safe == expected, (
        f"{person_key}/{candidate_label}/{event_dt_str}: live technique output "
        f"no longer matches the golden file - see the diff above for which "
        f"technique/field changed."
    )


@pytest.mark.parametrize("person_key", list(PEOPLE.keys()))
def test_golden_file_exists_and_has_expected_shape(person_key):
    """A lighter-weight sanity check independent of the heavy parametrized
    comparison above - catches a missing/corrupted golden file with a
    clear message rather than a wall of unrelated-looking failures."""
    golden = _load_golden(person_key)
    assert golden["person"] == person_key
    assert "ephemeris_mode" in golden
    assert set(golden["candidates"].keys()) == set(PEOPLE[person_key]["candidates"].keys())
    for cand in golden["candidates"].values():
        assert set(cand["events"].keys()) == set(PEOPLE[person_key]["event_datetimes"])
        for event in cand["events"].values():
            assert set(event["techniques"].keys()) == {
                "PRIMARY_DIRECT", "SECONDARY_DIRECT", "PSSR", "TRANSIT",
                "SRA", "LUNAR", "HARMONICS", "NATAL",
            }
