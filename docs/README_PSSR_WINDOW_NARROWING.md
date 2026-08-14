# PSSR Window Narrowing - README

Narrow a candidate birth-time window (typically the 24 h around a
recorded birth date) to the hour-scale range where the Primary
Solar/Secondary Return (PSSR) technique is most consistent with the
person's recorded life events, using the compendium-derived
event-significator pair table.

Implemented per the design contract in
[`docs/pssr_window_narrowing_design_v5.md`](pssr_window_narrowing_design_v5.md)
(the v5 doc, section-referenced throughout the code and below). The
design went through review passes (v1-v5); the v5 doc supersedes the
earlier drafts (v3/v4 are kept for the record in `docs/`).

---

## Overview

A recorded birth time may be off by hours. This feature answers:
"within the candidate window, which range makes the PSSR progressed
positions form the strongest, most relevant set of aspects to the
radical chart, across the person's recorded events?"

Pipeline (one candidate time point at a time):

1. Compute the four PSSR progressed position sets (direct/converse x
   regular/regressive) and per-point daily speeds
   (`PSSR_Auto(..., return_speeds=True)`, spec section 5.3).
2. Stage 1: for every event in the chart, find progressed-to-radix
   aspect in-orb hits between a **fast** progressed point and a
   **slow** radix point, gated by relevance (compendium) and speed
   (section 5.6).
3. Stage 2: fast-progressed-to-fast-radix hits between known major
   aspects, with Moon/arm orb rules (section 5.7).
4. Aggregate all events over the whole candidate window into
   aspect-tuple intervals; coarse pass (consensus over events) ->
   fine pass (consensus over aspect tuples) -> margin -> final window
   (sections 5.8-5.10).
5. Fail-open: any internal error returns the full input window with
   tier `none` and the error surfaced; a narrowed window is never
   silently produced from broken data.

## Files in this feature

### Source

| File | What it does |
|---|---|
| `src/topo_astro/significators/compendium.py` | Loads `compendium_reference/juan_combos_pairs_v1.json`; `event_title_for` (EventType -> title), `tier_score` (tier -> int: strong=8, weak=6, excluded=2, absent=None), `pair_strength` (unordered event-point-pair lookup -> strong/weak/excluded/None), `SYMBOL_MAP_NAMED` (symbols -> named points, incl. H1->ASC, H4->IC, H7->DESC, H10->MC, per v5 section 4.3), `normalize_title` (Unicode normalization). `Compendium.load()`; `compendium=None` switches the pipeline to kinematics-only mode (relevance open at "strong", tier 10). |
| `src/topo_astro/batch/pssr_window_config.py` | All tunable knobs (section 6.2). `ASPECT_CLASSES`, `ORB_FAST_SLOW_DEG`, `ORB_MOON_CONJ_OPP_DEG`, `ORB_MOON_GENERAL_ARC_MIN`, `SPEED_FLOOR_ARC_MIN_PER_DAY`, `SPEED_FLOOR_USE_ABSOLUTE`, `FAST_SET`/`SLOW_SET`/`FAST_FAST_SET`/`MOON`, `PAIR_RELEVANCE_MIN`, `SAFETY_MARGIN_MINUTES`, `SINGLE_EVENT_FINE_RANGE_MINUTES`, `MAX_ASPECTS_PER_EVENT`, `CONSENSUS_MAX_CARDINALITY`, `CONSENSUS_TIE_BREAK`, `STEP_SECONDS`, `COARSE_PASS_PREFILTER`, `COARSE_STEP_SECONDS`. Orb constants are imported **by reference** from `core/aspects.py` (identity `is` check; values cannot drift). |
| `src/topo_astro/batch/pssr_window.py` | The pipeline (section 3): `sweep_jds` (JD points over the window), `stage1_hits` / `stage2_hits` (per-point hit evaluation with relevance + speed gates), `evaluate_point`, `collect_event_hits` (per-event interval collection), `coarse_pass` / `fine_pass` (two-pass consensus), `_select_final_window` (tier + margin), `narrow_birth_time_window` (entry point, fail-open wrapper). Returns the `PSSRWindowReport` dict (schema in the v5 doc section 3.10). |
| `src/topo_astro/core/constants.py` | Added `calc_planets_labelled_speeds` (section 5.4): daily speeds (deg/day) alongside labelled positions. |
| `src/topo_astro/core/aspects.py` | Named PSSR orb constants `PSSR_PLANET_ORB_DEG` (= 12/60, fast-to-slow) and `PSSR_MOON_ORB_DEG` (= 32/60, Moon conj/opp), replacing the previously-inline literals in `find_pssr_swiss_aspects` (section 5.5). Values unchanged; extraction is byte-identical. |
| `src/topo_astro/techniques/pssr.py` | `PSSR_Auto` gains keyword-only `return_speeds` (default `False`); when set, `dict_info` additionally carries `prog_dir_speeds` / `reg_dir_speeds` / `prog_conv_speeds` / `reg_conv_speeds` (deg/day, Sun excluded, Moon included). Default output is byte-identical to before. |

