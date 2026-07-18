"""
csv_analysis.py - kept fully per your decision, not deleted. Since it has
zero current callers anywhere in the application, there was no existing
invocation to characterize - so this file BUILDS one: every test below
runs the real, current grid -> count_aspect_groups_txt -> csv_analysis
pipeline end-to-end against real fixture data, exactly reproducing what
main_techniques.other_techniques_from_times actually does today, so
csv_analysis.py finally has genuine behavior on record.

--------------------------------------------------------------------------
Two real findings surfaced by actually wiring this up, not just reading
the source - documented here rather than silently worked around:

1. count_aspect_groups_txt has no header-row-skipping logic (unlike its
   newer sibling count_extended_aspect_groups_txt, which explicitly has a
   flag_1st_row guard). Every COUNT.txt it writes has a garbage first line
   derived from mis-parsing the grid file's header row as if it were a
   data row (time becomes the literal string "Time", count becomes the
   literal string "Count"). Confirmed harmless in practice: csv_analysis's
   own regex requires count to be `(\\d+)`, which "Count" never matches,
   so this garbage line is silently and correctly excluded by every
   TechniqueType's regex - annotated below as a real but non-harmful
   characteristic, not a data-integrity bug.

2. A SEPARATE, genuinely significant bug: for TechniqueType.Secondary_Direct
   specifically, csv_analysis.extract_data_from_file sets flag_pssr=True
   (expecting the moon-aware 7-field format: opp-conj/sqr-tri-sext/major/
   minor/moon-opp-conj/moon-sqr-tri-sext/empty) - but the REAL production
   pipeline (main_techniques.other_techniques_from_times) calls
   count_aspect_groups_txt(filename, flag_pssr_count_moon) with
   flag_pssr_count_moon=False for SECONDARY_DIRECT (only PSSR gets True),
   which writes the SIMPLER 5-field format instead. The result: every real
   Secondary_Direct COUNT.txt file, fed into csv_analysis.py exactly as
   its own code implies it should be, silently parses to ZERO rows - not
   an error, not a crash, a completely silent 100% data loss for that
   technique. PSSR, Transit, and Primary_Direct do not have this problem
   (their flag_pssr/flag_count_moon expectations agree on both sides).
   This is a real bug worth fixing deliberately - either make
   other_techniques_from_times pass flag_pssr_count_moon=True for
   Secondary too, or fix csv_analysis's own Secondary_Direct branch to
   expect the simpler format - but which one is correct is a judgment
   call, not something to silently pick a side on here.
--------------------------------------------------------------------------
"""

import os
import tempfile
from datetime import datetime

import pytest
import swisseph as swe

import process_techniques_files as ptf
import pd_automate
import csv_analysis

swe.set_ephe_path("/usr/share/swisseph/ephe")

BEYONCE_GEOPOS = [29.7217, -95.3875, 32]
BEYONCE_RADIX_DT = datetime.fromisoformat("1981-09-04T02:28:44")
BEYONCE_EVENTS = [
    (datetime.fromisoformat("2012-01-07T12:00:00"), pd_automate.EventType.BIRTH_DAUGHTER, BEYONCE_GEOPOS),
    (datetime.fromisoformat("2005-09-10T12:00:00"), pd_automate.EventType.DIVORCE_SEPARATION, BEYONCE_GEOPOS),
]
CANDIDATE_TIMES = [BEYONCE_RADIX_DT, BEYONCE_RADIX_DT.replace(minute=33, second=44)]

# Reproduces main_techniques.other_techniques_from_times's real, exact
# technique -> (AspectType, flag_count_moon) mapping.
REAL_PIPELINE_MAPPING = {
    "SECONDARY_DIRECT": (ptf.TechniqueType.SECONDARY_DIRECT, pd_automate.AspectType.ANGLE_HOUSE_PRIMARY, False),
    "PSSR": (ptf.TechniqueType.PSSR, pd_automate.AspectType.MOON_ANGLE_HOUSE_PRIMARY, True),
    "TRANSIT": (ptf.TechniqueType.TRANSIT, pd_automate.AspectType.ANGLE_PRIMARY, False),
}
CSV_ANALYSIS_TYPE_MAP = {
    "SECONDARY_DIRECT": csv_analysis.TechniqueType.Secondary_Direct,
    "PSSR": csv_analysis.TechniqueType.PSSR,
    "TRANSIT": csv_analysis.TechniqueType.Transit,
}


