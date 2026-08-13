"""
Compendium lookup tests (significators.compendium) - the data-access layer
for the PSSR window-narrowing feature.

Spec: docs/pssr_window_narrowing_design_v5.md sections 4.2 (EventType ->
title mapping), 4.3 (symbol-name mapping) and 5.1 (module contract).

What is pinned here:

    - All 51 EventTypes resolve per the spec's 4.2 table: 40 map to the
      exact compendium titles, 11 have no compendium event (None).
    - The 40 mapped titles are cross-checked against BOTH reference files
      (the scoring JSON's event list and the pairs artifact's event keys)
      so the mapping cannot drift from the committed data.
    - tier_score returns the exact integers from the scoring JSON, None
      for absent keys (never a synthesized 0), and None for no-data /
      unknown inputs.
    - pair_strength is unordered, resolves inherited pairs, returns None
      for unlisted pairs and the three marked-none events, and keeps
      `excluded` distinct from `absent`.
    - SYMBOL_MAP_NAMED's values are all real compendium symbols, and the
      codebase-named forms ('Mean_Node', 'H1', ...) translate correctly.
    - Loading fails loudly when the artifacts are missing.
"""

import json
import os

import pytest

from topo_astro.significators.compendium import (
    SYMBOL_MAP_NAMED,
    Compendium,
    default_base_dir,
)
from topo_astro.significators.rules_data import EventType

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPENDIUM_DIR = os.path.join(REPO_ROOT, "compendium_reference")
SCORING_FILE = os.path.join(COMPENDIUM_DIR, "compendium_scoring_export_v2.json")
PAIRS_FILE = os.path.join(COMPENDIUM_DIR, "juan_combos_pairs_v1.json")


def _load_scoring():
    with open(SCORING_FILE, encoding="utf-8") as f:
        return json.load(f)


