"""
Persistence: constants.parse_selection_file, tested against the two real,
shipped saved_selections/*.txt files (not synthetic ones) - these are
real output from real past interactive sessions, so this is as close as
Phase 2 can get to a genuine end-to-end persistence round-trip without a
running Flask app.
"""

import os

import constants

SAVED_SELECTIONS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "fixtures", "saved_selections"
)

SHORT_FILE = os.path.join(SAVED_SELECTIONS_DIR, "beyonce_1981-09-05_02-24-52.txt")
LONG_FILE = os.path.join(SAVED_SELECTIONS_DIR, "beyonce_1981-09-05_02-26-04.txt")


class TestParseSelectionFileShortSample:
    def test_parses_every_event_header_as_a_top_level_key(self):
        result = constants.parse_selection_file(SHORT_FILE)
        assert result is not None
        # Every top-level key must be a full "Event: ..." header line's
        # content (parse_selection_file strips the "Event: " prefix but
        # keeps the rest of the line, commas and all, as the dict key).
        assert "1986-06-24T12:00:00, BIRTH_SISTER, 2, [29.7217, -95.3875, 32]" in result

    def test_divorce_separation_event_has_pd_technique_with_three_real_aspects(self):
        result = constants.parse_selection_file(SHORT_FILE)
        key = "2005-09-10T12:00:00, DIVORCE_SEPARATION, 10, [29.7217, -95.3875, 32]"
        assert key in result
        assert "PD" in result[key]
        assert result[key]["PD"] == [
            "(MC,261.980,(c)) (Neptune,262.087,(r)) (conjunction,6.43')",
            "(Pluto,189.094,(c)) (Saturn,189.106,(r)) (conjunction,0.69')",
            "(Uranus,209.464,(c)) (Mean_Node,119.428,(r)) (square,2.16')",
        ]

    def test_single_aspect_events_parse_to_a_one_item_list(self):
        result = constants.parse_selection_file(SHORT_FILE)
        key = "1986-06-24T12:00:00, BIRTH_SISTER, 2, [29.7217, -95.3875, 32]"
        assert result[key]["PD"] == ["(Jupiter,200.442,(d)) (H3,80.437,(r)) (trine,0.32')"]


class TestParseSelectionFileLongSample:
    def test_parses_without_error_and_returns_a_nonempty_dict(self):
        result = constants.parse_selection_file(LONG_FILE)
        assert result is not None
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_every_technique_value_is_a_list_of_nonempty_strings(self):
        """Structural invariant that must hold across the whole real file,
        not just one hand-picked event - a good complement to the
        hand-verified exact-content checks above."""
        result = constants.parse_selection_file(LONG_FILE)
        for event_key, techniques in result.items():
            assert isinstance(techniques, dict), f"event {event_key!r} did not map to a dict"
            for technique_key, aspects in techniques.items():
                assert isinstance(aspects, list), f"{event_key!r}/{technique_key!r} was not a list"
                for aspect in aspects:
                    assert isinstance(aspect, str) and aspect.strip() != ""


class TestParseSelectionFileMissingFile:
    def test_nonexistent_file_returns_none_without_raising(self, tmp_path):
        result = constants.parse_selection_file(str(tmp_path / "does_not_exist.txt"))
        assert result is None
