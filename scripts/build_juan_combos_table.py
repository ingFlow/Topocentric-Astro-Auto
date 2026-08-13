"""
scripts/build_juan_combos_table.py - one-time data builder for the Juan
Combos pairwise table (PSSR window-narrowing, spec v5 section 4.1).

Architectural layer: scripts/ (pre-Phase-10 data tooling, purely additive).
This script is NOT part of the installable package - it is executed once to
produce a hand-curated research data artifact, the same care class as
significators/rules_data.py.

Responsibilities:
    - Parse the "Astrological Combinations (Estadella)" sections of
      compendium_reference/Event Astrology a Compendium of Aspects.md into a
      structured (event, point_a, point_b) -> {strength, wording,
      aspects_hint, inherited_from} table.
    - Apply the tier-coding keyword rules (strong / weak / excluded) and
      the 14-point Juan Combos roster check from spec v5 section 4.1.
    - Handle the two source-internal anomalies (both currently unique to the
      "Success or Elected" section) explicitly, never silently:
        * Research-note sub-blocks: a bullet whose prose carries the
          "candidate_categories:" field starts an editorial research-note
          block that runs to the end of the section's bullet list. Those
          bullets are NOT pair attributions - they are excluded from the
          table and recorded in _meta.source_notes + the review file.
        * Genuine source double-listings (SANCTIONED_SOURCE_DUPLICATES) are
          merged first-wins and recorded; tier conflicts are a hard error.
    - Run the four automated quality gates G1-G4:
        G1: attributed pair count per event == the JSON's preserved
            juan_combos_total_combinations minus that event's excluded
            research-note bullets, for every event that has a section.
        G2: zero parser hits outside the 14-point roster; zero unparseable
            bullets (each failure is a hard error with the line number).
        G3: no duplicate canonical keys within an event, except the
            sanctioned genuine double-listings which are merged first-wins;
            a stale sanction or a tier conflict within a merged listing is
            also a hard error.
        G4: every one of the 40 JSON events has an entry (pairs or
            marked_none).
    - Emit compendium_reference/juan_combos_pairs_v1.json and a human-review
      copy (juan_combos_pairs_v1.review.txt). A human must review the coded
      output - every excluded/weak assignment, the excluded research notes
      and the merged duplicates in particular - and sign off in the JSON's
      _meta.reviewed_by / _meta.reviewed_on before this artifact is trusted
      by the narrowing pipeline.

Deterministic and idempotent: given the same inputs and an explicit
--built-on date, the emitted JSON is byte-identical across runs.

Usage:
    python scripts/build_juan_combos_table.py [--built-on YYYY-MM-DD]
"""

import argparse
import json
import os
import re
import sys
from datetime import date

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPENDIUM_DIR = os.path.join(REPO_ROOT, "compendium_reference")
SOURCE_FILE = os.path.join(COMPENDIUM_DIR, "Event Astrology a Compendium of Aspects.md")
SCORING_FILE = os.path.join(COMPENDIUM_DIR, "compendium_scoring_export_v2.json")
OUT_FILE = os.path.join(COMPENDIUM_DIR, "juan_combos_pairs_v1.json")
REVIEW_FILE = os.path.join(COMPENDIUM_DIR, "juan_combos_pairs_v1.review.txt")

# ---------------------------------------------------------------------------
# Point-name vocabulary (spec v5 section 4.1, 4.3)
# ---------------------------------------------------------------------------

# Compendium-side name (as it appears in the markdown bullet headers) mapped
# to the canonical compendium symbol used as the canonical key in the table.
COMPENDIUM_NAME_TO_SYMBOL = {
    "AS": "ASC",
    "MC": "MC",
    "Sun": "SUN",
    "Moon": "MOON",
    "Mercury": "MERCURY",
    "Venus": "VENUS",
    "Mars": "MARS",
    "Jupiter": "JUPITER",
    "Saturn": "SATURN",
    "Uranus": "URANUS",
    "Neptune": "NEPTUNE",
    "Pluto": "PLUTO",
    "Lunar Node": "NODE_ANY",
    "Part of Fortune": "POF",
}

# The 14-point Juan Combos roster. A parsed point outside this roster is a
# hard build error (G2), never a silent accept.
JUAN_COMBOS_ROSTER = frozenset(COMPENDIUM_NAME_TO_SYMBOL.values())

