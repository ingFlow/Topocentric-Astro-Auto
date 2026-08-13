# PSSR Window-Narrowing — Final Implementation Plan (v5)

**Purpose:** Final, executable specification for Step 0 of the rectification framework — narrowing an uncertain birth-time window (typically 24 hours) using the Precessed Solar Return technique, before POLARIS and Primary Directions take over the fine search.

**Status:** Spec only. This document is the implementation contract. It supersedes `pssr_window_narrowing_design.md` (v3, the technique analysis) and `pssr_window_narrowing_design_v4.md` (the first full spec). v4 was reviewed by the domain owner; this v5 incorporates their seven decisions verbatim (§8). No implementation has been done yet.

**How to use this document:** Written to be handed to an implementation agent as-is. §3 is the algorithm contract. §4 is the data-build contract. §6 is the config-file contract (every knob in one place). §5 is the file-level build list. §7 is the ordered execution plan with validation checklists. §8 is the decision log. §9 is the explicitly-excluded / future-research register. §10 is the short list of items still to verify against the source book — none blocks the build.

---

## 1. Goal and non-goals

**Goal.** Given a person's uncertain birth-time window (`dt_radix_start` … `dt_radix_end`, from their `data_input/*.json`), their natal geopos, and their dated, categorized life events, produce a **narrowed sub-window** of birth times whose PSSR charts best corroborate those events per Estadella's method — with the hard guarantee that the returned window never silently excludes the true birth time (the one failure mode worse than a slow search).

**Non-goals (deliberately out of scope):**
- No scoring of *how good* a birth time is in the abstract. Output is a window, not a ranked list.
- No PSSR 2 (progressed-to-progressed aspects) — excluded by the source.
- No Epoch/Dual-Test, no Mercury/Venus-return variants, no harmonics readings.
- **No houses and no angles anywhere in the narrowing system** (§3.3, §9.1). House-based evidence is explicitly deferred: houses are a verification tool for *after* the time is narrowed, not an input to the narrowing itself.
- **No Sun and no Part of Fortune as targets** (§3.3, §9.2). Both are receptive-only factors and are excluded from all stages of this feature.
- No change to the existing `PSSR_Auto` behavior for its current callers. Everything added is opt-in.
- No timezone work. The pipeline operates in the same naive-datetime frame the entire codebase already uses (§10.7).

**Why this narrows, quantitatively (the mechanism the whole plan rests on).** Sweeping the candidate birth time `t` across the window, the PSSR aspect that matters for rectification is the one between a *progressed return-chart factor* and a *radix factor*. As `t` moves, each side of the aspect moves at a measurable rate, and the in-orb episode width is `2 × orb ÷ relative rate`:

| Stage | Typical pairing | Relative rate (sweep frame) | Episode width at the stage's orb |
|---|---|---|---|
| 1 — wide (fast→slow) | Mercury/Venus/Mars vs Jupiter/Saturn/Uranus/Neptune/Pluto/Node | ~0.5–2.5°/day (dominated by the fast planet's rate; slow partner is ~fixed) | ~5–20 h (a Mars at the 30′ speed floor produces ~19 h — that weak discrimination is exactly what the speed gate exists to flag) |
| 2 — fine, Moon arm | progressed Moon vs slow planet | ~13°/day | ~1 h at 18′; ~2 h at 32′ (conj/opp) |
| 2 — fine, fast-to-fast arm | Mercury–Venus, Venus–Moon, etc. (two moving points) | ~2–15°/day | ~1–4 h at 12′ (18′/32′ when Moon is a party) |

The two-stage structure (§3.5–3.6) is the direct consequence: **stage 1 produces the coarse narrowing** (each hit's wide episode, intersected across events, collapses to hours — Estadella's 13:30–18:30 shape), and **stage 2 produces the fine refinement** (short episodes, intersected within the coarse window, collapse to tens of minutes — Estadella's 10–20-min Moon-stage shape). Fast-to-fast pairings belong in the fine stage with the Moon-to-slow arm — both move too fast to be coarse discriminators — and are explicitly **not** part of stage 1 (§3.6).

---

## 2. Verified facts about the current codebase (checked July 2026 state)

These were verified directly against the source tree during the v4 review and remain current. The spec is built on them; do not re-derive them.

| # | Fact | Evidence |
|---|---|---|
| F1 | The `src/topo_astro/` package layout exists (Phases 4–8 of the migration are largely committed). Phase 9 (structured `Aspect` codec) is **not** done — aspect strings are still the lingua franca. | `git log --oneline -15`; tree listing. |
| F2 | `PSSR_Auto(dt_radix, dt_event, rad_planets=None, geopos=None)` computes everything the pipeline needs except speeds: the two return moments (`swe.solcross_ut`), the four progressed/regressed dates (1 day = 1 year via `timelapse = timedelta(hours=jd_diff / 15.218425)`), the four progressed position sets (Sun excluded), and the aspect strings. `get_dict_info()` already exposes the return dates and `jd_diff_pssr_event` internals. | `src/topo_astro/techniques/pssr.py`. |
| F3 | **The speed question is settled: `swe.calc_ut()` already computes daily longitude speed — it is discarded at every call site.** The 6-element result array's index `[3]` is longitude speed in degrees/day; every call site keeps `xx[0]` only (`xx, _ = swe.calc_ut(...)`). The "additive speed return" is tiny plumbing, not new astronomy. | `src/topo_astro/core/constants.py:107,121,137`; `pyswisseph` API. |
| F4 | The existing PSSR aspect finder does **not** match the narrowing spec and is not reused: `find_pssr_swiss_aspects` applies a flat 32′ orb to the Moon and 12′ to all others **regardless of aspect type**, and evaluates **all nine** aspect types. The narrowing spec (§3.4) requires 18′ for Moon non-conjunction/opposition and **majors only**. The finder's two inline orb literals (`32/60`, `12/60`) are extracted to named constants in Step 3 so the config module can import them complete-by-reference (§6.2) — byte-identical behavior preserved. | `src/topo_astro/core/aspects.py:194–219`. |
| F5 | `calc_planets_pof_houses_labelled` returns planets + POF + houses **H1–H11 only** (`range(0,11)` — H12 is dropped, a pre-existing quirk). **Moot for this feature:** houses are excluded from the narrowing system entirely (§3.3), so the pipeline does not consume or need to fix this helper's house output. | `src/topo_astro/core/constants.py:132–152`. |
| F6 | The radix chart is **re-erected at every candidate time** `t` in the sweep: `rad(t) = calc_planets_labelled(jd(t), "(r)")` (planets + Node, which includes the Sun needed for the return computation). Natal-side speeds are therefore per-candidate, not once-per-person. | F2 + design math in §1. |
| F7 | `construct_technique(TechniqueType.PSSR, ...)` constructs `PSSR_Auto(dt_radix, dt_event, rad_planets)` — no geopos threaded (natal geopos only used when `rad_planets is None`, which call sites never allow). Consistent with returns being erected at birth coordinates. | `src/topo_astro/techniques/base.py:230–235`. |
| F8 | `FAST_TO_SLOW_COMBO` in the scoring engine includes the Moon in the fast set (`[MAR, MER, VEN, MON]` vs `[JUP, SAT, URA, NEP, PLU, NNO]`). The narrowing pipeline defines its **own** fast/slow constants with Moon excluded; the existing `AspectType` branches are untouched for their existing callers. | `src/topo_astro/significators/scoring.py:241–253`. |
| F9 | `generate_grid_angular_aspects(filename, start_time, end_time, increment_seconds, ...)` already supports parameterized stepping — the pattern exists, but the new pipeline does **not** reuse it (it needs per-point structured data, not grid-file rows). | `src/topo_astro/batch/grid_engine.py:119`. |
| F10 | **There is no compendium loader anywhere.** `significators/` contains only `rules_data.py` and `scoring.py`; `compendium.py` is genuinely new. | Tree listing of `src/topo_astro/significators/`. |
| F11 | `compendium_scoring_export_v2.json` (the tier data) has 40 events, each with per-symbol `tier_score` (0/1/2 per source, tier 0–10), `sample_sizes`, and structural-scope nulls. Symbol roster includes the 10 planets + `NODE_ANY` (+ `POF` and angle/house symbols, retained in the data for future research §9). Saturn/Neptune are absent as keys for some events — **an absent key means "no data", not 0**, and lookups must fail closed. | `compendium_reference/compendium_scoring_export_v2.json`. |
| F12 | The raw compendium (`Event Astrology a Compendium of Aspects.md`) contains "Astrological Combinations (Estadella)" sections for **all 40 events**, with format hazards: "Birth of Brother" is the first section and has **no markdown heading**; "Birth of Sister" is `##` while the rest are `#`; "Positive Travel Overseas" is a cross-reference section `(See Positive Travel)`; three events (Demobilization or Release, Assasination or Suicide, Gambling Loss) are marked `juan_combos_marked_none`/`total=0` in the JSON. Bullet format is uniform: `- **A-B / B-A**: prose`. | Raw compendium; JSON `sample_sizes`. |
| F13 | **`compendium_reference/` is currently untracked in git** (as are `docs/`). The compendium assets the pipeline depends on must be committed before implementation starts. | `git status --short`. |
| F14 | The Phase 2 characterization suite exists (153 tests, golden-file based) and is the regression gate every change in §7 must pass, including the PSSR technique's byte-identical output (`tests/test_techniques_golden.py`). | `docs/phase2_README.md`; `tests/`. |
| F15 | `PLANETS` is the 10 planets + `'Mean_Node'`. The codebase's node label is `Mean_Node`; the compendium's is `NODE_ANY`. The symbol-mapping layer (§4.3) is required. | `src/topo_astro/core/constants.py:38–41`. |
| F16 | `calculate_aspect(pos1, pos2, orb, flag_major=True)` in `core/aspects.py` already implements the **majors-only restriction** via the existing `MAJOR_ASPECTS` table (the five majors: conjunction, sextile, square, trine, opposition). The pipeline uses this existing primitive with `flag_major=True` for every stage; the config imports `MAJOR_ASPECTS` complete-by-reference (§6.2). | `src/topo_astro/core/aspects.py:131`; usage at lines 164, 268. |

---

## 3. The algorithm contract

### 3.1 Inputs and outputs

```
narrow_birth_time_window(
    dt_radix_start: datetime,        # window start (from data_input JSON)
    dt_radix_end:   datetime,        # window end
    dt_actual_dob:  datetime,        # working-hypothesis birth time (reporting only)
    geopos_natal:   list[lat, lon, alt],
    events:         list[Event],     # each: datetime, event_type (EventType), geopos (unused by PSSR)
    config:         NarrowConfig,    # §6 — the config module; defaults are its resolved values
) -> PSSRWindowReport
```

`PSSRWindowReport` (§3.10) must contain, at minimum: the final window (with and without margin), the coarse and fine corroboration counts, the confidence tier, the per-event detail (stage-attributed), the near-miss ledger, the parameters used, and where `dt_actual_dob` falls relative to the window.

### 3.2 The sweep

- Step `t` across `[dt_radix_start, dt_radix_end]` at `STEP_SECONDS = 60` (config), inclusive of both endpoints. The step size is safe: the fastest relative rate in the system (~15°/day, fast-to-fast with Moon) yields in-orb episodes ≥ ~1 h — two orders of magnitude above the sampling floor.
- At each grid point `t`, per event `e`:
  1. Recompute the candidate radix **once per grid point** (shared across events): `rad(t) = calc_planets_labelled(jd(t), "(r)")` (planets + Node; includes the Sun, which the return computation needs), plus **natal speeds** for all 11 points via `calc_planets_labelled_speeds(jd(t), "(r)")` (F3/F6).
  2. Construct `PSSR_Auto(dt_radix=t, dt_event=e.datetime, rad_planets=rad(t), return_speeds=True)` (§5.3) — one instance per (point, event). Read from `get_dict_info()` the four progressed dates and, via the opt-in flag, the four progressed position sets **with speeds**.
  3. Evaluate stage 1 (§3.5) and stage 2 (§3.6) against the candidate radix planet/Node positions.
- Per-grid-point cost ≈ 11 (natal) + 2 `solcross` + 44 (4 × 11 progressed) ≈ 60 Swiss Ephemeris calls. At 1,440 points × 20 events ≈ **~1.7M calls ≈ tens of seconds to a few minutes** in batch — acceptable. (Optional coarse-pass pre-filter — 5-minute grid, then 1-minute refinement inside surviving ranges — is a permitted optimization; the default is the single fine sweep.)
- The four variants (direct/converse SSR × direct/converse progression) are all evaluated at every point and treated as equal-weight channels. A hit carries its variant as provenance only.

### 3.3 Point sets and membership (resolved constants; defined in the config module §6)

| Constant | Members | Notes |
|---|---|---|
| `FAST_SET` | Mercury, Venus, Mars | **Moon deliberately excluded** — the Moon is its own factor (F8). |
| `SLOW_SET` | Jupiter, Saturn, Uranus, Neptune, Pluto, Mean_Node | The Lunar Node is in the slow/receptive group. |
| `FAST_FAST_SET` | Mercury, Venus, Mars, Moon | The member set of the fast-to-fast arm (§3.6). |
| `PROGRESSED_SET` | Sun excluded; planets + Node progress (Moon included); POF and angles/houses **never** progress | Matches existing `PSSR_Auto` behavior (F2). |
| `RECEPTIVE_ONLY` | Sun, POF | Never progressed; **neither is a target of any stage in this feature** (§9.2). |
| *(no angle/house set — removed)* | — | **Houses and angles are excluded from the narrowing system entirely** (§9.1). There is no angle-identity question to resolve: the v4 flag on natal-vs-return angles is moot. |

### 3.4 Aspect evaluation (orbs and aspect classes — resolved)

The pipeline implements its own aspect evaluation over raw degrees using the core primitive `calculate_aspect()` with `flag_major=True` (F16). It does **not** call `find_pssr_swiss_aspects` (F4).

| Rule | Value |
|---|---|
| Aspect classes | **Majors only**: conjunction, sextile, square, trine, opposition (F16 — `calculate_aspect(..., flag_major=True)`; the config's `ASPECT_CLASSES` is the existing `MAJOR_ASPECTS` table, imported). Minors are recorded in the near-miss ledger, never gating. |
| Orb, no Moon party | **12′** flat, all point types (existing PSSR value, imported complete-by-reference). |
| Orb, Moon is a party | **18′** for non-conjunction/opposition (new, book-derived); **32′** for conjunction and opposition (existing PSSR value, imported). A property of the Moon, uniform across both stages and both fine arms. |

### 3.5 Stage 1 — the wide-range narrowing stage (fast → slow)

The **only** stage that produces coarse narrowing. Membership, speed, and relevance per v3 §1.8–1.9, resolved:

- **Structure (Case A/B):** one point from `FAST_SET`, the other from `SLOW_SET`, either side may be the progressed/return factor or the radix factor.
- **Orb:** 12′ (no Moon can be involved by construction).
- **Aspect classes:** majors only.
- **Speed gate (hard pass/fail — resolved):** the single fast point's **absolute daily motion ≥ 30.0′/day**. Measured on the side the fast point actually sits: progressed-side → ephemeris speed at its progressed date; radix-side → natal speed. Retrograde planets pass on `|speed|` — the rule is about magnitude of daily motion ("not found in slow movement"). A below-floor hit is **excluded from range-finding entirely**, recorded in the near-miss ledger with the actual speed (the ledger is the calibration instrument for the floor).
- **Relevance gate:** the unordered pair (fast point, slow point) must resolve to `strong` in the Juan Combos pairwise table (§4.1) for this event. `weak` → near-miss, no range. `excluded` or absent → no hit (see §4.1 for the tiers and the three no-data events).
- **Explicitly not part of stage 1:** any pairing of two fast points (Mercury–Venus, Venus–Moon, etc.). Fast-to-fast pairings are **not** included in this stage's wide narrowing — they move too fast to act as coarse discriminators and are accounted for in the fine stage (§3.6), exactly like the Moon-to-slow arm.

### 3.6 Stage 2 — the fine-tuning stage (Moon-to-slow + fast-to-fast)

The fine-refinement stage, evaluated **within the coarse window produced by stage 1** (§3.8). Two arms, both fine-resolution by construction (§1):

**Arm 1 — Moon to slow planet.** 
- **Membership:** progressed Moon vs one target from `SLOW_SET`.
- **Orb:** 18′ / 32′ conj-opp (Moon property).
- **Aspect classes:** majors only.
- **Speed gate:** none — the Moon's minimum daily motion (~11.7°/day) is orders of magnitude above the floor, so the gate is mathematically vacuous for the only moving party. Stated explicitly so no one adds a redundant check.
- **Relevance gate:** the slow point's `tier_score` from `compendium_scoring_export_v2.json` for this event **≥ 6 (Moderate)**. Absent key → no data → fail closed.

**Arm 2 — fast-to-fast.**
- **Membership:** both points drawn from `FAST_FAST_SET` = {Mercury, Venus, Mars, Moon}, one from each side (return/progressed vs radix), neither a slow planet. This is the Venus–Moon class of pairing (Tyson's worked hit).
- **Orb:** 12′; 18′/32′ whenever the Moon is a party (Moon property, not stage property).
- **Aspect classes:** majors only.
- **Speed gate:** **both** points must individually clear the 30.0′/day floor. The Moon clears it trivially — no special-casing needed; the gate is applied uniformly for code simplicity.
- **Relevance gate:** the unordered pair must resolve to `strong` in the Juan Combos pairwise table for this event (the Moon is on Estadella's 14-point roster like everything else).
- **Positioning:** this arm is a stage-2 arm. Its in-orb episodes are fine-resolution (~1–4 h, §1), so it refines the coarse window; it is **explicitly excluded from stage 1** (§3.5).

### 3.7 Per-event, per-stage range-finding

- A **qualifying hit** is a (stage, arm, variant, progressed point, radix point, aspect class) tuple that passes the applicable membership + orb + speed + relevance gates at a given grid point. Distinct tuples are tracked separately; as `t` sweeps, each tuple's in-orb times form one or more contiguous intervals (a pair can come into orb, leave it, and — near a mutual station — return; collect per-tuple interval sets, then merge overlaps).
- **Per-stage event contribution:** `C1(e)` = union of `e`'s stage-1 hits' intervals; `C2(e)` = union of `e`'s stage-2 hits' intervals (both arms merged). Each event is counted **once per stage** in that stage's corroboration count no matter how many hits it has. This is the automated generalization of the book's "one representative aspect per event": the book's single-aspect practice was about interpretation, not intersection arithmetic — the union is the fail-safe choice (wider = less risk of silently excluding the true time). `MAX_ASPECTS_PER_EVENT: "all" | 1` is a config knob; `1` reproduces the book's practice exactly (tie-break per stage: the hit with the smallest orb at the center of its widest interval).
- **Events with no data:** events whose `EventType` maps to no compendium event (§4.2) or whose compendium event has `juan_combos_marked_none` (F12) can still contribute via stage-2 arm 1 (tier data exists for all 40 events). Only if a tier lookup also fails do they contribute nothing — and they are then reported explicitly, never silently absent.

### 3.8 Coarse pass — stage-1 consensus and the coarse window

- **Coarse consensus:** the literal interval intersection of `C1(e)` over all events with `C1(e) ≠ ∅`.
- **Partial consensus (fallback):** if the coarse intersection is empty, compute the **maximum-cardinality subset of stage-1-contributing events whose contributions mutually intersect** and use that subset's intersection; report the subset vs. the dropped events. Ties broken by earliest window start.
- **No stage-1 consensus:** if no subset of ≥ 2 events intersects (or fewer than 2 events contribute), the coarse window is the full input window — stage 1 passes through fail-open, never producing an empty window.
- **Coarse margin:** apply `SAFETY_MARGIN_MINUTES = 30` to the coarse window on both ends (clamped to the input window). The fine pass scans the margined coarse window, so the margin cannot cause a fine-stage corroboration to be missed just outside the raw coarse boundary.
- If the margined coarse window spans the full input window, the fine pass scans the full window.

### 3.9 Fine pass — stage-2 refinement within the coarse window

- Evaluate stage 2 only inside the margined coarse window from §3.8.
- **Fine consensus:** the interval intersection of `C2(e)` over events with `C2(e) ≠ ∅`, intersected with the coarse window.
- **Partial consensus (fallback):** same max-cardinality-subset rule among the stage-2-contributing events.
- **No fine consensus:** if the fine intersection is empty or fewer than 2 events contribute, the final window is the coarse window unchanged.
- Stage-2 hits that fall outside the coarse window are **not** discarded silently — they are recorded in the report as "fine hits outside coarse window" (valuable calibration information: a recurring systematic offset between the stages is exactly the kind of thing research wants to see).
- **Final margin:** apply `SAFETY_MARGIN_MINUTES` to the final window (clamped to the input window).

### 3.10 Confidence tiers and reporting

| Corroboration | Consensus | Pre-margin final range | Tier |
|---|---|---|---|
| coarse ≥ 2 | full or partial | any | `usable` |
| fine ≥ 2 | full or partial | any | `usable` |
| 1 (any stage) | — | ≤ 60 min | `usable` (single-event fine) |
| 1 (any stage) | — | > 60 min | `weak` |
| 0 | — | — | `none` (full window returned) |

The report must include: per event, contributing hits (stage, arm, variant, points, aspect, interval, orb at interval center, relevance source + wording, speed values) and the near-miss ledger (weak-relevance, excluded-relevance, speed-below-floor with actual speeds, minor-aspect, no-data, fine-outside-coarse); and for the final window: tier, coarse corroboration count / events-with-data count, fine corroboration count, consensus type (full/partial/none) per pass, margin applied, subset members where partial, and the signed distance of `dt_actual_dob` from the window.

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
- Point names normalized: `AS`→`ASC`, `Lunar Node`/`Node`→`NODE_ANY`, `Part of Fortune`→`POF`, planets → their compendium caps. A pair must fall inside the 14-point Juan Combos roster {ASC, MC, Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, NODE_ANY, POF} — a parser hit outside the roster is a hard build error, not a silent accept. (Note: only planet/Node pairs are consumed by the narrowing stages; the full roster is preserved in the data for future research §9.)
- **Strength tiers** (wording-cued, mirroring the "Other" source's existing methodology in the reference doc):
  - `strong` — expected/frequent-type positive attribution ("we always find", "frequent", "very common", "we find", "we often find", "the birth of X", plain positive statements).
  - `weak` — hedged or occasional ("occasionally", "sometimes", "to a lesser extent", "possible as well", "can occur", "may find").
  - `excluded` — "only exception" hedging ("the only occasional exception is", "the only exception is") — actively counter-indicative.
  - absent key = not catalogued for that event (no data). **`absent` ≠ `excluded`.**
- `aspects_hint` captures the parenthetical aspect-structure hints ("in conjunctions and harmonic aspects") as free text — recorded for future calibration, **not used** by the gate.
- Cross-reference sections: "Positive Travel Overseas" inherits "Positive Travel"'s pairs with `inherited_from: "Positive Travel"`.
- The three marked-none events (F12) get `pairs: {}` + an explicit `marked_none: true` in their entry.

**Build procedure (executed once, then reviewed — hand-curated research data, same care class as `rules_data.py`):**

1. `scripts/build_juan_combos_table.py` (new; `scripts/` created now, pre-Phase-10, purely additive).
2. Parse sections: the file is section-delimited by the known heading set (`KEY PLANETARY INDICATORS (STARKMAN)`, `Astrological Combinations (Estadella)`, `Summary of Astrological Signatures (Marr)`, `Historical Chart Examples (Marr & Starkman)`, `## Other`), with special handling for the headingless first section ("Birth of Brother") and the `(See Positive Travel)` cross-reference.
3. Parse bullets `- **A-B / B-A**: prose`, normalize names, code tiers by keyword rules, keep verbatim `wording`.
4. **Automated quality gates (must all pass before review):**
   - G1: parsed pair count per event == `sample_sizes.juan_combos_total_combinations` in `compendium_scoring_export_v2.json` for every event that has a section (the JSON's preserved totals are the cross-check — e.g. Birth of Brother = 45).
   - G2: zero parser hits outside the 14-point roster; zero unparseable bullets (each failure is a hard error with the line number).
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
| `POSITIVE_AC_MC`, `NEGATIVE_AC_MC`, `POSITIVE_2_8`, `NEGATIVE_2_8`, `POSITIVE_3_9`, `NEGATIVE_3_9`, `POSITIVE_5_11`, `NEGATIVE_5_11`, `POSITIVE_6_12`, `NEGATIVE_6_12`, `BLANK` | **no compendium event** — cannot contribute any stage by construction; reported as no-data. |

### 4.3 Symbol-name mapping (codebase ↔ compendium)

`Sun↔SUN, Moon↔MOON, Mercury↔MERCURY, Venus↔VENUS, Mars↔MARS, Jupiter↔JUPITER, Saturn↔SATURN, Uranus↔URANUS, Neptune↔NEPTUNE, Pluto↔PLUTO, Mean_Node↔NODE_ANY, POF↔POF, H1↔ASC, H4↔IC, H7↔DESC, H10↔MC`, minor cusps direct (`H2↔H2`, …). The narrowing stages consume only the planet/Node and (data-side) Sun/POF entries; the angle/house entries are retained in the mapping for future research (§9) so the module is complete rather than surgically trimmed. `Mean_Node→NODE_ANY` is the one genuinely lossy mapping (codebase node pole unspecified — F15) and is stated as such.

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

- New **keyword-only** constructor parameter `return_speeds=False`. When `True`, `calc_pssr_for_date` additionally computes and stores the four progressed position sets **with per-point daily speeds** (via the §5.4 helper) and exposes them in `dict_info` under `prog_dir_speeds`, `reg_dir_speeds`, `prog_conv_speeds`, `reg_conv_speeds` (parallel lists to the existing position lists).
- Default `False` ⇒ all existing callers (dispatcher, GUI, batch, tests) see byte-identical behavior — verified by golden tests.
- **Do not** modify `get_str_aspects`, `get_dict_info` shape, `find_pssr_swiss_aspects`, or the return-year logic.

### 5.4 `src/topo_astro/core/constants.py` — MODIFIED, additive only

- New helper `calc_planets_labelled_speeds(jd, label)` — same loop as `calc_planets_labelled`, keeping `xx[3]` alongside `xx[0]` (F3). Existing `calc_planets_labelled` untouched.

### 5.5 `src/topo_astro/core/aspects.py` — MODIFIED, behavior-preserving only

- Extract the two inline orb literals in `find_pssr_swiss_aspects` (F4) into module-level named constants `PSSR_MOON_ORB_DEG = 32/60` and `PSSR_PLANET_ORB_DEG = 12/60`, with the existing inline comment (`#{CHANGE it was 14/60 before...}`) moved onto the constant. The finder keeps calling `calculate_aspect` with the identical values — byte-identical behavior, verified by golden tests. Purpose: the config module imports these values complete-by-reference (§6.2) instead of duplicating them.

### 5.6 `src/topo_astro/batch/pssr_window_config.py` — NEW

The single research control panel — every business-logic knob of this feature in one module. Full contract in §6.

### 5.7 `src/topo_astro/batch/pssr_window.py` — NEW

The orchestration module. Pure functions, no globals. Responsibilities per §3: the sweep (§3.2), per-point stage evaluations (§3.5–3.6, via `calculate_aspect` from `core/aspects.py`), interval building and merging (§3.7), coarse pass (§3.8), fine pass (§3.9), the report (§3.10). **All decisions read from `pssr_window_config`; no hardcoded business values in this module.** Exposes `narrow_birth_time_window(...)` per the batch convention (callable directly; no CLI until Phase 10 of the migration). Module docstring per the migration's §3.3 standard.

### 5.8 `compendium_reference/juan_combos_pairs_v1.json` — NEW data artifact (§4.1)

### 5.9 Tests — NEW

`tests/test_compendium_lookup.py` (mapping, tier lookup incl. absent-key fail-closed, pair lookup incl. unordered keys and inherited pairs); `tests/test_juan_combos_data.py` (G1–G4 re-run as tests over the committed artifact); `tests/test_pssr_window_config.py` (config integrity: every knob present, imported values match their source constants — guards against drift between §5.5's extracted constants and the config); `tests/test_pssr_window.py` (per §7 validation checklists; golden-file style per the Phase 2 conventions, including a regression test that `PSSR_Auto` with `return_speeds=False` is byte-identical to pre-change output).

---

## 6. The config module contract (`src/topo_astro/batch/pssr_window_config.py`)

### 6.1 Principle: complete-by-reference

The config module is the **complete control panel for research**: every decision that a researcher may want to tinker with — window buffers/margins, aspect orbs, speed floors, relevance thresholds, stage membership, consensus behavior — lives here as a named constant with a docstring stating its provenance (book page, this spec's section, or the existing code location it came from).

Two sourcing rules:
1. **Where a value already exists in the codebase, the config imports it rather than duplicating it** (complete-by-reference). Existing modules never import the config — dependency flows one way only: `config → existing code`, `pipeline → config`. This keeps the config a faithful control panel without creating divergent copies or breaking existing conventions.
2. **Where a value is genuinely new** (a v5 decision), it is defined in the config with a `# NEW — §<section>, v5` comment and a one-line rationale.

### 6.2 The knob table (complete)

| Knob | Value / source | Provenance |
|---|---|---|
| `STEP_SECONDS` | `60` | NEW — §3.2. |
| `ASPECT_CLASSES` | `import aspects.MAJOR_ASPECTS` | EXISTING — `core/aspects.py` (F16); the majors table, applied via `calculate_aspect(..., flag_major=True)`. |
| `ORB_FAST_SLOW_DEG` | `import aspects.PSSR_PLANET_ORB_DEG` (= 12/60) | EXISTING — inline literal in `find_pssr_swiss_aspects`; named & imported per §5.5. |
| `ORB_MOON_CONJ_OPP_DEG` | `import aspects.PSSR_MOON_ORB_DEG` (= 32/60) | EXISTING — same. |
| `ORB_MOON_GENERAL_ARC_MIN` | `18.0` | NEW — book §1.5; the existing finder has no 18′ value (it applies 32′ to all Moon aspects), so this is a first-class new decision. |
| `SPEED_FLOOR_ARC_MIN_PER_DAY` | `30.0` | NEW — book's 30–35′/day range, lower bound; user-confirmed (D1). |
| `SPEED_FLOOR_USE_ABSOLUTE` | `True` | NEW — §3.5 (retrograde handled by magnitude). |
| `FAST_SET` | `frozenset({Planet.MER, Planet.VEN, Planet.MAR})` | EXISTING convention — `Planet` codes imported from `significators.rules_data`; membership per book §1.8 (Moon excluded). |
| `SLOW_SET` | `frozenset({Planet.JUP, Planet.SAT, Planet.URA, Planet.NEP, Planet.PLU, Planet.NNO})` | EXISTING convention — same import; membership per book §1.8. |
| `FAST_FAST_SET` | `frozenset({Planet.MER, Planet.VEN, Planet.MAR, Planet.MON})` | NEW — book §1.10a + D6 (folded into stage 2). |
| `MOON` | `Planet.MON` | EXISTING convention. |
| `PAIR_RELEVANCE_MIN` | `"strong"` | NEW — user-confirmed (D3); only `strong` pairs gate; `weak` goes to the near-miss ledger. |
| `STAGE2_TIER_FLOOR` | `6` | NEW — book §1.10 proposal; D4. |
| `SAFETY_MARGIN_MINUTES` | `30` | NEW — §3.8/§3.9 (the "window buffer" knob). |
| `SINGLE_EVENT_FINE_RANGE_MINUTES` | `60` | NEW — §3.10 tier boundary, measured pre-margin. |
| `MAX_ASPECTS_PER_EVENT` | `"all"` | NEW — §3.7; `"1"` reproduces the book's single-aspect practice. |
| `CONSENSUS_MAX_CARDINALITY` | `True` | NEW — §3.8/§3.9 partial-consensus fallback on/off. |
| `CONSENSUS_TIE_BREAK` | `"earliest_start"` | NEW — §3.8. |

Notes:
- Orb knobs are expressed in degrees where they import existing constants and in arcminutes where new — the pipeline converts internally to a single unit. Do not "normalize" the imports: the imported degree values must stay tied to the source constants so behavior cannot drift.
- The config contains **no logic** beyond constant definitions and imports (module docstring + provenance comments only). A researcher reading this file sees the full decision surface at a glance.
- `test_pssr_window_config.py` asserts the imported knobs equal their source constants at import time (drift guard, §5.9).

---

## 7. Execution plan (ordered, with validation checklists)

### Step 0 — Commit the reference assets
`compendium_reference/` and `docs/` are untracked (F13). Commit them first.
- [ ] `git add compendium_reference docs && git commit` — the two compendium files, this spec, v4, v3, migration/manual docs.

### Step 1 — Data build: the pairwise table
Implement §5.2; run it; run the manual review; commit `juan_combos_pairs_v1.json`.
- [ ] G1–G4 all pass; `_meta` records the review sign-off.
- [ ] Spot-verification: Birth of Brother → 45 pairs; the three marked-none events → empty; Positive Travel Overseas pairs carry `inherited_from`.

### Step 2 — `significators/compendium.py`
Implement §5.1 + `test_compendium_lookup.py`.
- [ ] All 51 `EventType`s resolve per §4.2 (40 mapped, 11 no-data).
- [ ] Absent-key tier lookups return `None`; unordered pair lookups return the same result as the ordered call; inherited pairs resolve.
- [ ] Full existing suite (153 tests) still green.

### Step 3 — Plumbing: speeds, orb extraction, and the config module
Implement §5.4, §5.5, §5.3, §5.6 in that order (config last, once the extracted constants exist) + `test_pssr_window_config.py` + regression tests.
- [ ] `PSSR_Auto(..., return_speeds=False)` output byte-identical to golden files (`test_techniques_golden.py` untouched and green).
- [ ] `find_pssr_swiss_aspects` behavior byte-identical after the orb-literal extraction (golden files green).
- [ ] Sanity: Moon speed ≈ 11.7–15.5°/day; Venus ~0.8–1.3°/day; station behavior visible (a chosen date where a fast planet stations shows |speed| near 0).
- [ ] Config imports resolve; `test_pssr_window_config.py` drift guards pass.
- [ ] Full suite green.

### Step 4 — Sweep and per-point evaluation
Implement §3.2–3.6 (stage logic with relevance stubbed open, to test the kinematics in isolation).
- [ ] Synthetic tests: a candidate window and events where an exact aspect is known (computed candidate time making progressed Mercury conjunct natal Jupiter exactly): stage 1 flags it at that time and only within 12′ on either side; a progressed-Moon-to-slow exact aspect fires stage-2 arm 1 with 18′/32′ boundary behavior; a Mercury–Venus exact aspect fires stage-2 arm 2 — **and is never produced by stage 1**.
- [ ] Orb-boundary tests at 12′/18′/32′ and major-only behavior (a 45° semisquare just inside orb never fires).
- [ ] Speed gate: with a stubbed speed below floor, the same stage-1 hit is excluded and lands in the near-miss ledger with its speed recorded; a fast-to-fast hit with one stalled point is likewise excluded.

### Step 5 — Relevance wiring
Wire §4 lookups into the stages.
- [ ] Per-gate unit tests on a fixture person (e.g. `data_input/ing tea.json`): a `strong` pair passes; the same pair for an event where it is `excluded` (e.g. Mars–Pluto for Birth of Son) does not; the same pair for an event where it is absent does not; a stage-2 arm-1 target at tier 6 passes, tier 4 fails, absent fails.
- [ ] Events with no-data EventTypes and the three marked-none events produce zero stage-1 hits and are reported.

### Step 6 — Ranges, coarse pass, fine pass, margin, report
Implement §3.7–3.10.
- [ ] Synthetic interval tests: full coarse consensus; empty coarse intersection → max-cardinality partial consensus with correct subset and dropped events; disjoint everything → full window passes through (`none` tier); fine consensus within the coarse window; empty fine consensus → coarse window returned; margins clamp to the input window.
- [ ] Fine hits outside the coarse window appear in the report's "fine hits outside coarse window" ledger.
- [ ] Corroboration tiers at the 2 / 1 / 0 boundaries, single-event ≤ 60 min vs > 60 min.

### Step 7 — End-to-end and calibration
Run `narrow_birth_time_window` over 2–3 real people from `data_input/` with well-populated event lists.
- [ ] Produces an hour-scale (or smaller) window with coarse corroboration ≥ 2 on at least one person; report contents complete (per-event stage/arm-attributed hits, near-misses, tier, actual-DOB placement).
- [ ] Timing recorded; if a full 24 h × full event list exceeds a few minutes, apply the optional coarse-pass (§3.2) and confirm the refined result matches the fine-sweep result on the same input.
- [ ] **Sensitivity analysis (documented, not auto-tuned):** run with `SPEED_FLOOR_ARC_MIN_PER_DAY` ∈ {25, 30, 35}, `ORB_MOON_GENERAL_ARC_MIN` ∈ {16, 18, 20}, `STAGE2_TIER_FLOOR` ∈ {4, 6, 8}, `SAFETY_MARGIN_MINUTES` ∈ {15, 30, 60} on one person; report coarse/fine corroboration counts and window widths per setting. This is the calibration deliverable; do not silently change the defaults without it. (The config module is what makes this pass trivial — every knob is already in one place.)
- [ ] Full existing suite green.

### Step 8 — Docs and hygiene
Module docstrings per the migration's §3.3 standard; cross-reference this spec from the module docstrings.
- [ ] Docstring audit for the new/modified files passes; the §9 future-research register is referenced from the pipeline module docstring.

---

## 8. Decision log

v4's five resolutions plus the domain owner's seven v5 decisions — all incorporated above:

| # | Item | Decision |
|---|---|---|
| D1 | Exact speed cutoff within 30–35′/day | **30.0′/day, absolute value** — the book's own lower bound; the floor gates specificity, not correctness, and the fail-safe design absorbs an over-permissive floor better than an over-strict one. **Confirmed by owner (v5 item 5).** |
| D2 | Whether fast-to-fast pairings require both points to clear the speed floor | **Yes — both points, individually, \|speed\| ≥ 30′/day.** The Moon passes trivially. |
| D3 | Strength-language cutoff for the pairwise table | Three tiers — `strong` / `weak` / `excluded` — coded at build time (§4.1). **Gate = `strong` only**; `weak` recorded in the near-miss ledger, never gating. **Confirmed by owner (v5 item 6).** |
| D4 | Exact `tier_score` floor for the fine stage's Moon arm | **≥ 6 (Moderate)** on the slow point; absent key fails closed. |
| D5 | How many corroborating events are "enough" | Three tiers: coarse ≥ 2 or fine ≥ 2 → `usable`; exactly 1 → `usable` only if pre-margin range ≤ 60 min, else `weak`; 0 → `none`, full window returned (§3.10). |
| D6 | **Fast-to-fast placement** | **Fast-to-fast pairings are removed from stage 1 entirely** and folded into the fine stage with the Moon-to-slow arm (§3.6). Rationale: two moving points ⇒ fine-resolution episodes; they behave like the Moon arm, not like coarse discriminators. **Owner decision (v5 item 1).** |
| D7 | **Houses and angles** | **Excluded from the narrowing system everywhere.** No angle/house target set exists in this feature; the v4 angle-identity question is moot. Houses are explicitly a post-narrowing verification tool. **Owner decision (v5 item 2).** |
| D8 | **Config module** | A single research control panel (`pssr_window_config.py`) holds every knob, complete-by-reference (§6). **Owner decision (v5 item 3).** |
| D9 | Sun and POF | **Excluded as targets at this stage** (receptive-only factors, no stage admits them). **Owner decision (v5 item 4)** — registered in §9.2 for future research. |
| D10 | Timezone handling | **None.** The pipeline inherits the codebase's naive-datetime frame unchanged. **Owner decision (v5 item 7).** |

---

## 9. Explicitly not included — future research register

This feature deliberately excludes the following. Each entry records what was excluded, why, and what the natural next exploration is — this register is the standing list for the technique's next evolution.

1. **Houses and angles (all 12 cusps incl. ASC/MC/DS/IC).** Excluded everywhere by owner decision (D7). They are **not** inputs to initial window narrowing — house-based evidence only becomes trustworthy once the time is narrowed, and is the verification/confirmation step for a candidate time, not the discovery step. Future exploration, in order: (a) house-cusp-based **verification** of a narrowed window (does the narrowed time produce event-appropriate house placements?), and (b) **fast-planet-to-house aspects** as expanding/verifying evidence. The book's "The Moon in conjunction with an angle is especially effective" line is recorded here so the Moon-to-angle fine-tuning idea is not lost — it was evaluated and set aside with this family. The compendium data (angle/house symbols) is retained and mapped (§4.3) so this exploration needs no data rebuild.
2. **Sun and Part of Fortune as targets.** Both are receptive-only factors (book §1.6) and no stage admits them at this stage (D9). The pairwise table is built with their pairs regardless — admitting a receptive Sun or POF target later (e.g. as a stage-1 target) is a config change, not a data rebuild.
3. **Weak-relevance pairs as gating evidence.** `weak` pairs never produce ranges (D3); they are recorded in the near-miss ledger. Future: revisit as expanding evidence if corroboration proves too sparse.
4. **Minor aspects.** Majors only (F16). Minors recorded in the ledger. Future: optional support-channel scoring.
5. **PSSR 2 (progressed-to-progressed).** Excluded per the source's own verdict that radix aspects are more accurate. Future: a separate, explicitly-labeled variant if ever wanted.
6. **PSSR applied to an Epoch (conception) chart, the Dual Test, and Mercury/Venus-return variants.** Book-adjacent material, not needed for narrowing.
7. **Timezone/LMT/DST refinement.** Excluded (D10). The known caveat (Phase 2 finding #6: modern-DST applied to historical dates) is inherited by this pipeline. Future: a dedicated timezone-correctness effort across the whole codebase — deliberately not scoped here.

---

## 10. Flagged items — verify during implementation; none blocks the build

1. **The 18′ Moon orb is a genuinely new value** (existing code has only 32′-flat for Moon). It is book-derived (p. 108: "For the Moon, a larger orb of 18' of arc is allowed (32' in conjunctions and oppositions)") and is the one orb in the system with no codebase precedent — the Step 7 sensitivity analysis is its confirmation loop.
2. **The 30–35′ speed range → 30′ pick** (D1). Confirmed by owner; the near-miss ledger's recorded speeds + Step 7 sensitivity is the confirmation loop.
3. **Fast-to-fast "both points clear the floor" is an extrapolation** (v3 flagged it as such; D2 keeps it). The same underlying logic (never credit a hit where a nominally-fast point is stalled) makes it the right default; flagged rather than assumed.
4. **Max-cardinality partial-consensus fallback is a design decision, not source-derived.** Fully testable; its outcome is always visible in the report (which events were dropped).
5. **`compendium_reference/` untracked** (F13) — committed in Step 0; no implementation before then.
6. **Timezone frame** — inherited caveat, out of scope (D10, §9.7).
7. **Verify against the source book during implementation (one pass, cheap):** the fine-stage orb paragraph (p. 108) and the speed-gate paragraph (p. 117) as quoted in v3 §1.5 and §1.9 — the spec's orbs, tiers, and floors are pinned to those exact quotes; a copy-editing discrepancy in the quotes would surface here. No design change is expected.

---

## 11. Relationship to the migration roadmap

- New code, written against the **post-Phase-8** layout: significator data/lookup under `significators/` (F10), no module-level mutable state, migration §3.3 docstring standard.
- **Phase 9 (Aspect model) is not done.** This design evaluates raw degrees via `calculate_aspect` and only *emits* strings in the report — no dependency on Phase 9 either way; the report is a natural first consumer of a future `Aspect` codec.
- The batch-convention call pattern (`narrow_birth_time_window(...)` callable from the module bottom) is used; a CLI arrives with Phase 10. `scripts/` is created early (Step 1) for the data builder — additive and harmless.
- Every change is additive or new-file; the full Phase 2 characterization suite must stay green after Steps 2, 3, and 7 in particular.

---

## 12. Acceptance summary

The implementation is complete when:
1. All of §7's checklists pass, including the full 153-test suite staying green throughout.
2. `juan_combos_pairs_v1.json` passes G1–G4 and is human-reviewed.
3. `pssr_window_config.py` exists as the complete knob surface (§6), imports every existing value complete-by-reference, and the pipeline contains zero hardcoded business values.
4. End-to-end runs on 2–3 real people produce window-narrowing results of the shape Estadella reports — a coarse narrowing from stage 1 (hours), refined by stage 2 (tens of minutes where fine evidence corroborates) — with complete per-event, stage-attributed reporting and zero silent data drops.
5. Stage 1 never produces fast-to-fast hits, and no house, angle, Sun, or POF target ever enters the evaluation (asserted by tests, not convention).
6. The §10 verification pass against the book has been completed and its outcome recorded in this document's next revision.