def _build_real_count_file(tmp_path, technique_name):
    """Runs the actual generate_grid_times_manual -> count_aspect_groups_txt
    pipeline for real, exactly as other_techniques_from_times does, and
    returns the path to the resulting COUNT.txt."""
    ptf.resetvars()
    technique, level_aspects, flag_count_moon = REAL_PIPELINE_MAPPING[technique_name]
    prefix = str(tmp_path / f"beyonce_{technique_name.lower()}")
    ptf.generate_grid_times_manual(prefix, CANDIDATE_TIMES, BEYONCE_EVENTS, BEYONCE_GEOPOS, level_aspects, technique)
    ptf.count_aspect_groups_txt(prefix, flag_count_moon)
    return prefix + "COUNT.txt"


class TestCountAspectGroupsTxtHeaderRowHandling:
    """Characterizes finding 1 above directly, independent of csv_analysis.py."""

    def test_first_written_line_is_a_garbage_parse_of_the_header_row(self, tmp_path):
        count_file = _build_real_count_file(tmp_path, "TRANSIT")
        with open(count_file) as f:
            first_line = f.readline().strip()
        assert first_line == "['Time, Count, opp-conj: 0, sqr-tri-sext: 0, major: 0, minor: 0, empty: 2']"

    def test_garbage_header_line_count_field_is_the_literal_word_count_not_a_number(self, tmp_path):
        """This is exactly why it's harmless downstream - "Count" can never
        satisfy csv_analysis's own \\d+ regex requirement for that field."""
        count_file = _build_real_count_file(tmp_path, "TRANSIT")
        with open(count_file) as f:
            first_line = f.readline()
        assert ", Count, opp-conj:" in first_line


class TestExtractDataFromFileAgainstRealPipelineOutput:
    """Runs extract_data_from_file against COUNT.txt files built by the
    real, current production pipeline - not hand-typed synthetic lines."""

    def test_pssr_parses_correctly_two_real_rows(self, tmp_path):
        count_file = _build_real_count_file(tmp_path, "PSSR")
        df = csv_analysis.extract_data_from_file(count_file, csv_analysis.TechniqueType.PSSR)
        assert len(df) == 2
        assert list(df.columns) == ["Time", "all-sr", "mj1-sr", "mj2-sr", "mja-sr", "min-sr", "mon-conj-sr", "mon-maj-sr", "e-sr"]
        assert df["Time"].tolist() == ["1981-09-04 02:28:43", "1981-09-04 02:33:44"]

    def test_transit_parses_correctly_two_real_rows(self, tmp_path):
        count_file = _build_real_count_file(tmp_path, "TRANSIT")
        df = csv_analysis.extract_data_from_file(count_file, csv_analysis.TechniqueType.Transit)
        assert len(df) == 2
        assert list(df.columns) == ["Time", "all-tr", "mj1-tr", "mj2-tr", "mja-tr", "min-tr", "e-tr"]

    def test_primary_direct_parses_correctly_two_real_rows(self, tmp_path):
        ptf.resetvars()
        prefix = str(tmp_path / "beyonce_primary")
        ptf.generate_grid_times_manual(
            prefix, CANDIDATE_TIMES, BEYONCE_EVENTS, BEYONCE_GEOPOS,
            pd_automate.AspectType.APPROPRIATE_INCLUDING_PLANET_COMBOS, ptf.TechniqueType.PRIMARY_DIRECT,
        )
        ptf.count_aspect_groups_txt(prefix, False)
        df = csv_analysis.extract_data_from_file(prefix + "COUNT.txt", csv_analysis.TechniqueType.Primary_Direct)
        assert len(df) == 2
        assert list(df.columns) == ["Time", "all-pd", "mj1-pd", "mj2-pd", "mja-pd", "min-pd", "e-pd"]

    def test_secondary_direct_silently_parses_to_zero_rows_confirmed_bug(self, tmp_path):
        """Locks in finding 2 above as current, real, characterized
        behavior. If this test ever starts failing because the DataFrame
        is no longer empty, that means the flag_pssr_count_moon /
        flag_pssr mismatch between other_techniques_from_times and
        csv_analysis.py has been deliberately fixed - which would be
        good news, but this test needs to be updated to match the fix
        rather than silently left behind expecting the old, broken shape."""
        count_file = _build_real_count_file(tmp_path, "SECONDARY_DIRECT")
        df = csv_analysis.extract_data_from_file(count_file, csv_analysis.TechniqueType.Secondary_Direct)
        assert df.empty
        assert len(df) == 0
        # the file itself DOES contain 2 real, valid data rows - confirming
        # this is a parsing/format mismatch, not an upstream data problem
        with open(count_file) as f:
            real_lines = [l for l in f.readlines() if "1981-09-04" in l]
        assert len(real_lines) == 2


