# PSSR Window-Narrowing — Final Implementation Plan (v4)

note v1-3 are not committed to this codebase - v4 is the first substantial plan worth tracking

**Purpose:** Final, executable specification for Step 0 of the rectification framework — narrowing an uncertain birth-time window (typically 24 hours) using the Precessed Solar Return technique, before POLARIS and Primary Directions take over the fine search.

**Status:** Spec only. This document is the implementation contract. It supersedes `pssr_window_narrowing_design.md` (v3); every item v3 left open is resolved here in §8. No implementation has been done yet.

**Source grounding:** v3's technique analysis (book page numbers, quotes, worked examples) is adopted wholesale and not re-argued here. This document adds (a) a verification pass against the *actual current codebase*, (b) resolutions for all five open items, (c) three corrections to v3's assumptions that the codebase check surfaced, and (d) the full work breakdown, data-build procedure, and acceptance criteria.

**How to use this document:** It is written to be handed to an implementation agent (or future you) as-is. §3 is the algorithm contract. §4 is the data-build contract. §5 is the file-level build list. §7 is the ordered execution plan with validation checklists. §8 is the decision log. §9 is the short list of items that could not be resolved from available material and must be verified against the source book during implementation — none of them blocks the build.

---

## 1. Goal and non-goals

**Goal.** Given a person's uncertain birth-time window (`dt_radix_start` … `dt_radix_end`, from their `data_input/*.json`), their natal geopos, and their dated, categorized life events, produce a **narrowed sub-window** of birth times whose PSSR charts best corroborate those events per Estadella's method — with the hard guarantee that the returned window never silently excludes the true birth time (the one failure mode worse than a slow search).

**Non-goals (deliberately out of scope):**
- No scoring of *how good* a birth time is in the abstract. Output is a window, not a ranked list.
- No PSSR 2 (progressed-to-progressed aspects) — excluded by the source (§1.13 of v3).
- No Epoch/Dual-Test, no Mercury/Venus-return variants, no harmonics readings (§1.14 of v3).
- No change to the existing `PSSR_Auto` behavior for its current callers. Everything added is opt-in.
- No timezone work. The pipeline operates in the same naive-datetime frame the entire codebase already uses (see §9 item 7).

**Why this narrows, quantitatively (the mechanism the whole plan rests on).** Sweeping the candidate birth time `t` across the window, the PSSR aspect that matters for rectification is the one between a *progressed return-chart factor* and a *radix factor*. As `t` moves:
- The radix chart is re-erected at `t`; its **angles sweep ~15°/hour** (the dominant mover for any angle/house target).
- The progressed positions move at their **ephemeris rate compounded through the 1-day-per-year shift** of the return moment (progressed Moon ~13°/day of candidate time, Mercury/Venus/Mars ~1–2°/day).
- Net relative rates therefore range from ~2°/day (slow-to-slow is structurally absent; stage-1 planet pairs are ~1.5–3°/day) to ~15°/day (Moon vs angle).

Against the technique's orbs (§3.4), this yields in-orb episodes of roughly: **stage 1: 4–10 hours** per qualifying hit; **stage 2 (Moon): ~1–1.5 hours** per qualifying hit. Intersecting the per-event contributions across several events collapses those to the shape Estadella reports: hours-wide after the planet stage, tens of minutes after the Moon stage. That is the entire narrowing mechanism: **orb width ÷ relative daily motion, per event, intersected across events.**

---

## 2. Verified facts about the current codebase (checked July 2026 state)

These were verified directly against the source tree during this review. The spec is built on them; do not re-derive them.