### Build and data

| File | What it does |
|---|---|
| `scripts/build_juan_combos_table.py` | Rebuilds `compendium_reference/juan_combos_pairs_v1.json` (+ `.review.txt`) from `Event Astrology a Compendium of Aspects.md` and `compendium_scoring_export_v2.json`. Runs gates G1-G4. **By design it emits the artifact unsigned** (`_meta.reviewed_by/reviewed_on: null`) - sign off manually after the final build. |
| `compendium_reference/juan_combos_pairs_v1.json` | The event-significator pair table (signed off 2026-08-14): per-event strong/weak/excluded pairs with wording, `inherited_from` for shared "Positive Travel" pairs, merged duplicates (MOON:NODE_ANY), 3 marked-none events, 5 source-note exclusions. |
| `compendium_reference/juan_combos_pairs_v1.review.txt` | Human-review aid: excluded/weak wordings, source-note exclusions, merged duplicates, per-event counts (40 events / 37 with pairs / 3 marked-none / 1384 pairs; strong 1178, weak 158, excluded 48). |

### Tests

| File | What it covers |
|---|---|
| `tests/test_compendium_lookup.py` (21) | EventType resolution, tier/pair lookups, fail-closed behavior, symbol map. |
| `tests/test_juan_combos_data.py` (12) | Gate tests over the signed artifact + `test_meta_self_consistency` (pins the sign-off). |
| `tests/test_pssr_plumbing.py` (12) | `return_speeds` backward-compat (byte-identical), speed keys, `calc_planets_labelled_speeds` vs positions. |
| `tests/test_pssr_window_config.py` (9) | Config knobs, drift guards (identity imports vs `core/aspects.py` / `core/constants.py`). |
| `tests/test_pssr_window.py` (49) | Steps 4-7: sweep, stage 1/2 rules, orb/speed boundaries, relevance wiring, real sweeps, coarse/fine consensus, tiers, margins, fail-open, end-to-end. |
| `tests/test_core_constants.py`, `tests/test_core_aspects.py` | Regression guards for the extraction changes. |

## Usage

### Entry point

```python
from datetime import datetime, timedelta
from topo_astro.batch.pssr_window import narrow_birth_time_window
from topo_astro.significators.compendium import Compendium
from topo_astro.significators.rules_data import EventType

report = narrow_birth_time_window(
    dt_radix_start=datetime(1969, 6, 27, 0, 0),          # candidate window
    dt_radix_end=datetime(1969, 6, 27, 0, 0) + timedelta(hours=24),
    dt_actual_dob=datetime(1969, 6, 27, 12, 0),           # recorded DOB
    geopos_natal=[51.5, -0.12, 0],                        # [lat, lon, alt]
    events=[
        {"datetime": datetime(1985, 4, 12, 10, 30),
         "event_type": EventType.SUCCESS_ELECTED},
    ],
    compendium=Compendium.load(),                         # or None for kinematics mode
)
```

