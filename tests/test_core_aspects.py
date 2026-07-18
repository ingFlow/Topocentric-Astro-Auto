"""
Core layer: the aspect-matching engine (aspects_base.calculate_aspect).

Covers every entry in ALL_ASPECTS at exactly its orb boundary (per Phase 2's
exhaustive test list: "one test per entry, each at exactly its orb boundary -
just inside = match, just outside = no match - plus the 0deg/360deg
wraparound case for conjunction"), plus the MAJOR_ASPECTS/ALL_ASPECTS
consistency check that Phase 3's de-duplication must continue to satisfy.

calculate_aspect's real contract (verified directly against the source):
    calculate_aspect(first_degrees, second_degrees, orb, flag_major)
    -> (aspect_name, actual_orb_used) on match, or None on no match.
    difference = abs(first_degrees - second_degrees) % 360, matched against
    EITHER the aspect's forward_ideal or its backward_ideal angle, each
    checked as [ideal - orb, ideal + orb] inclusive on both ends.
"""

import aspects_base

# Every (aspect_name, forward_ideal, backward_ideal) triple, read directly
# from aspects_base.ALL_ASPECTS - if a future phase adds/removes an aspect,
# this list (and therefore the boundary coverage below) updates with it.
ALL_ASPECT_ENTRIES = [
    (name, fwd, bwd) for name, (fwd, bwd) in aspects_base.ALL_ASPECTS.items()
]


def test_all_aspects_table_has_nine_entries():
    """Locks in the current table shape; a change here should be a
    deliberate significator/domain decision, not an accidental edit."""
    assert len(aspects_base.ALL_ASPECTS) == 9
    assert set(aspects_base.ALL_ASPECTS.keys()) == {
        "sextile", "conjunction", "trine", "square", "opposition",
        "45-semisquare", "135-sesquisquare", "30-semisextile", "150-quincunx",
    }


def test_major_aspects_is_subset_of_all_aspects_with_matching_angles():
    """MAJOR_ASPECTS must stay the same 5 entries, with identical angle
    pairs, as the corresponding entries in ALL_ASPECTS. Phase 3 changes
    MAJOR_ASPECTS from a hand-copied dict to one *derived* from
    ALL_ASPECTS - this test must keep passing unchanged after that move."""
    expected_major_names = {"sextile", "conjunction", "trine", "square", "opposition"}
    assert set(aspects_base.MAJOR_ASPECTS.keys()) == expected_major_names
    for name in expected_major_names:
        assert aspects_base.MAJOR_ASPECTS[name] == aspects_base.ALL_ASPECTS[name]


def _assert_boundary(first_degrees, second_degrees, orb, expected_aspect_name, flag_major=False):
    result = aspects_base.calculate_aspect(first_degrees, second_degrees, orb, flag_major)
    assert result is not None, (
        f"expected a match for {expected_aspect_name} at {first_degrees}/{second_degrees} "
        f"orb={orb}, got None"
    )
    aspect_name, actual_orb = result
    assert aspect_name == expected_aspect_name
    return actual_orb


def _assert_no_match(first_degrees, second_degrees, orb):
    result = aspects_base.calculate_aspect(first_degrees, second_degrees, orb, False)
    assert result is None, f"expected no match at {first_degrees}/{second_degrees} orb={orb}, got {result}"