| # | Fact | Evidence |
|---|---|---|
| F1 | The `src/topo_astro/` package layout exists (Phases 4–8 of the migration are largely committed: package move, significator extraction, dispatcher, blueprint split, state removal). Phase 9 (structured `Aspect` codec) is **not** done — aspect strings are still the lingua franca. | `git log --oneline -15`; tree listing. |
| F2 | `PSSR_Auto(dt_radix, dt_event, rad_planets=None, geopos=None)` computes everything the pipeline needs except speeds: the two return moments (`swe.solcross_ut`), the four progressed/regressed dates (1 day = 1 year via `timelapse = timedelta(hours=jd_diff / 15.218425)`), the four progressed position sets (Sun excluded), and the aspect strings. Its `get_dict_info()` already exposes the return dates and `jd_diff_pssr_event` internals. | `src/topo_astro/techniques/pssr.py`. |
| F3 | **The speed question v3 left open is resolved: `swe.calc_ut()` already computes daily longitude speed — it is discarded at every call site.** Every position in the pipeline comes from `swe.calc_ut(jd, planet)` returning a 6-element array; index `[3]` is longitude speed in degrees/day (pyswisseph always populates it). The code stores `xx[0]` only (`xx, _ = swe.calc_ut(...)`). The "additive speed return" is therefore tiny plumbing, not new astronomy. | `src/topo_astro/core/constants.py:107,121,137`; `pyswisseph` API. |
| F4 | The existing PSSR aspect finder does **not** match the narrowing spec and must not be reused as-is: `find_pssr_swiss_aspects` applies a flat 32′ orb to the Moon and 12′ to all others **regardless of aspect type**, and evaluates **all nine** aspect types. The narrowing spec (§3.4) requires 18′ for Moon non-conjunction/opposition and **majors only**. | `src/topo_astro/core/aspects.py:194–219` (`orb = 32/60` if Moon else `12/60`; `calculate_aspect(d1, d2, orb, False)`). |
| F5 | `calc_planets_pof_houses_labelled` returns planets + POF + houses **H1–H11 only** (the loop is `range(0,11)` — H12 is dropped). This is a pre-existing quirk. The pipeline will compute its own complete 12-cusp set via `swe.houses` anyway (it needs per-candidate natal houses); do **not** modify the shared helper. | `src/topo_astro/core/constants.py:132–152`. |
| F6 | The radix chart is **re-erected at every candidate time** `t` in the sweep: `rad_planets(t) = calc_planets_pof_houses_labelled(jd(t), geopos_natal)`, and the PSSR return targets are the *natal Sun at `t`* plus precession. This corrects v3's asymmetry note: natal-side speeds are per-candidate, not once-per-person (the natal chart moves with the candidate). | F2 + design math in §1. |
| F7 | `construct_technique(TechniqueType.PSSR, ...)` constructs `PSSR_Auto(dt_radix, dt_event, rad_planets)` — no geopos threaded (natal geopos only used by `PSSR_Auto` when `rad_planets is None`, which the call sites never allow). Consistent with v3 §1.4 (returns erected at birth coordinates). | `src/topo_astro/techniques/base.py:230–235`. |
| F8 | `FAST_TO_SLOW_COMBO` in the scoring engine **includes the Moon in the fast set** (`[MAR, MER, VEN, MON]` vs `[JUP, SAT, URA, NEP, PLU, NNO]`). v3 §1.8's correction stands: the narrowing pipeline defines its **own** fast/slow constants with Moon excluded — the existing `AspectType` branch is not reused for this feature. `MOON_ANGLE_HOUSE_PRIMARY` exists but is also not reused directly; both remain untouched for their existing callers. | `src/topo_astro/significators/scoring.py:241–253`. |
| F9 | `generate_grid_angular_aspects(filename, start_time, end_time, increment_seconds, ...)` already supports parameterized stepping — the pattern exists, but the new pipeline does **not** reuse it (it needs per-point structured data, not grid-file rows). | `src/topo_astro/batch/grid_engine.py:119`. |
| F10 | **There is no compendium loader anywhere.** v3's phrase "alongside wherever the existing Compendium loader/lookup lives (`significators/compendium.py`)" presumes a module that does not exist. `significators/` contains only `rules_data.py` and `scoring.py`. `compendium.py` is genuinely new. | Tree listing of `src/topo_astro/significators/`. |
| F11 | `compendium_scoring_export_v2.json` (the tier data) has 40 events, each with per-symbol `tier_score` (0/1/2 per source, tier 0–10), `sample_sizes`, and structural-scope nulls. Symbol roster: 10 planets + `NODE_ANY`, `POF`, `ASC/MC/DESC/IC`, minor houses `H2/H3/H5/H6/H8/H9/H11/H12`. Saturn/Neptune are present for most events but **absent as keys for some events — an absent key means "no data", not 0**, and lookups must fail closed. | `compendium_reference/compendium_scoring_export_v2.json`. |
| F12 | The raw compendium (`Event Astrology a Compendium of Aspects.md`) contains "Astrological Combinations (Estadella)" sections for **all 40 events**, but with format hazards: "Birth of Brother" is the first section and has **no markdown heading at all**; "Birth of Sister" is `##` while the rest are `#`; "Positive Travel Overseas" is a cross-reference section `(See Positive Travel)`; three events (Demobilization or Release, Assasination or Suicide, Gambling Loss) are marked `juan_combos_marked_none`/`total=0` in the JSON — exactly v3 §1.11's three. Bullet format is uniform: `- **A-B / B-A**: prose`. | `compendium_reference/Event Astrology a Compendium of Aspects.md`; JSON `sample_sizes`. |
| F13 | **`compendium_reference/` is currently untracked in git** (as are `docs/`). The compendium assets the pipeline depends on must be committed before implementation starts. | `git status --short`. |
| F14 | The Phase 2 characterization suite exists (153 tests, golden-file based) and is the regression gate every change in §7 must pass, with the PSSR technique's byte-identical output included (`tests/test_techniques_golden.py`). | `docs/phase2_README.md`; `tests/`. |
| F15 | `PLANETS` is the 10 planets + `'Mean_Node'`. The codebase's node label is `Mean_Node`; the compendium's is `NODE_ANY` (node, pole unspecified). The symbol-mapping layer (§4.3) is required. | `src/topo_astro/core/constants.py:38–41`. |

---

## 3. The algorithm contract

### 3.1 Inputs and outputs

```
narrow_birth_time_window(
    dt_radix_start: datetime,        # window start (from data_input JSON)
    dt_radix_end:   datetime,        # window end
    dt_actual_dob:  datetime,        # working-hypothesis birth time (reporting only)
    geopos_natal:   list[lat, lon, alt],
    events:         list[Event],     # each: datetime, event_type (EventType), geopos (unused by PSSR — §1.4)
    params:         NarrowParams,    # §6 table; defaults are the resolved values
) -> PSSRWindowReport
```

`PSSRWindowReport` (§3.11) must contain, at minimum: the final window (with and without margin), the confidence tier, the corroboration count, the per-event detail, the near-miss ledger, the parameters used, and where `dt_actual_dob` falls relative to the window.

