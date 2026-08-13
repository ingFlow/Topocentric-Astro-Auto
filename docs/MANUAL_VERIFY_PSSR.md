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
implementation: 152 passed; Step 1 raised it to 164).

---

## Step 0 - Reference assets

Goal: the compendium reference data and design docs are committed so the
data build is reproducible.

1. `git status` - `compendium_reference/` and `docs/` must be tracked
   (the only acceptable untracked item is `docs/ai_archive/`).
2. `git log --oneline -5` - confirm the commit that added
   `compendium_reference/` and `docs/` exists.
3. `compendium_reference/` must contain:
   - `Event Astrology a Compendium of Aspects.md`
   - `compendium_scoring_export_v2.json`
   - `juan_combos_pairs_v1.json`
   - `juan_combos_pairs_v1.review.txt`
4. `docs/` must contain the design docs v3/v4/v5, the developer manual,
   this file, and `CHANGELOG.md`.

---

## Step 1 - Juan Combos data build

Goal: the pairwise table artifact is built from the source markdown, all
four quality gates pass, and the artifact matches its gate tests.

1. Rebuild and verify the gates:

       python scripts/build_juan_combos_table.py --built-on YYYY-MM-DD

   Expected output: `Gates G1-G4 all passed.` with `events_total=40`,
   `events_with_pairs=37`, `events_marked_none=3`, `pairs_total=1384`,
   `source_notes: 5 excluded, 1 merged`.

2. Determinism: run the same command again and confirm the JSON is
   byte-identical (e.g. `git diff --stat compendium_reference/` shows no
   changes; or compare SHA-256 of `juan_combos_pairs_v1.json`).

3. Gate tests over the committed artifact:

       $env:PYTHONPATH = "<repo>\src"; python -m pytest tests/test_juan_combos_data.py -q

   Expected: 12 passed.

4. Open `compendium_reference/juan_combos_pairs_v1.review.txt` and review:
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
5. After review, sign off: edit `compendium_reference/juan_combos_pairs_v1.json`
   and set `_meta.reviewed_by` and `_meta.reviewed_on`. Re-run
   `tests/test_juan_combos_data.py` - the sign-off test (`test_meta_self_consistency`)
   will now fail until updated; that is the expected trigger to update the
   test to pin the signed review.

---

## Step 2 - Compendium lookup module

Goal: `src/topo_astro/significators/compendium.py` exposes the artifact to
the pipeline: symbol name mapping, EventType -> title, tier lookup, pair
strength lookup.

1. `$env:PYTHONPATH = "<repo>\src"; python -m pytest tests/test_compendium_lookup.py -q`
   - Expected: all pass.
2. Manual spot checks (python -c or REPL):
   - `event_title_for(EventType.ARREST)` returns the exact JSON title;
     every EventType with data in the compendium round-trips.
   - `event_title_for(...)` returns `None` for the 11 no-data EventTypes
     (no crash, no silent default).
   - `tier_score(title, "MARS")` style calls return only
     `"strong" / "weak" / "excluded"` (or the documented None semantics).
   - `pair_strength(event_title, point_a, point_b)` returns the same
     result for `(A, B)` and `(B, A)` (unordered).
   - Unlisted pair returns the documented no-data result (`None`), never
     a guessed tier.
   - Spot values against the review file: Birth of Brother
     MARS:POF -> excluded; Success or Elected MOON:NODE_ANY -> strong.
3. Confirm the module never imports the builder script and never reads
   the markdown at runtime (artifact-only).

---

## Step 3 - Configuration module

Goal: every business knob lives in `src/topo_astro/batch/pssr_window_config.py`.

1. `python -m pytest tests/test_pssr_window_config.py -q` - all pass.
2. Read `pssr_window_config.py` and check each knob against v5 section 6:
   every value is a named constant with a comment stating its source
   (spec section or source book); no tunable value is hard-coded inside
   `pssr_window.py` or the pipeline logic.
3. Manual: `python -c "import topo_astro.batch.pssr_window_config as c; print(c.PSSR_WINDOW_FULL_MINUTES, c.ORB_BOOST, ...)"`
   - Values print without errors and match the documented ranges.
4. Confirm no orphan knobs: every config constant is referenced somewhere
   in the pipeline (grep), and every pipeline decision uses a config knob.

---

## Step 4 - Planetary speed calculation

Goal: `calc_planets_labelled_speeds` in `src/topo_astro/core/constants.py`
returns labelled per-planet daily speeds consistent with the existing
`calc_planets`.

1. `python -m pytest tests/test_core_constants.py -q` - all pass.
2. Manual cross-check with a real birth chart:

       python -c "import topo_astro.core.constants as c; s = c.calc_planets_labelled_speeds(...)"

   - Keys are the labelled planet names (e.g. `MERCURY`), values are
     floats in degrees/day.
   - Every planet present in `calc_planets` output has the same speed
     value as the new labelled version (call both on the same birth data
     and compare numerically).
   - Moon's speed is the largest positive value; a station-retrograde
     planet (if any in the test chart) shows a near-zero value.
3. Regression: full suite still green.

---

## Step 5 - PSSR technique speeds and orbs

