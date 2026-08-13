# PSSR Window-Narrowing — Technique Analysis & Algorithm Design (v3)

**Purpose:** Design (not implement) Step 0 of the rectification framework — narrowing a 24-hour uncertain birth-time window using PSSR, before POLARIS and Primary Directions take over.

**Status:** Analysis and proposal only. No code below.

**What changed since v2:** three decisions, all yours, all incorporated below rather than left as open questions:

1. Relevance-gating for stage 1 (planet-to-planet) moves off `tier_score` and onto a direct lookup against Estadella's own Juan Combos pairwise data — v2's proposed numeric threshold on `tier_score` is superseded by this, though the underlying instinct behind it (only very relevant, obviously-indicative pairings) carries forward as the actual filtering goal, just achieved a different way. See §1.11 and §2 for what this requires building.
2. The speed threshold is a hard pass/fail gate, and `techniques/pssr.py` needs an additive, opt-in speed return so nothing else in the codebase breaks. See §1.9 and §2.
3. Fast-to-fast pairings (e.g. Venus–Moon) are a real, separate third category — not forced into stage 1 or stage 2. See §1.10a.

---

## 1. Full understanding of the technique

### 1.1 Definition, in Estadella's own words

"PSSR are the directions or progressions derived from the Precessed Solar Return (SSR), direct as well as prenatal. Its name (PSSR) comes from the acronym... Progress or Regress of the Sidereal (Precessed) Solar Return." (p. 97) Discovered by Cyril Fagan mid-20th century. Estadella is explicit that it's "basically a predictive tool," but "can also be used to confirm and even rectify a birth time" — rectification is presented as a secondary, later-developed application of a primarily predictive technique, not the technique's original purpose.

The mechanism, stated plainly: calculate the Precessed Solar Return (SSR) chart, then **direct or progress** its Moon, planets, and Lunar Node — forward (direct progression) and backward (regression) — and observe the aspects these progressed factors form with the **radical** (natal) factors: luminaries, planets, nodes, Part of Fortune, angles, and house cusps. "The aspects formed will coincide in time with the events the person will experience on a specific date." (p. 97)

The progression measure is the same as Secondary Directions/Progressions: **1 day = 1 year** (p. 98).

### 1.2 Four variants, all equally valid

You need **both** the Direct SSR (erected for the return nearest the event) **and** the Prenatal (converse/prior-year) SSR, and for each, **both** direct and converse (forward/backward) progression — four combinations in total:

- Direct SSR × direct progression
- Direct SSR × converse progression
- Prenatal SSR × direct progression
- Prenatal SSR × converse progression

"There are no differences between the directions or progressions derived from the Direct and Prenatal SSR, nor are there differences between the direct and converse aspects." (p. 99) The worked examples throughout the chapter confirm this in practice — Estadella explicitly notes he hasn't bothered to tag which of the four each hit came from, "as the interpretation does not vary" (p. 110). **All four should be checked and treated as equally valid indications**; none should be weighted above another.

### 1.3 What progresses and what doesn't

"Note that the angles or house cusps do not progress, but only the luminaries, the planets and Lunar Nodes." (p. 99) The return chart's angles/houses are fixed at their return-moment value; only Sun/Moon/planets/Node move under the 1-day-=-1-year progression. This matters for implementation: an aspect to a radix angle or house cusp is checked against the return chart's **un-progressed** angle, while an aspect to a radix planet is checked against a **progressed** planetary position.

### 1.4 Geographic reference — resolved

"SSRs do not have to be calculated for the place where the person is at the moment when the return goes into effect. They can be erected based on the birth coordinates." (p. 99) This confirms what the existing codebase already does (`PSSR_Auto` call sites consistently pass the natal `geopos`, not a per-event location) is correct, not an accidental simplification — no change needed there.

### 1.5 Orbs — resolved precisely

