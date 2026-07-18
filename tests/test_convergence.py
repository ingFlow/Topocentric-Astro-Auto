"""
categorize_aspect (the per-aspect-line classifier count_extended_aspect_groups_txt
uses) and the convergence family (sum_sec_prim / read_file / sum_all_m /
write_result) - run end-to-end against real Beyoncé grid data, exactly
reproducing what a real Primary-Direction-plus-Secondary-Progression
rectification convergence check does.

sum_sec_prim specifically combines PRIMARY_DIRECT and SECONDARY_DIRECT
extended-count files (confirmed directly: both of those TechniqueTypes'
`selected_categories` lists in count_extended_aspect_groups_txt include
'all_m'; PSSR and TRANSIT's lists do not) - which is exactly what its own
name ("sec" + "prim") implies, now confirmed against the source rather
than assumed from the name alone.
"""

import os
import tempfile
from datetime import datetime

import swisseph as swe

import process_techniques_files as ptf
import pd_automate

swe.set_ephe_path("/usr/share/swisseph/ephe")

BEYONCE_GEOPOS = [29.7217, -95.3875, 32]
BEYONCE_RADIX_DT = datetime.fromisoformat("1981-09-04T02:28:44")
BEYONCE_EVENTS = [
    (datetime.fromisoformat("2012-01-07T12:00:00"), pd_automate.EventType.BIRTH_DAUGHTER, BEYONCE_GEOPOS),
    (datetime.fromisoformat("2005-09-10T12:00:00"), pd_automate.EventType.DIVORCE_SEPARATION, BEYONCE_GEOPOS),
]
CANDIDATE_TIMES = [BEYONCE_RADIX_DT, BEYONCE_RADIX_DT.replace(minute=33, second=44)]


class TestCategorizeAspect:
    """One test per real branch, using the actual angle/planet vocabulary
    (H1/H4/H7/H10 for angles, real PLANETS entries, 'Moon' specifically
    distinguished from other planets) confirmed directly from the source."""

    def test_angle_then_planet_conjunction(self):
        assert ptf.categorize_aspect("H1", "Mars", "conjunction") == "p_a_conj"

    def test_angle_then_planet_major(self):
        assert ptf.categorize_aspect("H4", "Venus", "trine") == "p_a_maj"

    def test_angle_then_planet_minor(self):
        assert ptf.categorize_aspect("H10", "Jupiter", "45-semisquare") == "p_a_min"

    def test_planet_then_angle_conjunction(self):
        assert ptf.categorize_aspect("Saturn", "H7", "opposition") == "a_p_conj"

    def test_planet_then_angle_major(self):
        assert ptf.categorize_aspect("Mercury", "H1", "square") == "a_p_maj"

    def test_house_cusp_then_planet_conjunction(self):
        """A non-angular house cusp (H2, H3, H5, H6, H8, H9, H11, H12 -
        anything starting with 'H' that isn't one of the 4 angles above,
        which are checked first and would have already matched)."""
        assert ptf.categorize_aspect("H2", "Pluto", "conjunction") == "p_h_conj"

    def test_planet_then_house_cusp_major(self):
        assert ptf.categorize_aspect("Uranus", "H3", "sextile") == "h_p_maj"

    def test_planet_to_moon_conjunction(self):
        assert ptf.categorize_aspect("Sun", "Moon", "conjunction") == "mon_p_conj"

    def test_planet_to_planet_major(self):
        assert ptf.categorize_aspect("Venus", "Jupiter", "trine") == "p_p_maj"

    def test_planet_to_planet_minor(self):
        assert ptf.categorize_aspect("Mars", "Saturn", "150-quincunx") == "p_p_min"

    def test_unrecognized_point_names_return_none(self):
        assert ptf.categorize_aspect("SomeUnknownPoint", "AlsoUnknown", "conjunction") is None


def _build_extended_count_file(tmp_dir, technique):
    """Runs the real generate_grid_times_manual -> count_extended_aspect_groups_txt
    pipeline for one technique, returning the resulting COUNT.txt path."""
    ptf.resetvars()
    level_aspects = {
        ptf.TechniqueType.PRIMARY_DIRECT: pd_automate.AspectType.APPROPRIATE_INCLUDING_PLANET_COMBOS,
        ptf.TechniqueType.SECONDARY_DIRECT: pd_automate.AspectType.ANGLE_HOUSE_PRIMARY,
    }[technique]
    prefix = os.path.join(tmp_dir, f"beyonce_{technique}")
    ptf.generate_grid_times_manual(prefix, CANDIDATE_TIMES, BEYONCE_EVENTS, BEYONCE_GEOPOS, level_aspects, technique)
    ptf.count_extended_aspect_groups_txt(prefix, technique)
    return prefix + "COUNT.txt"


