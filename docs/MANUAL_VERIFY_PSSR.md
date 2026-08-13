# MANUAL VERIFY - PSSR Window-Narrowing Implementation

Manual verification checklist for the PSSR Window-Narrowing feature
(implementation contract: `docs/pssr_window_narrowing_design_v5.md`).

Run these steps when implementation is complete. Each step lists the exact
commands and the expected outcomes. Anything that does not match is a
defect - fix before proceeding.

## Prerequisites

Run from the repository root. All test commands use:

    $env:PYTHONPATH = "<repo>\src"; python -m pytest tests/ -q

The full suite must pass at the end of every step (baseline at the start of
implementation: 152 passed; Step 1 raised it to 164; Step 2 to 185; Step 3 to
206).

---

## Step 0 - Reference assets

Goal: the compendium reference data and design docs are committed so the
data build is reproducible.

1. `git status` - `compendium_reference/` and `docs/` must be tracked
   (the only acceptable untracked item is `docs/ai_archive/`).
2. `compendium_reference/` must contain:
   - `Event Astrology a Compendium of Aspects.md`
   - `compendium_scoring_export_v2.json`
   - `juan_combos_pairs_v1.json`
   - `juan_combos_pairs_v1.review.txt`
3. `docs/` must contain the design docs v3/v4/v5, the developer manual,
   this file, and `CHANGELOG.md`.

---

## Step 1 - Data build: the pairwise table

Goal: the pairwise table artifact is built from the source markdown, all
four quality gates pass, and the artifact matches its gate tests.

1. Rebuild and verify the gates:

       python scripts/build_juan_combos_table.py --built-on YYYY-MM-DD

   Expected output: `Gates G1-G4 all passed.` with `events_total=40`,
   `events_with_pairs=37`, `events_marked_none=3`, `pairs_total=1384`,
   `source_notes: 5 excluded, 1 merged`.

2. Determinism: run the same command again and confirm the JSON is
   byte-identical (e.g. `git diff --stat compendium_reference/` shows no
   changes).

3. Spot-verification (v5 section 7 Step 1): Birth of Brother -> 45 pairs
   (`n_total=45` in the artifact); the three marked-none events
   (Demobilization or Release, Assasination or Suicide, Gambling Loss) ->
   empty pairs; Positive Travel Overseas pairs carry `inherited_from`.

4. Gate tests over the committed artifact:

       $env:PYTHONPATH = "<repo>\src"; python -m pytest tests/test_juan_combos_data.py -q

   Expected: 12 passed.

5. Open `compendium_reference/juan_combos_pairs_v1.review.txt` and review:
   - Every `excluded` assignment (48 total) reads as counter-indicative
     ("only exception"-class wording).
   - Every `weak` assignment (158 total) reads as hedged ("possible",
     "sometimes", "occasionally"-class wording). Watch for whole-bullet
     `weak` codes where the hedge applies to a sub-case only (e.g.
     Success or Elected ASC:URANUS).
   - The "SOURCE-NOTE EXCLUSIONS" section lists exactly the 5
     "Short Relationships" bullets (lines 3421-3425).
   - The "MERGED SOURCE DUPLICATES" section lists exactly
     MOON:NODE_ANY (lines 3386, 3391), both strong.
6. After review, sign off: edit `compendium_reference/juan_combos_pairs_v1.json`
   and set `_meta.reviewed_by` and `_meta.reviewed_on`. Re-run
   `tests/test_juan_combos_data.py` - the sign-off test
   (`test_meta_self_consistency`) will then fail until updated; that is the
   expected trigger to update the test to pin the signed review.

---

## Step 2 - significators/compendium.py

Goal: `src/topo_astro/significators/compendium.py` exposes the artifacts
to the pipeline: EventType -> title mapping, per-symbol tier lookup, and
the unordered pairwise strength lookup.

1. `$env:PYTHONPATH = "<repo>\src"; python -m pytest tests/test_compendium_lookup.py -q`
   - Expected: 21 passed.
2. All 51 `EventType`s resolve per v5 section 4.2 (40 mapped, 11 no-data):
   - `Compendium.load()` then `compendium.event_title_for(EventType.ARREST)`
     returns the exact JSON title for every mapped EventType.
   - `compendium.event_title_for(EventType.POSITIVE_AC_MC)` and the other
     10 no-data EventTypes return `None` (no crash, no silent default).