"The maximum orb recommended is 12 minutes of arc for all the planets and all kinds of aspects. For the Moon, a larger orb of 18' of arc is allowed (**32' in conjunctions and oppositions**)." (p. 108) This is more precise than either of the two figures floating around your codebase and the design spec (a flat 32′, or an unresolved "18–32′" range) — it isn't ambiguity between two numbers, it's two numbers for two different situations: **12′ for planet-to-planet or planet-to-angle/house where the Moon isn't one of the two points; 18′ whenever the Moon *is* one of the two points, widening to 32′ specifically when that Moon aspect is a conjunction or opposition.** This applies uniformly whenever Moon is a party to the aspect — stage 2 (§1.10) or the fast-to-fast case (§1.10a) alike; it's a property of the Moon, not of which stage the hit falls into.

One more line worth carrying forward: "these orbs in minutes are only observed with an exact or rectified birth time. If we use an inexact time, the orbs will be greater or the aspects will simply disappear." (p. 108) That's a direct statement of exactly the mechanic the whole narrowing technique depends on — orb width as a function of birth-time accuracy — not just a caveat.

### 1.6 Sun and Part of Fortune

"The Sun and the Part of Fortune are only considered receptive factors, and never as progressed factors." (p. 109) Confirmed twice more in the rectification-specific section (p. 117): the Sun can be aspected but never supplies the moving/progressed side of an aspect. This matches the existing `PSSR_Auto` exclusion of the Sun from its own progressed set.

### 1.7 Where this sits in the rectification sequence

The book confirms the sequencing your design spec already assumes, in Estadella's own narration of the Tyson case: *"Despite the fact that with Polaris a 24 hour rectification is possible, I opted for PSSR, using the planets as a first step."* (p. 120) He then takes the PSSR-narrowed window (13:30–18:30) straight into POLARIS, run against all 38 documented events, to do the finer search (p. 122–123). That's the exact PSSR → POLARIS → Primary Directions chain your design spec's Milestone 3 describes, confirmed from the primary source rather than inferred.

### 1.8 The wide-range stage — structural shape

Confirmed directly (p. 117), and matching your manual transcript's stated parameters:

> "Only use aspects where Mercury, Venus or Mars intervene, **in the return as well as in the radical chart**, in relation to the slower planets: Jupiter, Saturn, Uranus, Neptune and Pluto, as well as the Lunar Node."

"In the return as well as in the radical chart" is the "both directions" — Mercury/Venus/Mars can sit on **either** side of the aspect (as the progressed/return factor aspecting a radix slow planet, *or* as the radix factor being aspected by a progressed slow planet) — matching precisely the two structural branches already in `significators/scoring.py`'s `FAST_TO_SLOW_COMBO`:

- **Case A:** radix slow planet ↔ progressed/return Mercury, Venus, or Mars
- **Case B:** radix Mercury, Venus, or Mars ↔ progressed/return slow planet

Correction needed relative to that existing code: **the book's "fast" group for this stage is Mercury, Venus, and Mars only — the Moon is not in it.** `FAST_TO_SLOW_COMBO` currently bundles `Planet.MON` into the same fast-planet set as MAR/MER/VEN. The book treats the Moon as its own separate factor with its own stage (§1.10) — every sentence about "the directed Mercury, Venus and Mars" and the speed rule below is written with Moon explicitly excluded and discussed separately, both immediately before ("the Moon as a directed factor is effective when looking for a birth time in a period of time of 2 or 3 hours") and after this exact paragraph.

**Aspect types:** the general interpretation section says minor aspects "are also valid, although less important, serving as support for the greater aspects" (p. 109) — but every single aspect used across both full worked rectification examples (Jefferson's 7 events, Tyson's 5) is a major aspect (conjunction, sextile, square, trine, or opposition); none is minor. I'd treat majors as the operative standard for *this specific application* (matching your transcript's explicit "MAJOR ASPECT" and the existing code's restriction), with minors available as optional secondary support rather than a first-pass requirement.

**Orb:** 12′, per §1.5, confirmed independently by your transcript.

### 1.9 The critical paragraph — the speed/direction check, in full, and resolved as a hard gate

Here is the passage that grounds the speed rule (p. 117):