Goal: `PSSR_Auto` gains the additive `return_speeds=False` keyword
(exposing the four progressed position sets' per-point speeds) and the
orb literals move into named constants, with NO behavior change by
default.

1. `python -m pytest tests/test_pssr_return_speeds.py -q` (or the
   corresponding test module) - all pass.
2. Backward-compatibility check - the critical one:

       python -c "import json; from topo_astro.techniques.pssr import PSSR_Auto; ..."

   Run `PSSR_Auto` with a real birth/event pair TWICE: once with the
   previous (default) call and once with `return_speeds=False`. The two
   `dict_info` outputs must be byte-identical.
3. With `return_speeds=True`, `dict_info` additionally contains the four
   keys (prog direct, regressive direct, progressive converse,
   regressive converse speeds), each mapping every progressed point to a
   speed; cross-check one or two values against
   `calc_planets_labelled_speeds` on the same dates.
4. Open `src/topo_astro/core/aspects.py`: `find_pssr_swiss_aspects` now
   uses `PSSR_PLANET_ORB_DEG` (12') / `PSSR_MOON_ORB_DEG` (18') /
   `PSSR_MOON_CONJ_OPP_ORB_DEG` (32') instead of inline literals, with
   the book citation (p.108) as the constant comment. No orb VALUE
   changed.
5. Full suite: `python -m pytest tests/ -q` - all pass (count grows by
   the new tests).

---

## Step 6 - Narrowing pipeline

Goal: `src/topo_astro/batch/pssr_window.py` implements Stage 0, Stage 1
(narrowing) and Stage 2 (consensus / fail-open) per v5 section 3.

1. `python -m pytest tests/test_pssr_window_pipeline.py -q` - all pass.
2. Targeted behavior checks (the tests assert these; re-read them to
   confirm they cover the contract):
   - Stage 0: no narrowing when the config disables narrowing, when
     birth time is unknown, when there are too few matches, or when
     matches are ambiguous - the window stays at the full PSSR range.
   - Stage 1: only strong-tier pair matches can narrow; `weak` matches
     only affect narrowing when the config enables them; `excluded`
     never narrows.
   - No fast-to-fast aspects in Stage 1 (per spec constraint).
   - The true birth time is never silently excluded: if the pipeline's
     chosen window would exclude it, the window is widened or the
     event is flagged, never silently dropped.
   - `None` vs zero are preserved distinctly (an absent match is not a
     zero-score match).
   - Fail-open: on any internal error the window remains the full range,
     the error is surfaced (logged / flagged), and the pipeline returns
     rather than raising.
3. Manual run on one small real case: pick a data_input event with a 24h
   window, run the pipeline, confirm the output lists the stages and the
   final narrowed range, and confirm the narrowed range is a strict
   subset of the full range (or is flagged as unchanged).
4. Full suite green.

---

## Step 7 - Real-data end-to-end + docs sweep

Goal: the pipeline runs over real data files and the design docs contain
no unimplemented requirements.

1. End-to-end on the Step 7 candidates
   (`data/data_input/`): `hussein.json`, `jacqui onassis.json`,
   `john lennon.json`, `ing tea prim.json`, `mae.json`,
   `margaret millard.json`.
   For each: the pipeline completes without raising, produces a window
   per event, and every narrowed window is a strict subset of the full
   range. Document the per-person results (windows before/after) in the
   changelog entry for Step 7.
2. Sanity: for at least one person, the known/first-listed event's true
   date lies inside the pipeline's window (fail-open checks).
3. Docs sweep - grep the design docs v3/v4/v5 for every requirement
   (section 5 build list and section 7 checklists) and confirm each is
   implemented or explicitly logged as not implemented in the changelog.
   Anything silently skipped is a defect.
4. Full suite green.

---

## Step 8 - Ranges documentation artifact

Goal: the ranges (orb / speed) values are documented with source
citations, and the config + constants match that documentation.

1. The ranges doc artifact exists (e.g.
   `docs/pssr_ranges_v1.md` or the path named in v5 section 8) and
   contains:
   - The orb ranges with the source book citations (p.108: 12' planets,
     18' Moon, 32' Moon conjunctions/oppositions; p.108: orbs only
     reliable with an exact/rectified birth time).
   - The daily-motion speed range with citation (p.117: 30'-35' per day).
   - Sun / Part of Fortune receptive-only note (p.109).
2. Cross-check: `PSSR_PLANET_ORB_DEG` == 12/60, `PSSR_MOON_ORB_DEG` ==
   18/60, `PSSR_MOON_CONJ_OPP_ORB_DEG` == 32/60, and the config's speed
   range == 30'-35' per day.
3. Full suite green.

---

## Final acceptance

1. `$env:PYTHONPATH = "<repo>\src"; python -m pytest tests/ -q` - all
   pass (count >= 164 + tests added by steps 2-8).
2. `docs/CHANGELOG.md` contains an entry for every step.
3. `compendium_reference/juan_combos_pairs_v1.json` is signed off
   (`_meta.reviewed_by` / `_meta.reviewed_on` set).
4. `git status` shows only intended files.
5. Every item in this checklist is ticked with the actual result.
