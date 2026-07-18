"""
Significator/scoring engine tests (pd_automate.is_acceptable_*,
count_*_acceptable_aspects) - the shared engine the migration plan's
Phase 5 extracts into significators/scoring.py, currently reused by
five of the seven techniques.

Uses REAL aspect strings pulled live from the golden PD output (not
hand-typed strings), for REAL EventTypes actually present in the fixture
data, covering both GoodBadFlag categories:
    - EventType.BIRTH_DAUGHTER      (GOOD) - Beyoncé, 2012-01-07
    - EventType.DIVORCE_SEPARATION  (BAD)  - Beyoncé, 2005-09-10
    - EventType.ARREST              (BAD)  - Winston, 1899-11-15 (positive control, see below)

--------------------------------------------------------------------------
Two findings from actually running this against real data, documented
here rather than silently worked around:

1. is_acceptable_angular_aspect(event_id, str_aspect, type) does NOT
   reliably return a bool. Reading its full body: most of its AspectType
   branches (11 of ~14) only ever `return True` inside a matching
   condition and have no corresponding `else: return False` - if the
   condition doesn't match, the function falls through to the end and
   implicitly returns None. Only FAST_TO_SLOW_COMBO and
   APPROPRIATE_INCLUDING_PLANET_COMBOS ever explicitly return False.
   Confirmed this doesn't affect real behavior: the function's only
   caller (count_event_acceptable_aspects) uses a plain truthy
   `if is_acceptable_angular_aspect(...):` check, which treats None and
   False identically. So this is safe as-is, but worth knowing before a
   refactor "cleans up" these implicit None returns into explicit False -
   that would be a safe change only as long as every caller keeps using
   truthy checks rather than `is True`/`is False` identity checks.

2. Beyoncé's real generated PD aspects for BIRTH_DAUGHTER (both direct
   and converse, and for that matter every one of her fixture events)
   score zero acceptable matches via is_acceptable_pd_aspect. This is not
   a bug: a search across all four people's real golden data confirms
   the scoring mechanism does produce real nonzero scores under other
   (person, event) combinations (e.g. Winston's ARREST, Jacqui's
   DEATH_HUSBAND_FRIEND) - Beyoncé's specific candidate/event
   combinations in this fixture set simply don't happen to match. For a
   rectification tool where "hits" are meant to be a comparatively rare,
   meaningful signal rather than the default outcome, an arbitrary
   candidate producing zero matches is itself realistic, expected
   behavior worth locking in, not a sign of a broken test.
--------------------------------------------------------------------------
"""

import json
import os

import pd_automate
from pd_automate import EventType, AspectType

GOLDEN_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "golden")


def _load_golden(person_key):
    with open(os.path.join(GOLDEN_DIR, f"{person_key}_techniques.json")) as f:
        return json.load(f)


def _direct_aspect_lines(golden, candidate_label, event_dt_str):
    event = golden["candidates"][candidate_label]["events"][event_dt_str]
    direct = event["techniques"]["PRIMARY_DIRECT"]["direct"]
    return [line for line in direct.split("\n") if line.strip()]


class TestIsAcceptablePdAspect:
    """is_acceptable_pd_aspect(event_id, str_aspect) -> score (0/False if
    not acceptable, > 0 if acceptable) for a single raw aspect string."""

    def test_beyonce_birth_daughter_real_aspects_currently_score_zero(self):
        """Characterizes real, current behavior: none of Beyoncé's real
        direct PD aspects for this event/candidate match PRIMARY_RULES /
        SECONDARY_RULES for BIRTH_DAUGHTER. See module docstring, finding 2."""
        golden = _load_golden("beyonce")
        lines = _direct_aspect_lines(golden, "actual_dob", "2012-01-07T12:00:00")
        scores = [pd_automate.is_acceptable_pd_aspect(EventType.BIRTH_DAUGHTER, line) for line in lines]
        assert all((not s) or s <= 0 for s in scores)

    def test_winston_arrest_real_aspect_scores_nonzero_positive_control(self):
        """Positive control proving the mechanism genuinely works: Winston's
        real direct PD aspect (H3,228.283,(r)) (Neptune,48.115,(d))
        (opposition,10.11') for his real ARREST event scores 20."""
        golden = _load_golden("winston")
        lines = _direct_aspect_lines(golden, "actual_dob", "1899-11-15T12:00:00")  # ARREST
        scores = [pd_automate.is_acceptable_pd_aspect(EventType.ARREST, line) for line in lines]
        assert any(s and s > 0 for s in scores), (
            "expected Winston's real ARREST direct PD aspects to include at least "
            "one acceptable match - if this fails, either the golden data changed "
            "or the scoring engine's behavior changed"
        )
        assert max(s for s in scores if s) == 20

    def test_blank_event_type_always_scores_zero(self):
        golden = _load_golden("beyonce")
        lines = _direct_aspect_lines(golden, "actual_dob", "2012-01-07T12:00:00")
        for line in lines:
            assert pd_automate.is_acceptable_pd_aspect(EventType.BLANK, line) == 0

    def test_bad_event_real_aspects_evaluate_without_error(self):
        """DIVORCE_SEPARATION is a BAD-flagged event - confirms the scoring
        path runs cleanly for a BAD category too, not just GOOD."""
        golden = _load_golden("beyonce")
        lines = _direct_aspect_lines(golden, "actual_dob", "2005-09-10T12:00:00")  # DIVORCE_SEPARATION
        scores = [pd_automate.is_acceptable_pd_aspect(EventType.DIVORCE_SEPARATION, line) for line in lines]
        assert all(isinstance(s, (int, float)) or s is False for s in scores)


