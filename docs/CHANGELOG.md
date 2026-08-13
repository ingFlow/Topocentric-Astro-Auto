# CHANGELOG - PSSR Window-Narrowing Implementation

Changelog for the PSSR Window-Narrowing feature implementation, following
the step order of `docs/pssr_window_narrowing_design_v5.md` (section 7).
Entries are added as each step lands; the most recent entry is on top.

All change sets must keep the full test suite green:

    $env:PYTHONPATH = "<repo>\src"; python -m pytest tests/ -q

---

## Step 6 - Ranges, coarse pass, fine pass, margin, report (2026-08-13)

### Changes

- `src/topo_astro/batch/pssr_window.py` (spec v5 sections 3.7-3.10)
  - Interval algebra: `intersect_intervals` (literal per-event interval
    intersection), `_max_cardinality_subset` (the max-cardinality
    partial-consensus fallback - exact, not greedy: any subset with a
    non-empty intersection has a common point, so the maximum-overlap
    point over all interval endpoints yields a maximum subset; ties
    broken per `CONSENSUS_TIE_BREAK` by earliest window start),
    `_apply_margin` (safety margin padded on both ends, clamped to the
    input window - never wider), `_clip_intervals`, `_window_span`.
  - `coarse_pass` (section 3.8): full consensus over the stage-1
    contributors; empty intersection -> max-cardinality partial
    consensus (subset members and dropped events visible in the report);
    fewer than 2 contributors or no agreeing subset -> fail-open to the
    full input window.
  - `fine_pass` (section 3.9): stage-2 contributions clipped to the
    margined coarse window; stage-2 hits outside it are recorded in the
    `fine_outside_coarse` ledger (never silently discarded); same
    full/partial/none consensus ladder; empty fine consensus -> the
    coarse window stands.
  - `_select_final_window` (section 3.10): 0 contributors -> `none`,
    full window; exactly 1 -> that event's own contribution range (C2 if
    non-empty else C1), pre-margin, tiered `usable` <= 60 min / `weak`
    > 60 min against `SINGLE_EVENT_FINE_RANGE_MINUTES`; 2+ -> the fine
    consensus if present, else the coarse consensus, else fail-open
    `none`. **Contract resolution (documented in the module docstring):**
    sections 3.8/3.9 fail the consensus passes open to the full window
    with fewer than 2 contributors, but section 3.10's "1 (any stage)"
    tier row and the section 7 checklist (single-event <= 60 vs > 60
    min) require the single corroborating event's own range to become
    the final window - otherwise that tier is unreachable. The consensus
    machinery never narrows below the input window on its own; the
    final-window selection applies the single-event rule.
  - `_restrict_to_single_aspect`: the `MAX_ASPECTS_PER_EVENT = "1"`
    branch - per stage keep the tuple with the widest interval and the
    hit nearest its center (the book's single-aspect practice).
  - `narrow_birth_time_window(...)` (section 3.1): the batch entry
    point. `config` defaults to the resolved config module (any object
    exposing the same constants works); `compendium` defaults to a
    loaded `Compendium` (production mode). Single fine sweep at
    `STEP_SECONDS` over the input window, then coarse -> margined coarse
    -> fine -> final margin -> report. The `PSSRWindowReport` dict
    carries: input window, coarse and fine pass outcomes (consensus
    type, pre-margin window, corroboration count, events-with-data
    count, margin, subset members / dropped events), final window with
    and without margin, tier + reason, signed distance of
    `dt_actual_dob` from the final window, per-event detail (stage/arm/
    variant-attributed hits with interval, orb at interval center,
    relevance source + wording, speed values, near-misses), the
    aggregated near-miss ledger, and the parameters used.
  - Fail-open on internal errors (manual Step 6 item 4): the entry
    point wraps the computation; on any exception it returns the full
    input window with tier `none`, reason `internal_error`, and the
    error surfaced in the report's `errors` list - it never raises and
    never silently narrows from broken data.
- `tests/test_pssr_window.py`
  15 new tests: full coarse consensus narrows; max-cardinality partial
  consensus with the dropped event visible; the partial-consensus knob
  off; disjoint everything -> full window + `none` tier; fewer than two
  contributors fails open; fine consensus narrows within the coarse
  window; empty fine consensus returns the coarse window; margin
  applies and clamps (never wider than the input window); fine-outside-
  coarse ledger + C2 clip; tiers at the 2 / 1 / 0 boundaries incl. the
  single-event <= 60 min (`usable`) vs > 60 min (`weak`) boundary; the
  full `narrow_birth_time_window` run end-to-end on the Beyonce fixture
  (report schema complete, final window inside the input window,
  `errors` empty); and the internal-error fail-open (a monkeypatched
  ephemeris crash returns the full window with the error surfaced).

### Verified

- Full suite: 254 passed (239 from Step 5 + 15 new).

---

## Step 5 - relevance wiring (2026-08-13)

### Changes

- `src/topo_astro/batch/pssr_window.py`
  The Step-4 kinematics-only gates are now wired to the compendium
  (spec v5 sections 3.7, 4.1, 4.2). The stub `_tier_gate` is replaced by
  `_tier_for(compendium, event_id, symbol)` -> `(tier_score | None,
  no_data)` and `_pair_relevance` takes the compendium and returns
  `("strong" | "weak" | "excluded" | "absent", no_data)`. Both gates keep
  the Step-4 behavior when `compendium=None` (gates open - pure
  kinematics mode, used by the Step-4 tests).
  - `stage1_hits`, `stage2_hits`, `evaluate_point` and
    `collect_event_hits` gained a keyword `compendium=None` threaded to
    the gates.
  - Stage 1 / arm 2 relevance: only `strong` pairs hit; `weak`,
    `excluded` and `absent` pairs go to the near-miss ledger as
    `<strength>_relevance`. An event with no compendium data at all, or
    one of the three marked-none events (no pairs catalogued at all),
    yields `no_data` near-misses - reported explicitly, never silently
    absent (v5 section 3.7).
  - Arm 1 (Moon to slow): the slow point's `tier_score` must be >=
    `STAGE2_TIER_FLOOR` (6); an absent tier key or no-data event fails
    closed into a `tier_below_floor` / `no_data` near-miss carrying the
    actual tier (None when absent). Marked-none events still contribute
    via arm 1 because their tier data exists.
- `src/topo_astro/significators/compendium.py`
  New `has_pair_data(event_id)` method so the pipeline can distinguish
  "event has pairs, this one is absent" from "event is marked-none / has
  no pairs at all" (both `pair_strength` cases return None). True only
  when the event has a catalogued pairs entry with at least one pair.
- `tests/test_pssr_window.py`
  10 new tests exercising the wiring against the real compendium:
  strong pair passes; excluded (Birth of Son Mars-Pluto) does not;
  absent (Mercury-Neptune) does not; weak (Jupiter-Venus) goes to the
  ledger as `weak_relevance`; unordered lookup gives the same result in
  Case A and Case B; arm-1 tier floor boundaries (8 and 6 pass, 4 and 2
  fail with the actual tier recorded, inclusive at 6); absent tier key
  fails closed with `tier=None` (Birth of Brother Saturn); no-data
  EventType (POSITIVE_AC_MC) contributes nothing and is reported as
  `no_data` in both stages; marked-none event (Demobilization or
  Release) has zero stage-1 hits but arm 1 still contributes (Jupiter
  tier 8) while an absent tier fails closed; a real sweep on the Beyonce
  fixture with the compendium wired where every stage-1 hit's pair
  resolves to strong for SUCCESS_ELECTED.

### Verified

- Full suite: 239 passed (229 from Step 4 + 10 new).

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

## Step 4 - Sweep and per-point stage evaluation (2026-08-13)

### New files

- `src/topo_astro/batch/pssr_window.py`
  The pipeline's kinematics (spec v5 sections 3.2-3.7), pure functions, no
  globals, zero hardcoded business values (everything read from
  `pssr_window_config`):
  - `sweep_jds` - the section-3.2 grid (inclusive endpoints, default
    `STEP_SECONDS`).
  - `evaluate_point` - recomputes the candidate radix once per grid point
    (shared across events), constructs `PSSR_Auto(..., return_speeds=True)`
    per (point, event), and evaluates stages 1 and 2 on the four
    equal-weight variants (dp/dr/cp/cr).
  - `stage1_hits` - fast-to-slow (Case A fast-progressed / Case B fast-
    radix), 12' orb, majors-only, speed gate measured on the side the fast
    point sits (progressed-side speed vs natal speed).
  - `stage2_hits` - arm 1 Moon-to-slow (32' conj/opp, 18' general; no
    speed gate - vacuous for the Moon; tier gate) and arm 2 fast-to-fast
    (both points individually clear the 30'/day floor; Moon party -> the
    18'/32' Moon orbs).
  - `_aspect_pair` / `_moon_aspect` - the 12'/18'/32' orb rules over raw
    degrees via `calculate_aspect(..., flag_major=True)`; the Moon's wider
    conj/opp orb is name-gated so a non-conj/opp major cannot sneak in at
    32' (calculate_aspect evaluates all majors within the orb it is given).
  - `_minor_near_miss` - a minor aspect inside the applicable orb is
    recorded in the near-miss ledger (`minor_aspect`), never gating.
  - `group_hits_by_tuple` / `build_intervals` / `merge_intervals` /
    `per_stage_union` - section-3.7 per-tuple contiguous in-orb intervals
    (gap > 1.5 grid steps splits a run; overlaps merged) and the per-event
    per-stage unions C1(e)/C2(e).
  - `collect_event_hits` - full sweep per event; the interval builder
    derives the step from the actual point spacing so it cannot drift from
    the sweep that produced the hits.
  The relevance gates (`_pair_relevance`, `_tier_gate`) are stubbed open
  with explicit STEP-4 markers - Step 5 wires the compendium lookups.
- `tests/test_pssr_window.py`
  23 tests. Synthetic (deterministic, no ephemeris): sweep endpoint/step;
  stage-1 exact-conjunction Case A and Case B; the 12' boundary sweep;
  fast-to-fast never produced by stage 1 (D6); Sun/POF/angles never enter;
  speed gate on the progressed side and the radix side, retrograde passing
  on |speed|, the exact floor boundary; arm-1 Moon 32' conj/opp vs 18'
  general boundaries and the opposition case; arm-2 fast-to-fast plus the
  Moon-party orbs and both-points speed gate; the 45-degree semisquare just
  inside orb never fires but is recorded as `minor_aspect`; interval
  building (gap split, distinct tuples, merge) and per-stage unions.
  Real-ephemeris (beyonce fixture): integrated-sweep invariants (every
  stage-1 hit within 12', correct fast/slow membership, no Sun/POF/angles
  anywhere, near-miss kinds bounded) and the checklist centerpiece - a real
  in-orb stage-1 episode walked outward from the tightest hit demonstrably
  leaves orb exactly at the 12' boundary.

### Fixes found during implementation

- `collect_event_hits` originally defaulted `build_intervals`' step to
  `STEP_SECONDS` (60) regardless of the sweep step actually used - with a
  600s sweep every run fragmented into singletons. The step is now derived
  from the point spacing (with an explicit override parameter).
- The first Moon-orb ladder tried the 32' conj/opp orb and accepted
  whatever major it returned - since `calculate_aspect` matches all majors
  within a given orb, a Moon square at 30' was wrongly credited the 32'
  orb. `_moon_aspect` now name-gates: only conjunction/opposition from the
  32' attempt, only other majors from the 18' attempt.

### Verified

- Step 4 checklist: orb boundaries at 12'/18'/32'; Mercury-Venus never
  produced by stage 1; speed gate exclusions land in the near-miss ledger
  with their speeds; semisquare just inside orb never fires.
- Real sweep: stage-1 episodes respect the 12' boundary on live
  ephemeris data.
- Full suite: 229 passed (206 from Step 3 + 23 new).

---

### Changed (extraction refactors, behavior-preserving)

- `src/topo_astro/core/constants.py` - new `calc_planets_labelled_speeds(jd, label)`
  (spec v5 section 5.4): same loop as `calc_planets_labelled`, returning
  `(name, longitude, speed, label)` 4-tuples in `PLANETS` order so the
  speeds are parallel to the existing position lists. The per-planet daily
  speed (`swe.calc_ut`'s `xx[3]`, degrees/day, signed for retrograde) is
  kept alongside the longitude; `calc_planets_labelled` itself is
  untouched.
- `src/topo_astro/core/aspects.py` - the two inline orb literals inside
  `find_pssr_swiss_aspects` are now module-level named constants (spec v5
  section 5.5): `PSSR_PLANET_ORB_DEG = 12/60` (the original `CHANGE` note
  moved onto it) and `PSSR_MOON_ORB_DEG = 32/60`. The finder calls
  `calculate_aspect` with identical values, so its output is byte-identical.
- `src/topo_astro/techniques/pssr.py` - `PSSR_Auto` gains a keyword-only
  `return_speeds=False` parameter (spec v5 section 5.3). When `True`,
  `calc_pssr_for_date` additionally computes the four progressed speed
  sets (prog/reg x direct/converse, Sun excluded, same JDs as the
  position lists) and exposes them in `dict_info` under
  `prog_dir_speeds` / `reg_dir_speeds` / `prog_conv_speeds` /
  `reg_conv_speeds` (each entry `(name, longitude, speed, label)`).
  With the default `return_speeds=False` the `dict_info` is byte-identical
  to the pre-change output (pinned by the golden files).

### New files

- `src/topo_astro/batch/pssr_window_config.py`
  The research control panel (spec v5 section 6): named constants only,
  no logic. Two sourcing rules (section 6.1): values already in the
  codebase are imported complete-by-reference (identity with their source
  constant) - `ASPECT_CLASSES = MAJOR_ASPECTS`, `ORB_FAST_SLOW_DEG =
  PSSR_PLANET_ORB_DEG`, `ORB_MOON_CONJ_OPP_DEG = PSSR_MOON_ORB_DEG`,
  `FAST_SET`/`SLOW_SET`/`MOON` from `significators.rules_data.Planet` - and
  genuinely new decisions are defined here with a `# NEW - <section>, v5`
  tag and one-line rationale. The full section 6.2 knob table is present:
  `STEP_SECONDS=60`, `ORB_MOON_GENERAL_ARC_MIN=18.0`,
  `SPEED_FLOOR_ARC_MIN_PER_DAY=30.0` (book 30-35'/day lower bound),
  `SPEED_FLOOR_USE_ABSOLUTE=True`, `FAST_FAST_SET={MER,VEN,MAR,MON}` (D6),
  `PAIR_RELEVANCE_MIN="strong"` (D3), `STAGE2_TIER_FLOOR=6` (D4),
  `SAFETY_MARGIN_MINUTES=30`, `SINGLE_EVENT_FINE_RANGE_MINUTES=60`,
  `MAX_ASPECTS_PER_EVENT="all"`, `CONSENSUS_MAX_CARDINALITY=True`,
  `CONSENSUS_TIE_BREAK="earliest_start"`.
- `tests/test_pssr_plumbing.py` - 12 tests pinning section 5.3/5.4/5.5:
  speeds match positions and `swe.calc_ut` directly, Moon/Venus speed
  sanity, the untouched 3-tuple shape of `calc_planets_labelled`, orb
  constant values, and the finder's Moon 32'/18'-filter and non-Moon 12'
  semantics; `PSSR_Auto` default-vs-explicit `return_speeds=False`
  identity, the four speed keys added when `True`, speed lists parallel to
  the prog/reg halves of the position lists, and the speed lists matching
  a recomputation from the exposed datetimes.
- `tests/test_pssr_window_config.py` - 9 tests pinning every section 6.2
  knob value and the identity (`is`) imports from `core/aspects.py`, so a
  copy-paste drift cannot slip through (section 6.1 complete-by-reference).

### Verified

- Golden files re-run the full PSSR default path for every (person,
  candidate, event) case and still match byte-for-byte - the extraction
  refactors changed no observable output.
- Full suite: 206 passed (185 from Step 2 + 21 new).

---

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