3. `compendium.tier_score(event_id, symbol)`:
   - Returns the exact integer from `compendium_scoring_export_v2.json`
     for every (event, symbol) present in the data.
   - Returns `None` for absent keys (e.g. SATURN for the events that lack
     it) - never a synthesized 0.
   - Accepts codebase named labels: `tier_score(id, "Mean_Node")` equals
     `tier_score(id, "NODE_ANY")`; `"H1"` equals `"ASC"`.
4. `compendium.pair_strength(event_id, point_a, point_b)`:
   - Unordered: `(A, B)` and `(B, A)` return the same result for every one
     of the 1384 pairs in the artifact.
   - Returns only `"strong" | "weak" | "excluded" | None`.
   - Inherited pairs resolve: `TRAVEL_OVERSEAS_POSITIVE` lookups match
     "Positive Travel"'s strengths (the artifact's `inherited_from`).
   - Unlisted pairs and the three marked-none events return `None`.
   - Spot values: Birth of Brother MARS:POF -> `"excluded"`;
     Success or Elected MOON:NODE_ANY -> `"strong"`.
5. Fail-closed: unknown event id (e.g. 9999), unknown symbol, and all
   no-data EventTypes return `None` for every lookup.
6. `SYMBOL_MAP_NAMED` covers v5 section 4.3 (planets, Mean_Node, POF,
   H1->ASC, H4->IC, H7->DESC, H10->MC, minor cusps direct, identity
   entries), and every value is a real symbol in `symbol_labels`.
7. Full suite: 185 passed (164 from Step 1 + 21 new).

---

## Step 3 - Plumbing: speeds, orb extraction, and the config module

Goal: `calc_planets_labelled_speeds` in `core/constants.py` (§5.4), the
named orb constants in `core/aspects.py` (§5.5), `PSSR_Auto`'s additive
`return_speeds` keyword (§5.3), and the config module
`batch/pssr_window_config.py` (§5.6) - built in that order, config last.

1. `python -m pytest tests/test_pssr_plumbing.py tests/test_pssr_window_config.py -q`
   - Expected: 12 + 9 = 21 passed. Also re-run
   `tests/test_core_constants.py tests/test_core_aspects.py` - all pass.
2. **Backward-compatibility (critical):** run `PSSR_Auto` with a real
   birth/event pair TWICE - once with the previous (default) call and once
   with `return_speeds=False`. The two `dict_info` outputs must be
   byte-identical. `tests/test_techniques_golden.py` untouched and green.
3. `find_pssr_swiss_aspects` behavior byte-identical after the orb-literal
   extraction (golden files green); the constants
   `PSSR_PLANET_ORB_DEG = 12/60` and `PSSR_MOON_ORB_DEG = 32/60` carry the
   original inline comment; no orb VALUE changed. Semantics pinned:
   Moon conj/opp fire up to 32', Moon other aspects only up to 18', and
   non-Moon pairs only up to 12'.
4. With `return_speeds=True`, `dict_info` additionally contains the four
   speed keys (`prog_dir_speeds`, `reg_dir_speeds`, `prog_conv_speeds`,
   `reg_conv_speeds`), each entry `(name, longitude, speed, label)`
   parallel to the corresponding prog/reg half of `direct_planets` /
   `converse_planets`; cross-check one or two values against
   `calc_planets_labelled_speeds` on the same dates.
5. `calc_planets_labelled_speeds(jd, label)` matches `calc_planets_labelled`
   positions, keeping the per-planet speed (xx[3]); existing
   `calc_planets_labelled` untouched. Sanity: Moon speed ~11.7-15.5
   deg/day; Venus can be near station (near 0) up to ~1.3 deg/day.
6. Config module: every knob from the v5 section 6.2 table is present with
   a provenance comment (book page / spec section / existing code
   location); the imported knobs equal their source constants
   (`test_pssr_window_config.py` drift guards pass, incl. identity `is`
   with `MAJOR_ASPECTS`, `PSSR_PLANET_ORB_DEG`, `PSSR_MOON_ORB_DEG`); the
   pipeline contains zero hardcoded business values.
7. Full suite: 206 passed (185 from Step 2 + 21 new).

---

## Step 4 - Sweep and per-point evaluation