def _load_pairs():
    with open(PAIRS_FILE, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def compendium():
    return Compendium.load(COMPENDIUM_DIR)


# Expected mapping per spec v5 section 4.2, kept self-contained here (not
# imported from the module) so a drift in either direction is caught.
EXPECTED_TITLES = {
    "BIRTH_BROTHER": "Birth of Brother",
    "BIRTH_SISTER": "Birth of Sister",
    "BIRTH_SON": "Birth of Son",
    "BIRTH_DAUGHTER": "Birth of Daughter",
    "BIRTH_GRANDSON": "Birth of Grandson",
    "BIRTH_GRANDDAUGHTER": "Birth of Granddaughter",
    "MARRIAGE_ENGAGEMENT_FOR_MALE": "Marriage for Male",
    "MARRIAGE_ENGAGEMENT_FOR_FEMALE": "Marriage for Female",
    "CHILDS_MARRIAGE": "Child's Marriage",
    "DIVORCE_SEPARATION": "Divorce or Separation",
    "DEATH_FATHER_GRAND": "Death of Father or Grandfather",
    "DEATH_MOTHER_GRAND": "Death of Mother or Grandmother",
    "DEATH_SON": "Death of Son",
    "DEATH_DAUGHTER": "Death of Daughter",
    "DEATH_WIFE_FRIEND": "Death of Wife or Female Friend",
    "DEATH_HUSBAND_FRIEND": "Death of Husband or Male Friend",
    "DEATH_BROTHER": "Death of Brother",
    "DEATH_SISTER": "Death of Sister",
    "DEATH": "Death",
    "ASSASINATION_SUICIDE": "Assasination or Suicide",
    "SUCCESS_ELECTED": "Success or Elected",
    "PROMOTION_JOB": "Job Promotion",
    "FAILURE_DEFEATED": "Failure or Defeat",
    "RESIGN_RETIRE": "Resign or Retire",
    "TRAVEL_OVERSEAS_POSITIVE": "Positive Travel Overseas",
    "TRAVEL_POSITIVE": "Positive Travel",
    "TRAVEL_NEGATIVE": "Negative Travel",
    "MOBILIZATION": "Mobilization",
    "DEMOBILIZATION_RELEASE": "Demobilization or Release",
    "ARREST": "Arrest",
    "ACCIDENT": "Accident",
    "HOSPITALIZATION_ILLNESS": "Hospitalization or Illness",
    "VIOLENCE": "Violence",
    "INTRIGUE": "Intrigue",
    "LOSSES": "Losses",
    "GAMBLING_LOSS": "Gambling Loss",
    "GAMBLING_GAIN": "Gambling Gain",
    "GRADUATION_PUBLICATION": "Graduation or Publication",
    "MOVE_HOME": "Move Home",
    "ARMY_PROMOTION": "Army Promotion",
}

NO_DATA_NAMES = {
    "POSITIVE_AC_MC",
    "NEGATIVE_AC_MC",
    "POSITIVE_2_8",
    "NEGATIVE_2_8",
    "POSITIVE_3_9",
    "NEGATIVE_3_9",
    "POSITIVE_5_11",
    "NEGATIVE_5_11",
    "POSITIVE_6_12",
    "NEGATIVE_6_12",
    "BLANK",
}

ALL_EVENT_NAMES = {
    name: value
    for name, value in vars(EventType).items()
    if isinstance(value, int) and name.isupper()
}


def _norm(title):
    """Normalize a title read from the reference files (curly vs straight
    apostrophe) so it can be matched against the spec's mapping table."""
    return title.replace("\u2019", "'").replace("\u2018", "'")


# ---------------------------------------------------------------------------
# 4.2 mapping: all 51 EventTypes resolve (40 mapped, 11 no-data).
# ---------------------------------------------------------------------------

def test_all_51_eventtypes_resolve_per_spec(compendium):
    assert len(ALL_EVENT_NAMES) == 51
    assert len(EXPECTED_TITLES) == 40
    assert len(NO_DATA_NAMES) == 11
    assert set(EXPECTED_TITLES) | NO_DATA_NAMES == set(ALL_EVENT_NAMES)

    for name, value in ALL_EVENT_NAMES.items():
        if name in NO_DATA_NAMES:
            assert compendium.event_title_for(value) is None, name
        else:
            assert compendium.event_title_for(value) == EXPECTED_TITLES[name], name


def test_mapped_titles_match_both_reference_files(compendium):
    scoring = _load_scoring()
    pairs = _load_pairs()
    scoring_titles = {_norm(event["title"]) for event in scoring["events"]}
    assert len(scoring_titles) == 40

    mapped_titles = set(EXPECTED_TITLES.values())
    assert mapped_titles == scoring_titles
    assert mapped_titles == {_norm(t) for t in pairs["events"]}


def test_event_title_for_unknown_id(compendium):
    assert compendium.event_title_for(9999) is None
    assert compendium.event_title_for(-1) is None


# ---------------------------------------------------------------------------
# tier_score: exact integers from the scoring JSON; None for absent keys.
# ---------------------------------------------------------------------------

def test_tier_score_matches_scoring_json(compendium):
    scoring = _load_scoring()
    for event in scoring["events"]:
        event_id = ALL_EVENT_NAMES[
            next(name for name, title in EXPECTED_TITLES.items() if title == _norm(event["title"]))
        ]
        for symbol, record in event["symbols"].items():
            assert compendium.tier_score(event_id, symbol) == record["tier_score"], (
                event["title"], symbol
            )


def test_tier_score_absent_key_is_none(compendium):
    scoring = _load_scoring()
    checked = 0
    for event in scoring["events"]:
        event_id = ALL_EVENT_NAMES[
            next(name for name, title in EXPECTED_TITLES.items() if title == _norm(event["title"]))
        ]
        for symbol in scoring["symbol_labels"]:
            if symbol in event["symbols"]:
                continue
            assert compendium.tier_score(event_id, symbol) is None, (event["title"], symbol)
            checked += 1
    assert checked > 0  # the absent-key case genuinely occurs in the data


def test_tier_score_never_synthesizes_zero(compendium):
    scoring = _load_scoring()
    for event in scoring["events"]:
        event_id = ALL_EVENT_NAMES[
            next(name for name, title in EXPECTED_TITLES.items() if title == _norm(event["title"]))
        ]
        for symbol, record in event["symbols"].items():
            actual = compendium.tier_score(event_id, symbol)
            if record["tier_score"] is None:
                assert actual is None
            else:
                assert isinstance(actual, int)
                assert actual in {0, 2, 4, 6, 8, 10}


def test_tier_score_symbol_normalization(compendium):
    scoring = _load_scoring()
    brother = EventType.BIRTH_BROTHER
    assert "ASC" in scoring["events"][0]["symbols"]
    assert compendium.tier_score(brother, "H1") == compendium.tier_score(brother, "ASC")
    assert compendium.tier_score(brother, "Mean_Node") == compendium.tier_score(brother, "NODE_ANY")
    assert compendium.tier_score(brother, "Sun") == compendium.tier_score(brother, "SUN")
    assert compendium.tier_score(brother, "Node") == compendium.tier_score(brother, "NODE_ANY")


def test_tier_score_fail_closed_inputs(compendium):
    assert compendium.tier_score(9999, "MOON") is None
    assert compendium.tier_score(EventType.BIRTH_BROTHER, "NOT_A_SYMBOL") is None
    assert compendium.tier_score(EventType.POSITIVE_AC_MC, "MOON") is None
    assert compendium.tier_score(EventType.BLANK, "SUN") is None


# ---------------------------------------------------------------------------
# pair_strength: unordered, inherited pairs, absent vs excluded, fail-closed.
# ---------------------------------------------------------------------------

def test_pair_strength_unordered_across_whole_artifact(compendium):
    pairs = _load_pairs()
    checked = 0
    for title, entry in pairs["events"].items():
        event_id = ALL_EVENT_NAMES[
            next(name for name, t in EXPECTED_TITLES.items() if t == _norm(title))
        ]
        for key in entry["pairs"]:
            a, b = key.split(":")
            assert compendium.pair_strength(event_id, a, b) == compendium.pair_strength(event_id, b, a)
            checked += 1
    assert checked == 1384  # every pair in the artifact is unordered-safe


def test_pair_strength_matches_artifact(compendium):
    pairs = _load_pairs()
    for title, entry in pairs["events"].items():
        event_id = ALL_EVENT_NAMES[
            next(name for name, t in EXPECTED_TITLES.items() if t == _norm(title))
        ]
        for key, pair in entry["pairs"].items():
            a, b = key.split(":")
            assert compendium.pair_strength(event_id, a, b) == pair["strength"], (title, key)


def test_pair_strength_absent_is_none_not_excluded(compendium):
    # MARS:POF for Birth of Brother is explicitly coded 'excluded' in the
    # reviewed table - it must surface as the string 'excluded', not None.
    assert compendium.pair_strength(EventType.BIRTH_BROTHER, "MARS", "POF") == "excluded"
    # An unlisted pair (e.g. SUN:SATURN for Birth of Brother) is absent.
    assert compendium.pair_strength(EventType.BIRTH_BROTHER, "SUN", "SATURN") is None
    assert compendium.pair_strength(EventType.BIRTH_BROTHER, "SUN", "SATURN") != "excluded"


def test_pair_strength_inherited_pairs_resolve(compendium):
    pairs = _load_pairs()
    overseas = pairs["events"]["Positive Travel Overseas"]
    own = {k: p for k, p in overseas["pairs"].items() if p["inherited_from"] is None}
    inherited = {k: p for k, p in overseas["pairs"].items() if p["inherited_from"] is not None}
    assert own and inherited

    for key, pair in inherited.items():
        a, b = key.split(":")
        assert compendium.pair_strength(EventType.TRAVEL_OVERSEAS_POSITIVE, a, b) == pair["strength"]
    for key, pair in own.items():
        a, b = key.split(":")
        assert compendium.pair_strength(EventType.TRAVEL_OVERSEAS_POSITIVE, a, b) == pair["strength"]

    # The inherited pairs must resolve on the parent event too, with the
    # same strength.
    parent = pairs["events"]["Positive Travel"]
    for key in inherited:
        a, b = key.split(":")
        parent_pair = parent["pairs"][key]
        assert (
            compendium.pair_strength(EventType.TRAVEL_POSITIVE, a, b)
            == parent_pair["strength"]
        )


def test_pair_strength_marked_none_events(compendium):
    for event_id in (
        EventType.ASSASINATION_SUICIDE,
        EventType.DEMOBILIZATION_RELEASE,
        EventType.GAMBLING_LOSS,
    ):
        assert compendium.event_title_for(event_id) is not None  # mapped, but no pairs
        assert compendium.pair_strength(event_id, "MARS", "VENUS") is None


def test_pair_strength_fail_closed_inputs(compendium):
    assert compendium.pair_strength(9999, "MARS", "VENUS") is None
    assert compendium.pair_strength(EventType.POSITIVE_AC_MC, "MARS", "VENUS") is None
    assert compendium.pair_strength(EventType.BIRTH_BROTHER, "NOT_A_POINT", "VENUS") is None
    assert compendium.pair_strength(EventType.BIRTH_BROTHER, "MARS", "NOT_A_POINT") is None


def test_pair_strength_symbol_normalization(compendium):
    success = EventType.SUCCESS_ELECTED
    assert compendium.pair_strength(success, "MOON", "NODE_ANY") == "strong"
    assert compendium.pair_strength(success, "Moon", "Mean_Node") == "strong"
    assert compendium.pair_strength(success, "Moon", "Node") == "strong"


def test_pair_strength_spot_values(compendium):
    assert compendium.pair_strength(EventType.SUCCESS_ELECTED, "MOON", "NODE_ANY") == "strong"
    assert compendium.pair_strength(EventType.BIRTH_BROTHER, "MARS", "POF") == "excluded"
    assert compendium.pair_strength(EventType.SUCCESS_ELECTED, "ASC", "URANUS") == "weak"


# ---------------------------------------------------------------------------
# SYMBOL_MAP_NAMED (spec 4.3).
# ---------------------------------------------------------------------------

def test_symbol_map_values_are_real_compendium_symbols():
    scoring = _load_scoring()
    known = set(scoring["symbol_labels"])
    for codebase_name, symbol in SYMBOL_MAP_NAMED.items():
        assert symbol in known, f"{codebase_name} -> {symbol} is not a compendium symbol"


def test_symbol_map_spot_checks():
    assert SYMBOL_MAP_NAMED["Sun"] == "SUN"
    assert SYMBOL_MAP_NAMED["Moon"] == "MOON"
    assert SYMBOL_MAP_NAMED["Mean_Node"] == "NODE_ANY"
    assert SYMBOL_MAP_NAMED["POF"] == "POF"
    assert SYMBOL_MAP_NAMED["H1"] == "ASC"
    assert SYMBOL_MAP_NAMED["H4"] == "IC"
    assert SYMBOL_MAP_NAMED["H7"] == "DESC"
    assert SYMBOL_MAP_NAMED["H10"] == "MC"
    assert SYMBOL_MAP_NAMED["H2"] == "H2"
    assert SYMBOL_MAP_NAMED["H12"] == "H12"
    # identity entries for names that are already compendium-side
    assert SYMBOL_MAP_NAMED["ASC"] == "ASC"
    assert SYMBOL_MAP_NAMED["MC"] == "MC"
    assert SYMBOL_MAP_NAMED["DESC"] == "DESC"
    assert SYMBOL_MAP_NAMED["IC"] == "IC"


# ---------------------------------------------------------------------------
# Loading behavior.
# ---------------------------------------------------------------------------

def test_load_default_base_dir_resolves(compendium):
    base = default_base_dir()
    assert os.path.isfile(os.path.join(base, "compendium_scoring_export_v2.json"))
    assert os.path.isfile(os.path.join(base, "juan_combos_pairs_v1.json"))


def test_load_missing_artifacts_raise(tmp_path):
    with pytest.raises(FileNotFoundError):
        Compendium.load(str(tmp_path))


def test_load_invalid_shape_raises(tmp_path):
    scoring = tmp_path / "compendium_scoring_export_v2.json"
    pairs = tmp_path / "juan_combos_pairs_v1.json"
    scoring.write_text("{}", encoding="utf-8")
    pairs.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError):
        Compendium.load(str(tmp_path))