class TestCountPdScoreAcceptableAspects:
    """count_pd_score_acceptable_aspects(event_id, str_all_aspects, score)
    -> (cumulative_score, filtered_acceptable_aspects_string)."""

    def test_cumulative_score_matches_sum_of_individual_scores(self):
        golden = _load_golden("winston")
        lines = _direct_aspect_lines(golden, "actual_dob", "1899-11-15T12:00:00")  # ARREST, has real hits
        str_all = "\n".join(lines)

        final_score, accepted_str = pd_automate.count_pd_score_acceptable_aspects(
            EventType.ARREST, str_all, 0
        )

        expected_total = sum(
            max(pd_automate.is_acceptable_pd_aspect(EventType.ARREST, line) or 0, 0)
            for line in lines
        )
        assert final_score == expected_total
        assert final_score > 0  # ARREST has a confirmed real hit in this fixture
        accepted_lines = [l for l in accepted_str.split("\n") if l.strip()]
        assert all(line in lines for line in accepted_lines)

    def test_score_accumulates_on_top_of_a_nonzero_starting_score(self):
        golden = _load_golden("winston")
        lines = _direct_aspect_lines(golden, "actual_dob", "1899-11-15T12:00:00")
        str_all = "\n".join(lines)

        score_from_zero, _ = pd_automate.count_pd_score_acceptable_aspects(EventType.ARREST, str_all, 0)
        score_from_ten, _ = pd_automate.count_pd_score_acceptable_aspects(EventType.ARREST, str_all, 10)

        assert score_from_ten == score_from_zero + 10


class TestIsAcceptableAngularAspect:
    """is_acceptable_angular_aspect(event_id, str_aspect, type) -> True,
    False, or (per finding 1 above) None. count_event_acceptable_aspects
    treats all non-True results identically via a truthy check, so this
    suite does the same rather than requiring a strict bool."""

    def test_runs_cleanly_and_returns_a_falsy_or_true_result_for_every_aspect_type(self):
        golden = _load_golden("beyonce")
        lines = _direct_aspect_lines(golden, "actual_dob", "2012-01-07T12:00:00")
        aspect_type_values = [
            v for k, v in vars(AspectType).items() if not k.startswith("_") and isinstance(v, int)
        ]
        for line in lines[:3]:
            for at_value in aspect_type_values:
                result = pd_automate.is_acceptable_angular_aspect(EventType.BIRTH_DAUGHTER, line, at_value)
                assert result is True or not result  # True, or falsy (False/None) - never anything else

    def test_appropriate_including_planet_combos_can_return_explicit_false(self):
        """The one branch confirmed (by reading the source) to explicitly
        return False rather than falling through to None."""
        golden = _load_golden("beyonce")
        lines = _direct_aspect_lines(golden, "actual_dob", "2012-01-07T12:00:00")
        result = pd_automate.is_acceptable_angular_aspect(
            EventType.BIRTH_DAUGHTER, lines[0], AspectType.APPROPRIATE_INCLUDING_PLANET_COMBOS
        )
        assert result is False or result is True  # never None for this specific branch


class TestCountEventAcceptableAspects:
    def test_count_increments_only_for_accepted_aspects(self):
        golden = _load_golden("beyonce")
        lines = _direct_aspect_lines(golden, "actual_dob", "2012-01-07T12:00:00")
        str_all = "\n".join(lines)

        count, accepted_str = pd_automate.count_event_acceptable_aspects(
            EventType.BIRTH_DAUGHTER, str_all, 0, AspectType.ANGLE_PRIMARY
        )
        accepted_lines = [l for l in accepted_str.split("\n") if l.strip()]
        assert count == len(accepted_lines)
        expected_count = sum(
            1 for line in lines
            if pd_automate.is_acceptable_angular_aspect(EventType.BIRTH_DAUGHTER, line, AspectType.ANGLE_PRIMARY)
        )
        assert count == expected_count


class TestIsAcceptablePlanetCombo:
    """is_acceptable_planet_combo(event_id, p1, p2) -> bool, checked
    against PLANETARY_COMBO[event_id] in either planet order."""

    def test_a_real_combo_present_in_the_table_is_accepted_either_order(self):
        combos = pd_automate.PLANETARY_COMBO[EventType.BIRTH_DAUGHTER]
        assert isinstance(combos, tuple) and len(combos) > 0
        first_combo = combos[0] if isinstance(combos[0], tuple) else None
        assert first_combo is not None, "expected BIRTH_DAUGHTER's PLANETARY_COMBO entry to be a direct combo list"
        p1, p2 = first_combo
        assert pd_automate.is_acceptable_planet_combo(EventType.BIRTH_DAUGHTER, p1, p2) is True
        assert pd_automate.is_acceptable_planet_combo(EventType.BIRTH_DAUGHTER, p2, p1) is True

    def test_an_absent_combo_is_rejected(self):
        # Verified directly against pd_automate.PLANETARY_COMBO[EventType.BIRTH_DAUGHTER]
        # that neither ordering of Saturn/Mars appears in its 21-entry combo list.
        assert pd_automate.is_acceptable_planet_combo(EventType.BIRTH_DAUGHTER, "Saturn", "Mars") is False
        assert pd_automate.is_acceptable_planet_combo(EventType.BIRTH_DAUGHTER, "Mars", "Saturn") is False