`config` defaults to the resolved `pssr_window_config` module; any object
exposing the same constants works (tests pass a small override
namespace). `compendium=None` runs without relevance data (relevance
open at "strong", tier 10).

Events are dicts with a `datetime` **instance** (a string will raise -
`julian.to_jd` needs a real datetime; when loading the JSON birth-data
format, parse with `datetime.fromisoformat`) and an `event_type` integer
constant from `topo_astro.significators.rules_data` (`EventType`, ids
1-51). The JSON/CSV birth-data format used by the batch tooling stores
them by name (e.g. `"SUCCESS_ELECTED"`), resolvable with
`getattr(EventType, name)`. Per-event geopos is not consumed by the
pipeline (only `geopos_natal` is). Speeds in the report are in deg/day.

Report highlights: `tier` (`usable` / `single_event` / `weak` / `none`),
`tier_reason`, `final_window_jd` + `final_window_pre_margin_jd`,
`coarse`/`fine` consensus sections (window, corroboration over
events-with-data, `subset_members`, `dropped_events`), `events` (per-event
hits with stage/arm/variant, aspect, separation, interval, relevance
source+wording, progressed/radix speeds), `near_miss_ledger`
(kinds: `absent_relevance`, `excluded_relevance`, `weak_relevance`,
`tier_below_floor`, `speed_below_floor`, `minor_aspect`,
`fine_outside_coarse`), `signed_distance_from_window_minutes`,
`parameters`, `errors` (empty on success).

### Rebuild the compendium artifact

```powershell
python scripts/build_juan_combos_table.py --built-on yyyy-mm-dd
```

then review `.review.txt`, sign off `_meta` in the JSON, and update
`test_meta_self_consistency` to pin the new values. The builder resets
the sign-off on every rebuild - that is by design.

### Tests

```powershell
$env:PYTHONPATH = "<repo>\src"
python -m pytest tests/ -q                    # full suite: 255 passed
python -m pytest tests/test_pssr_window.py -q # feature suite (49)
```

Scripts that import `tests/fixtures` additionally need the repo root on
the path: `$env:PYTHONPATH = "<repo>\src;<repo>"`.

## Validation

- Full suite: 255 passed (152 baseline + 103 added across the feature).
- Manual verification executed 2026-08-14 against
  [`docs/MANUAL_VERIFY_PSSR.md`](MANUAL_VERIFY_PSSR.md) - ALL CHECKS
  PASS, 0 defects (outcome section appended to that file).
- End-to-end (6 people, 24 h sweep, defaults): all runs produce an
  hour-scale `usable` window strictly inside the input, zero errors;
  results table in the CHANGELOG Step 7 entry and the verification
  outcome.
- Sensitivity analysis (hussein, coarse pass, one knob at a time):
  tier stays `usable` and coarse corroboration 11/16 across all tested
  settings; fine corroboration 14-16; width is linear in
  `SAFETY_MARGIN_MINUTES` (36/66/126 = pre-margin ~6 min + 2 x margin);
  the other knobs move width only within 66-75 min. Defaults unchanged.
- Coarse-pass prefilter equivalence: with `COARSE_PASS_PREFILTER=True`,
  the final window reproduces the full fine sweep exactly (0.000000 s
  edge difference, same tier/consensus/corroboration) at ~5x speed.

## Known quirks and data notes (by design, not defects)

- "Child's Marriage" has a curly apostrophe (U+2019) in
  `compendium_scoring_export_v2.json` vs a straight apostrophe in the
  markdown; `normalize_title` bridges it and all 18 pairs resolve.
- `find_pssr_swiss_aspects` (unused by the narrowing pipeline) keys its
  wide orb on the second point set only (`p2 == 'Moon'`); the pipeline
  implements its own symmetric orb rules.
- House cusps, Sun, and POF are excluded as progressed targets (v5
  sections 5.2/D7/D9) - excluded from hits, not from relevance data.