# Tier-coding keyword rules (spec v5 section 4.1). Checked in order:
# excluded first, then weak, then strong (the default for any positive
# statement that is not hedged and not counter-indicative).
EXCLUDED_MARKERS = (
    "only occasional exception",
    "only exception",
    "only positive event",
)
WEAK_MARKERS = (
    "occasionally",
    "sometimes",
    "to a lesser extent",
    "possible as well",
    "can occur",
    "can happen",
    "may find",
    "very rare",
    "less frequently",
)

TIER_STRONG = "strong"
TIER_WEAK = "weak"
TIER_EXCLUDED = "excluded"

MARKED_NONE_EVENTS = {
    "Demobilization or Release",
    "Assasination or Suicide",
    "Gambling Loss",
}

# Editorial research-note marker. A bullet whose prose carries this field
# starts a research-note sub-block that is NOT a pair attribution for the
# event (spec v5 section 4.1); it runs to the end of the section's bullet
# list. Currently unique to the "Success or Elected" section.
RESEARCH_NOTE_MARKER = "candidate_categories:"

# Source-internal duplicate pairings (genuine double-listings in the
# markdown, not parser artifacts). Each is merged first-wins and recorded in
# _meta.source_notes for the human review pass; any OTHER duplicate
# canonical key is a hard gate G3 failure. A sanction that no longer matches
# the source (stale entry) is also a hard error.
SANCTIONED_SOURCE_DUPLICATES = {
    ("Success or Elected", "MOON:NODE_ANY"): (
        "Genuine double-listing in the source: L3386 'Among the positive "
        "events, we find romantic relationships.' vs L3391 'Among the "
        "positive events, we find professional successes.' First occurrence "
        "wins; both are 'we find'-class strong."
    ),
}

BULLET_RE = re.compile(r"^\s*-\s*\*\*(.+?)\*\*\s*:\s*(.*)$")
HEADING_RE = re.compile(r"^#{1,2}\s*(.+?)\s*$")
ESTADELLA_HEADING = "Astrological Combinations (Estadella)"

# The JSON uses a curly apostrophe in "Child's Marriage" while the markdown
# uses a straight one; title matching normalizes both forms.
def normalize_title(title):
    """Normalize a compendium title for cross-file matching (curly vs
    straight apostrophes only - both files otherwise agree exactly)."""
    return title.replace("\u2019", "'").replace("\u2018", "'")


def normalize_point(name):
    """Map a compendium-side point name to its canonical symbol.

    Raises ValueError for anything outside the 14-point roster - the caller
    treats that as a hard build error (gate G2).
    """
    try:
        return COMPENDIUM_NAME_TO_SYMBOL[name]
    except KeyError:
        raise ValueError(f"point name {name!r} is outside the Juan Combos 14-point roster")


def code_tier(wording):
    """Code a bullet's prose to one of strong / weak / excluded.

    Precedence is fixed: a counter-indicative ('only exception' class)
    wording wins over hedged wording wins over the strong default. This is
    wording-cued, mirroring the 'Other' source's existing methodology in the
    reference doc (spec v5 section 4.1); the human review pass is the quality
    gate for these assignments.
    """
    lowered = wording.lower()
    for marker in EXCLUDED_MARKERS:
        if marker in lowered:
            return TIER_EXCLUDED
    for marker in WEAK_MARKERS:
        if marker in lowered:
            return TIER_WEAK
    return TIER_STRONG


def extract_aspects_hint(wording):
    """Capture the trailing aspect-structure parenthetical (e.g. "(in
    conjunctions and harmonic aspects)") as free text for future calibration.
    Parentheticals that are not aspect-structure hints (gender tags, example
    names, reference tags) are left inside the wording verbatim."""
    match = re.search(r"\((?P<hint>in\b[^()]*)\)\s*$", wording)
    if match:
        return match.group("hint").strip()
    return ""


def split_bullet_header(header):
    """Split a bullet header 'A-B / B-A' into its two unordered point-name
    pairs. Both halves must be present; a malformed header is a hard error."""
    left, _, right = header.partition(" / ")
    if not left or not right:
        raise ValueError(f"malformed bullet header: {header!r}")
    return [left.strip(), right.strip()]