> "It is important to highlight that, due to the characteristics of the Moon and the different planets relative to its motion or movement, this rectification technique should be used in one way or another. For example, the Moon as a directed factor is effective when looking for a birth time in a period of time of 2 or 3 hours. If the search is extended further in time, the directed Mercury, Venus and Mars will be more effective, given that they are slower in their motion and allow the delimitation of specific aspects by PSSR.
>
> Regarding the rectification using the planets, it is important to keep the following in mind:
>
> Only use aspects where Mercury, Venus or Mars intervene, in the return as well as in the radical chart, in relation to the slower planets: Jupiter, Saturn, Uranus, Neptune and Pluto, as well as the Lunar Node. The Sun should be used only as a receptive factor. **One aspect will only be effective in this case if Mercury, Venus or Mars are not found in slow movement in the return or radical chart. One daily movement over 30' to 35' of arc is the most suitable.**"

This is a genuine, quantitative validity condition, separate from the fast/slow *category* rule in §1.8: **whichever of Mercury, Venus, or Mars is involved in a candidate hit must actually be moving at roughly 30–35′ of arc per day, at the specific moment it's being evaluated (return-side if it's the progressed factor, radical-side if it's the receiving factor), or the hit doesn't count** — regardless of the fact that it structurally belongs to the "fast" category. Confirmed again in the Jefferson worked example (p. 118): *"The motion of Venus, moving at 74' of arc per day, is appropriate for a planet directed for rectification"* — Estadella explicitly checks and reports this figure as part of validating that specific hit.

Why this matters, and why it isn't redundant with the category rule: Mercury, Venus, and Mars all station and turn retrograde periodically. Near a station, a nominally "fast" planet's apparent motion drops toward zero — for that stretch, it behaves like an outer planet: barely moving across the 24-hour window, and consequently producing a wide, weakly-discriminating "in orb" range for almost any hour you test, which is exactly the failure mode the fast/slow structural split exists to avoid in the first place. The 30–35′/day floor is the mechanism that actually enforces "is this planet behaving like a fast point right now," rather than trusting a fixed category label that doesn't account for a planet's real behavior at a specific moment.

**Resolved: this is a hard pass/fail gate, not a soft weight.** A candidate hit where the relevant Mercury, Venus, or Mars falls below the floor is excluded from range-finding entirely, the same as an aspect that's simply out of orb — consistent with the book's own wording ("will only be effective... if").

**Still open:** the book gives a range (30′–35′/day), not a single number, and an implementation needs one specific cutoff. There's no textual basis for me to pick a value in that range on my own.

This also explains, quantitatively, why the two-stage split narrows the way it does. Average daily motions: Moon ≈ 13°/day, Mercury/Venus ≈ 1–1.5°/day (when not stationing), Mars ≈ 0.5°/day, outer planets from a few arcminutes down to well under one arcminute per day. Against a 12′ orb, a planet moving at the 30–35′/day floor crosses that orb in roughly 8–10 hours; a planet moving at a typical Venus rate (~74′/day, per the worked example) crosses it in under 4 hours. Against an 18–32′ Moon orb, the Moon's ~13°/day motion crosses it in on the order of tens of minutes. That's exactly the shape the book reports as typical outcomes (§1.10) — not a coincidence, a direct consequence of the orb-to-speed ratio.

### 1.10 The Moon fine-tuning stage

Separate factor, separate stage, no fast/slow category restriction — the Moon can be checked against a planet, an angle, or a house cusp, structurally more like how angles/houses are treated elsewhere in the significator system than like a member of a fixed "fast planet" category. Estadella, citing Starkman citing Marr: "the Moon should be considered as a kind of catalyst, while the planets give color to and reflect the real significance of an event... if we have the progressed Moon opposing natal Saturn, the interpretation to be made a priori will be in line with Saturn's meaning... The Moon in conjunction with an angle is especially effective." (pp. 108–109)

This is the same shape as `significators/scoring.py`'s existing `AspectType.MOON_ANGLE_HOUSE_PRIMARY` — Moon against any recognized-significator planet, or an angle/house against any recognized-significator planet, no category constraint on what the Moon itself can be — which happens to already be the `AspectType` your batch entrypoint (`entrypoints.py`'s `rect_ver_data_create`) assigns to PSSR, just never orchestrated together with stage 1 as one deliberate two-stage pipeline. Existing stage-2 rule, not something to build fresh.