- Timings are machine-dependent; the coarse-pass equivalence (0.0 s edge
  difference) is the pinned invariant, not wall-clock.

## Further research

From the v5 doc §9 future-research register (kept in sync by the
pipeline's module docstring), §10 flagged items, and codebase
observations. See also the CHANGELOG Step entries for calibration notes.

### v5 §9 register (explicitly not included; the standing next-evolution list)

1. **Houses and angles** (all 12 cusps incl. ASC/MC/DS/IC) - excluded
   everywhere by owner decision (D7): house evidence becomes trustworthy
   only once the time is narrowed, so it is the verification/confirmation
   step, not the discovery step. Future exploration in order:
   (a) house-cusp-based verification of a narrowed window, (b)
   fast-planet-to-house aspects as expanding/verifying evidence, and the
   recorded "Moon in conjunction with an angle is especially effective"
   line (Moon-to-angle fine-tuning). The compendium data is retained and
   mapped (§4.3) - no data rebuild needed.
2. **Sun and Part of Fortune as targets** - receptive-only factors
   (book §1.6); no stage admits them (D9). Their pairs exist in the
   table regardless; admitting them later is a config change, not a
   rebuild.
3. **Weak-relevance pairs as gating evidence** - `weak` never produces
   ranges (D3), only near-miss ledger entries. Revisit as expanding
   evidence if corroboration proves too sparse.
4. **Minor aspects** - majors only (F16); minors recorded in the
   ledger. Optional support-channel scoring is a config change.
5. **PSSR 2 (progressed-to-progressed)** - excluded per the source's
   own verdict that radix aspects are more accurate; the hit/interval/
   report machinery is variant-agnostic and would extend.
6. **Epoch-chart PSSR, the Dual Test, Mercury/Venus-return variants** -
   book-adjacent material, not needed for narrowing.
7. **Timezone/LMT/DST refinement** - excluded (D10); the inherited
   Phase-2 caveat (modern DST applied to historical dates) applies to
   this pipeline. A dedicated timezone-correctness effort across the
   codebase is deliberately not scoped here.

### v5 §10 flagged items (verify during implementation; none blocked the build)

- **18' Moon orb** - a genuinely new value (book p. 108, "32' in
  conjunctions and oppositions"); confirmed by the Step 7 sensitivity
  analysis (ORB_MOON_GENERAL_ARC_MIN 16/18/20 -> 75/66/74 min, tier
  usable throughout).
- **30'/day speed floor pick** (D1) - confirmed by sensitivity
  (SPEED_FLOOR_ARC_MIN_PER_DAY 25/30/35 -> 66/66/75 min).
- **Fast-to-fast "both points clear the floor" extrapolation** (D2) -
  kept as the right default; never credits a hit where a nominally-fast
  point is stalled.
- **Max-cardinality partial-consensus fallback** - a design decision,
  fully tested; its outcome is always visible in the report (which
  events were dropped).
- **`compendium_reference/` tracking** (F13) - committed in Step 0.
- **Book verification pass** (p. 108 orb / p. 117 speed-gate quotes) -
  deferred; the spec's orbs, tiers, and floors are pinned to those exact
  quotes and the sensitivity runs corroborate the values.

### Codebase observations (this implementation)

- **`COARSE_PASS_PREFILTER` for very long windows** (e.g. multi-
  thousand-hour spans like `data/data_input/ing tea prim.json`):
  validated equivalent (0.0 s window-edge difference), ~5x faster here;
  consider it when fine sweeps get expensive.
- **`find_pssr_swiss_aspects` p2-keyed orb asymmetry** (wide orb only
  when the Moon is in the second point set): pre-existing, unused by the
  narrowing pipeline; candidate for a future refactor to symmetric orbs
  now that the constants are shared.
- **CLI/entrypoint** (Phase 10 of the batch-tooling migration):
  `narrow_birth_time_window` is callable directly; a command-line
  wrapper over `data/data_input/*.json` birth files is future work.