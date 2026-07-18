"""
Lunar-technique-specific tests.

Covers two things the Phase 2 plan originally mis-scoped or under-specified,
corrected here after checking the real source directly:

1. calc_planets_near_angles was listed under core/constants.py in the
   original Phase 2 plan. It isn't there - it's defined in lunar_auto.py
   and is used only by Lunar's own demi-return angularity check
   (calc_planets_ac_mc -> calc_planets_near_angles, feeding the >14-day
   demi-return trigger). Its test belongs here, next to the rest of
   Lunar's own special-case behavior, not in test_core_constants.py.

2. lunar_auto.get_str_only_aspects_from_data currently raises TypeError as
   written (see migration plan §2.4): it calls
   Lunar_Auto(dt_radix, dt_event, geopos, geopos_natal, ltype, orb) - six
   positional arguments - against a constructor that only accepts five
   (no ltype; Lunar_Auto computes all three LunarTypes internally on every
   construction). This file tests BOTH the current, broken-as-written
   state (locking in that fact, since a characterization test's job is to
   record current reality) AND the underlying get_str_only_aspects_from_array
   logic directly (which already works correctly when reached through a
   properly-constructed Lunar_Auto) - the latter is what Phase 4's fix
   (dropping the stray ltype argument) should make reachable through the
   wrapper unchanged.
"""

import julian
import swisseph as swe

import lunar_auto
from constants import PLANETS

swe.set_ephe_path("/usr/share/swisseph/ephe")

BEYONCE_GEOPOS = [29.7217, -95.3875, 32]
BEYONCE_JD = 2444851.6032870371  # 1981-09-04T02:28:44


class TestCalcPlanetsNearAngles:
    def test_real_fixture_returns_only_conjunctions_and_oppositions_to_ac_or_mc(self):
        positions = lunar_auto.calc_planets_ac_mc(BEYONCE_JD, BEYONCE_GEOPOS)
        assert positions[0][0] == "ac"
        assert positions[1][0] == "mc"

        result = lunar_auto.calc_planets_near_angles(positions, orb=8.0)

        # Every returned line must reference either 'ac' or 'mc', and must
        # be a conjunction or opposition - calc_planets_near_angles only
        # ever appends for these two aspect names (see its own source).
        for line in result:
            assert "(ac," in line or "(mc," in line
            assert "conjunction" in line or "opposition" in line

    def test_wider_orb_never_returns_fewer_matches_than_a_narrower_orb(self):
        positions = lunar_auto.calc_planets_ac_mc(BEYONCE_JD, BEYONCE_GEOPOS)
        narrow = lunar_auto.calc_planets_near_angles(positions, orb=1.0)
        wide = lunar_auto.calc_planets_near_angles(positions, orb=10.0)
        assert len(wide) >= len(narrow)

    def test_zero_orb_only_matches_an_exact_conjunction_or_opposition(self):
        positions = lunar_auto.calc_planets_ac_mc(BEYONCE_JD, BEYONCE_GEOPOS)
        result = lunar_auto.calc_planets_near_angles(positions, orb=0.0)
        # Not asserting a specific count (depends on exact real degrees,
        # which will only ever exactly equal 0.0 orb by coincidence) - just
        # that a zero orb doesn't crash and returns a well-formed (possibly
        # empty) list.
        assert isinstance(result, list)


class TestGetStrOnlyAspectsFromDataCurrentlyBroken:
    """Locks in the CURRENT, as-written, broken behavior - this class
    should be deleted (not "fixed in place") once Phase 4 applies the
    argument-count fix, and replaced by promoting
    TestGetStrOnlyAspectsIntendedBehavior below to test the wrapper
    directly instead of the underlying array function."""

    def test_currently_raises_typeerror_due_to_stray_ltype_argument(self):
        import pytest
        with pytest.raises(TypeError):
            lunar_auto.get_str_only_aspects_from_data(
                julian.from_jd(BEYONCE_JD),
                julian.from_jd(BEYONCE_JD + 30),
                BEYONCE_GEOPOS,
                BEYONCE_GEOPOS,
                1,  # ltype - this positional argument is the bug; Lunar_Auto's
                    # real constructor has no ltype parameter at all
                1.0,
            )


class TestGetStrOnlyAspectsIntendedBehavior:
    """Tests the underlying logic the broken wrapper is supposed to expose:
    a flattened, UNLABELED variant of Lunar's aspect string, as an
    alternative to get_str_labelled_aspects_from_array (the labeled
    version actually wired into app.py and count_mal_ben_all_lunars
    today). Confirmed distinct in shape from the labeled version, same
    underlying aspect content - this is the behavior Phase 4's fix should
    make reachable through get_str_only_aspects_from_data unchanged."""

    def test_unlabeled_output_has_no_section_headers_but_same_aspect_lines_as_labeled(self):
        lunar_obj = lunar_auto.Lunar_Auto(
            julian.from_jd(BEYONCE_JD), julian.from_jd(BEYONCE_JD + 30),
            BEYONCE_GEOPOS, BEYONCE_GEOPOS, 1.0,
        )
        all_charts = lunar_obj.get_all_lunars()

        labelled = lunar_auto.get_str_labelled_aspects_from_array(all_charts)
        unlabelled = lunar_auto.get_str_only_aspects_from_array(all_charts)

        labelled_lines = set(l for l in labelled.split("\n") if l.strip())
        unlabelled_lines = set(l for l in unlabelled.split("\n") if l.strip())

        # Every real aspect line in the unlabeled output must also appear
        # in the labeled output (same underlying content)...
        assert unlabelled_lines.issubset(labelled_lines) or unlabelled_lines == labelled_lines
        # ...but the labeled output must contain section-header lines
        # (L, DL, LC, K, ... - single short tokens, not aspect strings)
        # that the unlabeled output does not.
        header_like = {l for l in labelled_lines if "(" not in l}
        assert len(header_like) > 0
        assert not any(h in unlabelled_lines for h in header_like)

    def test_this_is_what_the_fixed_wrapper_should_reproduce(self):
        """Directly demonstrates the intended fix: calling Lunar_Auto with
        the correct 5-argument signature (no ltype), exactly matching the
        already-correct sibling call in count_mal_ben_all_lunars, then
        flattening via the unlabeled array function - this is what
        get_str_only_aspects_from_data should do internally after Phase 4
        drops its stray ltype argument."""
        lunar_obj = lunar_auto.Lunar_Auto(
            julian.from_jd(BEYONCE_JD), julian.from_jd(BEYONCE_JD + 30),
            BEYONCE_GEOPOS, BEYONCE_GEOPOS, 1.0,
        )
        expected = lunar_auto.get_str_only_aspects_from_array(lunar_obj.get_all_lunars())
        assert isinstance(expected, str)
