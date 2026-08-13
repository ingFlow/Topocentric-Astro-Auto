"""
Batch engine: the grid-generation pipeline (generate_grid_times_manual ->
append_grid_acceptable_angles -> the raw str(list)-per-line grid file
format), run end-to-end against real fixture data.

--------------------------------------------------------------------------
Updated for Phase 7 (migration plan): batch/grid_engine.py's former
module-level globals (grid_aspects, date_technique, aspect_type) and
resetvars() no longer exist. generate_grid_times_manual now builds
grid_aspects as a LOCAL list on every call and append_grid_acceptable_angles
takes date_technique/aspect_type as explicit parameters and RETURNS the
row it builds, instead of appending to shared module state. This suite
previously called ptf.resetvars() before/after every test purely as
hygiene against exactly the cross-test state leakage Phase 7 eliminates
by construction - that hygiene call is no longer needed and has been
removed from setup_method/teardown_method below (there is no longer any
module-level accumulator to leak between tests, so there is nothing left
to reset).

Two tests specifically existed to characterize the pre-Phase-7 global-leak
behavior, and both said explicitly, in their own pre-Phase-7 docstrings,
what to do once that behavior changed:
    - test_grid_aspects_global_accumulates_across_multiple_calls_until_reset
      is now test_back_to_back_calls_do_not_leak_rows_into_each_other,
      asserting the OPPOSITE of what it asserted before: two
      generate_grid_times_manual calls in the same process, back-to-back,
      with NO reset in between, must NOT share any rows - true by
      construction now that grid_aspects is local, not by convention via
      a resetvars() call the caller had to remember to make.
    - test_resetvars_clears_grid_aspects_and_technique_selection tested a
      function (resetvars()) that has been deleted outright, per Phase 7's
      own task list, once confirmed "provably unnecessary" (see the
      migration plan's Phase 7 rationale and MIGRATION_MANUAL_V2.md
      Section 2.1(b)). There is no drop-in replacement to test - a fresh
      call to generate_grid_times_manual simply builds fresh, local state
      every time, which the leak test above already covers. This test
      class has been removed rather than kept as a stub for a function
      that no longer exists.

Scope note (unchanged from before this update): only PRIMARY_DIRECT is
exercised here as the representative technique. append_grid_acceptable_angles's
own source only has explicit branches for PRIMARY_DIRECT, SECONDARY_DIRECT,
PSSR, TRANSIT, and SRA - Harmonics and Lunar are confirmed (by reading the
source) not wired into batch mode at all, matching the Developer Manual's
own account. A fuller follow-up pass could add SECONDARY_DIRECT/PSSR/
TRANSIT/SRA cases the same way; this file establishes the pattern and
covers the one most load-bearing case (PRIMARY_DIRECT is also what the
significator-scoring tests already exercise most heavily).
--------------------------------------------------------------------------
"""

import ast
import os

import julian
import swisseph as swe
from datetime import datetime

from batch import grid_engine as ptf
from topo_astro.significators import rules_data as significators_rules

swe.set_ephe_path("/usr/share/swisseph/ephe")

BEYONCE_GEOPOS = [29.7217, -95.3875, 32]
BEYONCE_RADIX_DT = datetime.fromisoformat("1981-09-04T02:28:44")


class TestGenerateGridTimesManualEndToEnd:
    def test_writes_one_header_row_plus_one_row_per_candidate_time(self, tmp_path):
        list_dt_events = [
            (datetime.fromisoformat("2012-01-07T12:00:00"), significators_rules.EventType.BIRTH_DAUGHTER, BEYONCE_GEOPOS),
            (datetime.fromisoformat("2005-09-10T12:00:00"), significators_rules.EventType.DIVORCE_SEPARATION, BEYONCE_GEOPOS),
        ]
        candidate_times = [
            BEYONCE_RADIX_DT,
            BEYONCE_RADIX_DT.replace(minute=33, second=44),  # a second, nearby candidate
        ]
        out_prefix = str(tmp_path / "beyonce_grid_test")

        ptf.generate_grid_times_manual(
            out_prefix, candidate_times, list_dt_events, BEYONCE_GEOPOS,
            significators_rules.AspectType.ANGLE_HOUSE_PRIMARY, ptf.TechniqueType.PRIMARY_DIRECT,
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

    def test_back_to_back_calls_do_not_leak_rows_into_each_other(self, tmp_path):
        """Phase 7's replacement for the pre-Phase-7
        test_grid_aspects_global_accumulates_across_multiple_calls_until_reset,
        which asserted the leak itself as expected behavior (see this
        file's module docstring for the full history). grid_aspects is now
        built fresh, as a local variable, inside every
        generate_grid_times_manual call - there is no shared module list
        left to accumulate across calls, and therefore nothing that needs
        an explicit reset between them. This is verified here by driving
        two independent runs with DIFFERENT event lists back-to-back, with
        no reset call of any kind in between (none exists any more), and
        confirming each run's own output file reflects only its own
        events and candidate times - not the other run's."""
        events_a = [
            (datetime.fromisoformat("2012-01-07T12:00:00"), significators_rules.EventType.BIRTH_DAUGHTER, BEYONCE_GEOPOS),
        ]
        events_b = [
            (datetime.fromisoformat("2005-09-10T12:00:00"), significators_rules.EventType.DIVORCE_SEPARATION, BEYONCE_GEOPOS),
            (datetime.fromisoformat("1999-01-01T12:00:00"), significators_rules.EventType.ACCIDENT, BEYONCE_GEOPOS),
        ]
        candidate_a = [BEYONCE_RADIX_DT]
        candidate_b = [BEYONCE_RADIX_DT, BEYONCE_RADIX_DT.replace(minute=33, second=44)]

        prefix_a = str(tmp_path / "run_a")
        prefix_b = str(tmp_path / "run_b")

        ptf.generate_grid_times_manual(
            prefix_a, candidate_a, events_a, BEYONCE_GEOPOS,
            significators_rules.AspectType.ANGLE_HOUSE_PRIMARY, ptf.TechniqueType.PRIMARY_DIRECT,
        )
        # No reset of any kind between these two calls - none exists any
        # more, and none should be needed.
        ptf.generate_grid_times_manual(
            prefix_b, candidate_b, events_b, BEYONCE_GEOPOS,
            significators_rules.AspectType.ANGLE_HOUSE_PRIMARY, ptf.TechniqueType.TRANSIT,
        )

        with open(prefix_a + ".txt") as f:
            lines_a = [l for l in f.read().split("\n") if l.strip()]
        with open(prefix_b + ".txt") as f:
            lines_b = [l for l in f.read().split("\n") if l.strip()]

        # Run A: 1 header + 1 candidate time row. Must NOT have grown to
        # include anything from run B (which has a different event list
        # and a different, longer candidate-time list).
        assert len(lines_a) == 1 + len(candidate_a)
        # Run B: 1 header + 2 candidate time rows - its own, independent count.
        assert len(lines_b) == 1 + len(candidate_b)

        header_a = ast.literal_eval(lines_a[0])
        header_b = ast.literal_eval(lines_b[0])
        # Run A's header describes its own 1 event; run B's describes its
        # own 2 events - confirms the two runs' event lists never merged.
        assert len(header_a) == 1 + len(events_a) + 1
        assert len(header_b) == 1 + len(events_b) + 1

        # Run A's file content must not contain any trace of run B's
        # distinguishing event date, and vice versa.
        content_a = "\n".join(lines_a)
        content_b = "\n".join(lines_b)
        assert "2005-09-10" not in content_a and "1999-01-01" not in content_a
        assert content_a != content_b