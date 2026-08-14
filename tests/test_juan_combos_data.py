"""
Quality gates G1-G4 re-run over the committed Juan Combos pairs artifact
(compendium_reference/juan_combos_pairs_v1.json).

The artifact is produced once by scripts/build_juan_combos_table.py; these
tests re-run the four automated gates independently (no imports from the
builder) so the committed data cannot silently drift from the contract in
spec v5 section 4.1:

    G1: attributed pair count per event == the JSON's preserved
        juan_combos_total_combinations minus that event's excluded
        research-note bullets (the "Success or Elected" section contains a
        candidate_categories:-marked research-note block, see _meta).
    G2: every pair key is inside the 14-point Juan Combos roster and every
        pair entry matches the artifact schema.
    G3: no duplicate canonical keys within an event beyond the sanctioned
        genuine double-listing ("Success or Elected" MOON:NODE_ANY), which
        is merged first-wins and recorded in _meta.source_notes.
    G4: every one of the 40 JSON events has an entry (pairs or marked_none).

The tier assignments themselves (strong/weak/excluded) are wording-cued by
the builder but are subject to the human review pass - _meta.reviewed_by /
_reviewed_on must be signed before the artifact is trusted. These tests
therefore pin structural facts (counts, merges, exclusions, inheritance,
roster, schema) and only the non-controversial, session-decided specifics.
"""

import json
import os
import re
from datetime import date

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPENDIUM_DIR = os.path.join(REPO_ROOT, "compendium_reference")
ARTIFACT_FILE = os.path.join(COMPENDIUM_DIR, "juan_combos_pairs_v1.json")
SCORING_FILE = os.path.join(COMPENDIUM_DIR, "compendium_scoring_export_v2.json")

ROSTER = frozenset(
    {"ASC", "MC", "SUN", "MOON", "MERCURY", "VENUS", "MARS", "JUPITER", "SATURN",
     "URANUS", "NEPTUNE", "PLUTO", "NODE_ANY", "POF"}
)
TIERS = frozenset({"strong", "weak", "excluded"})
PAIR_SCHEMA_KEYS = frozenset({"strength", "wording", "aspects_hint", "inherited_from"})
ENTRY_SCHEMA_KEYS = frozenset({"n_total", "pairs", "marked_none"})

MARKED_NONE_EVENTS = {
    "Demobilization or Release",
    "Assasination or Suicide",
    "Gambling Loss",
}

KEY_RE = re.compile(r"^([A-Z_]+):([A-Z_]+)$")


def _load_artifact():
    with open(ARTIFACT_FILE, encoding="utf-8") as f:
        return json.load(f)