class TestCountExtendedAspectGroupsTxt:
    def test_skips_header_row_correctly_unlike_the_older_function(self):
        """Confirms the flag_1st_row guard actually works in practice -
        contrast with count_aspect_groups_txt (test_csv_analysis.py),
        which has no such guard and produces a garbage first line."""
        with tempfile.TemporaryDirectory() as d:
            count_file = _build_extended_count_file(d, ptf.TechniqueType.PRIMARY_DIRECT)
            with open(count_file) as f:
                lines = [l for l in f.readlines() if l.strip()]
            assert len(lines) == len(CANDIDATE_TIMES)  # no extra garbage header-derived row
            for line in lines:
                assert "'time':" in line
                assert not line.startswith("Row 1: {'time': 'Time'")

    def test_primary_direct_rows_include_all_m(self):
        with tempfile.TemporaryDirectory() as d:
            count_file = _build_extended_count_file(d, ptf.TechniqueType.PRIMARY_DIRECT)
            data = ptf.read_file(count_file)
            assert len(data) == len(CANDIDATE_TIMES)
            assert all(isinstance(v, int) for v in data.values())

    def test_secondary_direct_rows_include_all_m(self):
        with tempfile.TemporaryDirectory() as d:
            count_file = _build_extended_count_file(d, ptf.TechniqueType.SECONDARY_DIRECT)
            data = ptf.read_file(count_file)
            assert len(data) == len(CANDIDATE_TIMES)
            assert all(isinstance(v, int) for v in data.values())


class TestSumSecPrimEndToEnd:
    def test_combines_real_primary_and_secondary_all_m_values(self):
        with tempfile.TemporaryDirectory() as d:
            prim_file = _build_extended_count_file(d, ptf.TechniqueType.PRIMARY_DIRECT)
            sec_file = _build_extended_count_file(d, ptf.TechniqueType.SECONDARY_DIRECT)

            prim_data = ptf.read_file(prim_file)
            sec_data = ptf.read_file(sec_file)

            ptf.sum_sec_prim(prim_file, sec_file)

            # sum_sec_prim derives its own output path via prim_filename[:-18] -
            # confirm precisely where it actually lands rather than assuming.
            result_path = f"{prim_file[:-18]}summed_prim_sec.txt"
            assert os.path.exists(result_path)

            summed = {}
            with open(result_path) as f:
                for line in f:
                    row_number, row_data = line.split(":", 1)
                    import ast
                    row_dict = ast.literal_eval(row_data.strip())
                    summed[row_dict["time"]] = row_dict["sum_all_m"]

            expected = ptf.sum_all_m(prim_data, sec_data)
            assert summed == expected
            # every combined value must be the real, exact sum of both real inputs
            for time in expected:
                assert summed[time] == prim_data[time] + sec_data[time]

    def test_read_file_parses_row_number_and_dict_correctly(self):
        with tempfile.TemporaryDirectory() as d:
            prim_file = _build_extended_count_file(d, ptf.TechniqueType.PRIMARY_DIRECT)
            data = ptf.read_file(prim_file)
            assert list(data.keys()) == ["1981-09-04 02:28:43", "1981-09-04 02:33:44"]

    def test_sum_all_m_only_keeps_times_present_in_both_inputs(self):
        data1 = {"t1": 5, "t2": 3}
        data2 = {"t1": 2, "t3": 9}  # t2/t3 don't overlap
        result = ptf.sum_all_m(data1, data2)
        assert result == {"t1": 7}

    def test_write_result_creates_directory_if_missing(self):
        with tempfile.TemporaryDirectory() as d:
            nested_path = os.path.join(d, "a", "b", "c", "out.txt")
            ptf.write_result(nested_path, {"2000-01-01 00:00:00": 42})
            assert os.path.exists(nested_path)
            with open(nested_path) as f:
                content = f.read()
            assert "Row 1: {'time': '2000-01-01 00:00:00', 'sum_all_m': 42}" in content