Goal: `batch/pssr_window.py` implements the sweep and the stage logic
(v5 sections 3.2-3.6) with relevance stubbed open, so the kinematics are
tested in isolation.

1. `python -m pytest tests/test_pssr_window.py -q`
   - Expected: 23 passed.
2. Synthetic checks (the tests assert these; re-read them to confirm they
   cover the contract):
   - A fast-to-slow exact conjunction fires stage 1 in both Case A
     (fast progressed) and Case B (fast radix), and only within 12' on
     either side of the exact point.
   - A progressed-Moon-to-slow aspect fires stage 2 arm 1 with the 18'/32'
     boundary behavior (conjunction/opposition up to 32', other majors
     only up to 18' - the wider Moon orb is name-gated so a square at 30'
     does NOT get the 32' orb).
   - A Mercury-Venus exact aspect fires stage 2 arm 2 - and is never
     produced by stage 1 (fast-to-fast removed from stage 1, D6).
   - Orb-boundary tests at 12'/18'/32' and major-only behavior (a
     45-degree semisquare just inside orb never fires, but is recorded in
     the near-miss ledger as `minor_aspect`).
   - Speed gate: with a stubbed speed below the 30'/day floor, the same
     stage-1 hit is excluded and lands in the near-miss ledger with its
     speed recorded (`speed_below_floor`, `speed_deg_per_day`); a
     fast-to-fast hit with one stalled point is likewise excluded; a
     retrograde fast point passes on |speed|.
   - No Sun, POF, or angle/house point ever appears in a hit (asserted by
     membership tests and the real-sweep invariant test).
3. Real-ephemeris (beyonce fixture): `test_real_sweep_invariants` - every
   real stage-1 hit is within 12', stage-1 hits have correct fast/slow
   membership, and `test_real_sweep_in_orb_episode_ends_at_12_arcmin` walks
   outward from the tightest real stage-1 hit and confirms the pair leaves
   orb exactly at the 12' boundary (the "computed candidate time ... only
   within 12' on either side" checklist item, on live data).
4. Full suite: 229 passed (206 from Step 3 + 23 new).

---

## Step 5 - Relevance wiring

Goal: the compendium lookups (Step 2) are wired into the stages
(v5 sections 3.7, 4.1, 4.2).

1. Per-gate unit tests (in `tests/test_pssr_window.py`, real
   `Compendium.load()`): a `strong` pair passes its gate; `excluded`
   (Birth of Son Mars-Pluto) does not; absent (Birth of Son
   Mercury-Neptune) does not; `weak` (Birth of Son Jupiter-Venus) goes
   to the near-miss ledger as `weak_relevance`; unordered lookup gives
   the same result in Case A and Case B; arm-1 tier boundaries pass at 8
   and 6 (inclusive at the floor) and fail at 4 and 2 with the actual
   tier recorded; an absent tier key fails closed (`tier=None`).
2. No-data EventTypes (e.g. POSITIVE_AC_MC) produce zero stage-1 hits
   and `no_data` near-misses in both stages (reported, never silently
   absent). The three marked-none events (e.g. Demobilization or
   Release) also produce zero stage-1 hits, but arm 1 still contributes
   when the slow point's tier clears the floor (Jupiter 8 does;
   Saturn, tier absent, fails closed).
3. Real sweep on the Beyonce fixture with the compendium wired: every
   stage-1 hit for SUCCESS_ELECTED resolves to `strong` in the pairwise
   table.
4. Full suite: 239 passed (229 from Step 4 + 10 new).

---

## Step 6 - Ranges, coarse pass, fine pass, margin, report

Goal: intervals, consensus, margin and the report (v5 sections 3.7-3.10).

1. Synthetic interval tests (in `tests/test_pssr_window.py`, pure pass
   functions over hand-built interval sets):
   - Full coarse consensus produces the expected narrowed range.
   - Empty coarse intersection -> max-cardinality partial consensus with
     the correct subset and the dropped events visible.
   - Disjoint everything -> full window passes through (`none` tier).
   - Fine consensus within the coarse window narrows it further.
   - Empty fine consensus -> coarse window returned.
   - Margins clamp to the input window (never widen beyond it).
   - Partial consensus disabled via `CONSENSUS_MAX_CARDINALITY=False`.
2. Fine hits outside the coarse window appear in the report's
   `fine_outside_coarse` ledger (and C2 is clipped to the margined scan
   region before consensus).
