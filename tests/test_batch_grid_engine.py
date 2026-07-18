"""
Batch engine: the grid-generation pipeline (generate_grid_times_manual ->
append_grid_acceptable_angles -> the raw str(list)-per-line grid file
format), run end-to-end against real fixture data.

Also directly exercises and documents the hidden global state (grid_aspects,
date_technique, aspect_type) the migration plan's Phase 7 removes -
resetvars() is called before and after every test in this file so this
suite doesn't itself become a source of the exact cross-test state leakage
Phase 7 is designed to eliminate.

Scope note: only PRIMARY_DIRECT is exercised here as the representative
technique. append_grid_acceptable_angles's own source only has explicit
branches for PRIMARY_DIRECT, SECONDARY_DIRECT, PSSR, TRANSIT, and SRA -
Harmonics and Lunar are confirmed (by reading the source) not wired into
batch mode at all, matching the Developer Manual's own account. A fuller
follow-up pass could add SECONDARY_DIRECT/PSSR/TRANSIT/SRA cases the same
way; this file establishes the pattern and covers the one most load-bearing
case (PRIMARY_DIRECT is also what the significator-scoring tests already
exercise most heavily).
"""

import ast
import os

import julian
import swisseph as swe
from datetime import datetime

import process_techniques_files as ptf
import pd_automate

swe.set_ephe_path("/usr/share/swisseph/ephe")

BEYONCE_GEOPOS = [29.7217, -95.3875, 32]
BEYONCE_RADIX_DT = datetime.fromisoformat("1981-09-04T02:28:44")


def _reset_ptf_globals():
    ptf.resetvars()


class TestGenerateGridTimesManualEndToEnd:
    def setup_method(self):
        _reset_ptf_globals()

    def teardown_method(self):
        _reset_ptf_globals()

    def test_writes_one_header_row_plus_one_row_per_candidate_time(self, tmp_path):
        list_dt_events = [
            (datetime.fromisoformat("2012-01-07T12:00:00"), pd_automate.EventType.BIRTH_DAUGHTER, BEYONCE_GEOPOS),
            (datetime.fromisoformat("2005-09-10T12:00:00"), pd_automate.EventType.DIVORCE_SEPARATION, BEYONCE_GEOPOS),
        ]
        candidate_times = [
            BEYONCE_RADIX_DT,
            BEYONCE_RADIX_DT.replace(minute=33, second=44),  # a second, nearby candidate
        ]
        out_prefix = str(tmp_path / "beyonce_grid_test")

        ptf.generate_grid_times_manual(
            out_prefix, candidate_times, list_dt_events, BEYONCE_GEOPOS,
            pd_automate.AspectType.ANGLE_HOUSE_PRIMARY, ptf.TechniqueType.PRIMARY_DIRECT,
        )

        out_path = out_prefix + ".txt"
        assert os.path.exists(out_path)
        with open(out_path) as f:
            lines = [l for l in f.read().split("\n") if l.strip()]

        # header row + one row per candidate time
        assert len(lines) == 1 + len(candidate_times)

        header_row = ast.literal_eval(lines[0])
        assert header_row[0] == "Time"
        assert header_row[-1] == "Count"
        assert len(header_row) == 1 + len(list_dt_events) + 1  # Time, N events, Count

        for data_line in lines[1:]:
            row = ast.literal_eval(data_line)
            assert len(row) == len(header_row)
            assert isinstance(row[-1], int)  # the Count column

    def test_grid_aspects_global_accumulates_across_multiple_calls_until_reset(self, tmp_path):
        """Directly demonstrates the hidden global state Phase 7 removes:
        grid_aspects keeps growing across separate generate_grid_times_manual
        calls unless resetvars() is called between them - this is the exact
        behavior main_techniques.py's orchestration functions currently
        depend on remembering to do."""
        list_dt_events = [
            (datetime.fromisoformat("2012-01-07T12:00:00"), pd_automate.EventType.BIRTH_DAUGHTER, BEYONCE_GEOPOS),
        ]

        ptf.generate_grid_times_manual(
            str(tmp_path / "run1"), [BEYONCE_RADIX_DT], list_dt_events, BEYONCE_GEOPOS,
            pd_automate.AspectType.ANGLE_HOUSE_PRIMARY, ptf.TechniqueType.PRIMARY_DIRECT,
        )
        rows_after_run1 = len(ptf.grid_aspects)

        # WITHOUT calling resetvars(), run a second, independent grid generation
        ptf.generate_grid_times_manual(
            str(tmp_path / "run2"), [BEYONCE_RADIX_DT], list_dt_events, BEYONCE_GEOPOS,
            pd_automate.AspectType.ANGLE_HOUSE_PRIMARY, ptf.TechniqueType.PRIMARY_DIRECT,
        )
        rows_after_run2 = len(ptf.grid_aspects)

        assert rows_after_run2 > rows_after_run1, (
            "expected grid_aspects to have accumulated rows from BOTH calls "
            "since resetvars() was not called between them - if this ever "
            "fails, the global-state leak this test documents has already "
            "been fixed (e.g. by Phase 7), which is good, but means this "
            "test needs deliberately updating, not silently left behind"
        )

    def test_resetvars_clears_grid_aspects_and_technique_selection(self):
        list_dt_events = [
            (datetime.fromisoformat("2012-01-07T12:00:00"), pd_automate.EventType.BIRTH_DAUGHTER, BEYONCE_GEOPOS),
        ]
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            ptf.generate_grid_times_manual(
                os.path.join(d, "run"), [BEYONCE_RADIX_DT], list_dt_events, BEYONCE_GEOPOS,
                pd_automate.AspectType.ANGLE_HOUSE_PRIMARY, ptf.TechniqueType.PRIMARY_DIRECT,
            )
        assert len(ptf.grid_aspects) > 0
        assert ptf.date_technique == ptf.TechniqueType.PRIMARY_DIRECT

        ptf.resetvars()

        assert ptf.grid_aspects == []
        assert ptf.date_technique == -1
        assert ptf.aspect_type == -1