def _load_scoring():
    with open(SCORING_FILE, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# G4: every one of the 40 JSON events has an entry (pairs or marked_none).
# ---------------------------------------------------------------------------

def test_g4_all_events_present():
    artifact = _load_artifact()
    scoring = _load_scoring()
    scoring_titles = [event["title"] for event in scoring["events"]]

    assert len(scoring_titles) == 40
    assert set(artifact["events"]) == set(scoring_titles)
    assert artifact["_meta"]["events_total"] == 40

    events_with_pairs = [t for t, e in artifact["events"].items() if e["pairs"]]
    events_marked_none = [t for t, e in artifact["events"].items() if e["marked_none"]]
    assert len(events_with_pairs) == artifact["_meta"]["events_with_pairs"] == 37
    assert set(events_marked_none) == MARKED_NONE_EVENTS
    assert artifact["_meta"]["events_marked_none"] == 3
    assert len(events_with_pairs) + len(events_marked_none) == 40


def test_g4_marked_none_events_have_no_pairs():
    artifact = _load_artifact()
    for title in MARKED_NONE_EVENTS:
        entry = artifact["events"][title]
        assert entry["n_total"] == 0
        assert entry["pairs"] == {}
        assert entry["marked_none"] is True


# ---------------------------------------------------------------------------
# G1: attributed count == preserved total minus excluded research-note
# bullets, per event, cross-checked against compendium_scoring_export_v2.json.
# ---------------------------------------------------------------------------

def test_g1_counts_match_preserved_totals():
    artifact = _load_artifact()
    scoring = _load_scoring()

    excluded_per_event = {}
    for note in artifact["_meta"]["source_notes"]["excluded_research_notes"]:
        excluded_per_event[note["event"]] = excluded_per_event.get(note["event"], 0) + 1

    total_attributed = 0
    total_preserved = 0
    for event in scoring["events"]:
        title = event["title"]
        expected_total = event["sample_sizes"]["juan_combos_total_combinations"]
        entry = artifact["events"][title]
        expected_attributed = expected_total - excluded_per_event.get(title, 0)
        assert entry["n_total"] == expected_attributed, title
        total_attributed += entry["n_total"]
        total_preserved += expected_total

    assert total_attributed == total_preserved - len(
        artifact["_meta"]["source_notes"]["excluded_research_notes"]
    )


def test_g1_marked_none_flags_match_scoring_json():
    artifact = _load_artifact()
    scoring = _load_scoring()
    for event in scoring["events"]:
        title = event["title"]
        entry = artifact["events"][title]
        assert entry["marked_none"] == bool(event["sample_sizes"]["juan_combos_marked_none"]), title


# ---------------------------------------------------------------------------
# G2: schema and 14-point roster.
# ---------------------------------------------------------------------------

def test_g2_every_key_inside_roster_and_canonical():
    artifact = _load_artifact()
    for title, entry in artifact["events"].items():
        for key in entry["pairs"]:
            match = KEY_RE.match(key)
            assert match is not None, f"{title}: malformed key {key!r}"
            a, b = match.groups()
            assert a in ROSTER and b in ROSTER, f"{title}: {key} outside roster"
            assert a < b, f"{title}: {key} not canonical (sorted)"
            assert a != b, f"{title}: {key} is a same-point pair"


def test_g2_every_pair_matches_schema():
    artifact = _load_artifact()
    for title, entry in artifact["events"].items():
        assert set(entry) == ENTRY_SCHEMA_KEYS, title
        assert isinstance(entry["n_total"], int) and entry["n_total"] >= 0, title
        assert isinstance(entry["marked_none"], bool), title
        for key, pair in entry["pairs"].items():
            assert set(pair) == PAIR_SCHEMA_KEYS, f"{title} {key}"
            assert pair["strength"] in TIERS, f"{title} {key}"
            assert isinstance(pair["wording"], str) and pair["wording"], f"{title} {key}"
            assert isinstance(pair["aspects_hint"], str), f"{title} {key}"
            assert pair["inherited_from"] is None or isinstance(pair["inherited_from"], str), (
                f"{title} {key}"
            )


# ---------------------------------------------------------------------------
# G3: duplicates - only the sanctioned genuine double-listing may exist, and
# it must be merged first-wins and recorded.
# ---------------------------------------------------------------------------

def test_g3_merged_duplicates_are_the_only_n_total_gap():
    artifact = _load_artifact()
    merged_per_event = {}
    for note in artifact["_meta"]["source_notes"]["merged_duplicates"]:
        merged_per_event[note["event"]] = merged_per_event.get(note["event"], 0) + 1

    for title, entry in artifact["events"].items():
        merged = merged_per_event.get(title, 0)
        inherited = sum(1 for p in entry["pairs"].values() if p["inherited_from"] is not None)
        assert entry["n_total"] - (len(entry["pairs"]) - inherited) == merged, title

    assert sum(merged_per_event.values()) == 1


def test_g3_sanctioned_merge_details():
    artifact = _load_artifact()
    merged = artifact["_meta"]["source_notes"]["merged_duplicates"]
    assert len(merged) == 1
    note = merged[0]
    assert note["event"] == "Success or Elected"
    assert note["key"] == "MOON:NODE_ANY"
    assert note["lines"] == [3386, 3391]
    assert note["tiers"] == ["strong", "strong"]

    pair = artifact["events"]["Success or Elected"]["pairs"]["MOON:NODE_ANY"]
    assert pair["strength"] == "strong"
    assert pair["wording"] == "Among the positive events, we find romantic relationships."
    assert pair["inherited_from"] is None


def test_g3_excluded_research_notes_recorded():
    artifact = _load_artifact()
    excluded = artifact["_meta"]["source_notes"]["excluded_research_notes"]
    assert len(excluded) == 5
    assert all(note["event"] == "Success or Elected" for note in excluded)
    assert [note["line"] for note in excluded] == [3421, 3422, 3423, 3424, 3425]
    assert "candidate_categories" in excluded[0]["wording"]
    assert excluded[1]["wording"] == '"fleeting relationships"'

    # The excluded keys must not appear twice due to the note block: their
    # pair entries survive only from the main list.
    success = artifact["events"]["Success or Elected"]
    assert success["pairs"]["ASC:URANUS"]["wording"].startswith("In conjunctions and harmonic aspects")
    assert success["pairs"]["MARS:VENUS"]["wording"].startswith("On a professional level")
    assert success["pairs"]["JUPITER:VENUS"]["wording"].startswith("On a professional level")
    assert success["pairs"]["URANUS:VENUS"]["wording"].startswith("On a professional level")
    assert success["pairs"]["PLUTO:VENUS"]["wording"].startswith("On a professional level")


def test_g3_success_or_elected_counts():
    artifact = _load_artifact()
    success = artifact["events"]["Success or Elected"]
    assert success["n_total"] == 60
    assert len(success["pairs"]) == 59
    assert success["marked_none"] is False


# ---------------------------------------------------------------------------
# Cross-reference inheritance ("Positive Travel Overseas" <- "Positive
# Travel").
# ---------------------------------------------------------------------------

def test_positive_travel_overseas_inheritance():
    artifact = _load_artifact()
    parent = artifact["events"]["Positive Travel"]
    child = artifact["events"]["Positive Travel Overseas"]

    own = {k: p for k, p in child["pairs"].items() if p["inherited_from"] is None}
    inherited = {k: p for k, p in child["pairs"].items() if p["inherited_from"] == "Positive Travel"}

    assert child["n_total"] == 2
    assert set(own) == {"NEPTUNE:URANUS", "NEPTUNE:POF"}
    assert len(inherited) == 46
    assert len(child["pairs"]) == 48

    for key, pair in inherited.items():
        assert key in parent["pairs"]
        assert pair["wording"] == parent["pairs"][key]["wording"]
        assert pair["strength"] == parent["pairs"][key]["strength"]
        assert pair["aspects_hint"] == parent["pairs"][key]["aspects_hint"]

    for key, pair in parent["pairs"].items():
        assert pair["inherited_from"] is None


# ---------------------------------------------------------------------------
# _meta self-consistency.
# ---------------------------------------------------------------------------

def test_meta_self_consistency():
    artifact = _load_artifact()
    meta = artifact["_meta"]

    assert meta["pairs_total"] == sum(len(e["pairs"]) for e in artifact["events"].values())
    assert meta["events_with_pairs"] == sum(1 for e in artifact["events"].values() if e["pairs"])
    assert meta["events_marked_none"] == sum(1 for e in artifact["events"].values() if e["marked_none"])
    assert meta["events_total"] == len(artifact["events"])
    assert set(meta["tiers"]) == {"strong", "weak", "excluded"}

    try:
        date.fromisoformat(meta["built_on"])
    except ValueError:
        raise AssertionError(f"built_on is not an ISO date: {meta['built_on']!r}")

    # Human sign-off - pinned to the signed review (reviewed_on 2026-08-14).
    assert meta["reviewed_by"] == "ingFlow"
    assert meta["reviewed_on"] == "2026-08-14"
    assert meta["source_notes"]["policy"]