**Applies when Moon is paired with an angle, a house cusp, or a slow planet (Jupiter/Saturn/Uranus/Neptune/Pluto/Node).** Relevance is checked on the *other* point only, via `tier_score` — this is the one place in the whole design where the Compendium's synthesized aggregate is the right tool, precisely because Estadella's own framing treats the Moon like an angle rather than as a specific pairing to be looked up. **Resolved threshold:** `tier_score` on the non-Moon point, following the same spirit as the asymmetric bar you proposed for stage 1 — I'd default to requiring at least "Moderate" (≥6) on that single point, as the natural one-point analogue of "not obviously marginal," but this is a proposal for you to confirm rather than something settled by the text the way the pairwise mechanism now is.

Orb: 18′ generally, 32′ for conjunction/opposition specifically (§1.5).

**Typical outcome, stated directly (p. 116):** "Usually, the range will be 4 hours; only with the Moon one can reduce the range to 10–20 minutes." These read as *typical results of applying the technique to a real case*, not as fixed target parameters to hard-code as thresholds.

### 1.10a Fast-to-fast — a real third category, not folded into stage 1 or stage 2

Resolved: pairings between two of the personal/fast points (Mercury, Venus, Mars, and Moon when paired with one of the other three) are their own category, evaluated on their own terms rather than forced into either of the above. The Tyson worked example's "Venus 180° Moon" hit (p. 121) is the concrete instance that surfaced this — it's neither a fast-to-slow pairing (no slow planet or Node involved) nor a Moon-as-angle pairing (Moon's partner here is Venus, not an angle, house, or slow planet), and the book doesn't force it into either bucket either; it's simply listed as a valid hit for that event.

The book's own textual support for treating planet-to-same-category-planet pairings as generally valid: "The aspects between planets, like Venus progressed with natal Venus, are also valid." (p. 109) It doesn't give this a dedicated structural paragraph the way it does for fast-to-slow (§1.9) or Moon (§1.10), so the rules below are a synthesis, not a direct quote — flagged as such:

- **Membership:** any pairing of two points drawn from {Mercury, Venus, Mars, Moon}, on either side (return/progressed vs. radix), where neither point is a slow planet, angle, or house cusp. This covers Venus–Moon, but equally Mercury–Venus, Mercury–Mars, Venus–Mars, and Mercury/Mars/Venus–Moon generally, not just the one example that surfaced it.
- **Orb:** 12′ by default; 18′/32′ per §1.5 whenever Moon is one of the two points, regardless of which of these three categories the hit falls into — the orb is a property of the Moon, not of the stage.
- **Relevance:** the same Juan Combos pairwise lookup as stage 1 (§1.11), since this is still fundamentally "is this specific two-point combination attributed to this event by Estadella," and Moon is on his 14-point roster the same as everything else — there's no structural reason the pairwise mechanism should stop applying just because neither point is a "slow" planet.
- **Speed:** genuinely open. The book's 30–35′/day rule is written specifically for the fast-vs-slow case; whether it extends to require *both* points in a fast-to-fast pairing to individually clear that floor is my own extrapolation of the same underlying logic (don't credit a hit where a nominally-fast point is actually stalled), not something stated. Flagged rather than assumed either way.

### 1.11 Event relevance — resolved as two distinct mechanisms, not one