def find_event_sections(lines, titles):
    """Locate each event's (start_line, end_line) span in the markdown.

    Returns a dict {json_title: (start, end)}. Event boundaries are either
    the headingless first section (the file's first line, plain text - e.g.
    "Birth of Brother") or a `#`/`##` heading whose text matches a known
    JSON title.
    """
    normalized_titles = {normalize_title(t): t for t in titles}
    sections = {}
    current = None
    first_title = normalized_titles.get(normalize_title(lines[0].strip()))
    if first_title is not None:
        current = first_title
        sections[current] = {"start": 0, "end": None}
    for idx, line in enumerate(lines):
        heading = HEADING_RE.match(line)
        if heading is not None:
            title = normalized_titles.get(normalize_title(heading.group(1).strip()))
            if title is not None:
                if current is not None:
                    sections[current]["end"] = idx
                current = title
                sections[current] = {"start": idx, "end": None}
    if current is not None and sections[current]["end"] is None:
        sections[current]["end"] = len(lines)
    return sections


def extract_estadella_bullets(lines, start, end):
    """Return the (line_number, bullet_line) pairs inside one event's
    'Astrological Combinations (Estadella)' section (bullets only, from the
    section heading to the next heading)."""
    est_idx = None
    for idx in range(start, end):
        if ESTADELLA_HEADING in lines[idx]:
            est_idx = idx
            break
    if est_idx is None:
        raise ValueError(f"no '{ESTADELLA_HEADING}' heading in event section lines {start}-{end}")
    bullets = []
    for idx in range(est_idx + 1, end):
        line = lines[idx]
        if HEADING_RE.match(line):
            break
        if BULLET_RE.match(line):
            bullets.append((idx + 1, line))
    return bullets


def parse_bullet(bullet):
    """Parse one bullet line into (symbol_a, symbol_b, wording, aspects_hint).

    Raises ValueError (with the 1-based line number) for any roster miss or
    malformed header - hard errors per gate G2.
    """
    line_no, line = bullet
    header, prose = BULLET_RE.match(line).groups()
    points = []
    for part in split_bullet_header(header):
        point_name, separator, _ = part.partition("-")
        if not separator:
            raise ValueError(f"line {line_no}: bullet header has no '-' separator: {part!r}")
        points.append(normalize_point(point_name.strip()))
    a, b = sorted(points)
    wording = prose.strip()
    aspects_hint = extract_aspects_hint(wording)
    if aspects_hint:
        wording = re.sub(r"\(\s*" + re.escape(aspects_hint) + r"\s*\)\s*$", "", wording).strip()
    return a, b, wording, aspects_hint


def split_off_research_notes(bullets):
    """Split a section's bullets into pair attributions and research notes.

    A bullet whose prose carries the RESEARCH_NOTE_MARKER starts an editorial
    research-note block that runs to the end of the section's bullet list
    (the section itself ends at the next heading). Bullets in that block are
    NOT pair attributions for the event and are returned separately so the
    caller can record them for human review.
    """
    marker_idx = None
    for idx, (line_no, line) in enumerate(bullets):
        if RESEARCH_NOTE_MARKER in line:
            marker_idx = idx
            break
    if marker_idx is None:
        return bullets, []
    return bullets[:marker_idx], bullets[marker_idx:]