### 3.2 The sweep

- Step `t` across `[dt_radix_start, dt_radix_end]` at `step_seconds = 60` (default), inclusive of both endpoints. The step size is safe: the fastest relative rate in the system (~15°/h, Moon vs angle) yields in-orb episodes ≥ ~1 hour — two orders of magnitude above the sampling floor.
- At each grid point `t`, per event `e`:
  1. Recompute the candidate radix once per grid point (shared across events): `rad(t) = calc_planets_pof_houses_labelled(jd(t), geopos_natal)` plus the per-point full house set via `swe.houses` (F5), plus **natal speeds** for all 11 points (F3).
  2. Construct `PSSR_Auto(dt_radix=t, dt_event=e.datetime, rad_planets=rad(t), return_speeds=True)` (§5.3) — one instance per (point, event). Read from `get_dict_info()`: the four progressed dates, and with the opt-in flag, the four progressed position sets **with speeds**.
  3. Evaluate the three stages (§3.5–3.7) against the candidate radix points.
- Per-grid-point cost ≈ 12 (natal) + 1 `swe.houses` + 2 `solcross` + 44 (4 × 11 progressed) ≈ 60 Swiss Ephemeris calls. At 1,440 points × 20 events ≈ **~1.7M calls ≈ tens of seconds to a few minutes** in batch — acceptable. (Optional coarse-pass pre-filter, 5-minute grid then 1-minute refinement inside surviving ranges, is a permitted optimization; the default is the single fine sweep, per v3 §3.4.)
- The four variants (direct/converse SSR × direct/converse progression) are all evaluated at every point and treated as equal-weight channels, per v3 §1.2. A hit carries its variant as provenance only.

### 3.3 Point sets and membership (resolved constants)

| Constant | Members | Notes |
|---|---|---|
| `FAST_SET` | Mercury, Venus, Mars | **Moon deliberately excluded** (v3 §1.8 correction, F8). |
| `SLOW_SET` | Jupiter, Saturn, Uranus, Neptune, Pluto, Mean_Node | The Lunar Node is in the slow/receptive group. |
| `MOON_SET` | Moon | Own factor, own stage. |
| `ANGLE_HOUSE_SET` | natal ASC (H1), IC (H4), DS (H7), MC (H10), and minor cusps H2,H3,H5,H6,H8,H9,H11,H12 | Full 12-cusp set computed per candidate (F5). Angle identity: **natal angles** — see §9 item 1 for the one verification checkpoint. |
| `PROGRESSED_SET` | Sun excluded; planets + Node progress (Moon included); POF and angles/houses **never** progress (v3 §1.3, §1.6) | Matches existing `PSSR_Auto` behavior (F2). |
| `RECEPTIVE_ONLY` | Sun, POF | Never progressed. **Neither is currently a target of any stage** — see §9 item 2 (flagged, not silently dropped). |

### 3.4 Aspect evaluation (orbs and aspect classes — resolved)

The pipeline implements its own aspect evaluation over raw degrees using the core primitive `calculate_aspect()` (`core/aspects.py`). It does **not** call `find_pssr_swiss_aspects` (F4).

| Rule | Value |
|---|---|
| Aspect classes | **Majors only**: conjunction, sextile, square, trine, opposition (v3 §1.8 — every aspect in both worked rectification examples is major; minors are recorded in the near-miss ledger, never gating). |
| Orb, no Moon party | **12′** flat, all point types (v3 §1.5). |
| Orb, Moon is a party | **18′** for non-conjunction/opposition; **32′** for conjunction and opposition (v3 §1.5 — a property of the Moon, uniform across all three stages). |

### 3.5 Stage 1 — the wide-range planet stage (fast → slow)

Membership and relevance per v3 §1.8–1.9, resolved:

- **Structure (Case A/B):** one point from `FAST_SET`, the other from `SLOW_SET`, either side may be the progressed/return factor or the radix factor.
- **Orb:** 12′ (no Moon can be involved by construction).
- **Aspect classes:** majors only.
- **Speed gate (hard pass/fail — resolved):** the single fast point's **absolute daily motion ≥ 30.0′/day** (book's lower bound; §8 D1). Measured on the side the fast point actually sits: progressed-side → ephemeris speed at its progressed date; radix-side → natal speed. Retrograde planets pass on `|speed|` — the rule is about magnitude of daily motion ("not found in slow movement"). A below-floor hit is **excluded from range-finding entirely**, recorded in the near-miss ledger with the actual speed (this ledger is the calibration instrument for the floor).
- **Relevance gate (resolved, v3 decision 1):** the unordered pair (fast point, slow point) must resolve to `strong` in the Juan Combos pairwise table (§4.1) for this event. `weak` → near-miss, no range. `excluded` or absent → no hit (see §4.1 for the tiers and the 3 no-data events).

### 3.6 Fast-to-fast stage (resolved, v3 decision 3)