class TestLoadAndConcatenateFiles:
    """load_and_concatenate_files infers TechniqueType from filename
    substrings ('pssr'/'prim'/'sec'/'tran') and inner-joins every file on
    'Time' - confirms this against two real, filename-conforming files.

    Note: the substring check (`if 'pssr' in filename`) matches against the
    FULL PATH STRING passed in, not just the basename - confirmed directly
    while writing this test. pytest's own tmp_path fixture names its
    directory after the test function, and this class's tests are
    *specifically about* those four substrings, so tmp_path could never be
    trusted to stay clean here (a subdirectory created underneath it does
    NOT help - the test-function-derived parent directory name is still
    part of the full path either way). Every test below uses an explicit
    tempfile.mkdtemp(prefix="csvtest_") directory instead, confirmed
    clean of all four substrings, so the deliberate-collision test and the
    should-not-collide tests can both be trusted."""

    def test_merges_pssr_and_transit_on_matching_times(self):
        with tempfile.TemporaryDirectory(prefix="csvtest_") as clean_dir_str:
            from pathlib import Path
            clean_dir = Path(clean_dir_str)
            pssr_file = _build_real_count_file(clean_dir, "PSSR")
            transit_file = _build_real_count_file(clean_dir, "TRANSIT")

            pssr_renamed = str(clean_dir / "beyonce_pssrCOUNT.txt")
            transit_renamed = str(clean_dir / "beyonce_tranCOUNT.txt")
            os.replace(pssr_file, pssr_renamed)
            os.replace(transit_file, transit_renamed)

            merged = csv_analysis.load_and_concatenate_files([pssr_renamed, transit_renamed])
            assert len(merged) == 2  # both real times present in both files -> inner join keeps both
            assert "all-sr" in merged.columns
            assert "all-tr" in merged.columns

    def test_technique_inference_matches_against_the_full_path_not_just_the_basename(self):
        """Directly, deliberately demonstrates the characteristic noted in
        the class docstring, rather than leaving it as an incidental
        discovery. The if/elif chain checks 'pssr' before 'tran', so a
        REAL Transit file, placed in a directory whose name happens to
        contain 'pssr', gets misclassified as PSSR data purely because of
        its parent directory's name - even though the filename itself
        (and its actual content) is Transit, not PSSR."""
        with tempfile.TemporaryDirectory(prefix="csvtest_pssr_batch_") as colliding_dir_str:
            from pathlib import Path
            colliding_dir = Path(colliding_dir_str)
            transit_file = _build_real_count_file(colliding_dir, "TRANSIT")
            transit_renamed = str(colliding_dir / "beyonce_tranCOUNT.txt")
            os.replace(transit_file, transit_renamed)

            # extract_data_from_file takes an explicit technique argument, so
            # it is unaffected by this and parses correctly as Transit data.
            df = csv_analysis.extract_data_from_file(transit_renamed, csv_analysis.TechniqueType.Transit)
            assert len(df) == 2

            # load_and_concatenate_files instead INFERS the technique from the
            # full path - 'pssr' (checked first in the if/elif chain, and
            # present in this directory's name via the "csvtest_pssr_batch_"
            # prefix) causes this real Transit file to have its columns
            # labeled "-sr" (PSSR's suffix), not "-tr" (Transit's own suffix).
            merged = csv_analysis.load_and_concatenate_files([transit_renamed])
            assert "all-sr" in merged.columns, (
                "expected the real Transit file to be misclassified as PSSR "
                "('all-sr' columns) purely because its parent directory name "
                "contains 'pssr' - if this fails, the technique-inference "
                "logic no longer matches against the full path, which would "
                "be a deliberate improvement worth updating this test for"
            )
            assert "all-tr" not in merged.columns

    def test_secondary_file_in_the_mix_collapses_the_merge_to_zero_rows(self):
        """Direct, end-to-end demonstration of finding 2's real-world
        impact: because Secondary_Direct parses to an empty DataFrame,
        merging it with any other (real, non-empty) file on 'Time'
        collapses the WHOLE final result to zero rows too - this is
        exactly what would happen if csv_analysis.main()'s own file list
        (which includes a "_secondariesCOUNT.txt" file) were ever
        actually run against real data."""
        with tempfile.TemporaryDirectory(prefix="csvtest_") as clean_dir_str:
            from pathlib import Path
            clean_dir = Path(clean_dir_str)
            secondary_file = _build_real_count_file(clean_dir, "SECONDARY_DIRECT")
            transit_file = _build_real_count_file(clean_dir, "TRANSIT")

            secondary_renamed = str(clean_dir / "beyonce_secCOUNT.txt")
            transit_renamed = str(clean_dir / "beyonce_tranCOUNT.txt")
            os.replace(secondary_file, secondary_renamed)
            os.replace(transit_file, transit_renamed)

            merged = csv_analysis.load_and_concatenate_files([secondary_renamed, transit_renamed])
            assert merged.empty, (
                "expected the real Secondary_Direct/Transit merge to silently "
                "collapse to zero rows, demonstrating finding 2's real downstream impact"
            )


