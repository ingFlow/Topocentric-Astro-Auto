# CHANGELOG - PSSR Window-Narrowing Implementation

Changelog for the PSSR Window-Narrowing feature implementation, following
the step order of `docs/pssr_window_narrowing_design_v5.md` (section 7).
Entries are added as each step lands; the most recent entry is on top.

All change sets must keep the full test suite green:

    $env:PYTHONPATH = "<repo>\src"; python -m pytest tests/ -q

---

## Step 2 - `significators/compendium.py` (2026-08-13)

### New files

- `src/topo_astro/significators/compendium.py`
  The compendium data-access layer (spec v5 section 5.1; there was no
  compendium loader before). A `Compendium` instance - created via
  `Compendium.load(base_dir=None)`, defaulting to the repository-root
  `compendium_reference/`, override for tests - holds the two committed
  artifacts and exposes the lookups:
  - `event_title_for(event_id)` - EventType value -> compendium title per
    the section 4.2 table (40 mapped, 11 no-data EventTypes -> None;
    unknown event ids -> None, fail closed).
  - `tier_score(event_id, symbol)` - exact integers from the scoring
    JSON; None for absent keys (never a synthesized 0), unknown symbols
    and no-data events.
  - `pair_strength(event_id, point_a, point_b)` - unordered canonical
    lookup returning `"strong" | "weak" | "excluded" | None`; inherited
    pairs resolve; the three marked-none events and unlisted pairs return
    None (`absent` stays distinct from `excluded`).
  - `SYMBOL_MAP_NAMED` (section 4.3) plus `normalize_title()` /
    `to_compendium_symbol()` helpers. Titles are normalized on load
    (curly vs straight apostrophe - the reference files use a curly one in
    "Child's Marriage"). `Mean_Node`/`Node` -> `NODE_ANY` is the one
    lossy mapping (v5 F15) and is stated as such.
  No module-level mutable state; the loaded data lives on the instance.
- `tests/test_compendium_lookup.py`
  21 tests: the full 51-EventType resolution against a self-contained
  copy of the section 4.2 table; cross-file title consistency (scoring
  JSON + pairs artifact); tier lookups matched against the scoring JSON
  exactly, absent keys -> None, normalization; unordered pair lookups
  across all 1384 artifact pairs, inherited pairs, marked-none events,
  absent-vs-excluded; fail-closed inputs; SYMBOL_MAP_NAMED validity;
  load failures raise.

### Fixes found during implementation

- The reference files store "Child's Marriage" with a curly apostrophe
  (U+2019) while the spec table and code use a straight one - titles are
  now normalized on load so CHILDS_MARRIAGE lookups actually resolve.

### Verified

- All 51 EventTypes resolve per section 4.2 (40 mapped, 11 no-data).
- Absent-key tier lookups return None; unordered pair lookups return the
  same result as the ordered call; inherited pairs resolve.
- Full suite: 185 passed (164 from Step 1 + 21 new).

---

## Step 1 - Juan Combos pairwise data build (2026-08-13)

### New files

- `scripts/build_juan_combos_table.py`
  One-time data builder for the Juan Combos pairwise table (spec v5
  section 4.1). Parses the "Astrological Combinations (Estadella)"
  sections of `compendium_reference/Event Astrology a Compendium of
  Aspects.md` into a structured (event, point_a, point_b) -> {strength,
  wording, aspects_hint, inherited_from} table, applies the tier-coding
  keyword rules (strong / weak / excluded) and the 14-point roster check,
  runs the four automated quality gates G1-G4, and emits the artifact and
  a human-review copy. Deterministic: identical inputs + `--built-on`
  produce byte-identical output.
- `compendium_reference/juan_combos_pairs_v1.json`
  The committed research data artifact (40 events, 37 with pairs, 3
  marked-none, 1384 pairs total including 46 inherited). `_meta` carries
  provenance and `source_notes`; `_meta.reviewed_by` / `reviewed_on` are
  still `None` pending the human review pass.
- `compendium_reference/juan_combos_pairs_v1.review.txt`
  Human-review copy: per event, per pair, tier + wording, with every
  `excluded` / `weak` assignment, the excluded research notes and the
  merged duplicate clearly visible.
- `tests/test_juan_combos_data.py`
  12 tests that re-run gates G1-G4 independently over the committed
  artifact (no imports from the builder): counts vs the scoring JSON,
  roster and schema, merge/exclusion records, inheritance, meta
  self-consistency.

### Source-anomaly handling (user decision, Option A)

The source's "Success or Elected" section contains duplicate pairings.
Per decision, the builder handles them explicitly and never silently:

- Research-note sub-block: the 5 bullets in the "Short Relationships"
  sub-block (lines 3421-3425, prose carries the `candidate_categories:`
  field) are NOT pair attributions. They are excluded from the table and
  recorded in `_meta.source_notes.excluded_research_notes` and the review
  file.
- Genuine double-listing: `MOON:NODE_ANY` (lines 3386/3391) is listed
  twice in the main list. It is merged first-wins via the
  `SANCTIONED_SOURCE_DUPLICATES` allowlist and recorded in
  `_meta.source_notes.merged_duplicates`. Any OTHER duplicate canonical
  key, a stale allowlist entry, or a tier conflict within a merged
  listing is a hard gate G3 failure.
- Gate G1 compares the attributed count against the JSON's preserved
  total minus that event's excluded research-note bullets (Success or
  Elected: 60 == 65 - 5).

### Fixes found during verification

- `find_event_sections` now handles the headingless first section
  ("Birth of Brother" is the file's first line, plain text, with no `#`).
- `_meta.pairs_total` is computed AFTER the cross-reference inheritance
  step so it reflects the final artifact (1384 = 1338 own + 46
  inherited), not the pre-inheritance total.

### Verified

- Gates G1-G4 all pass in the builder.
- Artifact is deterministic (SHA-256 identical across re-runs).
- Full suite: 164 passed (152 baseline + 12 new).
- Spot checks: Mars-POF Birth of Brother -> `excluded` ("only positive
  event"); Positive Travel Overseas -> 2 own pairs (NEPTUNE:URANUS,
  NEPTUNE:POF) + 46 inherited from Positive Travel; tier distribution
  1178 strong / 158 weak / 48 excluded.

### Remaining human step

- Review `compendium_reference/juan_combos_pairs_v1.review.txt` and sign
  off by setting `_meta.reviewed_by` / `_meta.reviewed_on` in
  `juan_combos_pairs_v1.json`. See `docs/MANUAL_VERIFY_PSSR.md` step 1.

### Review notes for sign-off

- Tier coding flags a whole bullet `weak` when an "occasionally"-class
  hedge applies to only a sub-case; e.g. Success or Elected ASC:URANUS is
  coded `weak` because its opposition clause says "Occasionally...", even
  though its conjunction/harmonic clause is "we find"-class strong.
  Confirm such assignments are acceptable before signing off.

---