- **Membership:** both points drawn from `{Mercury, Venus, Mars, Moon}`, one from each side (return/progressed vs radix), neither a slow planet, angle, or house cusp. This is the Venus–Moon class of pairing (Tyson's worked hit).
- **Orb:** 12′; 18′/32′ whenever the Moon is a party (§3.4 — Moon property, not stage property).
- **Speed gate (resolved):** **both** points must individually clear the 30.0′/day floor (§8 D2). The Moon clears it trivially (minimum ~11.7°/day) — no special-casing needed, but the gate is applied uniformly anyway for code simplicity.
- **Relevance gate:** same pairwise table, `strong` only (v3 §1.10a — Moon is on Estadella's 14-point roster like everything else).

### 3.7 Stage 2 — the Moon fine-tuning stage (resolved)

- **Membership:** progressed Moon vs one target from `{SLOW_SET} ∪ ANGLE_HOUSE_SET`. Moon vs fast planet is *not* here — that is §3.6. Moon vs Sun/POF is currently out of scope (§9 item 2).
- **Orb:** 18′ / 32′ conj-opp.
- **Aspect classes:** majors only.
- **Speed gate:** none — the Moon's minimum daily motion (~11.7°/day) is orders of magnitude above the floor, so the gate is mathematically vacuous for the only moving party. Stated explicitly so no one adds a redundant check.
- **Relevance gate (resolved, v3 §1.10/§1.11):** the non-Moon point's `tier_score` from `compendium_scoring_export_v2.json` for this event **≥ 6 (Moderate)**. Absent key → no data → fail closed (§8 D4).

### 3.8 Per-event range-finding

- A **qualifying hit** is a (variant, progressed point, radix point, aspect class) tuple that passes the applicable stage's membership + orb + speed + relevance gates at a given grid point. Distinct tuples are tracked separately; as `t` sweeps, each hit's in-orb times form one or more contiguous intervals (a pair can come into orb, leave it, and — near a mutual station — return; handle by collecting per-tuple interval sets, then merging overlaps).
- **Event contribution:** the union of all its qualifying hits' intervals. The event is counted **once** in the corroboration count no matter how many hits it has. This is the automated generalization of the book's "one representative aspect per event" (v3 §1.12): the book's single-aspect practice was about interpretation, not about intersection arithmetic — the union is the fail-safe choice (wider = less risk of silently excluding the true time). `max_aspects_per_event: "all" | 1` is a parameter; setting it to `1` reproduces the book's practice exactly (tie-break: the hit with the smallest orb at the center of its widest interval).
- **Events with no data:** events whose `EventType` maps to no compendium event (§4.2) or whose compendium event has `juan_combos_marked_none` (F12) can still contribute via stage 2 (tier data exists for all 40 events). Only if a stage-2 lookup also fails do they contribute nothing — and they are then reported explicitly (v3 §3.3), never silently absent.

### 3.9 Intersection across events

- **Full consensus:** the literal interval intersection of all corroborating events' contributions. 
- **Partial consensus (fallback, resolved):** if the full intersection is empty, compute the **maximum-cardinality subset of events whose contributions mutually intersect** and use that subset's intersection; report the subset vs. the dropped events. Ties broken by earliest window start.
- **No consensus:** if no subset of ≥ 2 events intersects, return the full input window with tier `none` and the full report (fail-open).
- Corroboration counting uses the number of events with ≥ 1 qualifying hit (independent of the subset logic).

### 3.10 Safety margin (resolved)

Expand the consensus window by **±30 minutes** on both ends (clamped to the input window). Rationale: one order of magnitude above the Moon-stage resolution (~1 h episodes and Estadella's 10–20-min final ranges) and above grid noise, and one order below typical stage-1 windows (hours), so it does not undo the narrowing. It exists to honor the governing rule — never silently exclude the true time — and is a named parameter.

### 3.11 Confidence tiers and reporting

| Corroborating events | Consensus | Pre-margin range | Tier |
|---|---|---|---|
| ≥ 2 | full | any | `usable` |
| ≥ 2 | partial | any | `usable` (partial-consensus flag set) |
| 1 | — | ≤ 60 min | `usable` (single-event fine) |
| 1 | — | > 60 min | `weak` |
| 0 | — | — | `none` (full window returned) |

The report must include, per event: contributing hits (stage, variant, points, aspect, interval, orb at interval center, relevance source + wording, speed values), near-misses ledger (weak-relevance, excluded-relevance, speed-below-floor with actual speeds, minor-aspect, no-data), and for the final window: tier, corroboration count / events-with-data count, margin applied, subset members if partial, and the signed distance of `dt_actual_dob` from the window.

---

## 4. Data assets

### 4.1 The Juan Combos pairwise table (new — the feature's only genuinely new data build)

**Location:** `compendium_reference/juan_combos_pairs_v1.json`, committed (F13).

**Schema:**

```json
{
  "_meta": {
    "source_file": "compendium_reference/Event Astrology a Compendium of Aspects.md",
    "builder": "scripts/build_juan_combos_table.py",
    "built_on": "<date>",
    "reviewed_by": "<human>", "reviewed_on": "<date>",
    "tiers": { "strong": "expected/frequent/always-type wording", "weak": "possible/sometimes/to-a-lesser-extent wording", "excluded": "only-exception-type hedging wording" },
    "events_total": 40, "events_with_pairs": 37, "events_marked_none": 3, "pairs_total": "<n>"
  },
  "events": {
    "Birth of Son": {
      "n_total": 45,
      "pairs": {
        "MARS:PLUTO": { "strength": "excluded", "wording": "The only occasional exception is the birth of children (gender_unspecified).", "aspects_hint": "", "inherited_from": null },
        "MERCURY:VENUS": { "strength": "strong", "wording": "The birth of children (gender_unspecified) is frequent.", "aspects_hint": "", "inherited_from": null }
      }
    }
  }
}
```

**Key rules:**
- Canonical key `A:B` = the two compendium symbol names **alphabetically sorted** (direction-free — the source's "A-B / B-A" pairs are one entry). Lookup is unordered.
- Point names normalized: `AS`→`ASC`, `Lunar Node`/`Node`→`NODE_ANY`, `Part of Fortune`→`POF`, planets→their compendium caps. A pair must fall inside the 14-point Juan Combos roster {ASC, MC, Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, NODE_ANY, POF} (the compendium's own structural scope — it never names DESC, IC, or minor cusps; a parser hit outside the roster is a hard build error, not a silent accept).
- **Strength tiers** (wording-cued, mirroring the "Other" source's existing methodology in the reference doc §3.2):
  - `strong` — expected/frequent-type positive attribution ("we always find", "frequent", "very common", "we find", "we often find", "the birth of X", plain positive statements).
  - `weak` — hedged or occasional ("occasionally", "sometimes", "to a lesser extent", "possible as well", "can occur", "may find").
  - `excluded` — "only exception" hedging ("the only occasional exception is", "the only exception is") — actively counter-indicative per v3 §1.11's analysis.
  - absent key = not catalogued for that event (no data). **`absent` ≠ `excluded`.**
- The `aspects_hint` field captures the parenthetical aspect-structure hints ("in conjunctions and harmonic aspects") as free text — recorded for future calibration, **not used** by the gate.
- Cross-reference sections: "Positive Travel Overseas" inherits "Positive Travel"'s pairs with `inherited_from: "Positive Travel"`.
- The three marked-none events (F12) get `pairs: {}` + an explicit `marked_none: true` in their entry.

**Build procedure (executed once, then reviewed — this is hand-curated research data, same care class as `rules_data.py`):**

1. `scripts/build_juan_combos_table.py` (new; `scripts/` created now, pre-Phase-10, purely additive).
2. Parse sections: the file is section-delimited by the known heading set (`KEY PLANETARY INDICATORS (STARKMAN)`, `Astrological Combinations (Estadella)`, `Summary of Astrological Signatures (Marr)`, `Historical Chart Examples (Marr & Starkman)`, `## Other`), with special handling for the headingless first section ("Birth of Brother") and the `(See Positive Travel)` cross-reference.
3. Parse bullets `- **A-B / B-A**: prose`, normalize names, code tiers by keyword rules, keep verbatim `wording`.
4. **Automated quality gates (must all pass before review):**
   - G1: parsed pair count per event == `sample_sizes.juan_combos_total_combinations` in `compendium_scoring_export_v2.json` for every event that has a section (the JSON's preserved totals are the cross-check — e.g. Birth of Brother = 45).
   - G2: zero parser hits outside the 14-point roster; zero unparseable bullets (each such failure is a hard error with the line number).
   - G3: no duplicate canonical keys within an event.
   - G4: every one of the 40 JSON events has an entry (pairs or marked_none).
5. **Manual review pass:** a human reviews the full coded output (the script emits a review file: event → pair → tier → wording), especially every `excluded`/`weak` assignment, and signs off in `_meta`.

### 4.2 EventType ↔ compendium-title mapping (needed before the pipeline can look up anything)

Full mapping, verified against both files:

| `EventType` | Compendium event |
|---|---|
| `BIRTH_BROTHER` | Birth of Brother |
| `BIRTH_SISTER` | Birth of Sister |
| `BIRTH_SON` | Birth of Son |
| `BIRTH_DAUGHTER` | Birth of Daughter |
| `BIRTH_GRANDSON` | Birth of Grandson |
| `BIRTH_GRANDDAUGHTER` | Birth of Granddaughter |
| `MARRIAGE_ENGAGEMENT_FOR_MALE` | Marriage for Male |
| `MARRIAGE_ENGAGEMENT_FOR_FEMALE` | Marriage for Female |
| `CHILDS_MARRIAGE` | Child's Marriage |
| `DIVORCE_SEPARATION` | Divorce or Separation |
| `DEATH_FATHER_GRAND` | Death of Father or Grandfather |
| `DEATH_MOTHER_GRAND` | Death of Mother or Grandmother |
| `DEATH_SON` | Death of Son |
| `DEATH_DAUGHTER` | Death of Daughter |
| `DEATH_WIFE_FRIEND` | Death of Wife or Female Friend |
| `DEATH_HUSBAND_FRIEND` | Death of Husband or Male Friend |
| `DEATH_BROTHER` | Death of Brother |
| `DEATH_SISTER` | Death of Sister |
| `DEATH` | Death |
| `ASSASINATION_SUICIDE` | Assasination or Suicide *(no Juan Combos data)* |
| `SUCCESS_ELECTED` | Success or Elected |
| `PROMOTION_JOB` | Job Promotion |
| `FAILURE_DEFEATED` | Failure or Defeat |
| `RESIGN_RETIRE` | Resign or Retire |
| `TRAVEL_OVERSEAS_POSITIVE` | Positive Travel Overseas *(inherits Positive Travel pairs)* |
| `TRAVEL_POSITIVE` | Positive Travel |
| `TRAVEL_NEGATIVE` | Negative Travel |
| `MOBILIZATION` | Mobilization |
| `DEMOBILIZATION_RELEASE` | Demobilization or Release *(no Juan Combos data)* |
| `ARREST` | Arrest |
| `ACCIDENT` | Accident |
| `HOSPITALIZATION_ILLNESS` | Hospitalization or Illness |
| `VIOLENCE` | Violence |
| `INTRIGUE` | Intrigue |
| `LOSSES` | Losses |
| `GAMBLING_LOSS` | Gambling Loss *(no Juan Combos data)* |
| `GAMBLING_GAIN` | Gambling Gain |
| `GRADUATION_PUBLICATION` | Graduation or Publication |
| `MOVE_HOME` | Move Home |
| `ARMY_PROMOTION` | Army Promotion |
| `POSITIVE_AC_MC`, `NEGATIVE_AC_MC`, `POSITIVE_2_8`, `NEGATIVE_2_8`, `POSITIVE_3_9`, `NEGATIVE_3_9`, `POSITIVE_5_11`, `NEGATIVE_5_11`, `POSITIVE_6_12`, `NEGATIVE_6_12`, `BLANK` | **no compendium event** — cannot contribute stage 1 or stage 2 by construction; reported as no-data. |

### 4.3 Symbol-name mapping (codebase ↔ compendium)

`Sun↔SUN, Moon↔MOON, Mercury↔MERCURY, Venus↔VENUS, Mars↔MARS, Jupiter↔JUPITER, Saturn↔SATURN, Uranus↔URANUS, Neptune↔NEPTUNE, Pluto↔PLUTO, Mean_Node↔NODE_ANY, POF↔POF, H1↔ASC, H4↔IC, H7↔DESC, H10↔MC`, minor cusps direct (`H2↔H2`, …). The codebase-side house labels come from the pipeline's own `swe.houses` output; `Mean_Node→NODE_ANY` is the one genuinely lossy mapping (codebase node pole unspecified — F15) and is stated as such.

---

## 5. Module plan

### 5.1 `src/topo_astro/significators/compendium.py` — NEW

The compendium data-access layer (F10 — nothing exists yet). Pure functions, no module-level mutable state (Phase 7 discipline). Responsibilities:
- Load `compendium_scoring_export_v2.json` and `juan_combos_pairs_v1.json` from a configurable base path (default resolves `compendium_reference/` relative to the package root; override parameter for tests).
- `event_title_for(event_id: int) -> str | None` — §4.2 mapping.
- `tier_score(event_id: int, symbol: str) -> int | None` — from the JSON; `None` for absent keys (no data), never synthesizes 0.
- `pair_strength(event_id: int, point_a: str, point_b: str) -> str | None` — from the pairwise table; returns `"strong" | "weak" | "excluded" | None` (None = absent), unordered canonical lookup.
- `SYMBOL_MAP_NAMED` — §4.3.

### 5.2 `scripts/build_juan_combos_table.py` — NEW

One-time data builder + review-file emitter + G1–G4 quality gates (§4.1). Outputs `compendium_reference/juan_combos_pairs_v1.json` and a human-review copy. Idempotent and deterministic.

### 5.3 `src/topo_astro/techniques/pssr.py` — MODIFIED, additive only

- New **keyword-only** constructor parameter `return_speeds=False`. When `True`, `calc_pssr_for_date` additionally computes and stores the four progressed position sets **with per-point daily speeds** (via the new helper below) and exposes them in `dict_info` under `prog_dir_speeds`, `reg_dir_speeds`, `prog_conv_speeds`, `reg_conv_speeds` (parallel lists to the existing position lists).
- Default `False` ⇒ all existing callers (dispatcher, GUI, batch, tests) see byte-identical behavior — verified by golden tests.
- **Do not** modify `get_str_aspects`, `get_dict_info` shape, `find_pssr_swiss_aspects`, or the return-year logic.

### 5.4 `src/topo_astro/core/constants.py` — MODIFIED, additive only

- New helper `calc_planets_labelled_speeds(jd, label)` — same loop as `calc_planets_labelled`, keeping `xx[3]` alongside `xx[0]` (F3). Existing `calc_planets_labelled` untouched.

### 5.5 `src/topo_astro/batch/pssr_window.py` — NEW

The orchestration module. Pure functions, no globals. Responsibilities per §3: the sweep (§3.2), the per-point stage evaluations (§3.5–3.7, using `calculate_aspect` from `core/aspects.py`), interval building and merging (§3.8), full/partial consensus and margin (§3.9–3.10), the report (§3.11). Exposes `narrow_birth_time_window(...)` per the batch convention (callable directly; no CLI until Phase 10 of the migration). Module docstring per §3.3 of the migration standard.

### 5.6 `compendium_reference/juan_combos_pairs_v1.json` — NEW data artifact (§4.1)

### 5.7 Tests — NEW

`tests/test_compendium_lookup.py` (mapping, tier lookup incl. absent-key fail-closed, pair lookup incl. unordered keys and inherited pairs); `tests/test_juan_combos_data.py` (G1–G4 re-run as tests over the committed artifact); `tests/test_pssr_window.py` (per §7 validation checklists; golden-file style per the Phase 2 conventions, including a regression test that `PSSR_Auto` with `return_speeds=False` is byte-identical to pre-change output).

---

## 6. Parameter table (all named constants, resolved values, and tuning notes)

| Parameter | Resolved value | Rationale / tuning note |
|---|---|---|
| `step_seconds` | 60 | §3.2; safe against the fastest relative rate. |
| `speed_floor_arcmin_per_day` | 30.0 | Book's range is 30–35′/day (v3 §1.9); lower bound chosen (D1). Calibrate via the near-miss ledger's recorded speeds. |
| `speed_floor_use_absolute` | true | Station/retrograde handled by magnitude. |
| `stage1_orb_arcmin` | 12.0 | §3.4. |
| `stage2_orb_moon_general_arcmin` | 18.0 | §3.4. |
| `stage2_orb_moon_conj_opp_arcmin` | 32.0 | §3.4. |
| `aspect_classes` | majors only | §3.4. |
| `pair_relevance_min` | `"strong"` | Weak pairs recorded, never gating (D3). |
| `stage2_tier_floor` | 6 | Tier ≥ Moderate (D4). |
| `safety_margin_minutes` | 30 | §3.10. |
| `single_event_fine_range_minutes` | 60 | §3.11 tier boundary, measured pre-margin. |
| `max_aspects_per_event` | `"all"` | `"1"` reproduces the book's single-aspect practice. |
| `fast_set / slow_set / moon_set / angle_house_set` | §3.3 | Fixed by the technique; do not tune. |

---

## 7. Execution plan (ordered, with validation checklists)

### Step 0 — Commit the reference assets
`compendium_reference/` and `docs/` are untracked (F13). Commit them first.
- [ ] `git add compendium_reference docs && git commit` — the two compendium files, this doc, v3, migration/manual docs.

### Step 1 — Data build: the pairwise table
Implement §5.2; run it; run the manual review; commit `juan_combos_pairs_v1.json`.
- [ ] G1–G4 all pass; `_meta` records the review sign-off.
- [ ] Spot-verification: Birth of Brother → 45 pairs; the three marked-none events → empty; Positive Travel Overseas pairs carry `inherited_from`.

### Step 2 — `significators/compendium.py`
Implement §5.1 + `test_compendium_lookup.py`.
- [ ] All 51 `EventType`s resolve per §4.2 (40 mapped, 11 no-data).
- [ ] Absent-key tier lookups return `None`; unordered pair lookups return the same result as the ordered call; inherited pairs resolve.
- [ ] Full existing suite (153 tests) still green.

### Step 3 — Speed plumbing
Implement §5.4 + §5.3 + regression test.
- [ ] `PSSR_Auto(..., return_speeds=False)` output byte-identical to golden files (`test_techniques_golden.py` untouched and green).
- [ ] Sanity: Moon speed ≈ 11.7–15.5°/day; Venus ~0.8–1.3°/day; station behavior visible (a chosen date where a fast planet stations shows |speed| near 0).
- [ ] Full suite green.

### Step 4 — Sweep and per-point evaluation
Implement §3.2–3.7 (stage logic without relevance wiring yet — stubs that accept everything, to test the kinematics in isolation).
- [ ] Synthetic test: construct a candidate window and events where a specific exact aspect is known to occur (compute the candidate time that makes progressed Mercury conjunct natal Jupiter exactly); the pipeline flags it as a qualifying hit at that time and only within 12′ on either side.
- [ ] Orb-boundary tests at 12′/18′/32′ and major-only behavior (a 45° semisquare just inside orb never fires).
- [ ] Speed gate: with a stubbed speed below floor, the same hit is excluded and lands in the near-miss ledger with its speed recorded.

### Step 5 — Relevance wiring
Wire §4 lookups into the stages.
- [ ] Per-gate unit tests on a fixture person (e.g. `data_input/ing tea.json`): a pair present as `strong` passes; the same pair for an event where it is `excluded` (e.g. Mars–Pluto for Birth of Son) does not; the same pair for an event where it is absent does not; a stage-2 target at tier 6 passes, tier 4 fails, absent fails.
- [ ] Events with no-data EventTypes and the three marked-none events produce zero stage-1 hits and are reported.

### Step 6 — Range-finding, consensus, margin, report
Implement §3.8–3.11.
- [ ] Synthetic interval tests: full consensus; empty full-intersection → max-cardinality partial consensus with correct subset and dropped events; disjoint everything → `none` tier, full window returned; margin clamps to input window.
- [ ] Corroboration tiers at the 2 / 1 / 0 boundaries, single-event ≤ 60 min vs > 60 min.

### Step 7 — End-to-end and calibration
Run `narrow_birth_time_window` over 2–3 real people from `data_input/` with well-populated event lists.
- [ ] Produces an hour-scale (or smaller) window with ≥ 2 corroborating events on at least one person; report contents complete (per-event hits, near-misses, tier, actual-DOB placement).
- [ ] Timing recorded; if a full 24 h × full event list exceeds a few minutes, apply the optional coarse-pass (§3.2) and confirm the refined result matches the fine-sweep result on the same input.
- [ ] **Sensitivity analysis (documented, not auto-tuned):** run with `speed_floor_arcmin_per_day` ∈ {25, 30, 35}, `stage2_tier_floor` ∈ {4, 6, 8}, `safety_margin_minutes` ∈ {15, 30, 60} on one person; report corroboration counts and window widths per setting. This is the calibration deliverable; do not silently change the defaults without it.
- [ ] Full existing suite green.

### Step 8 — Docs and hygiene
Module docstrings per the migration's §3.3 standard; cross-reference this document from the module docstrings; mark §8's decisions as implemented in this doc's status line if desired.
- [ ] Docstring audit for the new/modified files passes.

---

## 8. Decision log (the v3 open items, resolved)

| v3 open item | Decision |
|---|---|
| D1. Exact speed cutoff within 30–35′/day (§1.9) | **30.0′/day, absolute value.** The book's own lower bound ("over 30′"); permissive side chosen deliberately — the floor gates *specificity*, not correctness, and the fail-safe design (margin, fail-open) absorbs an over-permissive floor better than an over-strict one. Named parameter; calibrated in Step 7. |
| D2. Whether fast-to-fast pairings require both points to clear the speed floor (§1.10a) | **Yes — both points, individually, |speed| ≥ 30′/day.** This is the same underlying logic (never credit a hit where a nominally-fast point is stalled), stated in v3 as the natural extension; the Moon passes trivially. |
| D3. Strength-language cutoff for the pairwise table (§1.11) | Three tiers — `strong` / `weak` / `excluded` — coded at build time from wording (§4.1). **Gate = `strong` only.** `weak` hits are recorded in the near-miss ledger (they remain visible and countable for calibration) but never produce a range; `excluded` and absent never fire. |
| D4. Exact `tier_score` floor for stage 2 (§1.10) | **≥ 6 (Moderate)** on the non-Moon point, as proposed in v3; absent key fails closed. Named parameter, calibrated in Step 7. |
| D5. How many corroborating events are "enough" (§3.3) | No pass/fail on the count. Three-tier output: **≥ 2 events → `usable`** (full or partial consensus); **1 event → `usable` only if its pre-margin range ≤ 60 min**, else `weak`; **0 → `none`**, full window returned. The corroboration ratio is always reported so thin evidence is visible. |

## 9. Flagged items — could not be resolved from available material; verify before or during implementation

1. **Stage-2 angle identity (v3 §1.3).** Whether "Moon in conjunction with an angle" uses the **natal** angles or the **return chart's** angles. The book's own mechanism list ("radical (natal) factors: … angles, and house cusps") and the codebase's existing practice (radix houses are already the fixed side of every `find_pssr_swiss_aspects` call) both point to **natal angles**; the spec defaults to that (§3.3) and needs no new computation. If the return-chart reading is preferred, the pipeline must add `swe.houses` at both return moments per (point, event) — a contained change to §3.2 step 2 and §3.3's `ANGLE_HOUSE_SET` definition. **Verify Estadella pp. 99–109 once during Step 4.**
2. **Sun and Part of Fortune as receptive targets.** Per the strict reading of the rectification section (fast-vs-slow only, Moon only), Sun and POF — receptive-only factors — are targets of **no** stage today. The pairwise table is built with their pairs regardless, so admitting them later (e.g. natal Sun as a stage-1 target) is a constants change, not a data rebuild. Confirm with the book's rectification chapter whether natal-Sun-receptive hits are meant to count.
3. **Speed floor value 30 vs 35.** Decided 30 (D1); the near-miss ledger + Step 7 sensitivity analysis is the confirmation loop.
4. **`weak` pair inclusion.** Decided strong-only (D3); revisit if stage-1 corroboration proves too sparse on real data.
5. **Consensus fallback cardinality.** The max-cardinality-subset rule (§3.9) is a design decision, not source-derived; its behavior is fully testable and its outcome always visible in the report.
6. **`compendium_reference/` untracked** (F13) — committed in Step 0; no implementation before then.
7. **Timezone frame.** The whole codebase treats the naive datetimes in `data_input/*.json` through `julian.to_jd` as-is; the known caveat (Phase 2 finding #6: modern-DST applied to historical dates) is inherited by this pipeline unchanged. Out of scope for this feature; do not attempt timezone fixes inside it.

---

## 10. Relationship to the migration roadmap

- The pipeline is new code, written against the **post-Phase-8** layout, so it must honor the conventions Phases 5–7 established: significator data/lookup lives under `significators/` (F10), no module-level mutable state, docstring standard §3.3.
- **Phase 9 (Aspect model) is not done.** This design deliberately evaluates raw degrees via `calculate_aspect` and only *emits* strings in the report — it has no dependency on Phase 9 either way, and its report is the natural first consumer of a future `Aspect` codec.
- The batch-convention call pattern (`narrow_birth_time_window(...)` callable from the module bottom) is used; a CLI arrives with Phase 10.
- Every change is additive or new-file; the full Phase 2 characterization suite must stay green after Steps 2, 3, and 7 in particular.

---

## 11. Acceptance summary

The implementation is complete when:
1. All of §7's checklists pass, including the full 153-test suite staying green throughout.
2. `juan_combos_pairs_v1.json` passes G1–G4 and is human-reviewed.
3. End-to-end runs on 2–3 real people produce window-narrowing results of the shape Estadella reports (hours → tens of minutes as events corroborate), with complete per-event reporting and zero silent data drops.
4. The §9 verification items (1 and 2) have been checked against the book and their outcomes recorded in this document's next revision.