Resolved, where earlier drafts had this as a single open question: relevance is required (not optional — "it is necessary to correctly attribute a PSSR to a specific event," p. 115; Venus is chosen for a sister's death specifically because Venus "represents the sister," p. 118), but it's checked two different ways depending on what's being evaluated:

- **Planet-to-planet (stage 1, and the fast-to-fast case in §1.10a):** a direct lookup against Estadella's own Juan Combos pairwise data — does *this specific pairing* appear, with sufficiently strong wording, in his combinations list for this event. This is more faithful to the technique than routing through the synthesized `tier_score`, which mixes Juan Combos together with three other sources at the individual-*symbol* level and loses exactly the pair-specific judgment this stage actually needs.
- **Moon-as-angle (stage 2):** `tier_score` on the single non-Moon point, since Estadella's own framing here isn't about a specific pairing, it's about whether the other point is a real significator on its own.

**What the pairwise mechanism needs, concretely, and doesn't yet exist:** the raw Juan Combos prose (the "Astrological Combinations (Estadella)" section under each event in `Event_Astrology_a_Compendium_of_Aspects.md`) has never been structured into a queryable (event, point, point) table. The existing JSON compendium only kept the *aggregate count* used to derive each individual symbol's `tier_score` contribution — it doesn't preserve which specific pairs were counted. Building this is genuinely new work, not something already sitting in a file somewhere waiting to be pointed at.

**And it isn't just presence-or-absence.** I checked this against the raw text rather than assuming a pair appearing in the list is enough on its own. For Birth of Son:

- **MC–Venus:** *"We always find births of children."* — a real, strong positive statement.
- **Mars–Pluto:** *"The only occasional exception is the birth of children."*
- **Mars–Lunar Node:** *"The only exception is the birth of children."*

Mars–Pluto and Mars–Lunar Node both technically *appear* in the list — a naive "is this pair mentioned at all" lookup would treat both as valid — but the wording is telling you the opposite: this is the rare exception, not the expected pattern. A lookup that only checks presence would let through pairs the source text is actively hedging against. The structured table needs to capture strength language, not just presence, most plausibly reusing the same rough tiering (strong/frequent-type wording vs. occasional/sometimes vs. "only exception"-type wording, with the last most likely excluded rather than counted as a hit) already used elsewhere in the Compendium's own methodology for scoring the "Other" source.

**One more concrete consequence worth having explicit:** a handful of events (Demobilization or Release, Assassination or Suicide, Gambling Loss) have *no* Juan Combos data at all — Estadella never wrote combinations notes for them. Under this mechanism, those events simply produce zero stage-1 hits, always, for any candidate pairing. That's a different failure mode from "the pair exists but is weakly worded" — it's "there's nothing to look up" — and it's worth being explicit about rather than having it show up as an unexplained gap later.

### 1.12 The overlap mechanism — confirmed, not just plausible

Both full worked examples in this chapter describe the overlap/intersection mechanism explicitly, as the actual professional practice, not an approximation of one:

Jefferson (p. 119): *"These events, the directions observed and the period of time that they were in orb... indicate that the birth time was between 13:15 and 15:00 (UT)... this period of time of almost two hours has been obtained from the overlap of operative aspects in orb, which are observed in the directions for the annotated events."*

Tyson (p. 121): *"we can deduce that the birth time is between 13:30 and 18:30. This period of time of 5 hours is obtained from the overlap of the operative aspects in orb."*

Per-event range-finding, followed by literal intersection across events. One more concrete detail from the worked examples, carried directly into the algorithm: in both cases, exactly **one** representative aspect is used per event, not a sum of every qualifying aspect for that event.

### 1.13 What's excluded — PSSR 2, named explicitly and precisely

Estadella devotes a full section to this, titled "A variant: PSSR 2" (pp. 111–113): "The progressed factors form aspects with the same progressed factors of the return, in direct or converse movement. These aspects are not as important as those that involve the radical factors in the original version, but they can also be taken into account." He cites the same two sources as the primary documentation of this variant — Fagan & Firebrace's *Primer of Sidereal Astrology*, and Alexander Marr's own *Prediction I*. Fagan & Firebrace's own verdict, quoted by Estadella: *"the aspects to the radical seem to give more accurate results"* than PSSR 2 (p. 112) — direct textual support for treating radix-to-PSSR (§1.8–1.10a) as the primary technique and PSSR 2 as correctly out of scope for this task.

### 1.14 Adjacent material, noted but not needed here

PSSR applied to an Epoch (conception) chart, a "Dual Test" crossing Radix and Epoch directions (Marr's own caution: keep them separate, since combined volume "can confuse or complicate the interpretation," p. 126), a secondary variant using Mercury or Venus returns instead of the Solar Return ("its importance is much less significant," p. 126), and a harmonic/malefic-benefic interpretive nuance for reading what a validated hit *means* (p. 109) — none of these bear on whether a candidate aspect is structurally valid, which is all this algorithm needs to decide.

---

## 2. How this fits into the existing codebase

| Piece | Location | Status |
|---|---|---|
| PSSR calculation | `techniques/pssr.py` (`PSSR_Auto`) | Reuse as-is for position; **needs extending for speed** — see below. |
| Uniform construction | `techniques/base.py`'s `construct_technique()` via `TechniqueType.PSSR` | Reuse — PSSR is one of the five dispatcher-unified techniques. |
| Aspect retrieval | `.get_str_aspects()` | Reuse — Phase 6 unified construction, not getter names. |
| Stage-1 / fast-to-fast structural shape | `AspectType.FAST_TO_SLOW_COMBO` | Reuse the *shape* (Case A/B), with the Moon dropped from the fast-planet set (§1.8) and the speed gate added (§1.9) — the relevance check is no longer this function's concern at all (§1.11 moves it to a new pairwise lookup). |
| Stage-2 structural shape | `AspectType.MOON_ANGLE_HOUSE_PRIMARY` | Reuse directly — already shaped like "Moon as angle"; relevance source moves from the deprecated `PRIMARY_RULES`/`planet_accept` to Compendium `tier_score`. |
| Candidate-time stepping | `batch/grid_engine.py`'s `generate_grid_angular_aspects(..., increment_seconds, ...)` | Reuse the parameterized-step pattern, not `generate_hourly_datetimes`'s hardcoded 5-minute step. |
| Aspect-string parsing | `abbreviate_aspect_string`, `categorize_aspect`, `get_aspect_str_orb` | Reusable patterns for extracting orb/point names. |

**Two concrete, new build requirements this round of decisions adds, neither of which exists in any form yet:**

1. **A structured Juan Combos pairwise lookup table**, per §1.11 — parsing the "Astrological Combinations (Estadella)" prose section of `Event_Astrology_a_Compendium_of_Aspects.md`, per event, into a queryable (event, point, point) → validity mapping that captures wording strength, not just presence. This is genuinely new — the existing `compendium_scoring_export_v2.json` only preserves the aggregate count derived from this text, not the individual pairs. Natural home: alongside wherever the existing Compendium loader/lookup lives (`significators/compendium.py`, per the placement recommendation below), as a sibling data source to the symbol-level `tier_score` lookup, not a replacement for it.

2. **An optional, additive speed return from `techniques/pssr.py`.** Per your plan: the PSSR technique needs an opt-in flag (default off, so every existing caller's behavior and output shape is completely unaffected) that, when set, returns planetary daily motion alongside the existing position/aspect data — no new method, no change to the default contract, nothing else in the codebase needs to change or even be aware this exists unless it asks for it. Whether the underlying `swe.calc`-level call already computes speed internally (Swiss Ephemeris typically does, when the speed flag is requested) and is simply discarding it, versus needing new computation, isn't something I can confirm without the file itself — worth checking early, since it changes whether this is a small plumbing change or a slightly larger one. One implementation asymmetry worth having on record before that work starts: natal Mercury/Venus/Mars speed is fixed per person and can be computed once, independent of which event or candidate time is being tested; return-chart-side speed has to be recomputed at every grid point, since the return moment itself shifts as the candidate time sweeps. Worth designing the opt-in around that distinction rather than treating both as the same cost.

Everything else from earlier drafts' inventory stands: the `EventType` ↔ Compendium-title mapping still needs to exist (Appendix B of the design spec's index-mismatch warning is unaffected by any of this round's decisions), Phase 7's global-state elimination is still pending so new code should avoid module-level state from the start, and Phase 9's structured-Aspect codec still doesn't exist so hand-parsing is unavoidable for now. Placement recommendation is unchanged: Compendium/mapping/pairwise-lookup logic beside `significators/`, orchestration in a new module rather than folded into `grid_engine.py`.

---

## 3. Possible solution approaches

### 3.1 Sampling the 24-hour window

A fine discrete grid (on the order of 1-minute steps) is a faithful, much simpler stand-in for continuous scanning at this stage — the orb-to-speed math in §1.9 shows even the Moon's narrowest windows run to tens of minutes, comfortably above a 1-minute sampling floor. Prefer querying instantaneous speed directly from the ephemeris call at each grid point over finite-differencing between adjacent samples — cheaper and exact, and finite-differencing would need a resolution fine enough to see stationary points clearly, a stricter requirement than position-sampling alone needs.

### 3.2 Scoring and aggregation: intersection, hardened rather than replaced

The core mechanism is confirmed (§1.12): per-event range-finding, then literal intersection across events. What I'd still add as engineering on top of a confirmed-correct core:

- **The speed gate is a hard filter** (§1.9), applied before range-finding, same as an out-of-orb aspect would be excluded.
- **Orb tightness as a tiebreaker**, not a replacement for intersection, where the raw overlap doesn't collapse cleanly.
- **A safety margin** around the raw intersection boundary before handing a window downstream — specifically because the design spec calls out silently excluding the true time as the one failure mode worse than a slow search.

### 3.3 Multiple indications per event, and events with none

**Confirmed by the worked examples:** one representative aspect per event, not a sum of every qualifying one (§1.12). If an event has more than one structurally valid, relevance-gated, speed-gated hit, it should still only contribute once to the intersection.

**Events with no valid indication:** normal, expected — including, now explicitly, the events with zero Juan Combos data at all (§1.11). Worth surfacing the count of events that produced zero hits alongside the final window, since a result built on 5 corroborating events out of 30 is meaningfully thinner evidence than one built on 20 out of 30, even if the resulting window looks identical.

### 3.4 Two-stage joint sweep vs. two independent scans

One sweep computing full PSSR aspect data (all four variants, all planets including Moon, speed included when requested) at each grid point once, with stage-1, fast-to-fast, and stage-2 acceptance all evaluated from that same computed data — stage 2 restricted to whatever window stage 1 (plus fast-to-fast) leaves standing.

### 3.5 Relevance gating — resolved, not a design choice anymore

No longer an open question at the mechanism level (§1.11): pairwise Juan Combos lookup for any planet-to-planet case (stage 1 and fast-to-fast alike), `tier_score` for Moon-as-angle (stage 2). What remains is calibration, not mechanism selection: the exact strength-language cutoff for the pairwise table (§1.11), and the exact `tier_score` floor for stage 2 (§1.10 proposes ≥6, unconfirmed).

---

## 4. Recommended approach

1. **One fine discrete sweep** across the 24-hour window, computing all four PSSR variants at each grid point, via `construct_technique(TechniqueType.PSSR, ...)` → `get_str_aspects()`, requesting speed via the new opt-in flag once that exists.
2. **Per event, per grid point, evaluate stage 1 and fast-to-fast together:** major aspect, correct planet grouping per §1.8/§1.10a, 12′ orb (18′/32′ if Moon involved), the relevant Mercury/Venus/Mars speed at or above the chosen cutoff within 30–35′/day, and the specific pairing present with strong-enough wording in the Juan Combos pairwise table.
3. **Evaluate stage 2 separately:** Moon against an angle/house/slow planet, 18′/32′ orb, the other point at or above the chosen `tier_score` floor.
4. **Find each event's operative time range(s)** from where a qualifying hit (any of the above three) stays valid, then **intersect across events**, one range per event regardless of how many aspects qualify.
5. **Select the surviving window with a deliberate safety margin**, not the razor-thin literal intersection boundary.
6. **Report per-event contributions alongside the final window** — which events fired, at what orb, through which mechanism (stage 1 / fast-to-fast / stage 2), and which events (including the Juan-Combos-empty ones) contributed nothing.

### What's still open

- **The exact speed cutoff within 30–35′/day** (§1.9) — no textual basis to pick one.
- **Whether fast-to-fast pairings also require both points to individually clear the speed floor** (§1.10a) — my own extrapolation, not stated in the text, flagged rather than assumed.
- **The exact strength-language cutoff for the Juan Combos pairwise table** (§1.11) — which wording counts as "good enough," beyond the clear-cut "only exception" case that should plainly be excluded.
- **The exact `tier_score` floor for stage 2** (§1.10) — proposed at ≥6 by analogy to the asymmetric bar you described for stage 1, not yet confirmed.
- **How many corroborating events should be considered "enough" to trust a resulting window**, given both worked examples used a small, hand-picked, unambiguous set (7 and 4–5 events respectively) rather than a person's full event list.

Still no code below this line, per your original instruction — this is still analysis and proposal. Let me know where you'd push back, particularly on the still-open items above.