def build_table(md_path, scoring_path, built_on=None):
    """Run the full build: parse, gate (G1-G4), and return the output dict.

    Raises SystemExit with a summary on any gate failure - the gates are the
    contract, and the builder never emits a table that fails them.
    """
    with open(md_path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    with open(scoring_path, encoding="utf-8") as f:
        scoring = json.load(f)

    titles = [event["title"] for event in scoring["events"]]
    sections = find_event_sections(lines, titles)

    errors = []
    events_out = {}
    total_pairs = 0
    events_with_pairs = 0
    excluded_records = []
    merged_records = []

    for event in scoring["events"]:
        title = event["title"]
        expected_total = event["sample_sizes"]["juan_combos_total_combinations"]
        expected_marked_none = event["sample_sizes"]["juan_combos_marked_none"]
        section = sections.get(title)
        if section is None:
            errors.append(f"[G4] {title}: no section found in the markdown")
            continue

        bullets = extract_estadella_bullets(lines, section["start"], section["end"])
        attributed, excluded_notes = split_off_research_notes(bullets)
        entry = {"n_total": len(attributed), "pairs": {}, "marked_none": False}
        if len(bullets) == 0:
            entry["marked_none"] = True

        if expected_marked_none and len(bullets) != 0:
            errors.append(
                f"[G1] {title}: JSON marks juan_combos_marked_none but {len(bullets)} bullets were parsed"
            )

        for bullet in excluded_notes:
            try:
                _, _, wording, _ = parse_bullet(bullet)
            except ValueError as exc:
                errors.append(f"[G2] {title}: {exc}")
                continue
            excluded_records.append(
                {
                    "event": title,
                    "line": bullet[0],
                    "wording": wording,
                    "reason": "research-note sub-block ('candidate_categories:' field)",
                }
            )

        occurrences = {}
        for bullet in attributed:
            try:
                parsed = parse_bullet(bullet)
            except ValueError as exc:
                errors.append(f"[G2] {title}: {exc}")
                continue
            key = f"{parsed[0]}:{parsed[1]}"
            occurrences.setdefault(key, []).append((bullet[0], parsed))
        for key, occ in occurrences.items():
            line_no, (a, b, wording, aspects_hint) = occ[0]
            pair = {
                "strength": code_tier(wording),
                "wording": wording,
                "aspects_hint": aspects_hint,
                "inherited_from": None,
            }
            if len(occ) == 1:
                entry["pairs"][key] = pair
                continue
            sanction = SANCTIONED_SOURCE_DUPLICATES.get((title, key))
            if sanction is None:
                lines_nos = ", ".join(str(n) for n, _ in occ)
                errors.append(f"[G3] {title}: duplicate canonical key {key} (lines {lines_nos})")
                continue
            tiers = [code_tier(w) for _, (_, _, w, _) in occ]
            if len(set(tiers)) > 1:
                lines_nos = ", ".join(str(n) for n, _ in occ)
                errors.append(
                    f"[G3] {title}: sanctioned duplicate {key} has conflicting tiers "
                    f"{tiers} (lines {lines_nos})"
                )
                continue
            pair["strength"] = tiers[0]
            entry["pairs"][key] = pair
            merged_records.append(
                {
                    "event": title,
                    "key": key,
                    "lines": [n for n, _ in occ],
                    "tiers": tiers,
                    "reason": sanction,
                }
            )

        # G1: the attributed count must equal the JSON's preserved total
        # minus that event's excluded research-note bullets.
        expected_attributed = expected_total - len(excluded_notes)
        if len(attributed) != expected_attributed:
            carve_out = (
                f" ({len(excluded_notes)} research-note bullets excluded)" if excluded_notes else ""
            )
            errors.append(
                f"[G1] {title}: parsed {len(attributed)} pairs{carve_out}, "
                f"JSON preserves {expected_total}"
            )

        if len(entry["pairs"]) > 0:
            events_with_pairs += 1
        events_out[title] = entry

    # G3: a sanction that no longer matches the source is a stale entry -
    # the allowlist must never drift out of sync with the real data.
    merged_keys = {(note["event"], note["key"]) for note in merged_records}
    for key in SANCTIONED_SOURCE_DUPLICATES:
        if key not in merged_keys:
            errors.append(f"[G3] stale sanction: {key} is sanctioned but was not found duplicated")

    # Cross-reference inheritance (spec v5 section 4.1): "Positive Travel
    # Overseas" inherits "Positive Travel"'s pairs, each marked with
    # inherited_from.
    inheritance = {"Positive Travel Overseas": "Positive Travel"}
    for child, parent in inheritance.items():
        parent_entry = events_out.get(parent)
        child_entry = events_out.get(child)
        if parent_entry is None or child_entry is None:
            continue
        for key, pair in parent_entry["pairs"].items():
            if key in child_entry["pairs"]:
                continue
            inherited = dict(pair)
            inherited["inherited_from"] = parent
            child_entry["pairs"][key] = inherited

    # G4: every one of the 40 JSON events must have an entry.
    missing_events = [title for title in titles if title not in events_out]
    for title in missing_events:
        errors.append(f"[G4] {title}: no entry produced")

    # pairs_total must reflect the final artifact, including pairs added by
    # the cross-reference inheritance step.
    total_pairs = sum(len(entry["pairs"]) for entry in events_out.values())

    if errors:
        raise SystemExit("\n".join(["QUALITY GATES FAILED:"] + errors))

    output = {
        "_meta": {
            "source_file": "compendium_reference/Event Astrology a Compendium of Aspects.md",
            "builder": "scripts/build_juan_combos_table.py",
            "built_on": built_on if built_on is not None else date.today().isoformat(),
            "reviewed_by": None,
            "reviewed_on": None,
            "tiers": {
                TIER_STRONG: "expected/frequent/always-type wording",
                TIER_WEAK: "possible/sometimes/to-a-lesser-extent wording",
                TIER_EXCLUDED: "only-exception-type hedging wording",
            },
            "events_total": len(events_out),
            "events_with_pairs": events_with_pairs,
            "events_marked_none": sum(1 for e in events_out.values() if e["marked_none"]),
            "pairs_total": total_pairs,
            "source_notes": {
                "policy": (
                    "Research-note sub-blocks marked 'candidate_categories:' "
                    "are not pair attributions and are excluded from the "
                    "table; genuine source double-listings are merged "
                    "first-wins. Both are recorded below and must be "
                    "reviewed before sign-off."
                ),
                "excluded_research_notes": excluded_records,
                "merged_duplicates": merged_records,
            },
        },
        "events": events_out,
    }
    return output


def write_review_file(output):
    """Emit the human-review copy: event -> pair -> tier -> wording, with
    every excluded/weak assignment clearly visible for the review pass."""
    lines = [
        "Juan Combos pairwise table - human review copy",
        "===============================================",
        "Review every assignment below, especially every 'excluded' and",
        "'weak' tier. Sign off in juan_combos_pairs_v1.json's _meta",
        "(reviewed_by / reviewed_on) once satisfied.",
        "",
    ]
    for title, entry in output["events"].items():
        lines.append(f"== {title}  (n={entry['n_total']}{', marked_none' if entry['marked_none'] else ''}) ==")
        if not entry["pairs"]:
            lines.append("  (no pairs)")
        for key in sorted(entry["pairs"]):
            pair = entry["pairs"][key]
            inherited = f"  [inherited from {pair['inherited_from']}]" if pair["inherited_from"] else ""
            hint = f"  [hint: {pair['aspects_hint']}]" if pair["aspects_hint"] else ""
            lines.append(f"  {key} -> {pair['strength']}{inherited}{hint}")
            lines.append(f"      {pair['wording']}")
        lines.append("")

    notes = output["_meta"]["source_notes"]
    excluded = notes["excluded_research_notes"]
    merged = notes["merged_duplicates"]
    lines.append("SOURCE-NOTE EXCLUSIONS (research notes, not pair attributions)")
    lines.append("============================================================")
    if not excluded:
        lines.append("  (none)")
    for note in excluded:
        lines.append(f"  {note['event']} L{note['line']}: {note['wording']}")
        lines.append(f"      reason: {note['reason']}")
    lines.append("")
    lines.append("MERGED SOURCE DUPLICATES (first occurrence wins)")
    lines.append("================================================")
    if not merged:
        lines.append("  (none)")
    for note in merged:
        loc = ", ".join(f"L{n}" for n in note["lines"])
        lines.append(f"  {note['event']} {note['key']} ({loc}): tiers {note['tiers']}")
        lines.append(f"      reason: {note['reason']}")
    lines.append("")
    with open(REVIEW_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--built-on", default=None, help="ISO date recorded in _meta.built_on (default: today)")
    args = parser.parse_args()

    output = build_table(SOURCE_FILE, SCORING_FILE, built_on=args.built_on)

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
        f.write("\n")
    write_review_file(output)

    meta = output["_meta"]
    notes = meta["source_notes"]
    print(f"Gates G1-G4 all passed.")
    print(f"  events_total={meta['events_total']} "
          f"events_with_pairs={meta['events_with_pairs']} "
          f"events_marked_none={meta['events_marked_none']} "
          f"pairs_total={meta['pairs_total']}")
    print(f"  source_notes: {len(notes['excluded_research_notes'])} excluded, "
          f"{len(notes['merged_duplicates'])} merged")
    print(f"Wrote {OUT_FILE}")
    print(f"Wrote {REVIEW_FILE} (review and sign off in _meta before use)")


if __name__ == "__main__":
    main()