class TestOrbBoundaryPerAspect:
    """One just-inside/just-outside pair per ALL_ASPECTS entry, using its
    forward_ideal angle and orb=1.0 throughout for a consistent, easy to
    audit boundary. second_degrees is fixed at 0.0 so first_degrees ==
    difference directly, keeping every case traceable to the ideal angle
    it's testing."""

    ORB = 1.0

    def test_sextile_boundary(self):
        fwd = aspects_base.ALL_ASPECTS["sextile"][0]  # 60
        _assert_boundary(fwd + self.ORB, 0.0, self.ORB, "sextile")  # 61 -> match (inclusive)
        _assert_no_match(fwd + self.ORB + 0.01, 0.0, self.ORB)      # 61.01 -> no match

    def test_trine_boundary(self):
        fwd = aspects_base.ALL_ASPECTS["trine"][0]  # 120
        _assert_boundary(fwd + self.ORB, 0.0, self.ORB, "trine")
        _assert_no_match(fwd + self.ORB + 0.01, 0.0, self.ORB)

    def test_square_boundary(self):
        fwd = aspects_base.ALL_ASPECTS["square"][0]  # 90
        _assert_boundary(fwd + self.ORB, 0.0, self.ORB, "square")
        _assert_no_match(fwd + self.ORB + 0.01, 0.0, self.ORB)

    def test_opposition_boundary(self):
        fwd = aspects_base.ALL_ASPECTS["opposition"][0]  # 180 (forward == backward for opposition)
        _assert_boundary(fwd + self.ORB, 0.0, self.ORB, "opposition")
        _assert_no_match(fwd + self.ORB + 0.01, 0.0, self.ORB)

    def test_45_semisquare_boundary(self):
        fwd = aspects_base.ALL_ASPECTS["45-semisquare"][0]  # 45
        _assert_boundary(fwd + self.ORB, 0.0, self.ORB, "45-semisquare")
        _assert_no_match(fwd + self.ORB + 0.01, 0.0, self.ORB)

    def test_135_sesquisquare_boundary(self):
        fwd = aspects_base.ALL_ASPECTS["135-sesquisquare"][0]  # 135
        _assert_boundary(fwd + self.ORB, 0.0, self.ORB, "135-sesquisquare")
        _assert_no_match(fwd + self.ORB + 0.01, 0.0, self.ORB)

    def test_30_semisextile_boundary(self):
        fwd = aspects_base.ALL_ASPECTS["30-semisextile"][0]  # 30
        _assert_boundary(fwd + self.ORB, 0.0, self.ORB, "30-semisextile")
        _assert_no_match(fwd + self.ORB + 0.01, 0.0, self.ORB)

    def test_150_quincunx_boundary(self):
        fwd = aspects_base.ALL_ASPECTS["150-quincunx"][0]  # 150
        _assert_boundary(fwd + self.ORB, 0.0, self.ORB, "150-quincunx")
        _assert_no_match(fwd + self.ORB + 0.01, 0.0, self.ORB)

    def test_conjunction_boundary_near_zero(self):
        """difference near 0 degrees - conjunction's forward_ideal (0)."""
        _assert_boundary(self.ORB, 0.0, self.ORB, "conjunction")             # diff=1 -> match
        _assert_no_match(self.ORB + 0.01, 0.0, self.ORB)                    # diff=1.01 -> no match

    def test_conjunction_wraparound_near_360(self):
        """The 0deg/360deg wraparound case: two points ~1 degree apart but
        straddling the 0/360 boundary (e.g. 359.5 and 0.5) must still
        register as a conjunction via ALL_ASPECTS['conjunction']'s
        backward_ideal of 360, not fail to match just because the naive
        difference looks close to 360 rather than close to 0."""
        first_degrees = 359.5
        second_degrees = 0.5
        # abs(359.5 - 0.5) % 360 == 359.0, which is within orb of
        # backward_ideal=360 (359.0 is inside [360-1, 360+1]).
        actual_orb = _assert_boundary(first_degrees, second_degrees, self.ORB, "conjunction")
        assert round(actual_orb, 6) == 1.0

    def test_all_nine_aspects_covered(self):
        """Meta-check: confirms the boundary tests above actually cover
        every current ALL_ASPECTS entry, so a future added aspect fails
        loudly here instead of silently going untested."""
        tested_names = {
            "sextile", "trine", "square", "opposition", "45-semisquare",
            "135-sesquisquare", "30-semisextile", "150-quincunx", "conjunction",
        }
        assert tested_names == set(aspects_base.ALL_ASPECTS.keys())


class TestFlagMajorRestrictsToFiveAspects:
    def test_flag_major_true_never_returns_a_minor_aspect(self):
        """With flag_major=True, calculate_aspect must only ever return one
        of the five MAJOR_ASPECTS names, even at a difference that would
        match a minor aspect under flag_major=False."""
        # 45 degrees is semisquare (minor) but not any major aspect.
        result_minor_context = aspects_base.calculate_aspect(45.0, 0.0, 1.0, True)
        assert result_minor_context is None

        result_all_context = aspects_base.calculate_aspect(45.0, 0.0, 1.0, False)
        assert result_all_context is not None
        assert result_all_context[0] == "45-semisquare"


class TestFindTransAspects:
    """The reserved alternate transit-aspect finder (aspects_base.find_trans_aspects,
    caller-supplied orb) - preserved per your decision, not deleted. This
    confirms it still produces sensible output at a known fixture, so its
    behavior is characterized even though nothing currently calls it.

    Note (characterization finding, not a bug): find_trans_aspects only
    accepts pairs drawn from ALL_PLANET_TRANS (Mars, Mercury, Venus,
    Jupiter, Saturn, Uranus, Neptune, Pluto, Node, Sun - deliberately
    excluding the Moon) and/or its own HOUSES set (ASC, H2, MC, H3, H5,
    H6 - a different, smaller set of house labels than the H1-H12 the
    rest of the system uses). A pair outside both returns an empty
    string rather than raising - confirmed here explicitly so a future
    reader doesn't mistake the Moon-exclusion for an oversight."""

    def test_find_trans_aspects_known_fixture(self):
        planet_set1 = [("Mars", 100.0, "r")]
        planet_set2 = [("Jupiter", 160.0, "d")]
        result = aspects_base.find_trans_aspects(planet_set1, planet_set2, 2.0)
        assert "sextile" in result
        assert "Mars" in result and "Jupiter" in result

    def test_find_trans_aspects_excludes_moon_by_design(self):
        planet_set1 = [("Sun", 100.0, "r")]
        planet_set2 = [("Moon", 160.0, "d")]
        result = aspects_base.find_trans_aspects(planet_set1, planet_set2, 2.0)
        assert result == ""