class TestCsvPostProcessingFunctions:
    """count_all_col / count_all_major / count_all_major_opp / create_csv_count_txt -
    the CSV-level post-processing functions, run against a real merged CSV
    built from the actual pipeline output above."""

    def _build_real_merged_csv(self, tmp_path):
        pssr_file = _build_real_count_file(tmp_path, "PSSR")
        transit_file = _build_real_count_file(tmp_path, "TRANSIT")
        pssr_renamed = str(tmp_path / "beyonce_pssrCOUNT.txt")
        transit_renamed = str(tmp_path / "beyonce_tranCOUNT.txt")
        os.replace(pssr_file, pssr_renamed)
        os.replace(transit_file, transit_renamed)

        merged = csv_analysis.load_and_concatenate_files([pssr_renamed, transit_renamed])
        csv_path = str(tmp_path / "merged.csv")
        merged.to_csv(csv_path, index=False)
        return csv_path

    def test_count_all_col_sums_every_all_column_and_sorts_descending(self, tmp_path, capsys):
        csv_path = self._build_real_merged_csv(tmp_path)
        csv_analysis.count_all_col(csv_path)

        import pandas as pd
        result = pd.read_csv(csv_path)
        assert "cumulative_all" in result.columns
        assert result["cumulative_all"].tolist() == sorted(result["cumulative_all"].tolist(), reverse=True)
        # cumulative_all must equal the real sum of all-sr + all-tr for each row
        expected = result["all-sr"] + result["all-tr"]
        assert result["cumulative_all"].tolist() == expected.tolist()

    def test_count_all_major_sums_mja_columns(self, tmp_path):
        csv_path = self._build_real_merged_csv(tmp_path)
        csv_analysis.count_all_major(csv_path)

        import pandas as pd
        result = pd.read_csv(csv_path)
        assert "count_mja" in result.columns
        assert result["count_mja"].tolist() == sorted(result["count_mja"].tolist(), reverse=True)

    def test_count_all_major_opp_sums_mj1_columns(self, tmp_path):
        csv_path = self._build_real_merged_csv(tmp_path)
        csv_analysis.count_all_major_opp(csv_path)

        import pandas as pd
        result = pd.read_csv(csv_path)
        assert "count_mj1" in result.columns
        assert result["count_mj1"].tolist() == sorted(result["count_mj1"].tolist(), reverse=True)


class TestCreateCsvCountTxt:
    """create_csv_count_txt(filename_read_list, filename_write) - requires
    a file called 'all-pd' to exist (its own sort_values call is
    hardcoded to that column), so this specifically needs a
    Primary_Direct-named file in the mix, unlike the other tests above."""

    def test_requires_a_primary_direct_file_or_raises_keyerror(self, tmp_path):
        """Confirms current, real behavior: create_csv_count_txt's
        hardcoded `sort_values(by=['all-pd'])` means it cannot run
        successfully against a file list that doesn't include a
        Primary_Direct ('prim' in the filename) file - raises KeyError,
        does not silently degrade. Worth knowing before ever calling this
        function with an arbitrary file list."""
        pssr_file = _build_real_count_file(tmp_path, "PSSR")
        pssr_renamed = str(tmp_path / "beyonce_pssrCOUNT.txt")
        os.replace(pssr_file, pssr_renamed)

        with pytest.raises(KeyError):
            csv_analysis.create_csv_count_txt([pssr_renamed], str(tmp_path / "out.csv"))

    def test_succeeds_and_writes_a_file_when_a_primary_direct_file_is_included(self, tmp_path):
        ptf.resetvars()
        prefix = str(tmp_path / "beyonce_primCOUNT")  # 'prim' substring required for technique inference
        ptf.generate_grid_times_manual(
            prefix.replace("COUNT", ""), CANDIDATE_TIMES, BEYONCE_EVENTS, BEYONCE_GEOPOS,
            pd_automate.AspectType.APPROPRIATE_INCLUDING_PLANET_COMBOS, ptf.TechniqueType.PRIMARY_DIRECT,
        )
        ptf.count_aspect_groups_txt(prefix.replace("COUNT", ""), False)
        prim_count_file = prefix.replace("COUNT", "") + "COUNT.txt"

        out_path = str(tmp_path / "final.csv")
        csv_analysis.create_csv_count_txt([prim_count_file], out_path)

        assert os.path.exists(out_path)
        import pandas as pd
        result = pd.read_csv(out_path)
        assert len(result) == 2
        assert "all-pd" in result.columns