3. Corroboration tiers at the 2 / 1 / 0 boundaries; a single event
   <= 60 min (`usable`, `single_event`) vs > 60 min (`weak`)
   (`SINGLE_EVENT_FINE_RANGE_MINUTES`). Contract resolution documented
   in the `pssr_window.py` module docstring: with exactly one
   corroborating event its own contribution range becomes the final
   window (C2 if non-empty else C1) - the consensus machinery itself
   never narrows below the input window with fewer than 2 contributors.
4. Fail-open: `narrow_birth_time_window` on any internal error returns
   the full input window with tier `none`, reason `internal_error`, and
   the error surfaced in the report's `errors` list - it returns rather
   than raises (verified by monkeypatching an ephemeris crash).
5. End-to-end entry-point run on the Beyonce fixture (coarse
   `STEP_SECONDS` keeps the test sweep small): report schema complete,
   final window inside the input window, `errors` empty.
6. Full suite: 254 passed (239 from Step 5 + 15 new).

---

## Step 7 - End-to-end and calibration

Goal: `narrow_birth_time_window` over 2-3 real people from `data_input/`
with well-populated event lists.

1. End-to-end on all six candidates (`hussein.json`, `jacqui onassis.json`,
   `john lennon.json`, `mae.json`, `margaret millard.json`,
   `ing tea prim.json`): every run completes without raising, produces a
   window per event (62-101 min, tier `usable`), and every narrowed window
   is a strict subset of the full 24 h range. john lennon is the strongest
   (fine consensus `full`, corroboration 4); the pre-margin fine range on
   hussein is ~6 min (sub-hour). Per-person results documented in the Step
   7 changelog entry.
2. Report contents complete: per-event stage/arm-attributed hits with
   interval and orb at interval center, relevance source + wording, speed
   values, near-miss ledger (incl. `fine_outside_coarse` entries carrying
   a `kind` marker), tier, coarse/fine corroboration over
   events-with-data, consensus type per pass, margin applied, subset
   members where partial, signed distance of the actual DOB from the
   final window, and the parameters used.
3. Timing recorded: full fine sweep 24 h x 16-22 events = 131-242 s per
   person. The optional coarse pass (section 3.2) was therefore
   implemented and verified: on hussein it reproduces the fine sweep
   exactly (0.0 s window-edge difference, same tier/consensus/
   corroboration) at 62 s vs 145 s. `COARSE_PASS_PREFILTER` defaults
   off; required for multi-thousand-hour windows (e.g. `ing tea.json`).
4. **Sensitivity analysis (documented, not auto-tuned)** - hussein:
   `SPEED_FLOOR_ARC_MIN_PER_DAY` {25,30,35}, `ORB_MOON_GENERAL_ARC_MIN`
   {16,18,20}, `STAGE2_TIER_FLOOR` {4,6,8}, `SAFETY_MARGIN_MINUTES`
   {15,30,60}. Every setting keeps tier `usable` and coarse corroboration
   11/16; fine corroboration 14-16. Width is linear in the safety margin
   (36/66/126 min = pre-margin ~6 min + 2 x margin); the other three
   knobs move width only within 66-75 min. Defaults unchanged. All knobs
   are driven through the `config` object end to end (the cfg-threading
   change in this step).
5. Full suite: 255 passed (254 from Step 6 + 1 new).

---

## Step 8 - Docs and hygiene

Goal: module docstrings per the migration manual's section 3.3 standard;
cross-reference the spec from the module docstrings.

1. Docstring audit for the new/modified files (compendium.py, config,
   pssr_window.py, constants.py, aspects.py, pssr.py): each module
   docstring states what the module is responsible for and which
   architectural layer it belongs to (and where relocated things came
   from).
2. The pipeline module docstring references the spec's section 9
   future-research register.
3. `docs/CHANGELOG.md` has an entry for every step (1-8).
4. Full suite green.

---

## Final acceptance

1. `$env:PYTHONPATH = "<repo>\src"; python -m pytest tests/ -q` - all
   pass (206 + tests added by steps 4-8).
2. `docs/CHANGELOG.md` contains an entry for every step.
3. `compendium_reference/juan_combos_pairs_v1.json` is signed off
   (`_meta.reviewed_by` / `_meta.reviewed_on` set).
4. `git status` shows only intended files.
5. Every item in this checklist is ticked with the actual result.