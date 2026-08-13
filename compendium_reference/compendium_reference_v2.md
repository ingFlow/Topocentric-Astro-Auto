## Document Purpose

This document does **not** reproduce the source compendium. It synthesizes it: for each of the
40 event types, the four underlying sources have been parsed, cross-referenced, and scored on a
single deterministic 0–10 scale, so that any candidate aspect can be looked up and compared
without re-reading the original text. Orb, applying/separating, dignity, timing, and chart
context are deliberately **out of scope** throughout — only the symbolic identity of the two
points involved in an aspect is evaluated, exactly as requested.

This is a living reference: sections 1–6 for each event are generated from a single
underlying scoring table (also usable directly by software — see §3.7), so the same aspect
will always receive the same evaluation, and updates to the underlying data will propagate
consistently across every section.

**This document reports each symbol's own tier_score independently, in full, and stops there.**
It is a per-symbol reference, not an aspect calculator: it does not combine two symbols' scores
into a single aspect-level number under any formula (MIN, AVERAGE, or otherwise). A consumer
that needs an aspect-level judgment looks up both points' scores here and combines them
elsewhere, using whatever rule fits its own purpose.

## The Four Sources

| Source | Author | Nature of the material |
|---|---|---|
| **POLARIS** | Isaac Starkman | A curated **Primary / Secondary** significator list per event — the most structured and most conservative of the four sources. |
| **Juan Combos** | Juan Estadella | Prose notes organized as pairwise combinations ("AS-Sun / Sun-AS: ...") tested against a **fixed roster of 14 points** (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune). |
| **Other** | Alexander Marr | Short-form symbolic notes in prose — Marr's own stated rule of thumb for the event, usually one to four sentences. |
| **Marr Aspects** | Alexander Marr | **Not a rule statement** — a set of worked example directions drawn from named, real natal charts, demonstrating the event's signature empirically. Figures quoted from this source are observed frequencies across examples, not authorial claims. |

## Notation & Symbol Legend

The compendium's own legend (reproduced in summary, not verbatim) defines:

- **R–R** = Radix directed to Radix; **R–E** = Radix to Prenatal Epoch; **E–E** = Epoch to Epoch;
  **E–R** = Epoch to Radix. *(Ignored in this document — see Scope, below.)*
- **d** = direct, **c** = converse (primary directions); **p** = progressed, **re** = regressed
  (secondary directions). *(Also ignored here — see Scope.)*
- Orbs are given in minutes of arc; `**` marks directions "very characteristic of the event," `*`
  marks directions "which support the outcome ... and its circumstances." *(Ignored here —
  see Scope.)*
- Planets: SUN, MON (Moon), MER (Mercury), VEN (Venus), MAR (Mars), JUP (Jupiter), SAT (Saturn),
  URA (Uranus), NEP (Neptune), PLU (Pluto).
- Angles: ASC/AS (Ascendant), MC (Midheaven), DESC/DS (Descendant), IC (Imum Coeli) — the 1st,
  10th, 7th and 4th house cusps respectively.
- House cusps 2, 3, 5, 6, 8, 9, 11, 12 are given as Roman numerals (II, III, V, VI, VIII, IX, XI, XII).
- Nodes: ANO (Ascending/North Node), DNO (Descending/South Node); POLARIS uses **NNO** for the
  same North Node; Marr's worked examples also use a plain **NOD** where the pole isn't specified;
  Juan Combos always says **"Lunar Node"** without specifying a pole.
- **PF / POF / Pars** all denote the **Part of Fortune** (variant spellings found across the source).
- **†** (this document's own mark, not the compendium's) — appended to a symbol's "Sources"
  cell in every Evaluation Rules table wherever that symbol reaches full agreement among the
  sources able to address it (§3.3 defines "applicable"; §3.4 defines the mark itself in full).
  **† indicates full agreement among applicable sources only — it does not indicate the strength
  of that agreement, which may still be low.** A daggered symbol can carry a low tier_score if
  the applicable sources agreed only weakly (e.g. every one of them scored it 1 rather than 2);
  always read the tier_score and the per-source 0/1/2 values next to a † mark, not in place of
  it — see §3.4 for the full explanation and the Evaluation Rules table footnote on every event
  that uses the mark.

A small number of source-side OCR/typo variants were normalized during extraction (e.g. `UR`,
`URR` → Uranus; `MRR` → Mercury; `HSC` → Ascendant; `OESC` → Descendant) — see §3.6.

## Methodology

### §3.1 Scope

Per the brief, only the **symbolic identity** of the two points in an aspect is evaluated:
planets, house cusps, angles, nodes, and other named points (e.g. the Part of Fortune). Orb,
applying/separating motion, dignity, timing, and broader chart context are excluded from every
score in this document, regardless of how prominently the original source emphasizes them.

### §3.2 Per-source scoring (0 / 1 / 2)

Each source produces an independent 0–2 score for a given point, in a given event, using rules
specific to that source's own structure:

- **POLARIS** — 2 if the point is in the event's **PRIMARY** list, 1 if in **SECONDARY**, 0 if
  named in neither.
- **Juan Combos** — of all the pairwise combinations catalogued for the event, let *k* = the
  number of those combinations naming this point and *n* = the event's total catalogued
  combinations (`n_juan_combos_total`). Score 0 if *k* = 0; otherwise score 2 or 1 according to
  the **sample-size-scaled rule in §3.2a** (this replaces the flat 35%-of-total cutoff used in
  earlier drafts of this document).
- **Other** — 2 if the point is named with a strong qualifier in its own sentence (e.g. "mainly,"
  "frequent," "always," "usually"), 1 if named without such a qualifier (or with a soft qualifier
  like "sometimes"/"occasionally"), 0 if not named at all.
- **Marr Aspects** — of all the worked example charts for the event, let *k* = the number of
  examples featuring this point at least once and *n* = the event's total worked examples
  (`n_marr_examples_total`). Score 0 if *k* = 0; otherwise score 2 or 1 according to the same
  **sample-size-scaled rule in §3.2a**.

A score of **0** means "checked, not found." A score of **None** (rendered "— (out of scope /
no data)" in the tables) means the source could not have addressed this point at all — see §3.3.

### §3.2a Sample-size-scaled threshold for Juan Combos and Marr Aspects (replaces the flat 35% cutoff)

**The problem with a flat percentage cutoff.** The compendium's 40 events vary enormously in how
much underlying data backs each percentage-based source: `n_juan_combos_total` ranges from 0
(several events) up to 72, and `n_marr_examples_total` ranges from 1 up to 306. A flat rule of
"score 2 if the point appears in ≥ 35% of the total" behaves very differently at these extremes.
At *n* = 1 — which occurs for real, e.g. *Graduation or Publication*'s Juan Combos total, and
*Gambling Gain*/*Gambling Loss*'s Marr Aspects totals — a single combination or example is either
0% or 100% of everything catalogued; there is no way for a flat percentage to distinguish "this
appeared once, out of one" from "this is a well-established, majority pattern." At *n* = 72 the
same 35% line requires roughly 25 independent hits, a much more demanding bar. Picking any
*single* flat percentage — 35%, or any other fixed value — only relocates this problem: whatever
number is chosen will still be too permissive at the smallest sample sizes in this corpus and,
comparatively, more conservative at the largest. The fix has to make the **required share of
supporting evidence itself a function of *n***, not just apply the same fraction everywhere.

**The rule.** For a candidate point with *k* occurrences out of *n* total (catalogued
combinations, for Juan Combos; worked examples, for Marr Aspects):

1. If *k* = 0, score **0**.
2. Otherwise, score **2** if *both* of the following hold, and score **1** otherwise:
   - **Absolute floor:** *k* ≥ 3. Fewer than three occurrences cannot be read as a recurring
     pattern rather than an incidental one, regardless of what percentage of a small *n* that
     represents — this is a floor on the amount of raw evidence, a separate axis from the
     percentage check below, and it is what makes *n* = 1 and *n* = 2 samples structurally unable
     to reach score 2 (no number of hits at those sample sizes can clear the floor).
   - **Adjusted share check:** the **Wilson score interval lower bound** of *k*/*n*, at a modest
     confidence level (z = 1.04, roughly an 85%-confidence one-sided bound — chosen as a sensible
     dampener for a descriptive corpus, not a clinical-trial-grade threshold), must be at least
     0.35. The Wilson lower bound is the standard statistical tool for asking "how far can I
     trust an observed proportion, given how many observations it's based on" — it shrinks toward
     the raw observed fraction *k*/*n* as *n* grows, and pulls sharply below that fraction when
     *n* is small, which is exactly the "how much can one combination swing the result" property
     the flat rule was missing. Formally, with *p̂* = *k*/*n*:

     ```
     center = p̂ + z²/(2n)
     margin = z · sqrt( p̂(1-p̂)/n + z²/(4n²) )
     denom  = 1 + z²/n
     Wilson lower bound = (center − margin) / denom
     ```

**What this looks like in practice.** The table below shows the minimum *k* (and the equivalent
share) needed to reach score 2 at representative values of *n* actually occurring in this
compendium, alongside what the old flat-35% rule would have required:

| *n* | *k* needed (new rule) | Equivalent share | *k* the old flat-35% rule needed |
|---|---|---|---|
| 1 | *unreachable* | — | 1 (100%) — score 2 available from a single hit |
| 2 | *unreachable* | — | 1 (50%) — score 2 available from a single hit |
| 4 | 3 | 75% | 2 (50%) |
| 8 | 5 | 63% | 3 (38%) |
| 16 | 8 | 50% | 6 (38%) |
| 18 | 9 | 50% | 7 (39%) |
| 45 | 20 | 44% | 16 (36%) |
| 54 | 23 | 43% | 19 (35%) |
| 72 | 30 | 42% | 26 (36%) |

At the smallest sample sizes in the corpus (*n* = 1, 2), score 2 is now **structurally
unreachable** regardless of *k* — a single or double data point cannot establish a majority
pattern, which is the correct and intended behavior, not a bug or an oversight. As *n* grows past
roughly 50–70 (the range most events actually fall in), the rule converges toward a required
share in the low-to-mid 40s, slightly more conservative than the old flat 35% but close to it —
this is deliberate: the rule is a genuine reweighting of confidence by sample size, not a
relabeled version of the old cutoff, and it is expected to land somewhat above 35% even at the
corpus's largest sample sizes, not to reproduce 35% exactly once *n* is "big enough."

**Scope of this change.** This replaces the flat 35% cutoff **for both** Juan Combos (*f*) and
Marr Aspects (*g*), since both use the identical percentage-of-total structure and both have
real, observed cases in this corpus at *n* = 1 (Juan Combos: *Graduation or Publication*, and by
extension the *n* = 0 "marked None" events; Marr Aspects: *Gambling Gain*, *Gambling Loss*).
Applying the fix to only one of the two would leave the identical problem live in the other.

**This rule changes 120 individual per-source scores** across the corpus relative to the old flat
35% cutoff — every one of them a downgrade from 2 to 1 (never the reverse, since the new rule is
strictly more conservative than the flat cutoff at every *n*), concentrated at the low end of the
sample-size range as intended. `tier_score` is recomputed from these corrected per-source values
via §3.4, below.

### §3.3 Structural scope limits (no data ≠ no support)

Two scope limits are true across the **entire** compendium, confirmed empirically against every
event rather than assumed:

- **Juan Combos** never once references the Descendant, the IC, or any minor house cusp (2nd,
  3rd, 5th, 6th, 8th, 9th, 11th, 12th) in any of its 1,341-plus catalogued combinations. Its
  method is a fixed pairwise roster (Ascendant, Midheaven, the ten planets, the Lunar Node, the
  Part of Fortune) — it is mechanically incapable of naming these points, for any event. Silence
  here is **not** a judgment that they're irrelevant.
- **POLARIS** never once uses the Part of Fortune, and never differentiates a South Node
  specifically (it uses a single North/Ascending Node designation, "NNO," throughout).

Wherever a point falls outside a source's structural scope for **every** event in the
compendium, that source is scored `None` (excluded from the numerator and denominator of
`tier_score` — see §3.4 — rather than 0), and the point-and-event-specific "Other" and "Marr
Aspects" sources — which have no such fixed roster — are left to speak for it instead.

### §3.4 Composite tier (tier_score, 0–10)

**tier_score is a proportional, source-weighted score, not a breadth-based one.** For a given
point and event:

```
tier_score = 10 × ( Σ applicable per-source values ) / ( 2 × number of applicable sources )
```

where "applicable" sources are the ones with a numeric 0/1/2 value from §3.2/§3.2a — any source
scored `None` under §3.3 is excluded from **both** the numerator and the denominator, not treated
as a 0. The raw result is then **rounded to the nearest of the six existing tier labels**
(0, 2, 4, 6, 8, 10); at an exact midpoint between two labels (a raw score of 1, 3, 5, 7, or 9 on
the underlying 0–10 scale), this document rounds **up**, toward the higher tier, for a single,
consistent, stated convention rather than leaving ties unresolved.

| Tier (0–10) | Label |
|---|---|
| **10** | Very Strong (Core Symbol) |
| **8** | Strong Symbol |
| **6** | Moderate (Relevant Symbol) |
| **4** | Weak (Occasional Symbol) |
| **2** | Very Weak (Speculative Symbol) |
| **0** | No Support |

**Why proportional rather than breadth-based.** An earlier version of this scoring scheme set
the tier from *breadth* alone — the count of applicable sources that scored a point 1-or-2, with
per-source intensity used only as a tie-breaker when exactly one source applied. That approach
could not distinguish a symbol where every applicable source agreed *strongly* (all scoring 2)
from one where every applicable source agreed only *weakly* (all scoring 1) — both received the
same tier under breadth alone, provided the *count* of agreeing sources was the same. The
proportional formula folds both breadth (how many sources speak to a point) and intensity (how
strongly each one does) into a single number, so full agreement at low intensity and full
agreement at high intensity are no longer scored identically. This means a symbol can have
**every** applicable source supporting it and still land at a middling tier if that support was
uniformly weak — see the Job Promotion event's 2nd House cusp for a real, worked instance of
exactly this pattern in this compendium.

**Structural ceiling and the † mark.** Because of §3.3, a house cusp (other than the 1st/10th) or
the Descendant can *never* have Juan Combos as an applicable source, and the Part of Fortune or
South Node can never have POLARIS as one — the number of sources that *could* apply to these
points is permanently capped below 4, for every event in the compendium. The † mark is reserved
for exactly this situation: a point whose number of applicable sources is reduced below the full
four (3 of 3, 2 of 2, or 1 of 1 possible), where **every** one of those applicable sources scores
it 1 or 2 — i.e. there is no disagreement among the smaller panel that could weigh in at all. A
point with all 4 sources applicable is **never** marked †, even when all four agree, because
there is no reduced panel to flag in that case — a plain, unmarked 4-of-4 already says everything
the mark would add.

**† is a statement about breadth of agreement, not about strength.** It certifies that no
applicable source came back silent or negative on this point — nothing more. It does **not**
certify that the sources which did weigh in did so strongly, and it is not a shorthand for a high
tier_score. A symbol can be daggered and still carry a low or middling tier_score if the
applicable sources that agreed did so only weakly (each scoring 1 rather than 2) — this is
expected under the proportional formula and is not a contradiction; read the tier_score and the
per-source 0/1/2 values next to any † mark, not in its place. (An earlier version of this
document described † only as a "structural ceiling — not weaker evidence than an unmarked 10,"
which read as a strength claim; that phrasing has been corrected throughout, including in every
per-event footnote, because it is not reliably true under the proportional formula.)

### §3.5 No aspect-level fusion

This document reports each symbol's own tier_score, independently, and stops there — it is a
per-symbol reference, not an aspect calculator. **There is no formula in this document, of any
kind, that combines two symbols' scores into a single aspect-level number.** An earlier version
used a MIN()-based "weakest link" rule to produce an aspect-level score from a pair of points;
that rule (and the worked walkthroughs built around it) has been removed entirely and is not
replaced by AVERAGE or any other fusion function. A consumer that wants an aspect-level judgment
looks up both points' tier_score values here — independently, in full — and combines them under
whatever rule suits its own purpose; that combination step is out of scope for this document.
Section 6 of each event demonstrates this as a side-by-side, non-combining lookup.

### §3.6 Known data-quality notes

- The source PDF's Marr Aspects tables are worked examples drawn from real named charts; a
  small number of entries (well under 1% of the corpus) use non-standard notation the parser
  could not fully resolve (e.g. an orb rendered as a date fragment) — these lines are skipped
  rather than guessed at.
- One abbreviation, **"SBT,"** appears three times (all within *Death of Mother or Grandmother*)
  and is not defined anywhere in the compendium's own legend. It has been excluded from scoring
  rather than guessed at.
- The *Success or Elected* chapter's Marr Aspects table contains a handful of entries (e.g. two
  concerning a criminal investigation into a third party) that appear topically mismatched to the
  event; given the sample size (306 examples), these do not materially affect the frequency-based
  scoring and have been left in place rather than edited out, in keeping with the brief's
  instruction not to invent or silently alter the source material.
- Qualifier-strength detection in the "Other" source (§3.2) is evaluated per sentence. Marr's
  short-form notes sometimes pack a primary planet ("mainly with Venus") and a secondary one
  ("sometimes assisted by Mars") into the same sentence; both may be scored at the same strength
  in that edge case. Treat the strong/weak distinction in "Other" as directional, not exact.
- Three lunar-node variants appear across the sources (North/Ascending, South/Descending,
  pole-unspecified). Source Summaries report them separately; the Consolidated Symbolism and
  Scoring tables merge them into one **"Lunar Node"** entry per event, scored from whichever
  variant(s) each source actually uses.
- **Sample size varies enormously across events**, for both Juan Combos (`n_juan_combos_total`:
  0–72) and Marr Aspects (`n_marr_examples_total`: 1–306), and this is now surfaced explicitly —
  both fields are attached to **every symbol record** (not stated once at the event level and
  left for a reader to track down), and every event whose total for either source falls below 10
  carries an explicit low-sample-size note in its Source Summary. A tier_score of 8 resting on
  `n_marr_examples_total` = 1 and a tier_score of 8 resting on `n_marr_examples_total` = 65 are
  both, correctly, tier 8 — the sample-size fields are what let a reader or a downstream system
  tell those two situations apart; they are not folded into tier_score itself, and tier_score is
  not adjusted or discounted based on them anywhere in this document.

### §3.7 Machine-readable companion

Every number in this document is generated from a single structured scoring table (point ×
event → {POLARIS, Juan Combos, Other, Marr Aspects, sources_supporting, sources_applicable,
at_structural_ceiling, tier_score, n_juan_combos_total, n_marr_examples_total}). A JSON export of
that table is available alongside this document for direct programmatic use, so software does
not need to parse the Markdown tables below. The per-symbol sample-size fields
(`n_juan_combos_total`, `n_marr_examples_total`) are present on **every** symbol record in the
export, event-level constants repeated at the symbol level so no downstream consumer needs to
join against a separate table to know how much data a given score rests on.

## How To Use This Document — Worked Walkthrough

Take the aspect from the brief: **Venus sextile 4th House cusp**, evaluated against
**Death of Mother or Grandmother** (the compendium's exact heading for "Death of Mother").

1. Open that event's section below and find **Venus** and **Imum Coeli (4th House cusp)** in its
   Evaluation Rules table.
2. **Venus**: look up its row — POLARIS, Juan Combos, Other, and Marr Aspects each contribute
   their 0/1/2 value (or `None` if structurally inapplicable, per §3.3); `tier_score` is read
   directly from the table, already computed under §3.4's proportional formula from those four
   values, along with `n_juan_combos_total` and `n_marr_examples_total` for that event.
3. **Imum Coeli / 4th House cusp**: same lookup. Juan Combos is `None` here (§3.3 — Juan Combos
   never addresses the IC), so its tier_score is computed from only the three sources that could
   apply. If all three of those support it, the row carries a **†** — full agreement among the
   sources able to speak to an angle other than the Ascendant/Midheaven — alongside whatever
   tier_score that agreement actually produced (which may be high or middling; the † mark alone
   doesn't say which — see §3.4).
4. **Both scores are read independently.** This document does not combine Venus's tier_score and
   the IC's tier_score into a single aspect-level number (§3.5) — the aspect type (sextile) and
   orb (4′) given in the brief play no role here either, per §3.1. A consumer that wants a single
   aspect-level judgment for this pairing takes both tier_score values away and combines them
   under its own rule; that step happens outside this document.
5. To compare against another candidate — say, **Neptune square Midheaven** for the same event —
   look up Neptune's tier_score and the Midheaven's tier_score the same way, independently. There
   is no ranking of "aspects" here, only a side-by-side lookup of each candidate point's own
   score — see §6 of each event for a worked demonstration of this side-by-side pattern.

## Index of Events

1. [Birth of Brother](#1-birth-of-brother) — *Birth — Sibling (male)*
2. [Birth of Sister](#2-birth-of-sister) — *Birth — Sibling (female)*
3. [Birth of Son](#3-birth-of-son) — *Birth — Child (male)*
4. [Birth of Daughter](#4-birth-of-daughter) — *Birth — Child (female)*
5. [Birth of Grandson](#5-birth-of-grandson) — *Birth — Grandchild (male)*
6. [Birth of Granddaughter](#6-birth-of-granddaughter) — *Birth — Grandchild (female)*
7. [Marriage for Male](#7-marriage-for-male) — *Union — Native's own marriage (male chart)*
8. [Marriage for Female](#8-marriage-for-female) — *Union — Native's own marriage (female chart)*
9. [Child’s Marriage](#9-childs-marriage) — *Union — Native's child marries*
10. [Positive Travel](#10-positive-travel) — *Travel — favorable journey*
11. [Positive Travel Overseas](#11-positive-travel-overseas) — *Travel — favorable journey abroad*
12. [Success or Elected](#12-success-or-elected) — *Achievement — professional success, honors, election*
13. [Graduation or Publication](#13-graduation-or-publication) — *Achievement — education / publishing milestone*
14. [Move Home](#14-move-home) — *Domestic — change of residence*
15. [Job Promotion](#15-job-promotion) — *Achievement — career advancement*
16. [Demobilization or Release](#16-demobilization-or-release) — *Liberation — release from service or confinement*
17. [Gambling Gain](#17-gambling-gain) — *Fortune — winning at chance*
18. [Army Promotion](#18-army-promotion) — *Achievement — military advancement*
19. [Death of Father or Grandfather](#19-death-of-father-or-grandfather) — *Death — Family (male elder)*
20. [Death of Mother or Grandmother](#20-death-of-mother-or-grandmother) — *Death — Family (female elder)*
21. [Death of Son](#21-death-of-son) — *Death — Child (male)*
22. [Death of Daughter](#22-death-of-daughter) — *Death — Child (female)*
23. [Death of Wife or Female Friend](#23-death-of-wife-or-female-friend) — *Death — Partnership (female)*
24. [Death of Husband or Male Friend](#24-death-of-husband-or-male-friend) — *Death — Partnership (male)*
25. [Death of Brother](#25-death-of-brother) — *Death — Family (sibling, male)*
26. [Death of Sister](#26-death-of-sister) — *Death — Family (sibling, female)*
27. [Death](#27-death) — *Death — the native's own mortality*
28. [Assasination or Suicide](#28-assasination-or-suicide) — *Death — violent or self-inflicted*
29. [Failure or Defeat](#29-failure-or-defeat) — *Adversity — setback, disgrace, loss of standing*
30. [Arrest](#30-arrest) — *Legal — imprisonment / confinement*
31. [Losses](#31-losses) — *Material — financial setback*
32. [Divorce or Separation](#32-divorce-or-separation) — *Relationship — rupture of partnership*
33. [Resign or Retire](#33-resign-or-retire) — *Career — voluntary departure*
34. [Mobilization](#34-mobilization) — *Military — call-up to service*
35. [Accident](#35-accident) — *Physical — mishap or injury*
36. [Hospitalization or Illness](#36-hospitalization-or-illness) — *Health — medical crisis*
37. [Violence](#37-violence) — *Physical harm — assault, injury inflicted by others*
38. [Intrigue](#38-intrigue) — *Deception — gossip, scandal, hidden dealings*
39. [Gambling Loss](#39-gambling-loss) — *Fortune — loss through chance or speculation*
40. [Negative Travel](#40-negative-travel) — *Travel — unfavorable journey*

---

## 1. Birth of Brother

*Category: Birth — Sibling (male)*

### 1. Event Overview

Marks the arrival of a brother into the native's family. The sources converge on Mercury and the 3rd house cusp (the traditional house of siblings) as the core signature, with the IC occasionally reinforcing the domestic/family angle.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Mercury, Jupiter, Sun, Moon, Venus, Mars, Uranus, Pluto
- Houses/Angles mentioned: Descendant (7th House cusp), Imum Coeli (4th House cusp), 3rd House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Mercury, Jupiter, Descendant (7th House cusp), Imum Coeli (4th House cusp), 3rd House cusp
- **Secondary**: Sun, Moon, Venus, Mars, Uranus, Pluto, North Node (Ascending)
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Mercury (10/45), Jupiter (10/45), Sun (9/45), Moon (9/45), Lunar Node (pole unspecified) (8/45), Venus (8/45), Uranus (7/45), Ascendant (1st House cusp) (6/45), Midheaven (10th House cusp) (6/45), Pluto (6/45)
- Total pairwise combinations catalogued for this event: 45
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: Marks the arrival of a brother into the native's family. The sources converge on Mercury and the 3rd house cusp (the traditional house of siblings) as the core signature, with the IC occasionally reinforcing the domestic/family angle.
- Points referenced: Mercury (strong), Imum Coeli (4th House cusp) (weak), 3rd House cusp (weak)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **11 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: 3rd House cusp (10/11, 91%), Sun (7/11, 64%), Jupiter (7/11, 64%), Moon (6/11, 55%), Mercury (6/11, 55%), Imum Coeli (4th House cusp) (6/11, 55%), Venus (6/11, 55%), Uranus (6/11, 55%)
- Node detail: North Node in 2, South Node in 0, unspecified-pole Node in 1 of 11 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Mercury** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Imum Coeli (4th House cusp)** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **3rd House cusp** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **Sun** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Moon** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Venus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Jupiter** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Uranus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Descendant (7th House cusp)** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Mars** — supported by POLARIS, Juan Combos, Marr Aspects (score 4/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Pluto** — supported by POLARIS, Juan Combos (score 2/10)
- **Ascendant (1st House cusp)** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Midheaven (10th House cusp)** — supported by Juan Combos, Marr Aspects (score 2/10)
- **5th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Mercury is corroborated by every source able to speak to it, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Sun, Moon, Venus, Mars, Jupiter, Uranus, Imum Coeli (4th House cusp), 3rd House cusp, Lunar Node (North/South/unspecified) are supported by three of the four sources. 2 of these (Imum Coeli (4th House cusp), 3rd House cusp) sit at the structural ceiling for their symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Pluto, Ascendant (1st House cusp), Midheaven (10th House cusp), Descendant (7th House cusp), Part of Fortune.

**Speculative / source-specific symbolism.** 5th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** Ascendant (1st House cusp) (in 4/11 example charts, 36%) recur in a substantial share of Marr's worked examples without being singled out in POLARIS's Primary/Secondary list. This is not a direct contradiction — POLARIS's list is a short, deliberately curated selection rather than an exhaustive one, and no case was found anywhere in the compendium of a POLARIS-Primary symbol being *absent* from a substantial Marr Aspects sample. Read it as an emphasis gap, not a disagreement about relevance.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Mercury | Primary | 1 · 10/45 combos | Strong emphasis | 2 · 6/11 charts (55%) | 4/4 | 45 / 11 | 8 | Strong Symbol |
| Imum Coeli (4th House cusp) | Primary | — (out of scope) | Mentioned | 2 · 6/11 charts (55%) | 3/3 † | 45 / 11 | 8 | Strong Symbol |
| 3rd House cusp | Primary | — (out of scope) | Mentioned | 2 · 10/11 charts (91%) | 3/3 † | 45 / 11 | 8 | Strong Symbol |
| Sun | Secondary | 1 · 9/45 combos | Absent | 2 · 7/11 charts (64%) | 3/4 | 45 / 11 | 6 | Moderate (Relevant Symbol) |
| Moon | Secondary | 1 · 9/45 combos | Absent | 2 · 6/11 charts (55%) | 3/4 | 45 / 11 | 6 | Moderate (Relevant Symbol) |
| Venus | Secondary | 1 · 8/45 combos | Absent | 2 · 6/11 charts (55%) | 3/4 | 45 / 11 | 6 | Moderate (Relevant Symbol) |
| Jupiter | Primary | 1 · 10/45 combos | Absent | 2 · 7/11 charts (64%) | 3/4 | 45 / 11 | 6 | Moderate (Relevant Symbol) |
| Uranus | Secondary | 1 · 7/45 combos | Absent | 2 · 6/11 charts (55%) | 3/4 | 45 / 11 | 6 | Moderate (Relevant Symbol) |
| Descendant (7th House cusp) | Primary | — (out of scope) | Absent | 1 · 2/11 charts (18%) | 2/3 | 45 / 11 | 6 | Moderate (Relevant Symbol) |
| Mars | Secondary | 1 · 5/45 combos | Absent | 1 · 4/11 charts (36%) | 3/4 | 45 / 11 | 4 | Weak (Occasional Symbol) |
| Lunar Node (North/South/unspecified) | Secondary | 1 · 8/45 combos | Absent | 1 · 3/11 charts (27%) | 3/4 | 45 / 11 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 6/45 combos | Absent | 1 · 1/11 charts (9%) | 2/3 | 45 / 11 | 4 | Weak (Occasional Symbol) |
| Pluto | Secondary | 1 · 6/45 combos | Absent | 0 · 0/11 charts (0%) | 2/4 | 45 / 11 | 2 | Very Weak (Speculative Symbol) |
| Ascendant (1st House cusp) | Absent | 1 · 6/45 combos | Absent | 1 · 4/11 charts (36%) | 2/4 | 45 / 11 | 2 | Very Weak (Speculative Symbol) |
| Midheaven (10th House cusp) | Absent | 1 · 6/45 combos | Absent | 1 · 1/11 charts (9%) | 2/4 | 45 / 11 | 2 | Very Weak (Speculative Symbol) |
| 5th House cusp | Absent | — (out of scope) | Absent | 1 · 3/11 charts (27%) | 1/3 | 45 / 11 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Mercury**: tier_score = 8 (n_juan_combos_total=45, n_marr_examples_total=11)  |  **Descendant (7th House cusp)**: tier_score = 6 (n_juan_combos_total=45, n_marr_examples_total=11) — *looked up independently; no combined score is produced for this pairing.*
- **Mercury**: tier_score = 8 (n_juan_combos_total=45, n_marr_examples_total=11)  |  **5th House cusp**: tier_score = 2 (n_juan_combos_total=45, n_marr_examples_total=11) — *looked up independently; no combined score is produced for this pairing.*
- **Imum Coeli (4th House cusp)**: tier_score = 8 (n_juan_combos_total=45, n_marr_examples_total=11)  |  **5th House cusp**: tier_score = 2 (n_juan_combos_total=45, n_marr_examples_total=11) — *looked up independently; no combined score is produced for this pairing.*
- **Descendant (7th House cusp)**: tier_score = 6 (n_juan_combos_total=45, n_marr_examples_total=11)  |  **Mars**: tier_score = 4 (n_juan_combos_total=45, n_marr_examples_total=11) — *looked up independently; no combined score is produced for this pairing.*

---

## 2. Birth of Sister

*Category: Birth — Sibling (female)*

### 1. Event Overview

The gender-mirrored counterpart to Birth of Brother. Venus and the 3rd house cusp form the core signature, with the IC again as an occasional reinforcement — a clean Mercury↔Venus mirroring between the two sibling-birth entries.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Moon, Mercury, Venus, Sun, Jupiter, Uranus, Pluto
- Houses/Angles mentioned: Descendant (7th House cusp), Imum Coeli (4th House cusp), 3rd House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Moon, Mercury, Venus, Descendant (7th House cusp), Imum Coeli (4th House cusp), 3rd House cusp
- **Secondary**: Sun, Jupiter, Uranus, Pluto, North Node (Ascending)
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Mercury (10/45), Jupiter (10/45), Sun (9/45), Moon (9/45), Lunar Node (pole unspecified) (8/45), Venus (8/45), Uranus (7/45), Ascendant (1st House cusp) (6/45), Midheaven (10th House cusp) (6/45), Pluto (6/45)
- Total pairwise combinations catalogued for this event: 45
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: The gender-mirrored counterpart to Birth of Brother. Venus and the 3rd house cusp form the core signature, with the IC again as an occasional reinforcement — a clean Mercury↔Venus mirroring between the two sibling-birth entries.
- Points referenced: Venus (strong), Imum Coeli (4th House cusp) (weak), 3rd House cusp (weak)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **9 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- **Low sample size:** only 9 worked examples available for this event in total — frequencies quoted below (and the corresponding tier_score contributions) are drawn from a very small pool and should be read as suggestive rather than well-established (see `n_marr_examples_total` on each symbol record).
- Most frequent points: 3rd House cusp (7/9, 78%), Moon (7/9, 78%), Venus (5/9, 56%), Mercury (5/9, 56%), Uranus (5/9, 56%), Jupiter (5/9, 56%), Ascendant (1st House cusp) (4/9, 44%), Mars (4/9, 44%)
- Node detail: North Node in 1, South Node in 0, unspecified-pole Node in 1 of 9 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Venus** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **3rd House cusp** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **Moon** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Mercury** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Jupiter** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Uranus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Imum Coeli (4th House cusp)** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **Descendant (7th House cusp)** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Sun** — supported by POLARIS, Juan Combos, Marr Aspects (score 4/10)
- **Pluto** — supported by POLARIS, Juan Combos, Marr Aspects (score 4/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Mars** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Ascendant (1st House cusp)** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Neptune** — supported by Marr Aspects (score 2/10)
- **Midheaven (10th House cusp)** — supported by Juan Combos (score 2/10)
- **8th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Venus is corroborated by every source able to speak to it, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Sun, Moon, Mercury, Jupiter, Uranus, Pluto, Imum Coeli (4th House cusp), 3rd House cusp, Lunar Node (North/South/unspecified) are supported by three of the four sources. 2 of these (Imum Coeli (4th House cusp), 3rd House cusp) sit at the structural ceiling for their symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Mars, Ascendant (1st House cusp), Descendant (7th House cusp), Part of Fortune.

**Speculative / source-specific symbolism.** Neptune (Marr Aspects only), Midheaven (10th House cusp) (Juan Combos only), 8th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** Mars (in 4/9 example charts, 44%), Ascendant (1st House cusp) (in 4/9 example charts, 44%) recur in a substantial share of Marr's worked examples without being singled out in POLARIS's Primary/Secondary list. This is not a direct contradiction — POLARIS's list is a short, deliberately curated selection rather than an exhaustive one, and no case was found anywhere in the compendium of a POLARIS-Primary symbol being *absent* from a substantial Marr Aspects sample. Read it as an emphasis gap, not a disagreement about relevance.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Venus | Primary | 1 · 8/45 combos | Strong emphasis | 2 · 5/9 charts (56%) | 4/4 | 45 / 9 | 8 | Strong Symbol |
| 3rd House cusp | Primary | — (out of scope) | Mentioned | 2 · 7/9 charts (78%) | 3/3 † | 45 / 9 | 8 | Strong Symbol |
| Moon | Primary | 1 · 9/45 combos | Absent | 2 · 7/9 charts (78%) | 3/4 | 45 / 9 | 6 | Moderate (Relevant Symbol) |
| Mercury | Primary | 1 · 10/45 combos | Absent | 2 · 5/9 charts (56%) | 3/4 | 45 / 9 | 6 | Moderate (Relevant Symbol) |
| Jupiter | Secondary | 1 · 10/45 combos | Absent | 2 · 5/9 charts (56%) | 3/4 | 45 / 9 | 6 | Moderate (Relevant Symbol) |
| Uranus | Secondary | 1 · 7/45 combos | Absent | 2 · 5/9 charts (56%) | 3/4 | 45 / 9 | 6 | Moderate (Relevant Symbol) |
| Imum Coeli (4th House cusp) | Primary | — (out of scope) | Mentioned | 1 · 1/9 charts (11%) | 3/3 † | 45 / 9 | 6 | Moderate (Relevant Symbol) |
| Descendant (7th House cusp) | Primary | — (out of scope) | Absent | 1 · 1/9 charts (11%) | 2/3 | 45 / 9 | 6 | Moderate (Relevant Symbol) |
| Sun | Secondary | 1 · 9/45 combos | Absent | 1 · 3/9 charts (33%) | 3/4 | 45 / 9 | 4 | Weak (Occasional Symbol) |
| Pluto | Secondary | 1 · 6/45 combos | Absent | 1 · 2/9 charts (22%) | 3/4 | 45 / 9 | 4 | Weak (Occasional Symbol) |
| Lunar Node (North/South/unspecified) | Secondary | 1 · 8/45 combos | Absent | 1 · 2/9 charts (22%) | 3/4 | 45 / 9 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 6/45 combos | Absent | 1 · 1/9 charts (11%) | 2/3 | 45 / 9 | 4 | Weak (Occasional Symbol) |
| Mars | Absent | 1 · 5/45 combos | Absent | 1 · 4/9 charts (44%) | 2/4 | 45 / 9 | 2 | Very Weak (Speculative Symbol) |
| Ascendant (1st House cusp) | Absent | 1 · 6/45 combos | Absent | 1 · 4/9 charts (44%) | 2/4 | 45 / 9 | 2 | Very Weak (Speculative Symbol) |
| Neptune | Absent | 0 · 0/45 combos | Absent | 1 · 1/9 charts (11%) | 1/4 | 45 / 9 | 2 | Very Weak (Speculative Symbol) |
| Midheaven (10th House cusp) | Absent | 1 · 6/45 combos | Absent | 0 · 0/9 charts (0%) | 1/4 | 45 / 9 | 2 | Very Weak (Speculative Symbol) |
| 8th House cusp | Absent | — (out of scope) | Absent | 1 · 1/9 charts (11%) | 1/3 | 45 / 9 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 1/9 charts (11%) | 1/3 | 45 / 9 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Venus**: tier_score = 8 (n_juan_combos_total=45, n_marr_examples_total=9)  |  **Pluto**: tier_score = 4 (n_juan_combos_total=45, n_marr_examples_total=9) — *looked up independently; no combined score is produced for this pairing.*
- **Venus**: tier_score = 8 (n_juan_combos_total=45, n_marr_examples_total=9)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=45, n_marr_examples_total=9) — *looked up independently; no combined score is produced for this pairing.*
- **3rd House cusp**: tier_score = 8 (n_juan_combos_total=45, n_marr_examples_total=9)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=45, n_marr_examples_total=9) — *looked up independently; no combined score is produced for this pairing.*
- **Pluto**: tier_score = 4 (n_juan_combos_total=45, n_marr_examples_total=9)  |  **Lunar Node (North/South/unspecified)**: tier_score = 4 (n_juan_combos_total=45, n_marr_examples_total=9) — *looked up independently; no combined score is produced for this pairing.*

---

## 3. Birth of Son

*Category: Birth — Child (male)*

### 1. Event Overview

The Sun and Mars are the classical significators of a male child, paired with the 5th house cusp (children) and the Ascendant, which the sources treat as the single most frequently activated angle for any childbirth. Uranus recurs specifically for unexpected or premature births.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Sun, Mars, Jupiter, Moon, Mercury, Venus, Uranus, Pluto
- Houses/Angles mentioned: Ascendant (1st House cusp), Imum Coeli (4th House cusp), 5th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Sun, Mars, Jupiter, Ascendant (1st House cusp), Imum Coeli (4th House cusp), 5th House cusp, North Node (Ascending)
- **Secondary**: Moon, Mercury, Venus, Uranus, Pluto
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Sun (11/60), Mercury (11/60), Jupiter (11/60), Ascendant (1st House cusp) (10/60), Moon (10/60), Venus (10/60), Uranus (10/60), Lunar Node (pole unspecified) (10/60), Part of Fortune (10/60), Mars (9/60)
- Total pairwise combinations catalogued for this event: 60
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: The Sun and Mars are the classical significators of a male child, paired with the 5th house cusp (children) and the Ascendant, which the sources treat as the single most frequently activated angle for any childbirth. Uranus recurs specifically for unexpected or premature births.
- Points referenced: Ascendant (1st House cusp) (strong), 5th House cusp (strong), Sun (mentioned), Mars (mentioned), Jupiter (mentioned), Uranus (mentioned)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **68 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: 5th House cusp (54/68, 79%), Sun (47/68, 69%), Mars (46/68, 68%), Jupiter (45/68, 66%), Imum Coeli (4th House cusp) (39/68, 57%), Uranus (38/68, 56%), Venus (37/68, 54%), Moon (36/68, 53%)
- Node detail: North Node in 8, South Node in 1, unspecified-pole Node in 9 of 68 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- **5th House cusp** — supported by POLARIS, Other, Marr Aspects (score 10/10)

**Secondary Symbols**
- **Sun** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Mars** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Jupiter** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Uranus** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 6/10)
- **Moon** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Venus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Imum Coeli (4th House cusp)** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Mercury** — supported by POLARIS, Juan Combos, Marr Aspects (score 4/10)
- **Pluto** — supported by POLARIS, Juan Combos, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Midheaven (10th House cusp)** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Saturn** — supported by Marr Aspects (score 2/10)
- **Neptune** — supported by Marr Aspects (score 2/10)
- **Descendant (7th House cusp)** — supported by Marr Aspects (score 2/10)
- **3rd House cusp** — supported by Marr Aspects (score 2/10)
- **8th House cusp** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)
- **12th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Sun, Mars, Jupiter, Uranus, Ascendant (1st House cusp) are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Moon, Mercury, Venus, Pluto, 5th House cusp, Lunar Node (North/South/unspecified) are supported by three of the four sources. 1 of these (5th House cusp) sits at the structural ceiling for its symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Midheaven (10th House cusp), Imum Coeli (4th House cusp), Part of Fortune.

**Speculative / source-specific symbolism.** Saturn (Marr Aspects only), Neptune (Marr Aspects only), Descendant (7th House cusp) (Marr Aspects only), 3rd House cusp (Marr Aspects only), 8th House cusp (Marr Aspects only), 9th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only), 12th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** No clear-cut contradictions were found for this event: the four sources differ in *emphasis* and *coverage* (which is discussed above) rather than making opposing claims about any single symbol.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| 5th House cusp | Primary | — (out of scope) | Strong emphasis | 2 · 54/68 charts (79%) | 3/3 † | 60 / 68 | 10 | Very Strong (Core Symbol) |
| Sun | Primary | 1 · 11/60 combos | Mentioned | 2 · 47/68 charts (69%) | 4/4 | 60 / 68 | 8 | Strong Symbol |
| Mars | Primary | 1 · 9/60 combos | Mentioned | 2 · 46/68 charts (68%) | 4/4 | 60 / 68 | 8 | Strong Symbol |
| Jupiter | Primary | 1 · 11/60 combos | Mentioned | 2 · 45/68 charts (66%) | 4/4 | 60 / 68 | 8 | Strong Symbol |
| Ascendant (1st House cusp) | Primary | 1 · 10/60 combos | Strong emphasis | 2 · 35/68 charts (51%) | 4/4 | 60 / 68 | 8 | Strong Symbol |
| Uranus | Secondary | 1 · 10/60 combos | Mentioned | 2 · 38/68 charts (56%) | 4/4 | 60 / 68 | 6 | Moderate (Relevant Symbol) |
| Moon | Secondary | 1 · 10/60 combos | Absent | 2 · 36/68 charts (53%) | 3/4 | 60 / 68 | 6 | Moderate (Relevant Symbol) |
| Venus | Secondary | 1 · 10/60 combos | Absent | 2 · 37/68 charts (54%) | 3/4 | 60 / 68 | 6 | Moderate (Relevant Symbol) |
| Lunar Node (North/South/unspecified) | Primary | 1 · 10/60 combos | Absent | 1 · 18/68 charts (26%) | 3/4 | 60 / 68 | 6 | Moderate (Relevant Symbol) |
| Imum Coeli (4th House cusp) | Primary | — (out of scope) | Absent | 2 · 39/68 charts (57%) | 2/3 | 60 / 68 | 6 | Moderate (Relevant Symbol) |
| Mercury | Secondary | 1 · 11/60 combos | Absent | 1 · 24/68 charts (35%) | 3/4 | 60 / 68 | 4 | Weak (Occasional Symbol) |
| Pluto | Secondary | 1 · 9/60 combos | Absent | 1 · 25/68 charts (37%) | 3/4 | 60 / 68 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 10/60 combos | Absent | 1 · 11/68 charts (16%) | 2/3 | 60 / 68 | 4 | Weak (Occasional Symbol) |
| Midheaven (10th House cusp) | Absent | 1 · 9/60 combos | Absent | 1 · 17/68 charts (25%) | 2/4 | 60 / 68 | 2 | Very Weak (Speculative Symbol) |
| Saturn | Absent | 0 · 0/60 combos | Absent | 1 · 2/68 charts (3%) | 1/4 | 60 / 68 | 2 | Very Weak (Speculative Symbol) |
| Neptune | Absent | 0 · 0/60 combos | Absent | 1 · 2/68 charts (3%) | 1/4 | 60 / 68 | 2 | Very Weak (Speculative Symbol) |
| Descendant (7th House cusp) | Absent | — (out of scope) | Absent | 1 · 16/68 charts (24%) | 1/3 | 60 / 68 | 2 | Very Weak (Speculative Symbol) |
| 3rd House cusp | Absent | — (out of scope) | Absent | 1 · 4/68 charts (6%) | 1/3 | 60 / 68 | 2 | Very Weak (Speculative Symbol) |
| 8th House cusp | Absent | — (out of scope) | Absent | 1 · 1/68 charts (1%) | 1/3 | 60 / 68 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | Absent | 1 · 1/68 charts (1%) | 1/3 | 60 / 68 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 1/68 charts (1%) | 1/3 | 60 / 68 | 2 | Very Weak (Speculative Symbol) |
| 12th House cusp | Absent | — (out of scope) | Absent | 1 · 2/68 charts (3%) | 1/3 | 60 / 68 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **5th House cusp**: tier_score = 10 (n_juan_combos_total=60, n_marr_examples_total=68)  |  **Pluto**: tier_score = 4 (n_juan_combos_total=60, n_marr_examples_total=68) — *looked up independently; no combined score is produced for this pairing.*
- **5th House cusp**: tier_score = 10 (n_juan_combos_total=60, n_marr_examples_total=68)  |  **12th House cusp**: tier_score = 2 (n_juan_combos_total=60, n_marr_examples_total=68) — *looked up independently; no combined score is produced for this pairing.*
- **Sun**: tier_score = 8 (n_juan_combos_total=60, n_marr_examples_total=68)  |  **12th House cusp**: tier_score = 2 (n_juan_combos_total=60, n_marr_examples_total=68) — *looked up independently; no combined score is produced for this pairing.*
- **Pluto**: tier_score = 4 (n_juan_combos_total=60, n_marr_examples_total=68)  |  **Part of Fortune**: tier_score = 4 (n_juan_combos_total=60, n_marr_examples_total=68) — *looked up independently; no combined score is produced for this pairing.*

---

## 4. Birth of Daughter

*Category: Birth — Child (female)*

### 1. Event Overview

The female counterpart to Birth of Son: Venus, with the Moon as a secondary significator, replaces Sun/Mars, while the 5th house cusp and Ascendant remain the shared backbone of any childbirth signature. Uranus again marks premature births.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Moon, Venus, Jupiter, Sun, Mercury, Mars, Uranus, Pluto
- Houses/Angles mentioned: Ascendant (1st House cusp), Imum Coeli (4th House cusp), 5th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Moon, Venus, Jupiter, Ascendant (1st House cusp), Imum Coeli (4th House cusp), 5th House cusp, North Node (Ascending)
- **Secondary**: Sun, Mercury, Mars, Uranus, Pluto
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Sun (11/60), Mercury (11/60), Jupiter (11/60), Ascendant (1st House cusp) (10/60), Moon (10/60), Venus (10/60), Uranus (10/60), Lunar Node (pole unspecified) (10/60), Part of Fortune (10/60), Mars (9/60)
- Total pairwise combinations catalogued for this event: 60
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: The female counterpart to Birth of Son: Venus, with the Moon as a secondary significator, replaces Sun/Mars, while the 5th house cusp and Ascendant remain the shared backbone of any childbirth signature. Uranus again marks premature births.
- Points referenced: Ascendant (1st House cusp) (strong), 5th House cusp (strong), Moon (mentioned), Venus (mentioned), Uranus (mentioned)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **59 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Venus (45/59, 76%), 5th House cusp (45/59, 76%), Jupiter (42/59, 71%), Moon (40/59, 68%), Uranus (37/59, 63%), Imum Coeli (4th House cusp) (34/59, 58%), Sun (32/59, 54%), Ascendant (1st House cusp) (30/59, 51%)
- Node detail: North Node in 8, South Node in 0, unspecified-pole Node in 14 of 59 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- **5th House cusp** — supported by POLARIS, Other, Marr Aspects (score 10/10)

**Secondary Symbols**
- **Moon** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Venus** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Uranus** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 6/10)
- **Sun** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Jupiter** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Imum Coeli (4th House cusp)** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Mercury** — supported by POLARIS, Juan Combos, Marr Aspects (score 4/10)
- **Mars** — supported by POLARIS, Juan Combos, Marr Aspects (score 4/10)
- **Pluto** — supported by POLARIS, Juan Combos, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Midheaven (10th House cusp)** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Saturn** — supported by Marr Aspects (score 2/10)
- **Neptune** — supported by Marr Aspects (score 2/10)
- **Descendant (7th House cusp)** — supported by Marr Aspects (score 2/10)
- **3rd House cusp** — supported by Marr Aspects (score 2/10)
- **8th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Moon, Venus, Uranus, Ascendant (1st House cusp) are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Sun, Mercury, Mars, Jupiter, Pluto, 5th House cusp, Lunar Node (North/South/unspecified) are supported by three of the four sources. 1 of these (5th House cusp) sits at the structural ceiling for its symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Midheaven (10th House cusp), Imum Coeli (4th House cusp), Part of Fortune.

**Speculative / source-specific symbolism.** Saturn (Marr Aspects only), Neptune (Marr Aspects only), Descendant (7th House cusp) (Marr Aspects only), 3rd House cusp (Marr Aspects only), 8th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** No clear-cut contradictions were found for this event: the four sources differ in *emphasis* and *coverage* (which is discussed above) rather than making opposing claims about any single symbol.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| 5th House cusp | Primary | — (out of scope) | Strong emphasis | 2 · 45/59 charts (76%) | 3/3 † | 60 / 59 | 10 | Very Strong (Core Symbol) |
| Moon | Primary | 1 · 10/60 combos | Mentioned | 2 · 40/59 charts (68%) | 4/4 | 60 / 59 | 8 | Strong Symbol |
| Venus | Primary | 1 · 10/60 combos | Mentioned | 2 · 45/59 charts (76%) | 4/4 | 60 / 59 | 8 | Strong Symbol |
| Ascendant (1st House cusp) | Primary | 1 · 10/60 combos | Strong emphasis | 2 · 30/59 charts (51%) | 4/4 | 60 / 59 | 8 | Strong Symbol |
| Uranus | Secondary | 1 · 10/60 combos | Mentioned | 2 · 37/59 charts (63%) | 4/4 | 60 / 59 | 6 | Moderate (Relevant Symbol) |
| Sun | Secondary | 1 · 11/60 combos | Absent | 2 · 32/59 charts (54%) | 3/4 | 60 / 59 | 6 | Moderate (Relevant Symbol) |
| Jupiter | Primary | 1 · 11/60 combos | Absent | 2 · 42/59 charts (71%) | 3/4 | 60 / 59 | 6 | Moderate (Relevant Symbol) |
| Lunar Node (North/South/unspecified) | Primary | 1 · 10/60 combos | Absent | 1 · 22/59 charts (37%) | 3/4 | 60 / 59 | 6 | Moderate (Relevant Symbol) |
| Imum Coeli (4th House cusp) | Primary | — (out of scope) | Absent | 2 · 34/59 charts (58%) | 2/3 | 60 / 59 | 6 | Moderate (Relevant Symbol) |
| Mercury | Secondary | 1 · 11/60 combos | Absent | 1 · 22/59 charts (37%) | 3/4 | 60 / 59 | 4 | Weak (Occasional Symbol) |
| Mars | Secondary | 1 · 9/60 combos | Absent | 1 · 24/59 charts (41%) | 3/4 | 60 / 59 | 4 | Weak (Occasional Symbol) |
| Pluto | Secondary | 1 · 9/60 combos | Absent | 1 · 16/59 charts (27%) | 3/4 | 60 / 59 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 10/60 combos | Absent | 1 · 11/59 charts (19%) | 2/3 | 60 / 59 | 4 | Weak (Occasional Symbol) |
| Midheaven (10th House cusp) | Absent | 1 · 9/60 combos | Absent | 1 · 11/59 charts (19%) | 2/4 | 60 / 59 | 2 | Very Weak (Speculative Symbol) |
| Saturn | Absent | 0 · 0/60 combos | Absent | 1 · 2/59 charts (3%) | 1/4 | 60 / 59 | 2 | Very Weak (Speculative Symbol) |
| Neptune | Absent | 0 · 0/60 combos | Absent | 1 · 2/59 charts (3%) | 1/4 | 60 / 59 | 2 | Very Weak (Speculative Symbol) |
| Descendant (7th House cusp) | Absent | — (out of scope) | Absent | 1 · 18/59 charts (31%) | 1/3 | 60 / 59 | 2 | Very Weak (Speculative Symbol) |
| 3rd House cusp | Absent | — (out of scope) | Absent | 1 · 2/59 charts (3%) | 1/3 | 60 / 59 | 2 | Very Weak (Speculative Symbol) |
| 8th House cusp | Absent | — (out of scope) | Absent | 1 · 1/59 charts (2%) | 1/3 | 60 / 59 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 2/59 charts (3%) | 1/3 | 60 / 59 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **5th House cusp**: tier_score = 10 (n_juan_combos_total=60, n_marr_examples_total=59)  |  **Mars**: tier_score = 4 (n_juan_combos_total=60, n_marr_examples_total=59) — *looked up independently; no combined score is produced for this pairing.*
- **5th House cusp**: tier_score = 10 (n_juan_combos_total=60, n_marr_examples_total=59)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=60, n_marr_examples_total=59) — *looked up independently; no combined score is produced for this pairing.*
- **Moon**: tier_score = 8 (n_juan_combos_total=60, n_marr_examples_total=59)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=60, n_marr_examples_total=59) — *looked up independently; no combined score is produced for this pairing.*
- **Mars**: tier_score = 4 (n_juan_combos_total=60, n_marr_examples_total=59)  |  **Pluto**: tier_score = 4 (n_juan_combos_total=60, n_marr_examples_total=59) — *looked up independently; no combined score is produced for this pairing.*

---

## 5. Birth of Grandson

*Category: Birth — Grandchild (male)*

### 1. Event Overview

An extended-family variant of Birth of Son. Alexander Marr's short-form 'Other' commentary records nothing for this specific event, so the signature here rests on POLARIS's list and the frequency pattern in Marr's worked example charts.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Sun, Mars, Jupiter, Moon, Mercury, Venus, Uranus, Pluto
- Houses/Angles mentioned: Ascendant (1st House cusp), Imum Coeli (4th House cusp), 5th House cusp, 9th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Sun, Mars, Jupiter, Ascendant (1st House cusp), Imum Coeli (4th House cusp), 5th House cusp, North Node (Ascending)
- **Secondary**: Moon, Mercury, Venus, Uranus, Pluto, 9th House cusp
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Mercury (11/52), Sun (10/52), Jupiter (10/52), Lunar Node (pole unspecified) (10/52), Moon (9/52), Ascendant (1st House cusp) (8/52), Mars (8/52), Uranus (8/52), Pluto (8/52), Midheaven (10th House cusp) (8/52)
- Total pairwise combinations catalogued for this event: 52
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- *No data available from this source* (the compendium explicitly marks this entry “None”).

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **6 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- **Low sample size:** only 6 worked examples available for this event in total — frequencies quoted below (and the corresponding tier_score contributions) are drawn from a very small pool and should be read as suggestive rather than well-established (see `n_marr_examples_total` on each symbol record).
- Most frequent points: Sun (6/6, 100%), Uranus (5/6, 83%), Jupiter (5/6, 83%), Venus (4/6, 67%), Pluto (4/6, 67%), Ascendant (1st House cusp) (4/6, 67%), Moon (4/6, 67%), 9th House cusp (3/6, 50%)
- Node detail: North Node in 3, South Node in 0, unspecified-pole Node in 0 of 6 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Sun** — supported by POLARIS, Juan Combos, Marr Aspects (score 8/10)
- **Jupiter** — supported by POLARIS, Juan Combos, Marr Aspects (score 8/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Juan Combos, Marr Aspects (score 8/10)
- **Imum Coeli (4th House cusp)** — supported by POLARIS, Marr Aspects (score 8/10)
- **5th House cusp** — supported by POLARIS, Marr Aspects (score 8/10)
- **Moon** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Mercury** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Venus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Mars** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Uranus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Pluto** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **9th House cusp** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Midheaven (10th House cusp)** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Descendant (7th House cusp)** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)
- **Part of Fortune** — supported by Juan Combos (score 2/10)

### 4. Consensus Analysis

**Medium-confidence symbolism.** Sun, Moon, Mercury, Venus, Mars, Jupiter, Uranus, Pluto, Ascendant (1st House cusp), Lunar Node (North/South/unspecified) are supported by three of the four sources. All of these sit at the structural ceiling for their symbol type — marked † in the table below — because Other carries no data at all for this event, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Midheaven (10th House cusp), Imum Coeli (4th House cusp), 5th House cusp, 9th House cusp. All of these are marked † in the table below: for each, only two sources could address the point at all (the other two are structurally out of scope for this event), and those two agree — a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

**Speculative / source-specific symbolism.** Descendant (7th House cusp) (Marr Aspects only), 11th House cusp (Marr Aspects only), Part of Fortune (Juan Combos only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** No clear-cut contradictions were found for this event: the four sources differ in *emphasis* and *coverage* (which is discussed above) rather than making opposing claims about any single symbol.

**Incomplete information.** Other (marked “None”) contribute no data to this event; the consolidated picture above rests on the remaining source(s) only.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Sun | Primary | 1 · 10/52 combos | — (no data) | 2 · 6/6 charts (100%) | 3/3 † | 52 / 6 | 8 | Strong Symbol |
| Jupiter | Primary | 1 · 10/52 combos | — (no data) | 2 · 5/6 charts (83%) | 3/3 † | 52 / 6 | 8 | Strong Symbol |
| Ascendant (1st House cusp) | Primary | 1 · 8/52 combos | — (no data) | 2 · 4/6 charts (67%) | 3/3 † | 52 / 6 | 8 | Strong Symbol |
| Imum Coeli (4th House cusp) | Primary | — (out of scope) | — (no data) | 1 · 3/6 charts (50%) | 2/2 † | 52 / 6 | 8 | Strong Symbol |
| 5th House cusp | Primary | — (out of scope) | — (no data) | 1 · 2/6 charts (33%) | 2/2 † | 52 / 6 | 8 | Strong Symbol |
| Moon | Secondary | 1 · 9/52 combos | — (no data) | 2 · 4/6 charts (67%) | 3/3 † | 52 / 6 | 6 | Moderate (Relevant Symbol) |
| Mercury | Secondary | 1 · 11/52 combos | — (no data) | 1 · 3/6 charts (50%) | 3/3 † | 52 / 6 | 6 | Moderate (Relevant Symbol) |
| Venus | Secondary | 1 · 8/52 combos | — (no data) | 2 · 4/6 charts (67%) | 3/3 † | 52 / 6 | 6 | Moderate (Relevant Symbol) |
| Mars | Primary | 1 · 8/52 combos | — (no data) | 1 · 2/6 charts (33%) | 3/3 † | 52 / 6 | 6 | Moderate (Relevant Symbol) |
| Uranus | Secondary | 1 · 8/52 combos | — (no data) | 2 · 5/6 charts (83%) | 3/3 † | 52 / 6 | 6 | Moderate (Relevant Symbol) |
| Pluto | Secondary | 1 · 8/52 combos | — (no data) | 2 · 4/6 charts (67%) | 3/3 † | 52 / 6 | 6 | Moderate (Relevant Symbol) |
| Lunar Node (North/South/unspecified) | Primary | 1 · 10/52 combos | — (no data) | 1 · 3/6 charts (50%) | 3/3 † | 52 / 6 | 6 | Moderate (Relevant Symbol) |
| 9th House cusp | Secondary | — (out of scope) | — (no data) | 1 · 3/6 charts (50%) | 2/2 † | 52 / 6 | 6 | Moderate (Relevant Symbol) |
| Midheaven (10th House cusp) | Absent | 1 · 8/52 combos | — (no data) | 1 · 2/6 charts (33%) | 2/3 | 52 / 6 | 4 | Weak (Occasional Symbol) |
| Descendant (7th House cusp) | Absent | — (out of scope) | — (no data) | 1 · 2/6 charts (33%) | 1/2 | 52 / 6 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | — (no data) | 1 · 2/6 charts (33%) | 1/2 | 52 / 6 | 2 | Very Weak (Speculative Symbol) |
| Part of Fortune | — (out of scope) | 1 · 6/52 combos | — (no data) | 0 · 0/6 charts (0%) | 1/2 | 52 / 6 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Sun**: tier_score = 8 (n_juan_combos_total=52, n_marr_examples_total=6)  |  **Mars**: tier_score = 6 (n_juan_combos_total=52, n_marr_examples_total=6) — *looked up independently; no combined score is produced for this pairing.*
- **Sun**: tier_score = 8 (n_juan_combos_total=52, n_marr_examples_total=6)  |  **Part of Fortune**: tier_score = 2 (n_juan_combos_total=52, n_marr_examples_total=6) — *looked up independently; no combined score is produced for this pairing.*
- **Jupiter**: tier_score = 8 (n_juan_combos_total=52, n_marr_examples_total=6)  |  **Part of Fortune**: tier_score = 2 (n_juan_combos_total=52, n_marr_examples_total=6) — *looked up independently; no combined score is produced for this pairing.*
- **Mars**: tier_score = 6 (n_juan_combos_total=52, n_marr_examples_total=6)  |  **Uranus**: tier_score = 6 (n_juan_combos_total=52, n_marr_examples_total=6) — *looked up independently; no combined score is produced for this pairing.*

---

## 6. Birth of Granddaughter

*Category: Birth — Grandchild (female)*

### 1. Event Overview

The female-line counterpart to Birth of Grandson, and equally reliant on POLARIS and the worked examples alone, since Marr's 'Other' commentary is silent here too.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Moon, Venus, Jupiter, Sun, Mercury, Mars, Uranus, Pluto
- Houses/Angles mentioned: Ascendant (1st House cusp), Imum Coeli (4th House cusp), 5th House cusp, 9th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Moon, Venus, Jupiter, Ascendant (1st House cusp), Imum Coeli (4th House cusp), 5th House cusp, North Node (Ascending)
- **Secondary**: Sun, Mercury, Mars, Uranus, Pluto, 9th House cusp
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Mercury (11/52), Sun (10/52), Jupiter (10/52), Lunar Node (pole unspecified) (10/52), Moon (9/52), Ascendant (1st House cusp) (8/52), Mars (8/52), Uranus (8/52), Pluto (8/52), Midheaven (10th House cusp) (8/52)
- Total pairwise combinations catalogued for this event: 52
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- *No data available from this source* (the compendium explicitly marks this entry “None”).

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **6 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- **Low sample size:** only 6 worked examples available for this event in total — frequencies quoted below (and the corresponding tier_score contributions) are drawn from a very small pool and should be read as suggestive rather than well-established (see `n_marr_examples_total` on each symbol record).
- Most frequent points: Moon (5/6, 83%), 5th House cusp (3/6, 50%), Mercury (3/6, 50%), Imum Coeli (4th House cusp) (3/6, 50%), Jupiter (3/6, 50%), North Node (Ascending) (3/6, 50%), Venus (3/6, 50%), Uranus (3/6, 50%)
- Node detail: North Node in 3, South Node in 0, unspecified-pole Node in 0 of 6 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Moon** — supported by POLARIS, Juan Combos, Marr Aspects (score 8/10)
- **Imum Coeli (4th House cusp)** — supported by POLARIS, Marr Aspects (score 8/10)
- **5th House cusp** — supported by POLARIS, Marr Aspects (score 8/10)
- **Mercury** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Venus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Jupiter** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Uranus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Pluto** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **9th House cusp** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Sun** — supported by POLARIS, Juan Combos (score 4/10)
- **Mars** — supported by POLARIS, Juan Combos (score 4/10)
- **Midheaven (10th House cusp)** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Descendant (7th House cusp)** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)
- **Part of Fortune** — supported by Juan Combos (score 2/10)

### 4. Consensus Analysis

**Medium-confidence symbolism.** Moon, Mercury, Venus, Jupiter, Uranus, Pluto, Ascendant (1st House cusp), Lunar Node (North/South/unspecified) are supported by three of the four sources. All of these sit at the structural ceiling for their symbol type — marked † in the table below — because Other carries no data at all for this event, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Sun, Mars, Midheaven (10th House cusp), Imum Coeli (4th House cusp), 5th House cusp, 9th House cusp. All of these are marked † in the table below: for each, only two sources could address the point at all (the other two are structurally out of scope for this event), and those two agree — a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

**Speculative / source-specific symbolism.** Descendant (7th House cusp) (Marr Aspects only), 11th House cusp (Marr Aspects only), Part of Fortune (Juan Combos only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** No clear-cut contradictions were found for this event: the four sources differ in *emphasis* and *coverage* (which is discussed above) rather than making opposing claims about any single symbol.

**Incomplete information.** Other (marked “None”) contribute no data to this event; the consolidated picture above rests on the remaining source(s) only.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Moon | Primary | 1 · 9/52 combos | — (no data) | 2 · 5/6 charts (83%) | 3/3 † | 52 / 6 | 8 | Strong Symbol |
| Imum Coeli (4th House cusp) | Primary | — (out of scope) | — (no data) | 1 · 3/6 charts (50%) | 2/2 † | 52 / 6 | 8 | Strong Symbol |
| 5th House cusp | Primary | — (out of scope) | — (no data) | 1 · 3/6 charts (50%) | 2/2 † | 52 / 6 | 8 | Strong Symbol |
| Mercury | Secondary | 1 · 11/52 combos | — (no data) | 1 · 3/6 charts (50%) | 3/3 † | 52 / 6 | 6 | Moderate (Relevant Symbol) |
| Venus | Primary | 1 · 8/52 combos | — (no data) | 1 · 3/6 charts (50%) | 3/3 † | 52 / 6 | 6 | Moderate (Relevant Symbol) |
| Jupiter | Primary | 1 · 10/52 combos | — (no data) | 1 · 3/6 charts (50%) | 3/3 † | 52 / 6 | 6 | Moderate (Relevant Symbol) |
| Uranus | Secondary | 1 · 8/52 combos | — (no data) | 1 · 3/6 charts (50%) | 3/3 † | 52 / 6 | 6 | Moderate (Relevant Symbol) |
| Pluto | Secondary | 1 · 8/52 combos | — (no data) | 1 · 1/6 charts (17%) | 3/3 † | 52 / 6 | 6 | Moderate (Relevant Symbol) |
| Ascendant (1st House cusp) | Primary | 1 · 8/52 combos | — (no data) | 1 · 1/6 charts (17%) | 3/3 † | 52 / 6 | 6 | Moderate (Relevant Symbol) |
| Lunar Node (North/South/unspecified) | Primary | 1 · 10/52 combos | — (no data) | 1 · 3/6 charts (50%) | 3/3 † | 52 / 6 | 6 | Moderate (Relevant Symbol) |
| 9th House cusp | Secondary | — (out of scope) | — (no data) | 1 · 1/6 charts (17%) | 2/2 † | 52 / 6 | 6 | Moderate (Relevant Symbol) |
| Sun | Secondary | 1 · 10/52 combos | — (no data) | 0 · 0/6 charts (0%) | 2/3 | 52 / 6 | 4 | Weak (Occasional Symbol) |
| Mars | Secondary | 1 · 8/52 combos | — (no data) | 0 · 0/6 charts (0%) | 2/3 | 52 / 6 | 4 | Weak (Occasional Symbol) |
| Midheaven (10th House cusp) | Absent | 1 · 8/52 combos | — (no data) | 1 · 1/6 charts (17%) | 2/3 | 52 / 6 | 4 | Weak (Occasional Symbol) |
| Descendant (7th House cusp) | Absent | — (out of scope) | — (no data) | 1 · 2/6 charts (33%) | 1/2 | 52 / 6 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | — (no data) | 1 · 2/6 charts (33%) | 1/2 | 52 / 6 | 2 | Very Weak (Speculative Symbol) |
| Part of Fortune | — (out of scope) | 1 · 6/52 combos | — (no data) | 0 · 0/6 charts (0%) | 1/2 | 52 / 6 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Moon**: tier_score = 8 (n_juan_combos_total=52, n_marr_examples_total=6)  |  **Ascendant (1st House cusp)**: tier_score = 6 (n_juan_combos_total=52, n_marr_examples_total=6) — *looked up independently; no combined score is produced for this pairing.*
- **Moon**: tier_score = 8 (n_juan_combos_total=52, n_marr_examples_total=6)  |  **Part of Fortune**: tier_score = 2 (n_juan_combos_total=52, n_marr_examples_total=6) — *looked up independently; no combined score is produced for this pairing.*
- **Imum Coeli (4th House cusp)**: tier_score = 8 (n_juan_combos_total=52, n_marr_examples_total=6)  |  **Part of Fortune**: tier_score = 2 (n_juan_combos_total=52, n_marr_examples_total=6) — *looked up independently; no combined score is produced for this pairing.*
- **Ascendant (1st House cusp)**: tier_score = 6 (n_juan_combos_total=52, n_marr_examples_total=6)  |  **Lunar Node (North/South/unspecified)**: tier_score = 6 (n_juan_combos_total=52, n_marr_examples_total=6) — *looked up independently; no combined score is produced for this pairing.*

---

## 7. Marriage for Male

*Category: Union — Native's own marriage (male chart)*

### 1. Event Overview

Describes a male native's own marriage. The Descendant (the partnership axis) combined with Venus or the Moon is the primary signature, while Midheaven directions involving the Sun or Jupiter mark cases where the marriage also raises the native's social standing.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Moon, Venus, Jupiter, Sun, Mercury, Mars, Uranus
- Houses/Angles mentioned: Midheaven (10th House cusp), Descendant (7th House cusp), 5th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Moon, Venus, Jupiter, Midheaven (10th House cusp), Descendant (7th House cusp), 5th House cusp, North Node (Ascending)
- **Secondary**: Sun, Mercury, Mars, Uranus
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Venus (11/45), Jupiter (10/45), Sun (9/45), Moon (9/45), Lunar Node (pole unspecified) (9/45), Midheaven (10th House cusp) (9/45), Ascendant (1st House cusp) (7/45), Uranus (7/45), Mercury (7/45), Part of Fortune (5/45)
- Total pairwise combinations catalogued for this event: 45
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: Describes a male native's own marriage. The Descendant (the partnership axis) combined with Venus or the Moon is the primary signature, while Midheaven directions involving the Sun or Jupiter mark cases where the marriage also raises the native's social standing.
- Points referenced: Sun (strong), Jupiter (strong), Midheaven (10th House cusp) (strong), Moon (mentioned), Venus (mentioned), Descendant (7th House cusp) (mentioned)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **55 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Venus (45/55, 82%), Moon (38/55, 69%), Jupiter (37/55, 67%), 5th House cusp (36/55, 65%), Sun (30/55, 55%), Descendant (7th House cusp) (28/55, 51%), Mercury (27/55, 49%), Ascendant (1st House cusp) (27/55, 49%)
- Node detail: North Node in 16, South Node in 0, unspecified-pole Node in 6 of 55 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Sun** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Moon** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Venus** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Jupiter** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Midheaven (10th House cusp)** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Descendant (7th House cusp)** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **Mercury** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **5th House cusp** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Mars** — supported by POLARIS, Juan Combos, Marr Aspects (score 4/10)
- **Uranus** — supported by POLARIS, Juan Combos, Marr Aspects (score 4/10)
- **Ascendant (1st House cusp)** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Imum Coeli (4th House cusp)** — supported by Marr Aspects (score 4/10)
- **Pluto** — supported by Juan Combos, Marr Aspects (score 2/10)
- **3rd House cusp** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)
- **12th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Sun, Moon, Venus, Jupiter, Midheaven (10th House cusp) are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Mercury, Mars, Uranus, Descendant (7th House cusp), Lunar Node (North/South/unspecified) are supported by three of the four sources. 1 of these (Descendant (7th House cusp)) sits at the structural ceiling for its symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Pluto, Ascendant (1st House cusp), 5th House cusp, Part of Fortune.

**Speculative / source-specific symbolism.** Imum Coeli (4th House cusp) (Marr Aspects only), 3rd House cusp (Marr Aspects only), 9th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only), 12th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** Ascendant (1st House cusp) (in 27/55 example charts, 49%), Imum Coeli (4th House cusp) (in 23/55 example charts, 42%) recur in a substantial share of Marr's worked examples without being singled out in POLARIS's Primary/Secondary list. This is not a direct contradiction — POLARIS's list is a short, deliberately curated selection rather than an exhaustive one, and no case was found anywhere in the compendium of a POLARIS-Primary symbol being *absent* from a substantial Marr Aspects sample. Read it as an emphasis gap, not a disagreement about relevance.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Sun | Secondary | 1 · 9/45 combos | Strong emphasis | 2 · 30/55 charts (55%) | 4/4 | 45 / 55 | 8 | Strong Symbol |
| Moon | Primary | 1 · 9/45 combos | Mentioned | 2 · 38/55 charts (69%) | 4/4 | 45 / 55 | 8 | Strong Symbol |
| Venus | Primary | 1 · 11/45 combos | Mentioned | 2 · 45/55 charts (82%) | 4/4 | 45 / 55 | 8 | Strong Symbol |
| Jupiter | Primary | 1 · 10/45 combos | Strong emphasis | 2 · 37/55 charts (67%) | 4/4 | 45 / 55 | 8 | Strong Symbol |
| Midheaven (10th House cusp) | Primary | 1 · 9/45 combos | Strong emphasis | 1 · 21/55 charts (38%) | 4/4 | 45 / 55 | 8 | Strong Symbol |
| Descendant (7th House cusp) | Primary | — (out of scope) | Mentioned | 2 · 28/55 charts (51%) | 3/3 † | 45 / 55 | 8 | Strong Symbol |
| Mercury | Secondary | 1 · 7/45 combos | Absent | 2 · 27/55 charts (49%) | 3/4 | 45 / 55 | 6 | Moderate (Relevant Symbol) |
| Lunar Node (North/South/unspecified) | Primary | 1 · 9/45 combos | Absent | 1 · 22/55 charts (40%) | 3/4 | 45 / 55 | 6 | Moderate (Relevant Symbol) |
| 5th House cusp | Primary | — (out of scope) | Absent | 2 · 36/55 charts (65%) | 2/3 | 45 / 55 | 6 | Moderate (Relevant Symbol) |
| Mars | Secondary | 1 · 3/45 combos | Absent | 1 · 17/55 charts (31%) | 3/4 | 45 / 55 | 4 | Weak (Occasional Symbol) |
| Uranus | Secondary | 1 · 7/45 combos | Absent | 1 · 20/55 charts (36%) | 3/4 | 45 / 55 | 4 | Weak (Occasional Symbol) |
| Ascendant (1st House cusp) | Absent | 1 · 7/45 combos | Absent | 2 · 27/55 charts (49%) | 2/4 | 45 / 55 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 5/45 combos | Absent | 1 · 19/55 charts (35%) | 2/3 | 45 / 55 | 4 | Weak (Occasional Symbol) |
| Imum Coeli (4th House cusp) | Absent | — (out of scope) | Absent | 2 · 23/55 charts (42%) | 1/3 | 45 / 55 | 4 | Weak (Occasional Symbol) |
| Pluto | Absent | 1 · 4/45 combos | Absent | 1 · 20/55 charts (36%) | 2/4 | 45 / 55 | 2 | Very Weak (Speculative Symbol) |
| 3rd House cusp | Absent | — (out of scope) | Absent | 1 · 6/55 charts (11%) | 1/3 | 45 / 55 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | Absent | 1 · 2/55 charts (4%) | 1/3 | 45 / 55 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 9/55 charts (16%) | 1/3 | 45 / 55 | 2 | Very Weak (Speculative Symbol) |
| 12th House cusp | Absent | — (out of scope) | Absent | 1 · 1/55 charts (2%) | 1/3 | 45 / 55 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Sun**: tier_score = 8 (n_juan_combos_total=45, n_marr_examples_total=55)  |  **Mars**: tier_score = 4 (n_juan_combos_total=45, n_marr_examples_total=55) — *looked up independently; no combined score is produced for this pairing.*
- **Sun**: tier_score = 8 (n_juan_combos_total=45, n_marr_examples_total=55)  |  **12th House cusp**: tier_score = 2 (n_juan_combos_total=45, n_marr_examples_total=55) — *looked up independently; no combined score is produced for this pairing.*
- **Moon**: tier_score = 8 (n_juan_combos_total=45, n_marr_examples_total=55)  |  **12th House cusp**: tier_score = 2 (n_juan_combos_total=45, n_marr_examples_total=55) — *looked up independently; no combined score is produced for this pairing.*
- **Mars**: tier_score = 4 (n_juan_combos_total=45, n_marr_examples_total=55)  |  **Uranus**: tier_score = 4 (n_juan_combos_total=45, n_marr_examples_total=55) — *looked up independently; no combined score is produced for this pairing.*

---

## 8. Marriage for Female

*Category: Union — Native's own marriage (female chart)*

### 1. Event Overview

The female-chart counterpart to Marriage for Male: the Descendant pairs with the Sun or Jupiter rather than Venus/Moon, reflecting the traditional convention of solar significators for a woman's spouse.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Sun, Mars, Jupiter, Moon, Mercury, Venus, Uranus
- Houses/Angles mentioned: Midheaven (10th House cusp), Descendant (7th House cusp), 5th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Sun, Mars, Jupiter, Midheaven (10th House cusp), Descendant (7th House cusp), 5th House cusp, North Node (Ascending)
- **Secondary**: Moon, Mercury, Venus, Uranus
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Venus (11/45), Jupiter (10/45), Sun (9/45), Moon (9/45), Lunar Node (pole unspecified) (9/45), Midheaven (10th House cusp) (9/45), Ascendant (1st House cusp) (7/45), Uranus (7/45), Mercury (7/45), Part of Fortune (5/45)
- Total pairwise combinations catalogued for this event: 45
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: The female-chart counterpart to Marriage for Male: the Descendant pairs with the Sun or Jupiter rather than Venus/Moon, reflecting the traditional convention of solar significators for a woman's spouse.
- Points referenced: Sun (strong), Jupiter (strong), Midheaven (10th House cusp) (strong), Descendant (7th House cusp) (mentioned)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **22 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Moon (18/22, 82%), Uranus (17/22, 77%), Sun (16/22, 73%), Jupiter (16/22, 73%), Midheaven (10th House cusp) (14/22, 64%), 5th House cusp (14/22, 64%), Mercury (13/22, 59%), Venus (12/22, 55%)
- Node detail: North Node in 4, South Node in 0, unspecified-pole Node in 2 of 22 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Sun** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Jupiter** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Midheaven (10th House cusp)** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Moon** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Mercury** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Venus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Mars** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Uranus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Descendant (7th House cusp)** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **5th House cusp** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Ascendant (1st House cusp)** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Imum Coeli (4th House cusp)** — supported by Marr Aspects (score 4/10)
- **Pluto** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Saturn** — supported by Marr Aspects (score 2/10)
- **3rd House cusp** — supported by Marr Aspects (score 2/10)
- **6th House cusp** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Sun, Jupiter, Midheaven (10th House cusp) are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Moon, Mercury, Venus, Mars, Uranus, Descendant (7th House cusp), Lunar Node (North/South/unspecified) are supported by three of the four sources. 1 of these (Descendant (7th House cusp)) sits at the structural ceiling for its symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Pluto, Ascendant (1st House cusp), 5th House cusp, Part of Fortune.

**Speculative / source-specific symbolism.** Saturn (Marr Aspects only), Imum Coeli (4th House cusp) (Marr Aspects only), 3rd House cusp (Marr Aspects only), 6th House cusp (Marr Aspects only), 9th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** Imum Coeli (4th House cusp) (in 11/22 example charts, 50%), Ascendant (1st House cusp) (in 11/22 example charts, 50%) recur in a substantial share of Marr's worked examples without being singled out in POLARIS's Primary/Secondary list. This is not a direct contradiction — POLARIS's list is a short, deliberately curated selection rather than an exhaustive one, and no case was found anywhere in the compendium of a POLARIS-Primary symbol being *absent* from a substantial Marr Aspects sample. Read it as an emphasis gap, not a disagreement about relevance.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Sun | Primary | 1 · 9/45 combos | Strong emphasis | 2 · 16/22 charts (73%) | 4/4 | 45 / 22 | 8 | Strong Symbol |
| Jupiter | Primary | 1 · 10/45 combos | Strong emphasis | 2 · 16/22 charts (73%) | 4/4 | 45 / 22 | 8 | Strong Symbol |
| Midheaven (10th House cusp) | Primary | 1 · 9/45 combos | Strong emphasis | 2 · 14/22 charts (64%) | 4/4 | 45 / 22 | 8 | Strong Symbol |
| Moon | Secondary | 1 · 9/45 combos | Absent | 2 · 18/22 charts (82%) | 3/4 | 45 / 22 | 6 | Moderate (Relevant Symbol) |
| Mercury | Secondary | 1 · 7/45 combos | Absent | 2 · 13/22 charts (59%) | 3/4 | 45 / 22 | 6 | Moderate (Relevant Symbol) |
| Venus | Secondary | 1 · 11/45 combos | Absent | 2 · 12/22 charts (55%) | 3/4 | 45 / 22 | 6 | Moderate (Relevant Symbol) |
| Mars | Primary | 1 · 3/45 combos | Absent | 1 · 4/22 charts (18%) | 3/4 | 45 / 22 | 6 | Moderate (Relevant Symbol) |
| Uranus | Secondary | 1 · 7/45 combos | Absent | 2 · 17/22 charts (77%) | 3/4 | 45 / 22 | 6 | Moderate (Relevant Symbol) |
| Descendant (7th House cusp) | Primary | — (out of scope) | Mentioned | 1 · 7/22 charts (32%) | 3/3 † | 45 / 22 | 6 | Moderate (Relevant Symbol) |
| Lunar Node (North/South/unspecified) | Primary | 1 · 9/45 combos | Absent | 1 · 6/22 charts (27%) | 3/4 | 45 / 22 | 6 | Moderate (Relevant Symbol) |
| 5th House cusp | Primary | — (out of scope) | Absent | 2 · 14/22 charts (64%) | 2/3 | 45 / 22 | 6 | Moderate (Relevant Symbol) |
| Ascendant (1st House cusp) | Absent | 1 · 7/45 combos | Absent | 2 · 11/22 charts (50%) | 2/4 | 45 / 22 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 5/45 combos | Absent | 1 · 4/22 charts (18%) | 2/3 | 45 / 22 | 4 | Weak (Occasional Symbol) |
| Imum Coeli (4th House cusp) | Absent | — (out of scope) | Absent | 2 · 11/22 charts (50%) | 1/3 | 45 / 22 | 4 | Weak (Occasional Symbol) |
| Pluto | Absent | 1 · 4/45 combos | Absent | 1 · 6/22 charts (27%) | 2/4 | 45 / 22 | 2 | Very Weak (Speculative Symbol) |
| Saturn | Absent | 0 · 0/45 combos | Absent | 1 · 2/22 charts (9%) | 1/4 | 45 / 22 | 2 | Very Weak (Speculative Symbol) |
| 3rd House cusp | Absent | — (out of scope) | Absent | 1 · 1/22 charts (5%) | 1/3 | 45 / 22 | 2 | Very Weak (Speculative Symbol) |
| 6th House cusp | Absent | — (out of scope) | Absent | 1 · 1/22 charts (5%) | 1/3 | 45 / 22 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | Absent | 1 · 1/22 charts (5%) | 1/3 | 45 / 22 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 2/22 charts (9%) | 1/3 | 45 / 22 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Sun**: tier_score = 8 (n_juan_combos_total=45, n_marr_examples_total=22)  |  **5th House cusp**: tier_score = 6 (n_juan_combos_total=45, n_marr_examples_total=22) — *looked up independently; no combined score is produced for this pairing.*
- **Sun**: tier_score = 8 (n_juan_combos_total=45, n_marr_examples_total=22)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=45, n_marr_examples_total=22) — *looked up independently; no combined score is produced for this pairing.*
- **Jupiter**: tier_score = 8 (n_juan_combos_total=45, n_marr_examples_total=22)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=45, n_marr_examples_total=22) — *looked up independently; no combined score is produced for this pairing.*
- **5th House cusp**: tier_score = 6 (n_juan_combos_total=45, n_marr_examples_total=22)  |  **Ascendant (1st House cusp)**: tier_score = 4 (n_juan_combos_total=45, n_marr_examples_total=22) — *looked up independently; no combined score is produced for this pairing.*

---

## 9. Child’s Marriage

*Category: Union — Native's child marries*

### 1. Event Overview

Marriage viewed from the parent's own chart rather than the couple's. Alexander Marr's short-form commentary is silent for this event, so the signature rests on POLARIS's list and the worked examples.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Sun, Moon, Mercury, Venus, Jupiter, Mars, Uranus, Pluto
- Houses/Angles mentioned: Midheaven (10th House cusp), Descendant (7th House cusp), 5th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Sun, Moon, Mercury, Venus, Jupiter, Midheaven (10th House cusp), Descendant (7th House cusp), 5th House cusp, North Node (Ascending)
- **Secondary**: Mars, Uranus, Pluto
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Moon (6/18), Lunar Node (pole unspecified) (5/18), Midheaven (10th House cusp) (5/18), Sun (5/18), Jupiter (4/18), Mercury (3/18), Uranus (3/18), Venus (3/18), Ascendant (1st House cusp) (2/18)
- Total pairwise combinations catalogued for this event: 18
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- *No data available from this source* (the compendium explicitly marks this entry “None”).

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **5 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- **Low sample size:** only 5 worked examples available for this event in total — frequencies quoted below (and the corresponding tier_score contributions) are drawn from a very small pool and should be read as suggestive rather than well-established (see `n_marr_examples_total` on each symbol record).
- Most frequent points: Moon (5/5, 100%), Jupiter (4/5, 80%), Descendant (7th House cusp) (3/5, 60%), Venus (3/5, 60%), Sun (3/5, 60%), Mercury (3/5, 60%), Ascendant (1st House cusp) (3/5, 60%), Part of Fortune (3/5, 60%)
- Node detail: North Node in 1, South Node in 0, unspecified-pole Node in 1 of 5 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- **Descendant (7th House cusp)** — supported by POLARIS, Marr Aspects (score 10/10)

**Secondary Symbols**
- **Sun** — supported by POLARIS, Juan Combos, Marr Aspects (score 8/10)
- **Moon** — supported by POLARIS, Juan Combos, Marr Aspects (score 8/10)
- **Mercury** — supported by POLARIS, Juan Combos, Marr Aspects (score 8/10)
- **Venus** — supported by POLARIS, Juan Combos, Marr Aspects (score 8/10)
- **Jupiter** — supported by POLARIS, Juan Combos, Marr Aspects (score 8/10)
- **5th House cusp** — supported by POLARIS, Marr Aspects (score 8/10)
- **Uranus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Midheaven (10th House cusp)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Ascendant (1st House cusp)** — supported by Juan Combos, Marr Aspects (score 6/10)
- **Part of Fortune** — supported by Marr Aspects (score 6/10)

**Occasional Symbols**
- **Mars** — supported by POLARIS (score 2/10)
- **Pluto** — supported by POLARIS (score 2/10)
- **Imum Coeli (4th House cusp)** — supported by Marr Aspects (score 2/10)
- **3rd House cusp** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**Medium-confidence symbolism.** Sun, Moon, Mercury, Venus, Jupiter, Uranus, Midheaven (10th House cusp), Lunar Node (North/South/unspecified) are supported by three of the four sources. All of these sit at the structural ceiling for their symbol type — marked † in the table below — because Other carries no data at all for this event, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Ascendant (1st House cusp), Descendant (7th House cusp), 5th House cusp. All of these are marked † in the table below: for each, only two sources could address the point at all (the other two are structurally out of scope for this event), and those two agree — a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

**Speculative / source-specific symbolism.** Mars (POLARIS only), Pluto (POLARIS only), Imum Coeli (4th House cusp) (Marr Aspects only), 3rd House cusp (Marr Aspects only), 9th House cusp (Marr Aspects only), Part of Fortune (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** No clear-cut contradictions were found for this event: the four sources differ in *emphasis* and *coverage* (which is discussed above) rather than making opposing claims about any single symbol.

**Incomplete information.** Other (marked “None”) contribute no data to this event; the consolidated picture above rests on the remaining source(s) only.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Descendant (7th House cusp) | Primary | — (out of scope) | — (no data) | 2 · 3/5 charts (60%) | 2/2 † | 18 / 5 | 10 | Very Strong (Core Symbol) |
| Sun | Primary | 1 · 5/18 combos | — (no data) | 2 · 3/5 charts (60%) | 3/3 † | 18 / 5 | 8 | Strong Symbol |
| Moon | Primary | 1 · 6/18 combos | — (no data) | 2 · 5/5 charts (100%) | 3/3 † | 18 / 5 | 8 | Strong Symbol |
| Mercury | Primary | 1 · 3/18 combos | — (no data) | 2 · 3/5 charts (60%) | 3/3 † | 18 / 5 | 8 | Strong Symbol |
| Venus | Primary | 1 · 3/18 combos | — (no data) | 2 · 3/5 charts (60%) | 3/3 † | 18 / 5 | 8 | Strong Symbol |
| Jupiter | Primary | 1 · 4/18 combos | — (no data) | 2 · 4/5 charts (80%) | 3/3 † | 18 / 5 | 8 | Strong Symbol |
| 5th House cusp | Primary | — (out of scope) | — (no data) | 1 · 2/5 charts (40%) | 2/2 † | 18 / 5 | 8 | Strong Symbol |
| Uranus | Secondary | 1 · 3/18 combos | — (no data) | 1 · 2/5 charts (40%) | 3/3 † | 18 / 5 | 6 | Moderate (Relevant Symbol) |
| Midheaven (10th House cusp) | Primary | 1 · 5/18 combos | — (no data) | 1 · 2/5 charts (40%) | 3/3 † | 18 / 5 | 6 | Moderate (Relevant Symbol) |
| Lunar Node (North/South/unspecified) | Primary | 1 · 5/18 combos | — (no data) | 1 · 2/5 charts (40%) | 3/3 † | 18 / 5 | 6 | Moderate (Relevant Symbol) |
| Ascendant (1st House cusp) | Absent | 1 · 2/18 combos | — (no data) | 2 · 3/5 charts (60%) | 2/3 | 18 / 5 | 6 | Moderate (Relevant Symbol) |
| Part of Fortune | — (out of scope) | 0 · 0/18 combos | — (no data) | 2 · 3/5 charts (60%) | 1/2 | 18 / 5 | 6 | Moderate (Relevant Symbol) |
| Mars | Secondary | 0 · 0/18 combos | — (no data) | 0 · 0/5 charts (0%) | 1/3 | 18 / 5 | 2 | Very Weak (Speculative Symbol) |
| Pluto | Secondary | 0 · 0/18 combos | — (no data) | 0 · 0/5 charts (0%) | 1/3 | 18 / 5 | 2 | Very Weak (Speculative Symbol) |
| Imum Coeli (4th House cusp) | Absent | — (out of scope) | — (no data) | 1 · 1/5 charts (20%) | 1/2 | 18 / 5 | 2 | Very Weak (Speculative Symbol) |
| 3rd House cusp | Absent | — (out of scope) | — (no data) | 1 · 1/5 charts (20%) | 1/2 | 18 / 5 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | — (no data) | 1 · 1/5 charts (20%) | 1/2 | 18 / 5 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Descendant (7th House cusp)**: tier_score = 10 (n_juan_combos_total=18, n_marr_examples_total=5)  |  **Midheaven (10th House cusp)**: tier_score = 6 (n_juan_combos_total=18, n_marr_examples_total=5) — *looked up independently; no combined score is produced for this pairing.*
- **Descendant (7th House cusp)**: tier_score = 10 (n_juan_combos_total=18, n_marr_examples_total=5)  |  **9th House cusp**: tier_score = 2 (n_juan_combos_total=18, n_marr_examples_total=5) — *looked up independently; no combined score is produced for this pairing.*
- **Sun**: tier_score = 8 (n_juan_combos_total=18, n_marr_examples_total=5)  |  **9th House cusp**: tier_score = 2 (n_juan_combos_total=18, n_marr_examples_total=5) — *looked up independently; no combined score is produced for this pairing.*
- **Midheaven (10th House cusp)**: tier_score = 6 (n_juan_combos_total=18, n_marr_examples_total=5)  |  **Lunar Node (North/South/unspecified)**: tier_score = 6 (n_juan_combos_total=18, n_marr_examples_total=5) — *looked up independently; no combined score is produced for this pairing.*

---

## 10. Positive Travel

*Category: Travel — favorable journey*

### 1. Event Overview

A favorable trip or journey. The 3rd or 9th house cusp combined with the Moon, Mercury or Uranus is the recurring pattern, and Jupiter marks longer journeys or extended stays abroad.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Moon, Mercury, Jupiter, Uranus, Sun, Venus
- Houses/Angles mentioned: Ascendant (1st House cusp), Midheaven (10th House cusp), 9th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Moon, Mercury, Jupiter, Uranus, Ascendant (1st House cusp), Midheaven (10th House cusp), 9th House cusp
- **Secondary**: Sun, Venus, North Node (Ascending)
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Jupiter (12/46), Mercury (11/46), Lunar Node (pole unspecified) (10/46), Venus (9/46), Uranus (8/46), Midheaven (10th House cusp) (8/46), Moon (7/46), Ascendant (1st House cusp) (7/46), Part of Fortune (7/46), Sun (6/46)
- Total pairwise combinations catalogued for this event: 46
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: A favorable trip or journey. The 3rd or 9th house cusp combined with the Moon, Mercury or Uranus is the recurring pattern, and Jupiter marks longer journeys or extended stays abroad.
- Points referenced: Moon (mentioned), Mercury (mentioned), Jupiter (mentioned), Uranus (mentioned), Neptune (mentioned), 3rd House cusp (mentioned), 9th House cusp (mentioned)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **21 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Moon (15/21, 71%), Venus (13/21, 62%), Sun (11/21, 52%), Jupiter (11/21, 52%), Ascendant (1st House cusp) (11/21, 52%), 9th House cusp (10/21, 48%), Mercury (9/21, 43%), Midheaven (10th House cusp) (7/21, 33%)
- Node detail: North Node in 2, South Node in 0, unspecified-pole Node in 1 of 21 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Moon** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Jupiter** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **9th House cusp** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **Mercury** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 6/10)
- **Uranus** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 6/10)
- **Sun** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Venus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Midheaven (10th House cusp)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Neptune** — supported by Juan Combos, Other, Marr Aspects (score 4/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 4/10)
- **3rd House cusp** — supported by Other, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Mars** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Pluto** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Imum Coeli (4th House cusp)** — supported by Marr Aspects (score 2/10)
- **5th House cusp** — supported by Marr Aspects (score 2/10)
- **6th House cusp** — supported by Marr Aspects (score 2/10)
- **8th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Moon, Mercury, Jupiter, Uranus are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Sun, Venus, Neptune, Ascendant (1st House cusp), Midheaven (10th House cusp), 9th House cusp, Lunar Node (North/South/unspecified) are supported by three of the four sources. 1 of these (9th House cusp) sits at the structural ceiling for its symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Mars, Pluto, 3rd House cusp, Part of Fortune.

**Speculative / source-specific symbolism.** Imum Coeli (4th House cusp) (Marr Aspects only), 5th House cusp (Marr Aspects only), 6th House cusp (Marr Aspects only), 8th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** No clear-cut contradictions were found for this event: the four sources differ in *emphasis* and *coverage* (which is discussed above) rather than making opposing claims about any single symbol.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Moon | Primary | 1 · 7/46 combos | Mentioned | 2 · 15/21 charts (71%) | 4/4 | 46 / 21 | 8 | Strong Symbol |
| Jupiter | Primary | 1 · 12/46 combos | Mentioned | 2 · 11/21 charts (52%) | 4/4 | 46 / 21 | 8 | Strong Symbol |
| 9th House cusp | Primary | — (out of scope) | Mentioned | 2 · 10/21 charts (48%) | 3/3 † | 46 / 21 | 8 | Strong Symbol |
| Mercury | Primary | 1 · 11/46 combos | Mentioned | 1 · 9/21 charts (43%) | 4/4 | 46 / 21 | 6 | Moderate (Relevant Symbol) |
| Uranus | Primary | 1 · 8/46 combos | Mentioned | 1 · 5/21 charts (24%) | 4/4 | 46 / 21 | 6 | Moderate (Relevant Symbol) |
| Sun | Secondary | 1 · 6/46 combos | Absent | 2 · 11/21 charts (52%) | 3/4 | 46 / 21 | 6 | Moderate (Relevant Symbol) |
| Venus | Secondary | 1 · 9/46 combos | Absent | 2 · 13/21 charts (62%) | 3/4 | 46 / 21 | 6 | Moderate (Relevant Symbol) |
| Ascendant (1st House cusp) | Primary | 1 · 7/46 combos | Absent | 2 · 11/21 charts (52%) | 3/4 | 46 / 21 | 6 | Moderate (Relevant Symbol) |
| Midheaven (10th House cusp) | Primary | 1 · 8/46 combos | Absent | 1 · 7/21 charts (33%) | 3/4 | 46 / 21 | 6 | Moderate (Relevant Symbol) |
| Neptune | Absent | 1 · 3/46 combos | Mentioned | 1 · 1/21 charts (5%) | 3/4 | 46 / 21 | 4 | Weak (Occasional Symbol) |
| Lunar Node (North/South/unspecified) | Secondary | 1 · 10/46 combos | Absent | 1 · 3/21 charts (14%) | 3/4 | 46 / 21 | 4 | Weak (Occasional Symbol) |
| 3rd House cusp | Absent | — (out of scope) | Mentioned | 1 · 2/21 charts (10%) | 2/3 | 46 / 21 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 7/46 combos | Absent | 1 · 3/21 charts (14%) | 2/3 | 46 / 21 | 4 | Weak (Occasional Symbol) |
| Mars | Absent | 1 · 1/46 combos | Absent | 1 · 2/21 charts (10%) | 2/4 | 46 / 21 | 2 | Very Weak (Speculative Symbol) |
| Pluto | Absent | 1 · 3/46 combos | Absent | 1 · 2/21 charts (10%) | 2/4 | 46 / 21 | 2 | Very Weak (Speculative Symbol) |
| Imum Coeli (4th House cusp) | Absent | — (out of scope) | Absent | 1 · 4/21 charts (19%) | 1/3 | 46 / 21 | 2 | Very Weak (Speculative Symbol) |
| 5th House cusp | Absent | — (out of scope) | Absent | 1 · 2/21 charts (10%) | 1/3 | 46 / 21 | 2 | Very Weak (Speculative Symbol) |
| 6th House cusp | Absent | — (out of scope) | Absent | 1 · 1/21 charts (5%) | 1/3 | 46 / 21 | 2 | Very Weak (Speculative Symbol) |
| 8th House cusp | Absent | — (out of scope) | Absent | 1 · 1/21 charts (5%) | 1/3 | 46 / 21 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 2/21 charts (10%) | 1/3 | 46 / 21 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Moon**: tier_score = 8 (n_juan_combos_total=46, n_marr_examples_total=21)  |  **Lunar Node (North/South/unspecified)**: tier_score = 4 (n_juan_combos_total=46, n_marr_examples_total=21) — *looked up independently; no combined score is produced for this pairing.*
- **Moon**: tier_score = 8 (n_juan_combos_total=46, n_marr_examples_total=21)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=46, n_marr_examples_total=21) — *looked up independently; no combined score is produced for this pairing.*
- **Jupiter**: tier_score = 8 (n_juan_combos_total=46, n_marr_examples_total=21)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=46, n_marr_examples_total=21) — *looked up independently; no combined score is produced for this pairing.*
- **Lunar Node (North/South/unspecified)**: tier_score = 4 (n_juan_combos_total=46, n_marr_examples_total=21)  |  **3rd House cusp**: tier_score = 4 (n_juan_combos_total=46, n_marr_examples_total=21) — *looked up independently; no combined score is produced for this pairing.*

---

## 11. Positive Travel Overseas

*Category: Travel — favorable journey abroad*

### 1. Event Overview

A geographically specific variant of Positive Travel, sharing its base symbolism (3rd/9th house cusp with the Moon, Mercury or Uranus; Jupiter for duration) while adding Neptune for overseas travel or flights specifically. Juan Combos points back to its general 'Positive Travel' entry and adds only one supplementary combination of its own.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Moon, Mercury, Jupiter, Uranus, Sun, Venus, Neptune
- Houses/Angles mentioned: Ascendant (1st House cusp), Midheaven (10th House cusp), 9th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Moon, Mercury, Jupiter, Uranus, Ascendant (1st House cusp), Midheaven (10th House cusp), 9th House cusp
- **Secondary**: Sun, Venus, Neptune, North Node (Ascending)
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Neptune (2/2), Uranus (1/2), Part of Fortune (1/2)
- Total pairwise combinations catalogued for this event: 2
- **Low sample size:** only 2 combinations catalogued for this event in total — any single symbol's Juan Combos percentage here rests on very little underlying data, and the tier_score for symbols resting mainly on this source should be read with that in mind (see `n_juan_combos_total` on each symbol record).
- Unique observation: this entry explicitly cross-references **Positive Travel** for its main combination list and supplies only the combinations shown above as specific to this event.
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: A geographically specific variant of Positive Travel, sharing its base symbolism (3rd/9th house cusp with the Moon, Mercury or Uranus; Jupiter for duration) while adding Neptune for overseas travel or flights specifically. Juan Combos points back to its general 'Positive Travel' entry and adds only one supplementary combination of its own.
- Points referenced: Moon (mentioned), Mercury (mentioned), Jupiter (mentioned), Uranus (mentioned), Neptune (mentioned), 3rd House cusp (mentioned), 9th House cusp (mentioned)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **73 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: 9th House cusp (55/73, 75%), Jupiter (48/73, 66%), Moon (44/73, 60%), Midheaven (10th House cusp) (42/73, 58%), Venus (37/73, 51%), Mercury (36/73, 49%), Ascendant (1st House cusp) (36/73, 49%), Sun (35/73, 48%)
- Node detail: North Node in 9, South Node in 1, unspecified-pole Node in 6 of 73 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Uranus** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **9th House cusp** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **Neptune** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 6/10)
- **Moon** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **Mercury** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **Jupiter** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Marr Aspects (score 6/10)
- **Midheaven (10th House cusp)** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Sun** — supported by POLARIS, Marr Aspects (score 4/10)
- **Venus** — supported by POLARIS, Marr Aspects (score 4/10)
- **3rd House cusp** — supported by Other, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Marr Aspects (score 2/10)
- **Mars** — supported by Marr Aspects (score 2/10)
- **Saturn** — supported by Marr Aspects (score 2/10)
- **Pluto** — supported by Marr Aspects (score 2/10)
- **Descendant (7th House cusp)** — supported by Marr Aspects (score 2/10)
- **Imum Coeli (4th House cusp)** — supported by Marr Aspects (score 2/10)
- **2nd House cusp** — supported by Marr Aspects (score 2/10)
- **5th House cusp** — supported by Marr Aspects (score 2/10)
- **6th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)
- **12th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Uranus, Neptune are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Moon, Mercury, Jupiter, 9th House cusp are supported by three of the four sources. 1 of these (9th House cusp) sits at the structural ceiling for its symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Sun, Venus, Ascendant (1st House cusp), Midheaven (10th House cusp), 3rd House cusp, Lunar Node (North/South/unspecified), Part of Fortune.

**Speculative / source-specific symbolism.** Mars (Marr Aspects only), Saturn (Marr Aspects only), Pluto (Marr Aspects only), Descendant (7th House cusp) (Marr Aspects only), Imum Coeli (4th House cusp) (Marr Aspects only), 2nd House cusp (Marr Aspects only), 5th House cusp (Marr Aspects only), 6th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only), 12th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** No clear-cut contradictions were found for this event: the four sources differ in *emphasis* and *coverage* (which is discussed above) rather than making opposing claims about any single symbol.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Uranus | Primary | 1 · 1/2 combos | Mentioned | 2 · 34/73 charts (47%) | 4/4 | 2 / 73 | 8 | Strong Symbol |
| 9th House cusp | Primary | — (out of scope) | Mentioned | 2 · 55/73 charts (75%) | 3/3 † | 2 / 73 | 8 | Strong Symbol |
| Neptune | Secondary | 1 · 2/2 combos | Mentioned | 1 · 17/73 charts (23%) | 4/4 | 2 / 73 | 6 | Moderate (Relevant Symbol) |
| Moon | Primary | 0 · 0/2 combos | Mentioned | 2 · 44/73 charts (60%) | 3/4 | 2 / 73 | 6 | Moderate (Relevant Symbol) |
| Mercury | Primary | 0 · 0/2 combos | Mentioned | 2 · 36/73 charts (49%) | 3/4 | 2 / 73 | 6 | Moderate (Relevant Symbol) |
| Jupiter | Primary | 0 · 0/2 combos | Mentioned | 2 · 48/73 charts (66%) | 3/4 | 2 / 73 | 6 | Moderate (Relevant Symbol) |
| Ascendant (1st House cusp) | Primary | 0 · 0/2 combos | Absent | 2 · 36/73 charts (49%) | 2/4 | 2 / 73 | 6 | Moderate (Relevant Symbol) |
| Midheaven (10th House cusp) | Primary | 0 · 0/2 combos | Absent | 2 · 42/73 charts (58%) | 2/4 | 2 / 73 | 6 | Moderate (Relevant Symbol) |
| Sun | Secondary | 0 · 0/2 combos | Absent | 2 · 35/73 charts (48%) | 2/4 | 2 / 73 | 4 | Weak (Occasional Symbol) |
| Venus | Secondary | 0 · 0/2 combos | Absent | 2 · 37/73 charts (51%) | 2/4 | 2 / 73 | 4 | Weak (Occasional Symbol) |
| 3rd House cusp | Absent | — (out of scope) | Mentioned | 1 · 7/73 charts (10%) | 2/3 | 2 / 73 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 1/2 combos | Absent | 1 · 14/73 charts (19%) | 2/3 | 2 / 73 | 4 | Weak (Occasional Symbol) |
| Lunar Node (North/South/unspecified) | Secondary | 0 · 0/2 combos | Absent | 1 · 16/73 charts (22%) | 2/4 | 2 / 73 | 2 | Very Weak (Speculative Symbol) |
| Mars | Absent | 0 · 0/2 combos | Absent | 1 · 9/73 charts (12%) | 1/4 | 2 / 73 | 2 | Very Weak (Speculative Symbol) |
| Saturn | Absent | 0 · 0/2 combos | Absent | 1 · 2/73 charts (3%) | 1/4 | 2 / 73 | 2 | Very Weak (Speculative Symbol) |
| Pluto | Absent | 0 · 0/2 combos | Absent | 1 · 12/73 charts (16%) | 1/4 | 2 / 73 | 2 | Very Weak (Speculative Symbol) |
| Descendant (7th House cusp) | Absent | — (out of scope) | Absent | 1 · 8/73 charts (11%) | 1/3 | 2 / 73 | 2 | Very Weak (Speculative Symbol) |
| Imum Coeli (4th House cusp) | Absent | — (out of scope) | Absent | 1 · 8/73 charts (11%) | 1/3 | 2 / 73 | 2 | Very Weak (Speculative Symbol) |
| 2nd House cusp | Absent | — (out of scope) | Absent | 1 · 1/73 charts (1%) | 1/3 | 2 / 73 | 2 | Very Weak (Speculative Symbol) |
| 5th House cusp | Absent | — (out of scope) | Absent | 1 · 3/73 charts (4%) | 1/3 | 2 / 73 | 2 | Very Weak (Speculative Symbol) |
| 6th House cusp | Absent | — (out of scope) | Absent | 1 · 1/73 charts (1%) | 1/3 | 2 / 73 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 13/73 charts (18%) | 1/3 | 2 / 73 | 2 | Very Weak (Speculative Symbol) |
| 12th House cusp | Absent | — (out of scope) | Absent | 1 · 2/73 charts (3%) | 1/3 | 2 / 73 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Uranus**: tier_score = 8 (n_juan_combos_total=2, n_marr_examples_total=73)  |  **Part of Fortune**: tier_score = 4 (n_juan_combos_total=2, n_marr_examples_total=73) — *looked up independently; no combined score is produced for this pairing.*
- **Uranus**: tier_score = 8 (n_juan_combos_total=2, n_marr_examples_total=73)  |  **12th House cusp**: tier_score = 2 (n_juan_combos_total=2, n_marr_examples_total=73) — *looked up independently; no combined score is produced for this pairing.*
- **9th House cusp**: tier_score = 8 (n_juan_combos_total=2, n_marr_examples_total=73)  |  **12th House cusp**: tier_score = 2 (n_juan_combos_total=2, n_marr_examples_total=73) — *looked up independently; no combined score is produced for this pairing.*
- **Part of Fortune**: tier_score = 4 (n_juan_combos_total=2, n_marr_examples_total=73)  |  **Lunar Node (North/South/unspecified)**: tier_score = 2 (n_juan_combos_total=2, n_marr_examples_total=73) — *looked up independently; no combined score is produced for this pairing.*

---

## 12. Success or Elected

*Category: Achievement — professional success, honors, election*

### 1. Event Overview

The broadest achievement category in the compendium, spanning elections, honors, decorations, favorable romantic affairs, salary rises and business succession. The Midheaven and Ascendant anchor the signature, joined by the Sun, Moon, Mercury, Jupiter, Uranus and Venus depending on which flavor of success is in play.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Sun, Moon, Mercury, Venus, Jupiter, Uranus
- Houses/Angles mentioned: Ascendant (1st House cusp), Midheaven (10th House cusp), 3rd House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Sun, Moon, Mercury, Venus, Jupiter, Uranus, Ascendant (1st House cusp), Midheaven (10th House cusp), 3rd House cusp
- **Secondary**: North Node (Ascending)
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Venus (16/65), Jupiter (13/65), Uranus (13/65), Ascendant (1st House cusp) (11/65), Lunar Node (pole unspecified) (11/65), Sun (10/65), Moon (10/65), Mercury (10/65), Midheaven (10th House cusp) (10/65), Part of Fortune (9/65)
- Total pairwise combinations catalogued for this event: 65
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: The broadest achievement category in the compendium, spanning elections, honors, decorations, favorable romantic affairs, salary rises and business succession. The Midheaven and Ascendant anchor the signature, joined by the Sun, Moon, Mercury, Jupiter, Uranus and Venus depending on which flavor of success is in play.
- Points referenced: Venus (strong), Mars (strong), Jupiter (strong), Pluto (strong), Ascendant (1st House cusp) (strong), 5th House cusp (strong), 8th House cusp (strong), Sun (mentioned), Moon (mentioned), Mercury (mentioned), Uranus (mentioned), Neptune (mentioned), Midheaven (10th House cusp) (mentioned), 2nd House cusp (mentioned), 3rd House cusp (mentioned)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **306 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Jupiter (231/306, 75%), Sun (213/306, 70%), Midheaven (10th House cusp) (199/306, 65%), Moon (193/306, 63%), Mercury (189/306, 62%), Venus (186/306, 61%), Ascendant (1st House cusp) (173/306, 57%), Uranus (166/306, 54%)
- Node detail: North Node in 49, South Node in 6, unspecified-pole Node in 15 of 306 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Sun** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Moon** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Mercury** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Venus** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Jupiter** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Uranus** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Midheaven (10th House cusp)** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **3rd House cusp** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **Mars** — supported by Juan Combos, Other, Marr Aspects (score 6/10)
- **Pluto** — supported by Juan Combos, Other, Marr Aspects (score 6/10)
- **5th House cusp** — supported by Other, Marr Aspects (score 6/10)
- **8th House cusp** — supported by Other, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Neptune** — supported by Juan Combos, Other, Marr Aspects (score 4/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 4/10)
- **2nd House cusp** — supported by Other, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Saturn** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Descendant (7th House cusp)** — supported by Marr Aspects (score 2/10)
- **Imum Coeli (4th House cusp)** — supported by Marr Aspects (score 2/10)
- **6th House cusp** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)
- **12th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Sun, Moon, Mercury, Venus, Jupiter, Uranus, Ascendant (1st House cusp), Midheaven (10th House cusp) are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Mars, Neptune, Pluto, 3rd House cusp, Lunar Node (North/South/unspecified) are supported by three of the four sources. 1 of these (3rd House cusp) sits at the structural ceiling for its symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Saturn, 2nd House cusp, 5th House cusp, 8th House cusp, Part of Fortune.

**Speculative / source-specific symbolism.** Descendant (7th House cusp) (Marr Aspects only), Imum Coeli (4th House cusp) (Marr Aspects only), 6th House cusp (Marr Aspects only), 9th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only), 12th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** No clear-cut contradictions were found for this event: the four sources differ in *emphasis* and *coverage* (which is discussed above) rather than making opposing claims about any single symbol.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Sun | Primary | 1 · 10/65 combos | Mentioned | 2 · 213/306 charts (70%) | 4/4 | 65 / 306 | 8 | Strong Symbol |
| Moon | Primary | 1 · 10/65 combos | Mentioned | 2 · 193/306 charts (63%) | 4/4 | 65 / 306 | 8 | Strong Symbol |
| Mercury | Primary | 1 · 10/65 combos | Mentioned | 2 · 189/306 charts (62%) | 4/4 | 65 / 306 | 8 | Strong Symbol |
| Venus | Primary | 1 · 16/65 combos | Strong emphasis | 2 · 186/306 charts (61%) | 4/4 | 65 / 306 | 8 | Strong Symbol |
| Jupiter | Primary | 1 · 13/65 combos | Strong emphasis | 2 · 231/306 charts (75%) | 4/4 | 65 / 306 | 8 | Strong Symbol |
| Uranus | Primary | 1 · 13/65 combos | Mentioned | 2 · 166/306 charts (54%) | 4/4 | 65 / 306 | 8 | Strong Symbol |
| Ascendant (1st House cusp) | Primary | 1 · 11/65 combos | Strong emphasis | 2 · 173/306 charts (57%) | 4/4 | 65 / 306 | 8 | Strong Symbol |
| Midheaven (10th House cusp) | Primary | 1 · 10/65 combos | Mentioned | 2 · 199/306 charts (65%) | 4/4 | 65 / 306 | 8 | Strong Symbol |
| 3rd House cusp | Primary | — (out of scope) | Mentioned | 2 · 155/306 charts (51%) | 3/3 † | 65 / 306 | 8 | Strong Symbol |
| Mars | Absent | 1 · 7/65 combos | Strong emphasis | 1 · 83/306 charts (27%) | 3/4 | 65 / 306 | 6 | Moderate (Relevant Symbol) |
| Pluto | Absent | 1 · 8/65 combos | Strong emphasis | 1 · 66/306 charts (22%) | 3/4 | 65 / 306 | 6 | Moderate (Relevant Symbol) |
| 5th House cusp | Absent | — (out of scope) | Strong emphasis | 1 · 12/306 charts (4%) | 2/3 | 65 / 306 | 6 | Moderate (Relevant Symbol) |
| 8th House cusp | Absent | — (out of scope) | Strong emphasis | 1 · 16/306 charts (5%) | 2/3 | 65 / 306 | 6 | Moderate (Relevant Symbol) |
| Neptune | Absent | 1 · 1/65 combos | Mentioned | 1 · 24/306 charts (8%) | 3/4 | 65 / 306 | 4 | Weak (Occasional Symbol) |
| Lunar Node (North/South/unspecified) | Secondary | 1 · 11/65 combos | Absent | 1 · 70/306 charts (23%) | 3/4 | 65 / 306 | 4 | Weak (Occasional Symbol) |
| 2nd House cusp | Absent | — (out of scope) | Mentioned | 1 · 12/306 charts (4%) | 2/3 | 65 / 306 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 9/65 combos | Absent | 1 · 77/306 charts (25%) | 2/3 | 65 / 306 | 4 | Weak (Occasional Symbol) |
| Saturn | Absent | 1 · 1/65 combos | Absent | 1 · 25/306 charts (8%) | 2/4 | 65 / 306 | 2 | Very Weak (Speculative Symbol) |
| Descendant (7th House cusp) | Absent | — (out of scope) | Absent | 1 · 50/306 charts (16%) | 1/3 | 65 / 306 | 2 | Very Weak (Speculative Symbol) |
| Imum Coeli (4th House cusp) | Absent | — (out of scope) | Absent | 1 · 20/306 charts (7%) | 1/3 | 65 / 306 | 2 | Very Weak (Speculative Symbol) |
| 6th House cusp | Absent | — (out of scope) | Absent | 1 · 18/306 charts (6%) | 1/3 | 65 / 306 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | Absent | 1 · 38/306 charts (12%) | 1/3 | 65 / 306 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 70/306 charts (23%) | 1/3 | 65 / 306 | 2 | Very Weak (Speculative Symbol) |
| 12th House cusp | Absent | — (out of scope) | Absent | 1 · 14/306 charts (5%) | 1/3 | 65 / 306 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Sun**: tier_score = 8 (n_juan_combos_total=65, n_marr_examples_total=306)  |  **8th House cusp**: tier_score = 6 (n_juan_combos_total=65, n_marr_examples_total=306) — *looked up independently; no combined score is produced for this pairing.*
- **Sun**: tier_score = 8 (n_juan_combos_total=65, n_marr_examples_total=306)  |  **12th House cusp**: tier_score = 2 (n_juan_combos_total=65, n_marr_examples_total=306) — *looked up independently; no combined score is produced for this pairing.*
- **Moon**: tier_score = 8 (n_juan_combos_total=65, n_marr_examples_total=306)  |  **12th House cusp**: tier_score = 2 (n_juan_combos_total=65, n_marr_examples_total=306) — *looked up independently; no combined score is produced for this pairing.*
- **8th House cusp**: tier_score = 6 (n_juan_combos_total=65, n_marr_examples_total=306)  |  **Neptune**: tier_score = 4 (n_juan_combos_total=65, n_marr_examples_total=306) — *looked up independently; no combined score is produced for this pairing.*

---

## 13. Graduation or Publication

*Category: Achievement — education / publishing milestone*

### 1. Event Overview

Completing a course of study or publishing a work. Marr's short-form commentary is silent and Juan Combos supplies only a single combination, so this entry leans heavily on POLARIS's list and the worked example charts.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Sun, Moon, Mercury, Venus, Jupiter, Uranus
- Houses/Angles mentioned: Ascendant (1st House cusp), Midheaven (10th House cusp), 3rd House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Sun, Moon, Mercury, Venus, Jupiter, Uranus, Ascendant (1st House cusp), Midheaven (10th House cusp), 3rd House cusp
- **Secondary**: North Node (Ascending)
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Jupiter (1/1), Uranus (1/1)
- Total pairwise combinations catalogued for this event: 1
- **Low sample size:** only 1 combination catalogued for this event in total — any single symbol's Juan Combos percentage here rests on very little underlying data, and the tier_score for symbols resting mainly on this source should be read with that in mind (see `n_juan_combos_total` on each symbol record).
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- *No data available from this source* (the compendium explicitly marks this entry “None”).

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **22 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Midheaven (10th House cusp) (19/22, 86%), Mercury (16/22, 73%), Moon (15/22, 68%), 3rd House cusp (14/22, 64%), Venus (13/22, 59%), Ascendant (1st House cusp) (13/22, 59%), Sun (13/22, 59%), Jupiter (10/22, 45%)

### 3. Consolidated Symbolism

**Primary Symbols**
- **3rd House cusp** — supported by POLARIS, Marr Aspects (score 10/10)

**Secondary Symbols**
- **Jupiter** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Uranus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Sun** — supported by POLARIS, Marr Aspects (score 6/10)
- **Moon** — supported by POLARIS, Marr Aspects (score 6/10)
- **Mercury** — supported by POLARIS, Marr Aspects (score 6/10)
- **Venus** — supported by POLARIS, Marr Aspects (score 6/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Marr Aspects (score 6/10)
- **Midheaven (10th House cusp)** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Mars** — supported by Marr Aspects (score 2/10)
- **Pluto** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS (score 2/10)
- **Part of Fortune** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**Medium-confidence symbolism.** Jupiter, Uranus are supported by three of the four sources. All of these sit at the structural ceiling for their symbol type — marked † in the table below — because Other carries no data at all for this event, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Sun, Moon, Mercury, Venus, Ascendant (1st House cusp), Midheaven (10th House cusp), 3rd House cusp. All of these are marked † in the table below: for each, only two sources could address the point at all (the other two are structurally out of scope for this event), and those two agree — a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

**Speculative / source-specific symbolism.** Mars (Marr Aspects only), Pluto (Marr Aspects only), 9th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only), Lunar Node (North/South/unspecified) (POLARIS only), Part of Fortune (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** No clear-cut contradictions were found for this event: the four sources differ in *emphasis* and *coverage* (which is discussed above) rather than making opposing claims about any single symbol.

**Incomplete information.** Other (marked “None”) contribute no data to this event; the consolidated picture above rests on the remaining source(s) only.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| 3rd House cusp | Primary | — (out of scope) | — (no data) | 2 · 14/22 charts (64%) | 2/2 † | 1 / 22 | 10 | Very Strong (Core Symbol) |
| Jupiter | Primary | 1 · 1/1 combos | — (no data) | 1 · 10/22 charts (45%) | 3/3 † | 1 / 22 | 6 | Moderate (Relevant Symbol) |
| Uranus | Primary | 1 · 1/1 combos | — (no data) | 1 · 5/22 charts (23%) | 3/3 † | 1 / 22 | 6 | Moderate (Relevant Symbol) |
| Sun | Primary | 0 · 0/1 combos | — (no data) | 2 · 13/22 charts (59%) | 2/3 | 1 / 22 | 6 | Moderate (Relevant Symbol) |
| Moon | Primary | 0 · 0/1 combos | — (no data) | 2 · 15/22 charts (68%) | 2/3 | 1 / 22 | 6 | Moderate (Relevant Symbol) |
| Mercury | Primary | 0 · 0/1 combos | — (no data) | 2 · 16/22 charts (73%) | 2/3 | 1 / 22 | 6 | Moderate (Relevant Symbol) |
| Venus | Primary | 0 · 0/1 combos | — (no data) | 2 · 13/22 charts (59%) | 2/3 | 1 / 22 | 6 | Moderate (Relevant Symbol) |
| Ascendant (1st House cusp) | Primary | 0 · 0/1 combos | — (no data) | 2 · 13/22 charts (59%) | 2/3 | 1 / 22 | 6 | Moderate (Relevant Symbol) |
| Midheaven (10th House cusp) | Primary | 0 · 0/1 combos | — (no data) | 2 · 19/22 charts (86%) | 2/3 | 1 / 22 | 6 | Moderate (Relevant Symbol) |
| Mars | Absent | 0 · 0/1 combos | — (no data) | 1 · 1/22 charts (5%) | 1/3 | 1 / 22 | 2 | Very Weak (Speculative Symbol) |
| Pluto | Absent | 0 · 0/1 combos | — (no data) | 1 · 1/22 charts (5%) | 1/3 | 1 / 22 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | — (no data) | 1 · 1/22 charts (5%) | 1/2 | 1 / 22 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | — (no data) | 1 · 2/22 charts (9%) | 1/2 | 1 / 22 | 2 | Very Weak (Speculative Symbol) |
| Lunar Node (North/South/unspecified) | Secondary | 0 · 0/1 combos | — (no data) | 0 · 0/22 charts (0%) | 1/3 | 1 / 22 | 2 | Very Weak (Speculative Symbol) |
| Part of Fortune | — (out of scope) | 0 · 0/1 combos | — (no data) | 1 · 3/22 charts (14%) | 1/2 | 1 / 22 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **3rd House cusp**: tier_score = 10 (n_juan_combos_total=1, n_marr_examples_total=22)  |  **Ascendant (1st House cusp)**: tier_score = 6 (n_juan_combos_total=1, n_marr_examples_total=22) — *looked up independently; no combined score is produced for this pairing.*
- **3rd House cusp**: tier_score = 10 (n_juan_combos_total=1, n_marr_examples_total=22)  |  **Part of Fortune**: tier_score = 2 (n_juan_combos_total=1, n_marr_examples_total=22) — *looked up independently; no combined score is produced for this pairing.*
- **Jupiter**: tier_score = 6 (n_juan_combos_total=1, n_marr_examples_total=22)  |  **Part of Fortune**: tier_score = 2 (n_juan_combos_total=1, n_marr_examples_total=22) — *looked up independently; no combined score is produced for this pairing.*
- **Ascendant (1st House cusp)**: tier_score = 6 (n_juan_combos_total=1, n_marr_examples_total=22)  |  **Midheaven (10th House cusp)**: tier_score = 6 (n_juan_combos_total=1, n_marr_examples_total=22) — *looked up independently; no combined score is produced for this pairing.*

---

## 14. Move Home

*Category: Domestic — change of residence*

### 1. Event Overview

A change of residence. As with several less common categories, Alexander Marr's short-form commentary offers no separate note here; the signature is built from POLARIS and the worked examples only.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Sun, Moon, Mercury, Venus, Jupiter, Uranus
- Houses/Angles mentioned: Ascendant (1st House cusp), Imum Coeli (4th House cusp), 3rd House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Sun, Moon, Mercury, Venus, Jupiter, Ascendant (1st House cusp), Imum Coeli (4th House cusp), 3rd House cusp, North Node (Ascending)
- **Secondary**: Uranus
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Mercury (7/18), Midheaven (10th House cusp) (5/18), Jupiter (4/18), Lunar Node (pole unspecified) (4/18), Moon (4/18), Sun (3/18), Uranus (3/18), Venus (2/18), Neptune (2/18), Part of Fortune (1/18)
- Total pairwise combinations catalogued for this event: 18
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- *No data available from this source* (the compendium explicitly marks this entry “None”).

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **16 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Jupiter (12/16, 75%), Mercury (11/16, 69%), Venus (10/16, 62%), Moon (10/16, 62%), Ascendant (1st House cusp) (10/16, 62%), 3rd House cusp (9/16, 56%), Uranus (9/16, 56%), Imum Coeli (4th House cusp) (9/16, 56%)
- Node detail: North Node in 1, South Node in 1, unspecified-pole Node in 3 of 16 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- **Imum Coeli (4th House cusp)** — supported by POLARIS, Marr Aspects (score 10/10)
- **3rd House cusp** — supported by POLARIS, Marr Aspects (score 10/10)

**Secondary Symbols**
- **Sun** — supported by POLARIS, Juan Combos, Marr Aspects (score 8/10)
- **Moon** — supported by POLARIS, Juan Combos, Marr Aspects (score 8/10)
- **Mercury** — supported by POLARIS, Juan Combos, Marr Aspects (score 8/10)
- **Venus** — supported by POLARIS, Juan Combos, Marr Aspects (score 8/10)
- **Jupiter** — supported by POLARIS, Juan Combos, Marr Aspects (score 8/10)
- **Uranus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Marr Aspects (score 6/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Pluto** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Midheaven (10th House cusp)** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Mars** — supported by Marr Aspects (score 2/10)
- **Saturn** — supported by Marr Aspects (score 2/10)
- **Neptune** — supported by Juan Combos (score 2/10)
- **Descendant (7th House cusp)** — supported by Marr Aspects (score 2/10)
- **2nd House cusp** — supported by Marr Aspects (score 2/10)
- **5th House cusp** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**Medium-confidence symbolism.** Sun, Moon, Mercury, Venus, Jupiter, Uranus, Lunar Node (North/South/unspecified) are supported by three of the four sources. All of these sit at the structural ceiling for their symbol type — marked † in the table below — because Other carries no data at all for this event, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Pluto, Ascendant (1st House cusp), Midheaven (10th House cusp), Imum Coeli (4th House cusp), 3rd House cusp, Part of Fortune. All of these are marked † in the table below: for each, only two sources could address the point at all (the other two are structurally out of scope for this event), and those two agree — a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

**Speculative / source-specific symbolism.** Mars (Marr Aspects only), Saturn (Marr Aspects only), Neptune (Juan Combos only), Descendant (7th House cusp) (Marr Aspects only), 2nd House cusp (Marr Aspects only), 5th House cusp (Marr Aspects only), 9th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** No clear-cut contradictions were found for this event: the four sources differ in *emphasis* and *coverage* (which is discussed above) rather than making opposing claims about any single symbol.

**Incomplete information.** Other (marked “None”) contribute no data to this event; the consolidated picture above rests on the remaining source(s) only.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Imum Coeli (4th House cusp) | Primary | — (out of scope) | — (no data) | 2 · 9/16 charts (56%) | 2/2 † | 18 / 16 | 10 | Very Strong (Core Symbol) |
| 3rd House cusp | Primary | — (out of scope) | — (no data) | 2 · 9/16 charts (56%) | 2/2 † | 18 / 16 | 10 | Very Strong (Core Symbol) |
| Sun | Primary | 1 · 3/18 combos | — (no data) | 2 · 8/16 charts (50%) | 3/3 † | 18 / 16 | 8 | Strong Symbol |
| Moon | Primary | 1 · 4/18 combos | — (no data) | 2 · 10/16 charts (62%) | 3/3 † | 18 / 16 | 8 | Strong Symbol |
| Mercury | Primary | 1 · 7/18 combos | — (no data) | 2 · 11/16 charts (69%) | 3/3 † | 18 / 16 | 8 | Strong Symbol |
| Venus | Primary | 1 · 2/18 combos | — (no data) | 2 · 10/16 charts (62%) | 3/3 † | 18 / 16 | 8 | Strong Symbol |
| Jupiter | Primary | 1 · 4/18 combos | — (no data) | 2 · 12/16 charts (75%) | 3/3 † | 18 / 16 | 8 | Strong Symbol |
| Uranus | Secondary | 1 · 3/18 combos | — (no data) | 2 · 9/16 charts (56%) | 3/3 † | 18 / 16 | 6 | Moderate (Relevant Symbol) |
| Lunar Node (North/South/unspecified) | Primary | 1 · 4/18 combos | — (no data) | 1 · 5/16 charts (31%) | 3/3 † | 18 / 16 | 6 | Moderate (Relevant Symbol) |
| Ascendant (1st House cusp) | Primary | 0 · 0/18 combos | — (no data) | 2 · 10/16 charts (62%) | 2/3 | 18 / 16 | 6 | Moderate (Relevant Symbol) |
| Part of Fortune | — (out of scope) | 1 · 1/18 combos | — (no data) | 1 · 2/16 charts (12%) | 2/2 † | 18 / 16 | 6 | Moderate (Relevant Symbol) |
| Pluto | Absent | 1 · 1/18 combos | — (no data) | 1 · 4/16 charts (25%) | 2/3 | 18 / 16 | 4 | Weak (Occasional Symbol) |
| Midheaven (10th House cusp) | Absent | 1 · 5/18 combos | — (no data) | 1 · 4/16 charts (25%) | 2/3 | 18 / 16 | 4 | Weak (Occasional Symbol) |
| Mars | Absent | 0 · 0/18 combos | — (no data) | 1 · 1/16 charts (6%) | 1/3 | 18 / 16 | 2 | Very Weak (Speculative Symbol) |
| Saturn | Absent | 0 · 0/18 combos | — (no data) | 1 · 1/16 charts (6%) | 1/3 | 18 / 16 | 2 | Very Weak (Speculative Symbol) |
| Neptune | Absent | 1 · 2/18 combos | — (no data) | 0 · 0/16 charts (0%) | 1/3 | 18 / 16 | 2 | Very Weak (Speculative Symbol) |
| Descendant (7th House cusp) | Absent | — (out of scope) | — (no data) | 1 · 3/16 charts (19%) | 1/2 | 18 / 16 | 2 | Very Weak (Speculative Symbol) |
| 2nd House cusp | Absent | — (out of scope) | — (no data) | 1 · 1/16 charts (6%) | 1/2 | 18 / 16 | 2 | Very Weak (Speculative Symbol) |
| 5th House cusp | Absent | — (out of scope) | — (no data) | 1 · 1/16 charts (6%) | 1/2 | 18 / 16 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | — (no data) | 1 · 4/16 charts (25%) | 1/2 | 18 / 16 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | — (no data) | 1 · 2/16 charts (12%) | 1/2 | 18 / 16 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Imum Coeli (4th House cusp)**: tier_score = 10 (n_juan_combos_total=18, n_marr_examples_total=16)  |  **Part of Fortune**: tier_score = 6 (n_juan_combos_total=18, n_marr_examples_total=16) — *looked up independently; no combined score is produced for this pairing.*
- **Imum Coeli (4th House cusp)**: tier_score = 10 (n_juan_combos_total=18, n_marr_examples_total=16)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=18, n_marr_examples_total=16) — *looked up independently; no combined score is produced for this pairing.*
- **3rd House cusp**: tier_score = 10 (n_juan_combos_total=18, n_marr_examples_total=16)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=18, n_marr_examples_total=16) — *looked up independently; no combined score is produced for this pairing.*
- **Part of Fortune**: tier_score = 6 (n_juan_combos_total=18, n_marr_examples_total=16)  |  **Pluto**: tier_score = 4 (n_juan_combos_total=18, n_marr_examples_total=16) — *looked up independently; no combined score is produced for this pairing.*

---

## 15. Job Promotion

*Category: Achievement — career advancement*

### 1. Event Overview

An advance in professional standing or income. The Midheaven paired with the Sun or Jupiter is the classic promotion signature, while the 2nd house cusp with Venus or Jupiter marks a rise in salary specifically.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Sun, Moon, Mercury, Venus, Jupiter, Uranus, Pluto
- Houses/Angles mentioned: Ascendant (1st House cusp), Midheaven (10th House cusp), 2nd House cusp, 3rd House cusp, 11th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Sun, Moon, Mercury, Venus, Jupiter, Uranus, Ascendant (1st House cusp), Midheaven (10th House cusp), 2nd House cusp, 3rd House cusp
- **Secondary**: Pluto, 11th House cusp, North Node (Ascending)
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Jupiter (12/54), Venus (11/54), Mercury (10/54), Uranus (10/54), Lunar Node (pole unspecified) (10/54), Ascendant (1st House cusp) (9/54), Sun (9/54), Moon (9/54), Part of Fortune (9/54), Midheaven (10th House cusp) (9/54)
- Total pairwise combinations catalogued for this event: 54
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: An advance in professional standing or income. The Midheaven paired with the Sun or Jupiter is the classic promotion signature, while the 2nd house cusp with Venus or Jupiter marks a rise in salary specifically.
- Points referenced: Sun (strong), Jupiter (strong), Midheaven (10th House cusp) (strong), Mercury (mentioned), Venus (mentioned), Pluto (mentioned), 2nd House cusp (mentioned), 8th House cusp (mentioned), Moon (weak)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **38 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Midheaven (10th House cusp) (29/38, 76%), Jupiter (29/38, 76%), Sun (24/38, 63%), Mercury (24/38, 63%), Uranus (24/38, 63%), Venus (24/38, 63%), 3rd House cusp (21/38, 55%), Moon (20/38, 53%)
- Node detail: North Node in 5, South Node in 0, unspecified-pole Node in 0 of 38 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Sun** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Moon** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Mercury** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Venus** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Jupiter** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Midheaven (10th House cusp)** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Pluto** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 6/10)
- **Uranus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **2nd House cusp** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **3rd House cusp** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 4/10)
- **11th House cusp** — supported by POLARIS, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Mars** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Saturn** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Neptune** — supported by Marr Aspects (score 2/10)
- **Descendant (7th House cusp)** — supported by Marr Aspects (score 2/10)
- **Imum Coeli (4th House cusp)** — supported by Marr Aspects (score 2/10)
- **6th House cusp** — supported by Marr Aspects (score 2/10)
- **8th House cusp** — supported by Other (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **12th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Sun, Moon, Mercury, Venus, Jupiter, Pluto, Midheaven (10th House cusp) are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Uranus, Ascendant (1st House cusp), 2nd House cusp, Lunar Node (North/South/unspecified) are supported by three of the four sources. 1 of these (2nd House cusp) sits at the structural ceiling for its symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Mars, Saturn, 3rd House cusp, 11th House cusp, Part of Fortune.

**Speculative / source-specific symbolism.** Neptune (Marr Aspects only), Descendant (7th House cusp) (Marr Aspects only), Imum Coeli (4th House cusp) (Marr Aspects only), 6th House cusp (Marr Aspects only), 8th House cusp (Other only), 9th House cusp (Marr Aspects only), 12th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** No clear-cut contradictions were found for this event: the four sources differ in *emphasis* and *coverage* (which is discussed above) rather than making opposing claims about any single symbol.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Sun | Primary | 1 · 9/54 combos | Strong emphasis | 2 · 24/38 charts (63%) | 4/4 | 54 / 38 | 8 | Strong Symbol |
| Moon | Primary | 1 · 9/54 combos | Mentioned | 2 · 20/38 charts (53%) | 4/4 | 54 / 38 | 8 | Strong Symbol |
| Mercury | Primary | 1 · 10/54 combos | Mentioned | 2 · 24/38 charts (63%) | 4/4 | 54 / 38 | 8 | Strong Symbol |
| Venus | Primary | 1 · 11/54 combos | Mentioned | 2 · 24/38 charts (63%) | 4/4 | 54 / 38 | 8 | Strong Symbol |
| Jupiter | Primary | 1 · 12/54 combos | Strong emphasis | 2 · 29/38 charts (76%) | 4/4 | 54 / 38 | 8 | Strong Symbol |
| Midheaven (10th House cusp) | Primary | 1 · 9/54 combos | Strong emphasis | 2 · 29/38 charts (76%) | 4/4 | 54 / 38 | 8 | Strong Symbol |
| Pluto | Secondary | 1 · 7/54 combos | Mentioned | 1 · 5/38 charts (13%) | 4/4 | 54 / 38 | 6 | Moderate (Relevant Symbol) |
| Uranus | Primary | 1 · 10/54 combos | Absent | 2 · 24/38 charts (63%) | 3/4 | 54 / 38 | 6 | Moderate (Relevant Symbol) |
| Ascendant (1st House cusp) | Primary | 1 · 9/54 combos | Absent | 2 · 20/38 charts (53%) | 3/4 | 54 / 38 | 6 | Moderate (Relevant Symbol) |
| 2nd House cusp | Primary | — (out of scope) | Mentioned | 1 · 6/38 charts (16%) | 3/3 † | 54 / 38 | 6 | Moderate (Relevant Symbol) |
| 3rd House cusp | Primary | — (out of scope) | Absent | 2 · 21/38 charts (55%) | 2/3 | 54 / 38 | 6 | Moderate (Relevant Symbol) |
| Lunar Node (North/South/unspecified) | Secondary | 1 · 10/54 combos | Absent | 1 · 5/38 charts (13%) | 3/4 | 54 / 38 | 4 | Weak (Occasional Symbol) |
| 11th House cusp | Secondary | — (out of scope) | Absent | 1 · 12/38 charts (32%) | 2/3 | 54 / 38 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 9/54 combos | Absent | 1 · 5/38 charts (13%) | 2/3 | 54 / 38 | 4 | Weak (Occasional Symbol) |
| Mars | Absent | 1 · 2/54 combos | Absent | 1 · 2/38 charts (5%) | 2/4 | 54 / 38 | 2 | Very Weak (Speculative Symbol) |
| Saturn | Absent | 1 · 1/54 combos | Absent | 1 · 2/38 charts (5%) | 2/4 | 54 / 38 | 2 | Very Weak (Speculative Symbol) |
| Neptune | Absent | 0 · 0/54 combos | Absent | 1 · 2/38 charts (5%) | 1/4 | 54 / 38 | 2 | Very Weak (Speculative Symbol) |
| Descendant (7th House cusp) | Absent | — (out of scope) | Absent | 1 · 3/38 charts (8%) | 1/3 | 54 / 38 | 2 | Very Weak (Speculative Symbol) |
| Imum Coeli (4th House cusp) | Absent | — (out of scope) | Absent | 1 · 2/38 charts (5%) | 1/3 | 54 / 38 | 2 | Very Weak (Speculative Symbol) |
| 6th House cusp | Absent | — (out of scope) | Absent | 1 · 2/38 charts (5%) | 1/3 | 54 / 38 | 2 | Very Weak (Speculative Symbol) |
| 8th House cusp | Absent | — (out of scope) | Mentioned | 0 · 0/38 charts (0%) | 1/3 | 54 / 38 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | Absent | 1 · 5/38 charts (13%) | 1/3 | 54 / 38 | 2 | Very Weak (Speculative Symbol) |
| 12th House cusp | Absent | — (out of scope) | Absent | 1 · 1/38 charts (3%) | 1/3 | 54 / 38 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Sun**: tier_score = 8 (n_juan_combos_total=54, n_marr_examples_total=38)  |  **Lunar Node (North/South/unspecified)**: tier_score = 4 (n_juan_combos_total=54, n_marr_examples_total=38) — *looked up independently; no combined score is produced for this pairing.*
- **Sun**: tier_score = 8 (n_juan_combos_total=54, n_marr_examples_total=38)  |  **12th House cusp**: tier_score = 2 (n_juan_combos_total=54, n_marr_examples_total=38) — *looked up independently; no combined score is produced for this pairing.*
- **Moon**: tier_score = 8 (n_juan_combos_total=54, n_marr_examples_total=38)  |  **12th House cusp**: tier_score = 2 (n_juan_combos_total=54, n_marr_examples_total=38) — *looked up independently; no combined score is produced for this pairing.*
- **Lunar Node (North/South/unspecified)**: tier_score = 4 (n_juan_combos_total=54, n_marr_examples_total=38)  |  **11th House cusp**: tier_score = 4 (n_juan_combos_total=54, n_marr_examples_total=38) — *looked up independently; no combined score is produced for this pairing.*

---

## 16. Demobilization or Release

*Category: Liberation — release from service or confinement*

### 1. Event Overview

Release from military service, or by extension from confinement generally. The 12th house cusp (endings, institutions) combined with Jupiter or Venus is the stated signature. Juan Combos records no data for this event.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Venus, Jupiter, Uranus, Moon, Mercury
- Houses/Angles mentioned: Ascendant (1st House cusp), Midheaven (10th House cusp), 12th House cusp, 3rd House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Venus, Jupiter, Uranus, Ascendant (1st House cusp), Midheaven (10th House cusp), 12th House cusp
- **Secondary**: Moon, Mercury, 3rd House cusp, North Node (Ascending)
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- *No data available from this source* (the compendium explicitly marks this entry “None”).

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: Release from military service, or by extension from confinement generally. The 12th house cusp (endings, institutions) combined with Jupiter or Venus is the stated signature. Juan Combos records no data for this event.
- Points referenced: Venus (mentioned), Jupiter (mentioned), Ascendant (1st House cusp) (mentioned), 12th House cusp (mentioned)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **13 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Venus (11/13, 85%), Midheaven (10th House cusp) (9/13, 69%), Jupiter (9/13, 69%), Sun (8/13, 62%), Mercury (8/13, 62%), Moon (7/13, 54%), Uranus (7/13, 54%), Mars (7/13, 54%)
- Node detail: North Node in 4, South Node in 0, unspecified-pole Node in 0 of 13 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Venus** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **Jupiter** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **12th House cusp** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **Moon** — supported by POLARIS, Marr Aspects (score 6/10)
- **Mercury** — supported by POLARIS, Marr Aspects (score 6/10)
- **Uranus** — supported by POLARIS, Marr Aspects (score 6/10)
- **Midheaven (10th House cusp)** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **3rd House cusp** — supported by POLARIS, Marr Aspects (score 4/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Marr Aspects (score 4/10)
- **Sun** — supported by Marr Aspects (score 4/10)
- **Mars** — supported by Marr Aspects (score 4/10)
- **Imum Coeli (4th House cusp)** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)
- **Pluto** — supported by Marr Aspects (score 2/10)
- **Descendant (7th House cusp)** — supported by Marr Aspects (score 2/10)
- **5th House cusp** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **Part of Fortune** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**Medium-confidence symbolism.** Venus, Jupiter, Ascendant (1st House cusp), 12th House cusp are supported by three of the four sources. All of these sit at the structural ceiling for their symbol type — marked † in the table below — because Juan Combos carries no data at all for this event, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Moon, Mercury, Uranus, Midheaven (10th House cusp), 3rd House cusp, Lunar Node (North/South/unspecified).

**Speculative / source-specific symbolism.** Sun (Marr Aspects only), Mars (Marr Aspects only), Pluto (Marr Aspects only), Descendant (7th House cusp) (Marr Aspects only), Imum Coeli (4th House cusp) (Marr Aspects only), 5th House cusp (Marr Aspects only), 9th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only), Part of Fortune (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** Sun (in 8/13 example charts, 62%), Mars (in 7/13 example charts, 54%) recur in a substantial share of Marr's worked examples without being singled out in POLARIS's Primary/Secondary list. This is not a direct contradiction — POLARIS's list is a short, deliberately curated selection rather than an exhaustive one, and no case was found anywhere in the compendium of a POLARIS-Primary symbol being *absent* from a substantial Marr Aspects sample. Read it as an emphasis gap, not a disagreement about relevance.

**Incomplete information.** Juan Combos (marked “None”) contribute no data to this event; the consolidated picture above rests on the remaining source(s) only.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Venus | Primary | — (out of scope) | Mentioned | 2 · 11/13 charts (85%) | 3/3 † | 0 / 13 | 8 | Strong Symbol |
| Jupiter | Primary | — (out of scope) | Mentioned | 2 · 9/13 charts (69%) | 3/3 † | 0 / 13 | 8 | Strong Symbol |
| Ascendant (1st House cusp) | Primary | — (out of scope) | Mentioned | 2 · 7/13 charts (54%) | 3/3 † | 0 / 13 | 8 | Strong Symbol |
| 12th House cusp | Primary | — (out of scope) | Mentioned | 1 · 4/13 charts (31%) | 3/3 † | 0 / 13 | 6 | Moderate (Relevant Symbol) |
| Moon | Secondary | — (out of scope) | Absent | 2 · 7/13 charts (54%) | 2/3 | 0 / 13 | 6 | Moderate (Relevant Symbol) |
| Mercury | Secondary | — (out of scope) | Absent | 2 · 8/13 charts (62%) | 2/3 | 0 / 13 | 6 | Moderate (Relevant Symbol) |
| Uranus | Primary | — (out of scope) | Absent | 2 · 7/13 charts (54%) | 2/3 | 0 / 13 | 6 | Moderate (Relevant Symbol) |
| Midheaven (10th House cusp) | Primary | — (out of scope) | Absent | 2 · 9/13 charts (69%) | 2/3 | 0 / 13 | 6 | Moderate (Relevant Symbol) |
| 3rd House cusp | Secondary | — (out of scope) | Absent | 1 · 4/13 charts (31%) | 2/3 | 0 / 13 | 4 | Weak (Occasional Symbol) |
| Lunar Node (North/South/unspecified) | Secondary | — (out of scope) | Absent | 1 · 4/13 charts (31%) | 2/3 | 0 / 13 | 4 | Weak (Occasional Symbol) |
| Sun | Absent | — (out of scope) | Absent | 2 · 8/13 charts (62%) | 1/3 | 0 / 13 | 4 | Weak (Occasional Symbol) |
| Mars | Absent | — (out of scope) | Absent | 2 · 7/13 charts (54%) | 1/3 | 0 / 13 | 4 | Weak (Occasional Symbol) |
| Imum Coeli (4th House cusp) | Absent | — (out of scope) | Absent | 1 · 5/13 charts (38%) | 1/3 | 0 / 13 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 5/13 charts (38%) | 1/3 | 0 / 13 | 2 | Very Weak (Speculative Symbol) |
| Pluto | Absent | — (out of scope) | Absent | 1 · 2/13 charts (15%) | 1/3 | 0 / 13 | 2 | Very Weak (Speculative Symbol) |
| Descendant (7th House cusp) | Absent | — (out of scope) | Absent | 1 · 3/13 charts (23%) | 1/3 | 0 / 13 | 2 | Very Weak (Speculative Symbol) |
| 5th House cusp | Absent | — (out of scope) | Absent | 1 · 1/13 charts (8%) | 1/3 | 0 / 13 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | Absent | 1 · 3/13 charts (23%) | 1/3 | 0 / 13 | 2 | Very Weak (Speculative Symbol) |
| Part of Fortune | — (out of scope) | — (out of scope) | Absent | 1 · 3/13 charts (23%) | 1/2 | 0 / 13 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Venus**: tier_score = 8 (n_juan_combos_total=0, n_marr_examples_total=13)  |  **Lunar Node (North/South/unspecified)**: tier_score = 4 (n_juan_combos_total=0, n_marr_examples_total=13) — *looked up independently; no combined score is produced for this pairing.*
- **Venus**: tier_score = 8 (n_juan_combos_total=0, n_marr_examples_total=13)  |  **Part of Fortune**: tier_score = 2 (n_juan_combos_total=0, n_marr_examples_total=13) — *looked up independently; no combined score is produced for this pairing.*
- **Jupiter**: tier_score = 8 (n_juan_combos_total=0, n_marr_examples_total=13)  |  **Part of Fortune**: tier_score = 2 (n_juan_combos_total=0, n_marr_examples_total=13) — *looked up independently; no combined score is produced for this pairing.*
- **Lunar Node (North/South/unspecified)**: tier_score = 4 (n_juan_combos_total=0, n_marr_examples_total=13)  |  **Sun**: tier_score = 4 (n_juan_combos_total=0, n_marr_examples_total=13) — *looked up independently; no combined score is produced for this pairing.*

---

## 17. Gambling Gain

*Category: Fortune — winning at chance*

### 1. Event Overview

A win at games of chance. Jupiter (luck), Venus (pleasure/gain) and Uranus (a sudden reversal of fortune) form the signature, typically expressed through the 5th house cusp or the Ascendant. Only one worked example survives in Marr Aspects, so the empirical base for this entry is thin.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Venus, Jupiter, Uranus, Pluto
- Houses/Angles mentioned: Ascendant (1st House cusp), Midheaven (10th House cusp), 2nd House cusp, 5th House cusp
- Nodes/Points mentioned: none
- **Primary** (highest POLARIS confidence): Venus, Jupiter, Uranus, Ascendant (1st House cusp), Midheaven (10th House cusp), 2nd House cusp, 5th House cusp
- **Secondary**: Pluto
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Jupiter (3/3), Sun (1/3), Venus (1/3), Uranus (1/3)
- Total pairwise combinations catalogued for this event: 3
- **Low sample size:** only 3 combinations catalogued for this event in total — any single symbol's Juan Combos percentage here rests on very little underlying data, and the tier_score for symbols resting mainly on this source should be read with that in mind (see `n_juan_combos_total` on each symbol record).
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: A win at games of chance. Jupiter (luck), Venus (pleasure/gain) and Uranus (a sudden reversal of fortune) form the signature, typically expressed through the 5th house cusp or the Ascendant. Only one worked example survives in Marr Aspects, so the empirical base for this entry is thin.
- Points referenced: Venus (mentioned), Jupiter (mentioned), Uranus (mentioned), Ascendant (1st House cusp) (mentioned), 5th House cusp (mentioned)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **1 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- **Low sample size:** only 1 worked example available for this event in total — frequencies quoted below (and the corresponding tier_score contributions) are drawn from a very small pool and should be read as suggestive rather than well-established (see `n_marr_examples_total` on each symbol record).
- Most frequent points: Venus (1/1, 100%), Sun (1/1, 100%), 5th House cusp (1/1, 100%), Moon (1/1, 100%), Mercury (1/1, 100%), Uranus (1/1, 100%), Imum Coeli (4th House cusp) (1/1, 100%), Mars (1/1, 100%)

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Jupiter** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Venus** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 6/10)
- **Uranus** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 6/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **5th House cusp** — supported by POLARIS, Other, Marr Aspects (score 6/10)

**Occasional Symbols**
- **2nd House cusp** — supported by POLARIS (score 4/10)
- **Sun** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Moon** — supported by Marr Aspects (score 2/10)
- **Mercury** — supported by Marr Aspects (score 2/10)
- **Mars** — supported by Marr Aspects (score 2/10)
- **Midheaven (10th House cusp)** — supported by POLARIS (score 2/10)
- **Imum Coeli (4th House cusp)** — supported by Marr Aspects (score 2/10)
- **Pluto** — supported by POLARIS (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Venus, Jupiter, Uranus are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Ascendant (1st House cusp), 5th House cusp are supported by three of the four sources. 1 of these (5th House cusp) sits at the structural ceiling for its symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Sun.

**Speculative / source-specific symbolism.** Moon (Marr Aspects only), Mercury (Marr Aspects only), Mars (Marr Aspects only), Pluto (POLARIS only), Midheaven (10th House cusp) (POLARIS only), Imum Coeli (4th House cusp) (Marr Aspects only), 2nd House cusp (POLARIS only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** No clear-cut contradictions were found for this event: the four sources differ in *emphasis* and *coverage* (which is discussed above) rather than making opposing claims about any single symbol.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Jupiter | Primary | 2 · 3/3 combos | Mentioned | 1 · 1/1 charts (100%) | 4/4 | 3 / 1 | 8 | Strong Symbol |
| Venus | Primary | 1 · 1/3 combos | Mentioned | 1 · 1/1 charts (100%) | 4/4 | 3 / 1 | 6 | Moderate (Relevant Symbol) |
| Uranus | Primary | 1 · 1/3 combos | Mentioned | 1 · 1/1 charts (100%) | 4/4 | 3 / 1 | 6 | Moderate (Relevant Symbol) |
| Ascendant (1st House cusp) | Primary | 0 · 0/3 combos | Mentioned | 1 · 1/1 charts (100%) | 3/4 | 3 / 1 | 6 | Moderate (Relevant Symbol) |
| 5th House cusp | Primary | — (out of scope) | Mentioned | 1 · 1/1 charts (100%) | 3/3 † | 3 / 1 | 6 | Moderate (Relevant Symbol) |
| 2nd House cusp | Primary | — (out of scope) | Absent | 0 · 0/1 charts (0%) | 1/3 | 3 / 1 | 4 | Weak (Occasional Symbol) |
| Sun | Absent | 1 · 1/3 combos | Absent | 1 · 1/1 charts (100%) | 2/4 | 3 / 1 | 2 | Very Weak (Speculative Symbol) |
| Moon | Absent | 0 · 0/3 combos | Absent | 1 · 1/1 charts (100%) | 1/4 | 3 / 1 | 2 | Very Weak (Speculative Symbol) |
| Mercury | Absent | 0 · 0/3 combos | Absent | 1 · 1/1 charts (100%) | 1/4 | 3 / 1 | 2 | Very Weak (Speculative Symbol) |
| Mars | Absent | 0 · 0/3 combos | Absent | 1 · 1/1 charts (100%) | 1/4 | 3 / 1 | 2 | Very Weak (Speculative Symbol) |
| Midheaven (10th House cusp) | Primary | 0 · 0/3 combos | Absent | 0 · 0/1 charts (0%) | 1/4 | 3 / 1 | 2 | Very Weak (Speculative Symbol) |
| Imum Coeli (4th House cusp) | Absent | — (out of scope) | Absent | 1 · 1/1 charts (100%) | 1/3 | 3 / 1 | 2 | Very Weak (Speculative Symbol) |
| Pluto | Secondary | 0 · 0/3 combos | Absent | 0 · 0/1 charts (0%) | 1/4 | 3 / 1 | 2 | Very Weak (Speculative Symbol) |
| Lunar Node (North/South/unspecified) | Absent | 0 · 0/3 combos | Absent | 0 · 0/1 charts (0%) | 0/4 | 3 / 1 | 0 | No Support |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Jupiter**: tier_score = 8 (n_juan_combos_total=3, n_marr_examples_total=1)  |  **Moon**: tier_score = 2 (n_juan_combos_total=3, n_marr_examples_total=1) — *looked up independently; no combined score is produced for this pairing.*
- **Jupiter**: tier_score = 8 (n_juan_combos_total=3, n_marr_examples_total=1)  |  **Lunar Node (North/South/unspecified)**: tier_score = 0 (n_juan_combos_total=3, n_marr_examples_total=1) — *looked up independently; no combined score is produced for this pairing.*
- **Venus**: tier_score = 6 (n_juan_combos_total=3, n_marr_examples_total=1)  |  **Lunar Node (North/South/unspecified)**: tier_score = 0 (n_juan_combos_total=3, n_marr_examples_total=1) — *looked up independently; no combined score is produced for this pairing.*
- **Moon**: tier_score = 2 (n_juan_combos_total=3, n_marr_examples_total=1)  |  **Mercury**: tier_score = 2 (n_juan_combos_total=3, n_marr_examples_total=1) — *looked up independently; no combined score is produced for this pairing.*

---

## 18. Army Promotion

*Category: Achievement — military advancement*

### 1. Event Overview

The military-specific counterpart to Job Promotion. Alexander Marr's short-form prose is silent here, so the entry rests on POLARIS's list, a small Juan Combos set, and the worked examples.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Sun, Moon, Mercury, Mars, Jupiter, Uranus, Pluto, Venus
- Houses/Angles mentioned: Ascendant (1st House cusp), Midheaven (10th House cusp), 3rd House cusp, 2nd House cusp, 11th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Sun, Moon, Mercury, Mars, Jupiter, Uranus, Pluto, Ascendant (1st House cusp), Midheaven (10th House cusp), 3rd House cusp
- **Secondary**: Venus, 2nd House cusp, 11th House cusp, North Node (Ascending)
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Mars (6/6), Ascendant (1st House cusp) (1/6), Midheaven (10th House cusp) (1/6), Sun (1/6), Moon (1/6), Mercury (1/6), Part of Fortune (1/6)
- Total pairwise combinations catalogued for this event: 6
- **Low sample size:** only 6 combinations catalogued for this event in total — any single symbol's Juan Combos percentage here rests on very little underlying data, and the tier_score for symbols resting mainly on this source should be read with that in mind (see `n_juan_combos_total` on each symbol record).
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- *No data available from this source* (the compendium explicitly marks this entry “None”).

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **17 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Jupiter (13/17, 76%), Moon (13/17, 76%), Midheaven (10th House cusp) (12/17, 71%), 3rd House cusp (10/17, 59%), Uranus (10/17, 59%), Mercury (10/17, 59%), Venus (10/17, 59%), Sun (8/17, 47%)
- Node detail: North Node in 0, South Node in 0, unspecified-pole Node in 1 of 17 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- **3rd House cusp** — supported by POLARIS, Marr Aspects (score 10/10)

**Secondary Symbols**
- **Sun** — supported by POLARIS, Juan Combos, Marr Aspects (score 8/10)
- **Moon** — supported by POLARIS, Juan Combos, Marr Aspects (score 8/10)
- **Mercury** — supported by POLARIS, Juan Combos, Marr Aspects (score 8/10)
- **Mars** — supported by POLARIS, Juan Combos, Marr Aspects (score 8/10)
- **Midheaven (10th House cusp)** — supported by POLARIS, Juan Combos, Marr Aspects (score 8/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Venus** — supported by POLARIS, Marr Aspects (score 6/10)
- **Jupiter** — supported by POLARIS, Marr Aspects (score 6/10)
- **Uranus** — supported by POLARIS, Marr Aspects (score 6/10)
- **Pluto** — supported by POLARIS, Marr Aspects (score 6/10)
- **2nd House cusp** — supported by POLARIS, Marr Aspects (score 6/10)
- **11th House cusp** — supported by POLARIS, Marr Aspects (score 6/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Marr Aspects (score 4/10)
- **Saturn** — supported by Marr Aspects (score 2/10)
- **Neptune** — supported by Marr Aspects (score 2/10)
- **Descendant (7th House cusp)** — supported by Marr Aspects (score 2/10)
- **Imum Coeli (4th House cusp)** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**Medium-confidence symbolism.** Sun, Moon, Mercury, Mars, Ascendant (1st House cusp), Midheaven (10th House cusp) are supported by three of the four sources. All of these sit at the structural ceiling for their symbol type — marked † in the table below — because Other carries no data at all for this event, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Venus, Jupiter, Uranus, Pluto, 2nd House cusp, 3rd House cusp, 11th House cusp, Lunar Node (North/South/unspecified), Part of Fortune. All of these are marked † in the table below: for each, only two sources could address the point at all (the other two are structurally out of scope for this event), and those two agree — a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

**Speculative / source-specific symbolism.** Saturn (Marr Aspects only), Neptune (Marr Aspects only), Descendant (7th House cusp) (Marr Aspects only), Imum Coeli (4th House cusp) (Marr Aspects only), 9th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** No clear-cut contradictions were found for this event: the four sources differ in *emphasis* and *coverage* (which is discussed above) rather than making opposing claims about any single symbol.

**Incomplete information.** Other (marked “None”) contribute no data to this event; the consolidated picture above rests on the remaining source(s) only.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| 3rd House cusp | Primary | — (out of scope) | — (no data) | 2 · 10/17 charts (59%) | 2/2 † | 6 / 17 | 10 | Very Strong (Core Symbol) |
| Sun | Primary | 1 · 1/6 combos | — (no data) | 2 · 8/17 charts (47%) | 3/3 † | 6 / 17 | 8 | Strong Symbol |
| Moon | Primary | 1 · 1/6 combos | — (no data) | 2 · 13/17 charts (76%) | 3/3 † | 6 / 17 | 8 | Strong Symbol |
| Mercury | Primary | 1 · 1/6 combos | — (no data) | 2 · 10/17 charts (59%) | 3/3 † | 6 / 17 | 8 | Strong Symbol |
| Mars | Primary | 2 · 6/6 combos | — (no data) | 1 · 7/17 charts (41%) | 3/3 † | 6 / 17 | 8 | Strong Symbol |
| Midheaven (10th House cusp) | Primary | 1 · 1/6 combos | — (no data) | 2 · 12/17 charts (71%) | 3/3 † | 6 / 17 | 8 | Strong Symbol |
| Ascendant (1st House cusp) | Primary | 1 · 1/6 combos | — (no data) | 1 · 5/17 charts (29%) | 3/3 † | 6 / 17 | 6 | Moderate (Relevant Symbol) |
| Venus | Secondary | 0 · 0/6 combos | — (no data) | 2 · 10/17 charts (59%) | 2/3 | 6 / 17 | 6 | Moderate (Relevant Symbol) |
| Jupiter | Primary | 0 · 0/6 combos | — (no data) | 2 · 13/17 charts (76%) | 2/3 | 6 / 17 | 6 | Moderate (Relevant Symbol) |
| Uranus | Primary | 0 · 0/6 combos | — (no data) | 2 · 10/17 charts (59%) | 2/3 | 6 / 17 | 6 | Moderate (Relevant Symbol) |
| Pluto | Primary | 0 · 0/6 combos | — (no data) | 1 · 4/17 charts (24%) | 2/3 | 6 / 17 | 6 | Moderate (Relevant Symbol) |
| 2nd House cusp | Secondary | — (out of scope) | — (no data) | 1 · 1/17 charts (6%) | 2/2 † | 6 / 17 | 6 | Moderate (Relevant Symbol) |
| 11th House cusp | Secondary | — (out of scope) | — (no data) | 1 · 5/17 charts (29%) | 2/2 † | 6 / 17 | 6 | Moderate (Relevant Symbol) |
| Part of Fortune | — (out of scope) | 1 · 1/6 combos | — (no data) | 1 · 2/17 charts (12%) | 2/2 † | 6 / 17 | 6 | Moderate (Relevant Symbol) |
| Lunar Node (North/South/unspecified) | Secondary | 0 · 0/6 combos | — (no data) | 1 · 1/17 charts (6%) | 2/3 | 6 / 17 | 4 | Weak (Occasional Symbol) |
| Saturn | Absent | 0 · 0/6 combos | — (no data) | 1 · 3/17 charts (18%) | 1/3 | 6 / 17 | 2 | Very Weak (Speculative Symbol) |
| Neptune | Absent | 0 · 0/6 combos | — (no data) | 1 · 1/17 charts (6%) | 1/3 | 6 / 17 | 2 | Very Weak (Speculative Symbol) |
| Descendant (7th House cusp) | Absent | — (out of scope) | — (no data) | 1 · 2/17 charts (12%) | 1/2 | 6 / 17 | 2 | Very Weak (Speculative Symbol) |
| Imum Coeli (4th House cusp) | Absent | — (out of scope) | — (no data) | 1 · 2/17 charts (12%) | 1/2 | 6 / 17 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | — (no data) | 1 · 4/17 charts (24%) | 1/2 | 6 / 17 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **3rd House cusp**: tier_score = 10 (n_juan_combos_total=6, n_marr_examples_total=17)  |  **Pluto**: tier_score = 6 (n_juan_combos_total=6, n_marr_examples_total=17) — *looked up independently; no combined score is produced for this pairing.*
- **3rd House cusp**: tier_score = 10 (n_juan_combos_total=6, n_marr_examples_total=17)  |  **9th House cusp**: tier_score = 2 (n_juan_combos_total=6, n_marr_examples_total=17) — *looked up independently; no combined score is produced for this pairing.*
- **Sun**: tier_score = 8 (n_juan_combos_total=6, n_marr_examples_total=17)  |  **9th House cusp**: tier_score = 2 (n_juan_combos_total=6, n_marr_examples_total=17) — *looked up independently; no combined score is produced for this pairing.*
- **Pluto**: tier_score = 6 (n_juan_combos_total=6, n_marr_examples_total=17)  |  **2nd House cusp**: tier_score = 6 (n_juan_combos_total=6, n_marr_examples_total=17) — *looked up independently; no combined score is produced for this pairing.*

---

## 19. Death of Father or Grandfather

*Category: Death — Family (male elder)*

### 1. Event Overview

The father's death signature centers on the Sun and Saturn — the classical paternal significators — expressed through the Midheaven. An afflicted Ascendant combined with Saturn recurs for the mourning response itself, a pattern shared with the mother's death entry.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Sun, Mars, Saturn, Neptune, Pluto, Moon, Uranus
- Houses/Angles mentioned: Ascendant (1st House cusp), Midheaven (10th House cusp), 8th House cusp, 12th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Sun, Mars, Saturn, Neptune, Pluto, Ascendant (1st House cusp), Midheaven (10th House cusp), 8th House cusp, North Node (Ascending)
- **Secondary**: Moon, Uranus, 12th House cusp
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Saturn (12/57), Neptune (12/57), Lunar Node (pole unspecified) (12/57), Mars (11/57), Pluto (11/57), Uranus (10/57), Ascendant (1st House cusp) (8/57), Moon (8/57), Sun (7/57), Midheaven (10th House cusp) (7/57)
- Total pairwise combinations catalogued for this event: 57
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: The father's death signature centers on the Sun and Saturn — the classical paternal significators — expressed through the Midheaven. An afflicted Ascendant combined with Saturn recurs for the mourning response itself, a pattern shared with the mother's death entry.
- Points referenced: Saturn (strong), Ascendant (1st House cusp) (strong), Sun (mentioned), Midheaven (10th House cusp) (mentioned)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **43 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Sun (36/43, 84%), 8th House cusp (34/43, 79%), Saturn (33/43, 77%), Midheaven (10th House cusp) (32/43, 74%), Mars (29/43, 67%), Uranus (24/43, 56%), Ascendant (1st House cusp) (24/43, 56%), Pluto (24/43, 56%)
- Node detail: North Node in 3, South Node in 13, unspecified-pole Node in 9 of 43 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Sun** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Saturn** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Midheaven (10th House cusp)** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Moon** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Mars** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Uranus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Neptune** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Pluto** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **8th House cusp** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **12th House cusp** — supported by POLARIS, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Mercury** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Venus** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Jupiter** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Descendant (7th House cusp)** — supported by Marr Aspects (score 2/10)
- **Imum Coeli (4th House cusp)** — supported by Marr Aspects (score 2/10)
- **2nd House cusp** — supported by Marr Aspects (score 2/10)
- **3rd House cusp** — supported by Marr Aspects (score 2/10)
- **5th House cusp** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Sun, Saturn, Ascendant (1st House cusp), Midheaven (10th House cusp) are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Moon, Mars, Uranus, Neptune, Pluto, Lunar Node (North/South/unspecified) are supported by three of the four sources.

Supported by exactly two sources (moderate confidence): Mercury, Venus, Jupiter, 8th House cusp, 12th House cusp, Part of Fortune.

**Speculative / source-specific symbolism.** Descendant (7th House cusp) (Marr Aspects only), Imum Coeli (4th House cusp) (Marr Aspects only), 2nd House cusp (Marr Aspects only), 3rd House cusp (Marr Aspects only), 5th House cusp (Marr Aspects only), 9th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** Jupiter (in 17/43 example charts, 40%), Mercury (in 16/43 example charts, 37%) recur in a substantial share of Marr's worked examples without being singled out in POLARIS's Primary/Secondary list. This is not a direct contradiction — POLARIS's list is a short, deliberately curated selection rather than an exhaustive one, and no case was found anywhere in the compendium of a POLARIS-Primary symbol being *absent* from a substantial Marr Aspects sample. Read it as an emphasis gap, not a disagreement about relevance.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Sun | Primary | 1 · 7/57 combos | Mentioned | 2 · 36/43 charts (84%) | 4/4 | 57 / 43 | 8 | Strong Symbol |
| Saturn | Primary | 1 · 12/57 combos | Strong emphasis | 2 · 33/43 charts (77%) | 4/4 | 57 / 43 | 8 | Strong Symbol |
| Ascendant (1st House cusp) | Primary | 1 · 8/57 combos | Strong emphasis | 2 · 24/43 charts (56%) | 4/4 | 57 / 43 | 8 | Strong Symbol |
| Midheaven (10th House cusp) | Primary | 1 · 7/57 combos | Mentioned | 2 · 32/43 charts (74%) | 4/4 | 57 / 43 | 8 | Strong Symbol |
| Moon | Secondary | 1 · 8/57 combos | Absent | 2 · 20/43 charts (47%) | 3/4 | 57 / 43 | 6 | Moderate (Relevant Symbol) |
| Mars | Primary | 1 · 11/57 combos | Absent | 2 · 29/43 charts (67%) | 3/4 | 57 / 43 | 6 | Moderate (Relevant Symbol) |
| Uranus | Secondary | 1 · 10/57 combos | Absent | 2 · 24/43 charts (56%) | 3/4 | 57 / 43 | 6 | Moderate (Relevant Symbol) |
| Neptune | Primary | 1 · 12/57 combos | Absent | 2 · 20/43 charts (47%) | 3/4 | 57 / 43 | 6 | Moderate (Relevant Symbol) |
| Pluto | Primary | 1 · 11/57 combos | Absent | 2 · 24/43 charts (56%) | 3/4 | 57 / 43 | 6 | Moderate (Relevant Symbol) |
| Lunar Node (North/South/unspecified) | Primary | 1 · 12/57 combos | Absent | 2 · 25/43 charts (58%) | 3/4 | 57 / 43 | 6 | Moderate (Relevant Symbol) |
| 8th House cusp | Primary | — (out of scope) | Absent | 2 · 34/43 charts (79%) | 2/3 | 57 / 43 | 6 | Moderate (Relevant Symbol) |
| 12th House cusp | Secondary | — (out of scope) | Absent | 1 · 7/43 charts (16%) | 2/3 | 57 / 43 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 5/57 combos | Absent | 1 · 17/43 charts (40%) | 2/3 | 57 / 43 | 4 | Weak (Occasional Symbol) |
| Mercury | Absent | 1 · 3/57 combos | Absent | 1 · 16/43 charts (37%) | 2/4 | 57 / 43 | 2 | Very Weak (Speculative Symbol) |
| Venus | Absent | 1 · 4/57 combos | Absent | 1 · 8/43 charts (19%) | 2/4 | 57 / 43 | 2 | Very Weak (Speculative Symbol) |
| Jupiter | Absent | 1 · 4/57 combos | Absent | 1 · 17/43 charts (40%) | 2/4 | 57 / 43 | 2 | Very Weak (Speculative Symbol) |
| Descendant (7th House cusp) | Absent | — (out of scope) | Absent | 1 · 5/43 charts (12%) | 1/3 | 57 / 43 | 2 | Very Weak (Speculative Symbol) |
| Imum Coeli (4th House cusp) | Absent | — (out of scope) | Absent | 1 · 6/43 charts (14%) | 1/3 | 57 / 43 | 2 | Very Weak (Speculative Symbol) |
| 2nd House cusp | Absent | — (out of scope) | Absent | 1 · 1/43 charts (2%) | 1/3 | 57 / 43 | 2 | Very Weak (Speculative Symbol) |
| 3rd House cusp | Absent | — (out of scope) | Absent | 1 · 4/43 charts (9%) | 1/3 | 57 / 43 | 2 | Very Weak (Speculative Symbol) |
| 5th House cusp | Absent | — (out of scope) | Absent | 1 · 1/43 charts (2%) | 1/3 | 57 / 43 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | Absent | 1 · 2/43 charts (5%) | 1/3 | 57 / 43 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 1/43 charts (2%) | 1/3 | 57 / 43 | 2 | Very Weak (Speculative Symbol) |

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Sun**: tier_score = 8 (n_juan_combos_total=57, n_marr_examples_total=43)  |  **12th House cusp**: tier_score = 4 (n_juan_combos_total=57, n_marr_examples_total=43) — *looked up independently; no combined score is produced for this pairing.*
- **Sun**: tier_score = 8 (n_juan_combos_total=57, n_marr_examples_total=43)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=57, n_marr_examples_total=43) — *looked up independently; no combined score is produced for this pairing.*
- **Saturn**: tier_score = 8 (n_juan_combos_total=57, n_marr_examples_total=43)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=57, n_marr_examples_total=43) — *looked up independently; no combined score is produced for this pairing.*
- **12th House cusp**: tier_score = 4 (n_juan_combos_total=57, n_marr_examples_total=43)  |  **Part of Fortune**: tier_score = 4 (n_juan_combos_total=57, n_marr_examples_total=43) — *looked up independently; no combined score is produced for this pairing.*

---

## 20. Death of Mother or Grandmother

*Category: Death — Family (female elder)*

### 1. Event Overview

The mother's death signature mirrors the father's: the Moon and Venus (rather than the Sun) combine with the IC (rather than the Midheaven) as the core symbolism, while the same Ascendant-Saturn mourning pattern again appears as a cross-parent signature.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Moon, Venus, Mars, Saturn, Neptune, Pluto, Sun, Uranus
- Houses/Angles mentioned: Ascendant (1st House cusp), Imum Coeli (4th House cusp), 8th House cusp, 12th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Moon, Venus, Mars, Saturn, Neptune, Pluto, Ascendant (1st House cusp), Imum Coeli (4th House cusp), 8th House cusp, North Node (Ascending)
- **Secondary**: Sun, Uranus, 12th House cusp
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Neptune (12/57), Pluto (12/57), Lunar Node (pole unspecified) (12/57), Mars (11/57), Saturn (11/57), Uranus (10/57), Ascendant (1st House cusp) (8/57), Moon (8/57), Midheaven (10th House cusp) (7/57), Venus (6/57)
- Total pairwise combinations catalogued for this event: 57
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: The mother's death signature mirrors the father's: the Moon and Venus (rather than the Sun) combine with the IC (rather than the Midheaven) as the core symbolism, while the same Ascendant-Saturn mourning pattern again appears as a cross-parent signature.
- Points referenced: Saturn (strong), Ascendant (1st House cusp) (strong), Moon (mentioned), Venus (mentioned), Imum Coeli (4th House cusp) (mentioned)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **38 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Venus (27/38, 71%), Imum Coeli (4th House cusp) (27/38, 71%), Moon (25/38, 66%), 8th House cusp (24/38, 63%), Mars (24/38, 63%), Uranus (22/38, 58%), Saturn (22/38, 58%), Neptune (17/38, 45%)
- Node detail: North Node in 2, South Node in 9, unspecified-pole Node in 8 of 38 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Moon** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Venus** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Saturn** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Imum Coeli (4th House cusp)** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **Mars** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Uranus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Neptune** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Pluto** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **8th House cusp** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Sun** — supported by POLARIS, Juan Combos, Marr Aspects (score 4/10)
- **12th House cusp** — supported by POLARIS, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Mercury** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Jupiter** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Midheaven (10th House cusp)** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Descendant (7th House cusp)** — supported by Marr Aspects (score 2/10)
- **3rd House cusp** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Moon, Venus, Saturn, Ascendant (1st House cusp) are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Sun, Mars, Uranus, Neptune, Pluto, Imum Coeli (4th House cusp), Lunar Node (North/South/unspecified) are supported by three of the four sources. 1 of these (Imum Coeli (4th House cusp)) sits at the structural ceiling for its symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Mercury, Jupiter, Midheaven (10th House cusp), 8th House cusp, 12th House cusp, Part of Fortune.

**Speculative / source-specific symbolism.** Descendant (7th House cusp) (Marr Aspects only), 3rd House cusp (Marr Aspects only), 9th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** No clear-cut contradictions were found for this event: the four sources differ in *emphasis* and *coverage* (which is discussed above) rather than making opposing claims about any single symbol.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Moon | Primary | 1 · 8/57 combos | Mentioned | 2 · 25/38 charts (66%) | 4/4 | 57 / 38 | 8 | Strong Symbol |
| Venus | Primary | 1 · 6/57 combos | Mentioned | 2 · 27/38 charts (71%) | 4/4 | 57 / 38 | 8 | Strong Symbol |
| Saturn | Primary | 1 · 11/57 combos | Strong emphasis | 2 · 22/38 charts (58%) | 4/4 | 57 / 38 | 8 | Strong Symbol |
| Ascendant (1st House cusp) | Primary | 1 · 8/57 combos | Strong emphasis | 1 · 14/38 charts (37%) | 4/4 | 57 / 38 | 8 | Strong Symbol |
| Imum Coeli (4th House cusp) | Primary | — (out of scope) | Mentioned | 2 · 27/38 charts (71%) | 3/3 † | 57 / 38 | 8 | Strong Symbol |
| Mars | Primary | 1 · 11/57 combos | Absent | 2 · 24/38 charts (63%) | 3/4 | 57 / 38 | 6 | Moderate (Relevant Symbol) |
| Uranus | Secondary | 1 · 10/57 combos | Absent | 2 · 22/38 charts (58%) | 3/4 | 57 / 38 | 6 | Moderate (Relevant Symbol) |
| Neptune | Primary | 1 · 12/57 combos | Absent | 2 · 17/38 charts (45%) | 3/4 | 57 / 38 | 6 | Moderate (Relevant Symbol) |
| Pluto | Primary | 1 · 12/57 combos | Absent | 1 · 12/38 charts (32%) | 3/4 | 57 / 38 | 6 | Moderate (Relevant Symbol) |
| Lunar Node (North/South/unspecified) | Primary | 1 · 12/57 combos | Absent | 2 · 19/38 charts (50%) | 3/4 | 57 / 38 | 6 | Moderate (Relevant Symbol) |
| 8th House cusp | Primary | — (out of scope) | Absent | 2 · 24/38 charts (63%) | 2/3 | 57 / 38 | 6 | Moderate (Relevant Symbol) |
| Sun | Secondary | 1 · 5/57 combos | Absent | 1 · 11/38 charts (29%) | 3/4 | 57 / 38 | 4 | Weak (Occasional Symbol) |
| 12th House cusp | Secondary | — (out of scope) | Absent | 1 · 2/38 charts (5%) | 2/3 | 57 / 38 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 5/57 combos | Absent | 1 · 7/38 charts (18%) | 2/3 | 57 / 38 | 4 | Weak (Occasional Symbol) |
| Mercury | Absent | 1 · 3/57 combos | Absent | 1 · 12/38 charts (32%) | 2/4 | 57 / 38 | 2 | Very Weak (Speculative Symbol) |
| Jupiter | Absent | 1 · 4/57 combos | Absent | 1 · 9/38 charts (24%) | 2/4 | 57 / 38 | 2 | Very Weak (Speculative Symbol) |
| Midheaven (10th House cusp) | Absent | 1 · 7/57 combos | Absent | 1 · 5/38 charts (13%) | 2/4 | 57 / 38 | 2 | Very Weak (Speculative Symbol) |
| Descendant (7th House cusp) | Absent | — (out of scope) | Absent | 1 · 10/38 charts (26%) | 1/3 | 57 / 38 | 2 | Very Weak (Speculative Symbol) |
| 3rd House cusp | Absent | — (out of scope) | Absent | 1 · 2/38 charts (5%) | 1/3 | 57 / 38 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | Absent | 1 · 2/38 charts (5%) | 1/3 | 57 / 38 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 1/38 charts (3%) | 1/3 | 57 / 38 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Moon**: tier_score = 8 (n_juan_combos_total=57, n_marr_examples_total=38)  |  **8th House cusp**: tier_score = 6 (n_juan_combos_total=57, n_marr_examples_total=38) — *looked up independently; no combined score is produced for this pairing.*
- **Moon**: tier_score = 8 (n_juan_combos_total=57, n_marr_examples_total=38)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=57, n_marr_examples_total=38) — *looked up independently; no combined score is produced for this pairing.*
- **Venus**: tier_score = 8 (n_juan_combos_total=57, n_marr_examples_total=38)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=57, n_marr_examples_total=38) — *looked up independently; no combined score is produced for this pairing.*
- **8th House cusp**: tier_score = 6 (n_juan_combos_total=57, n_marr_examples_total=38)  |  **Sun**: tier_score = 4 (n_juan_combos_total=57, n_marr_examples_total=38) — *looked up independently; no combined score is produced for this pairing.*

---

## 21. Death of Son

*Category: Death — Child (male)*

### 1. Event Overview

The 5th house cusp combined with Mars, Saturn, Neptune or Pluto forms the core signature; the specific malefic involved is said to color the manner of death (Mars: violent or wartime, Neptune: drowning or unclear circumstances).

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Mars, Saturn, Neptune, Pluto, Sun, Mercury, Uranus
- Houses/Angles mentioned: Descendant (7th House cusp), Imum Coeli (4th House cusp), 5th House cusp, 8th House cusp, 12th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Mars, Saturn, Neptune, Pluto, Descendant (7th House cusp), Imum Coeli (4th House cusp), 5th House cusp, 8th House cusp, North Node (Ascending)
- **Secondary**: Sun, Mercury, Uranus, 12th House cusp
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Neptune (13/59), Pluto (13/59), Saturn (12/59), Lunar Node (pole unspecified) (12/59), Mars (11/59), Uranus (10/59), Ascendant (1st House cusp) (8/59), Moon (8/59), Midheaven (10th House cusp) (6/59), Mercury (6/59)
- Total pairwise combinations catalogued for this event: 59
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: The 5th house cusp combined with Mars, Saturn, Neptune or Pluto forms the core signature; the specific malefic involved is said to color the manner of death (Mars: violent or wartime, Neptune: drowning or unclear circumstances).
- Points referenced: Mars (mentioned), Neptune (mentioned), Saturn (weak), Pluto (weak), Ascendant (1st House cusp) (weak), Imum Coeli (4th House cusp) (weak), 5th House cusp (weak)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **14 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Saturn (11/14, 79%), Mars (10/14, 71%), 5th House cusp (9/14, 64%), Sun (8/14, 57%), Uranus (8/14, 57%), 8th House cusp (7/14, 50%), Neptune (7/14, 50%), Moon (7/14, 50%)
- Node detail: North Node in 1, South Node in 1, unspecified-pole Node in 4 of 14 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Mars** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Saturn** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Neptune** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Imum Coeli (4th House cusp)** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **5th House cusp** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **Pluto** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 6/10)
- **Sun** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Uranus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Descendant (7th House cusp)** — supported by POLARIS, Marr Aspects (score 6/10)
- **8th House cusp** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Mercury** — supported by POLARIS, Juan Combos, Marr Aspects (score 4/10)
- **Ascendant (1st House cusp)** — supported by Juan Combos, Other, Marr Aspects (score 4/10)
- **Moon** — supported by Juan Combos, Marr Aspects (score 4/10)
- **12th House cusp** — supported by POLARIS, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Venus** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Jupiter** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Midheaven (10th House cusp)** — supported by Juan Combos, Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Mars, Saturn, Neptune, Pluto are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Sun, Mercury, Uranus, Ascendant (1st House cusp), Imum Coeli (4th House cusp), 5th House cusp, Lunar Node (North/South/unspecified) are supported by three of the four sources. 2 of these (Imum Coeli (4th House cusp), 5th House cusp) sit at the structural ceiling for their symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Moon, Venus, Jupiter, Midheaven (10th House cusp), Descendant (7th House cusp), 8th House cusp, 12th House cusp, Part of Fortune.

**Where the sources pull apart.** Moon (in 7/14 example charts, 50%), Ascendant (1st House cusp) (in 6/14 example charts, 43%) recur in a substantial share of Marr's worked examples without being singled out in POLARIS's Primary/Secondary list. This is not a direct contradiction — POLARIS's list is a short, deliberately curated selection rather than an exhaustive one, and no case was found anywhere in the compendium of a POLARIS-Primary symbol being *absent* from a substantial Marr Aspects sample. Read it as an emphasis gap, not a disagreement about relevance.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Mars | Primary | 1 · 11/59 combos | Mentioned | 2 · 10/14 charts (71%) | 4/4 | 59 / 14 | 8 | Strong Symbol |
| Saturn | Primary | 1 · 12/59 combos | Mentioned | 2 · 11/14 charts (79%) | 4/4 | 59 / 14 | 8 | Strong Symbol |
| Neptune | Primary | 1 · 13/59 combos | Mentioned | 2 · 7/14 charts (50%) | 4/4 | 59 / 14 | 8 | Strong Symbol |
| Imum Coeli (4th House cusp) | Primary | — (out of scope) | Mentioned | 2 · 7/14 charts (50%) | 3/3 † | 59 / 14 | 8 | Strong Symbol |
| 5th House cusp | Primary | — (out of scope) | Mentioned | 2 · 9/14 charts (64%) | 3/3 † | 59 / 14 | 8 | Strong Symbol |
| Pluto | Primary | 1 · 13/59 combos | Mentioned | 1 · 5/14 charts (36%) | 4/4 | 59 / 14 | 6 | Moderate (Relevant Symbol) |
| Sun | Secondary | 1 · 5/59 combos | Absent | 2 · 8/14 charts (57%) | 3/4 | 59 / 14 | 6 | Moderate (Relevant Symbol) |
| Uranus | Secondary | 1 · 10/59 combos | Absent | 2 · 8/14 charts (57%) | 3/4 | 59 / 14 | 6 | Moderate (Relevant Symbol) |
| Lunar Node (North/South/unspecified) | Primary | 1 · 12/59 combos | Absent | 1 · 6/14 charts (43%) | 3/4 | 59 / 14 | 6 | Moderate (Relevant Symbol) |
| Descendant (7th House cusp) | Primary | — (out of scope) | Absent | 1 · 3/14 charts (21%) | 2/3 | 59 / 14 | 6 | Moderate (Relevant Symbol) |
| 8th House cusp | Primary | — (out of scope) | Absent | 2 · 7/14 charts (50%) | 2/3 | 59 / 14 | 6 | Moderate (Relevant Symbol) |
| Mercury | Secondary | 1 · 6/59 combos | Absent | 1 · 4/14 charts (29%) | 3/4 | 59 / 14 | 4 | Weak (Occasional Symbol) |
| Ascendant (1st House cusp) | Absent | 1 · 8/59 combos | Mentioned | 1 · 6/14 charts (43%) | 3/4 | 59 / 14 | 4 | Weak (Occasional Symbol) |
| Moon | Absent | 1 · 8/59 combos | Absent | 2 · 7/14 charts (50%) | 2/4 | 59 / 14 | 4 | Weak (Occasional Symbol) |
| 12th House cusp | Secondary | — (out of scope) | Absent | 1 · 4/14 charts (29%) | 2/3 | 59 / 14 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 5/59 combos | Absent | 1 · 3/14 charts (21%) | 2/3 | 59 / 14 | 4 | Weak (Occasional Symbol) |
| Venus | Absent | 1 · 5/59 combos | Absent | 1 · 3/14 charts (21%) | 2/4 | 59 / 14 | 2 | Very Weak (Speculative Symbol) |
| Jupiter | Absent | 1 · 4/59 combos | Absent | 1 · 5/14 charts (36%) | 2/4 | 59 / 14 | 2 | Very Weak (Speculative Symbol) |
| Midheaven (10th House cusp) | Absent | 1 · 6/59 combos | Absent | 1 · 2/14 charts (14%) | 2/4 | 59 / 14 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Mars**: tier_score = 8 (n_juan_combos_total=59, n_marr_examples_total=14)  |  **Descendant (7th House cusp)**: tier_score = 6 (n_juan_combos_total=59, n_marr_examples_total=14) — *looked up independently; no combined score is produced for this pairing.*
- **Mars**: tier_score = 8 (n_juan_combos_total=59, n_marr_examples_total=14)  |  **Midheaven (10th House cusp)**: tier_score = 2 (n_juan_combos_total=59, n_marr_examples_total=14) — *looked up independently; no combined score is produced for this pairing.*
- **Saturn**: tier_score = 8 (n_juan_combos_total=59, n_marr_examples_total=14)  |  **Midheaven (10th House cusp)**: tier_score = 2 (n_juan_combos_total=59, n_marr_examples_total=14) — *looked up independently; no combined score is produced for this pairing.*
- **Descendant (7th House cusp)**: tier_score = 6 (n_juan_combos_total=59, n_marr_examples_total=14)  |  **8th House cusp**: tier_score = 6 (n_juan_combos_total=59, n_marr_examples_total=14) — *looked up independently; no combined score is produced for this pairing.*

---

## 22. Death of Daughter

*Category: Death — Child (female)*

### 1. Event Overview

Alexander Marr's stated rule is identical to Death of Son (the same 5th-house-cusp-plus-malefic formula covers both), so any distinction between the two entries here comes from POLARIS's list and the worked examples rather than a separate stated principle.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Moon, Venus, Neptune, Pluto, Mercury, Mars, Uranus
- Houses/Angles mentioned: Descendant (7th House cusp), Imum Coeli (4th House cusp), 5th House cusp, 8th House cusp, 12th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Moon, Venus, Neptune, Pluto, Descendant (7th House cusp), Imum Coeli (4th House cusp), 5th House cusp, 8th House cusp, North Node (Ascending)
- **Secondary**: Mercury, Mars, Uranus, 12th House cusp
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Neptune (13/59), Pluto (13/59), Saturn (12/59), Lunar Node (pole unspecified) (12/59), Mars (11/59), Uranus (10/59), Ascendant (1st House cusp) (8/59), Moon (8/59), Midheaven (10th House cusp) (6/59), Mercury (6/59)
- Total pairwise combinations catalogued for this event: 59
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: Alexander Marr's stated rule is identical to Death of Son (the same 5th-house-cusp-plus-malefic formula covers both), so any distinction between the two entries here comes from POLARIS's list and the worked examples rather than a separate stated principle.
- Points referenced: Mars (mentioned), Neptune (mentioned), Saturn (weak), Pluto (weak), Ascendant (1st House cusp) (weak), Imum Coeli (4th House cusp) (weak), 5th House cusp (weak)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **14 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Venus (10/14, 71%), Moon (10/14, 71%), 8th House cusp (9/14, 64%), Sun (9/14, 64%), Mars (8/14, 57%), Ascendant (1st House cusp) (7/14, 50%), Uranus (7/14, 50%), Neptune (7/14, 50%)
- Node detail: North Node in 0, South Node in 3, unspecified-pole Node in 3 of 14 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Neptune** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Imum Coeli (4th House cusp)** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **Mars** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 6/10)
- **Pluto** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 6/10)
- **Moon** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Venus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Uranus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Ascendant (1st House cusp)** — supported by Juan Combos, Other, Marr Aspects (score 6/10)
- **5th House cusp** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Descendant (7th House cusp)** — supported by POLARIS, Marr Aspects (score 6/10)
- **8th House cusp** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Mercury** — supported by POLARIS, Juan Combos, Marr Aspects (score 4/10)
- **Saturn** — supported by Juan Combos, Other, Marr Aspects (score 4/10)
- **Sun** — supported by Juan Combos, Marr Aspects (score 4/10)
- **12th House cusp** — supported by POLARIS, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Jupiter** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Midheaven (10th House cusp)** — supported by Juan Combos, Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Mars, Neptune, Pluto are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Moon, Mercury, Venus, Saturn, Uranus, Ascendant (1st House cusp), Imum Coeli (4th House cusp), 5th House cusp, Lunar Node (North/South/unspecified) are supported by three of the four sources. 2 of these (Imum Coeli (4th House cusp), 5th House cusp) sit at the structural ceiling for their symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Sun, Jupiter, Midheaven (10th House cusp), Descendant (7th House cusp), 8th House cusp, 12th House cusp, Part of Fortune.

**Where the sources pull apart.** Sun (in 9/14 example charts, 64%), Ascendant (1st House cusp) (in 7/14 example charts, 50%) recur in a substantial share of Marr's worked examples without being singled out in POLARIS's Primary/Secondary list. This is not a direct contradiction — POLARIS's list is a short, deliberately curated selection rather than an exhaustive one, and no case was found anywhere in the compendium of a POLARIS-Primary symbol being *absent* from a substantial Marr Aspects sample. Read it as an emphasis gap, not a disagreement about relevance.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Neptune | Primary | 1 · 13/59 combos | Mentioned | 2 · 7/14 charts (50%) | 4/4 | 59 / 14 | 8 | Strong Symbol |
| Imum Coeli (4th House cusp) | Primary | — (out of scope) | Mentioned | 2 · 7/14 charts (50%) | 3/3 † | 59 / 14 | 8 | Strong Symbol |
| Mars | Secondary | 1 · 11/59 combos | Mentioned | 2 · 8/14 charts (57%) | 4/4 | 59 / 14 | 6 | Moderate (Relevant Symbol) |
| Pluto | Primary | 1 · 13/59 combos | Mentioned | 1 · 2/14 charts (14%) | 4/4 | 59 / 14 | 6 | Moderate (Relevant Symbol) |
| Moon | Primary | 1 · 8/59 combos | Absent | 2 · 10/14 charts (71%) | 3/4 | 59 / 14 | 6 | Moderate (Relevant Symbol) |
| Venus | Primary | 1 · 5/59 combos | Absent | 2 · 10/14 charts (71%) | 3/4 | 59 / 14 | 6 | Moderate (Relevant Symbol) |
| Uranus | Secondary | 1 · 10/59 combos | Absent | 2 · 7/14 charts (50%) | 3/4 | 59 / 14 | 6 | Moderate (Relevant Symbol) |
| Ascendant (1st House cusp) | Absent | 1 · 8/59 combos | Mentioned | 2 · 7/14 charts (50%) | 3/4 | 59 / 14 | 6 | Moderate (Relevant Symbol) |
| 5th House cusp | Primary | — (out of scope) | Mentioned | 1 · 6/14 charts (43%) | 3/3 † | 59 / 14 | 6 | Moderate (Relevant Symbol) |
| Lunar Node (North/South/unspecified) | Primary | 1 · 12/59 combos | Absent | 1 · 6/14 charts (43%) | 3/4 | 59 / 14 | 6 | Moderate (Relevant Symbol) |
| Descendant (7th House cusp) | Primary | — (out of scope) | Absent | 1 · 2/14 charts (14%) | 2/3 | 59 / 14 | 6 | Moderate (Relevant Symbol) |
| 8th House cusp | Primary | — (out of scope) | Absent | 2 · 9/14 charts (64%) | 2/3 | 59 / 14 | 6 | Moderate (Relevant Symbol) |
| Mercury | Secondary | 1 · 6/59 combos | Absent | 1 · 4/14 charts (29%) | 3/4 | 59 / 14 | 4 | Weak (Occasional Symbol) |
| Saturn | Absent | 1 · 12/59 combos | Mentioned | 1 · 6/14 charts (43%) | 3/4 | 59 / 14 | 4 | Weak (Occasional Symbol) |
| Sun | Absent | 1 · 5/59 combos | Absent | 2 · 9/14 charts (64%) | 2/4 | 59 / 14 | 4 | Weak (Occasional Symbol) |
| 12th House cusp | Secondary | — (out of scope) | Absent | 1 · 3/14 charts (21%) | 2/3 | 59 / 14 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 5/59 combos | Absent | 1 · 3/14 charts (21%) | 2/3 | 59 / 14 | 4 | Weak (Occasional Symbol) |
| Jupiter | Absent | 1 · 4/59 combos | Absent | 1 · 4/14 charts (29%) | 2/4 | 59 / 14 | 2 | Very Weak (Speculative Symbol) |
| Midheaven (10th House cusp) | Absent | 1 · 6/59 combos | Absent | 1 · 3/14 charts (21%) | 2/4 | 59 / 14 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Neptune**: tier_score = 8 (n_juan_combos_total=59, n_marr_examples_total=14)  |  **Lunar Node (North/South/unspecified)**: tier_score = 6 (n_juan_combos_total=59, n_marr_examples_total=14) — *looked up independently; no combined score is produced for this pairing.*
- **Neptune**: tier_score = 8 (n_juan_combos_total=59, n_marr_examples_total=14)  |  **Midheaven (10th House cusp)**: tier_score = 2 (n_juan_combos_total=59, n_marr_examples_total=14) — *looked up independently; no combined score is produced for this pairing.*
- **Imum Coeli (4th House cusp)**: tier_score = 8 (n_juan_combos_total=59, n_marr_examples_total=14)  |  **Midheaven (10th House cusp)**: tier_score = 2 (n_juan_combos_total=59, n_marr_examples_total=14) — *looked up independently; no combined score is produced for this pairing.*
- **Lunar Node (North/South/unspecified)**: tier_score = 6 (n_juan_combos_total=59, n_marr_examples_total=14)  |  **Descendant (7th House cusp)**: tier_score = 6 (n_juan_combos_total=59, n_marr_examples_total=14) — *looked up independently; no combined score is produced for this pairing.*

---

## 23. Death of Wife or Female Friend

*Category: Death — Partnership (female)*

### 1. Event Overview

For a male native, the Descendant or IC afflicted by Saturn is the primary signature; Uranus marks a sudden death and Neptune an unclear or drowning-related one — a manner-of-death coloring shared with several other death entries.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Moon, Venus, Mars, Saturn, Neptune, Pluto, Uranus
- Houses/Angles mentioned: Descendant (7th House cusp), Imum Coeli (4th House cusp), 8th House cusp, 5th House cusp, 12th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Moon, Venus, Mars, Saturn, Neptune, Pluto, Descendant (7th House cusp), Imum Coeli (4th House cusp), 8th House cusp, North Node (Ascending)
- **Secondary**: Uranus, 5th House cusp, 12th House cusp
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Saturn (13/62), Neptune (13/62), Pluto (13/62), Lunar Node (pole unspecified) (12/62), Mars (11/62), Uranus (10/62), Ascendant (1st House cusp) (9/62), Moon (8/62), Mercury (7/62), Midheaven (10th House cusp) (7/62)
- Total pairwise combinations catalogued for this event: 62
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: For a male native, the Descendant or IC afflicted by Saturn is the primary signature; Uranus marks a sudden death and Neptune an unclear or drowning-related one — a manner-of-death coloring shared with several other death entries.
- Points referenced: Moon (strong), Venus (strong), Saturn (strong), Descendant (7th House cusp) (strong), Imum Coeli (4th House cusp) (strong), Uranus (mentioned), Neptune (mentioned)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **15 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Descendant (7th House cusp) (11/15, 73%), Mars (11/15, 73%), Venus (10/15, 67%), 8th House cusp (10/15, 67%), Neptune (9/15, 60%), Sun (8/15, 53%), Moon (8/15, 53%), Saturn (8/15, 53%)
- Node detail: North Node in 1, South Node in 4, unspecified-pole Node in 4 of 15 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- **Descendant (7th House cusp)** — supported by POLARIS, Other, Marr Aspects (score 10/10)
- **Imum Coeli (4th House cusp)** — supported by POLARIS, Other, Marr Aspects (score 10/10)

**Secondary Symbols**
- **Moon** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Venus** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Saturn** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Neptune** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Uranus** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 6/10)
- **Mars** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Pluto** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **8th House cusp** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Sun** — supported by Juan Combos, Marr Aspects (score 4/10)
- **5th House cusp** — supported by POLARIS, Marr Aspects (score 4/10)
- **12th House cusp** — supported by POLARIS, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Mercury** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Jupiter** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Ascendant (1st House cusp)** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Midheaven (10th House cusp)** — supported by Juan Combos, Marr Aspects (score 2/10)
- **2nd House cusp** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Moon, Venus, Saturn, Uranus, Neptune are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Mars, Pluto, Descendant (7th House cusp), Imum Coeli (4th House cusp), Lunar Node (North/South/unspecified) are supported by three of the four sources. 2 of these (Descendant (7th House cusp), Imum Coeli (4th House cusp)) sit at the structural ceiling for their symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Sun, Mercury, Jupiter, Ascendant (1st House cusp), Midheaven (10th House cusp), 5th House cusp, 8th House cusp, 12th House cusp, Part of Fortune.

**Speculative / source-specific symbolism.** 2nd House cusp (Marr Aspects only), 9th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** Sun (in 8/15 example charts, 53%), Mercury (in 7/15 example charts, 47%) recur in a substantial share of Marr's worked examples without being singled out in POLARIS's Primary/Secondary list. This is not a direct contradiction — POLARIS's list is a short, deliberately curated selection rather than an exhaustive one, and no case was found anywhere in the compendium of a POLARIS-Primary symbol being *absent* from a substantial Marr Aspects sample. Read it as an emphasis gap, not a disagreement about relevance.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Descendant (7th House cusp) | Primary | — (out of scope) | Strong emphasis | 2 · 11/15 charts (73%) | 3/3 † | 62 / 15 | 10 | Very Strong (Core Symbol) |
| Imum Coeli (4th House cusp) | Primary | — (out of scope) | Strong emphasis | 2 · 8/15 charts (53%) | 3/3 † | 62 / 15 | 10 | Very Strong (Core Symbol) |
| Moon | Primary | 1 · 8/62 combos | Strong emphasis | 2 · 8/15 charts (53%) | 4/4 | 62 / 15 | 8 | Strong Symbol |
| Venus | Primary | 1 · 6/62 combos | Strong emphasis | 2 · 10/15 charts (67%) | 4/4 | 62 / 15 | 8 | Strong Symbol |
| Saturn | Primary | 1 · 13/62 combos | Strong emphasis | 2 · 8/15 charts (53%) | 4/4 | 62 / 15 | 8 | Strong Symbol |
| Neptune | Primary | 1 · 13/62 combos | Mentioned | 2 · 9/15 charts (60%) | 4/4 | 62 / 15 | 8 | Strong Symbol |
| Uranus | Secondary | 1 · 10/62 combos | Mentioned | 1 · 7/15 charts (47%) | 4/4 | 62 / 15 | 6 | Moderate (Relevant Symbol) |
| Mars | Primary | 1 · 11/62 combos | Absent | 2 · 11/15 charts (73%) | 3/4 | 62 / 15 | 6 | Moderate (Relevant Symbol) |
| Pluto | Primary | 1 · 13/62 combos | Absent | 1 · 7/15 charts (47%) | 3/4 | 62 / 15 | 6 | Moderate (Relevant Symbol) |
| Lunar Node (North/South/unspecified) | Primary | 1 · 12/62 combos | Absent | 2 · 9/15 charts (60%) | 3/4 | 62 / 15 | 6 | Moderate (Relevant Symbol) |
| 8th House cusp | Primary | — (out of scope) | Absent | 2 · 10/15 charts (67%) | 2/3 | 62 / 15 | 6 | Moderate (Relevant Symbol) |
| Sun | Absent | 1 · 6/62 combos | Absent | 2 · 8/15 charts (53%) | 2/4 | 62 / 15 | 4 | Weak (Occasional Symbol) |
| 5th House cusp | Secondary | — (out of scope) | Absent | 1 · 1/15 charts (7%) | 2/3 | 62 / 15 | 4 | Weak (Occasional Symbol) |
| 12th House cusp | Secondary | — (out of scope) | Absent | 1 · 2/15 charts (13%) | 2/3 | 62 / 15 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 5/62 combos | Absent | 1 · 3/15 charts (20%) | 2/3 | 62 / 15 | 4 | Weak (Occasional Symbol) |
| Mercury | Absent | 1 · 7/62 combos | Absent | 1 · 7/15 charts (47%) | 2/4 | 62 / 15 | 2 | Very Weak (Speculative Symbol) |
| Jupiter | Absent | 1 · 4/62 combos | Absent | 1 · 2/15 charts (13%) | 2/4 | 62 / 15 | 2 | Very Weak (Speculative Symbol) |
| Ascendant (1st House cusp) | Absent | 1 · 9/62 combos | Absent | 1 · 4/15 charts (27%) | 2/4 | 62 / 15 | 2 | Very Weak (Speculative Symbol) |
| Midheaven (10th House cusp) | Absent | 1 · 7/62 combos | Absent | 1 · 4/15 charts (27%) | 2/4 | 62 / 15 | 2 | Very Weak (Speculative Symbol) |
| 2nd House cusp | Absent | — (out of scope) | Absent | 1 · 1/15 charts (7%) | 1/3 | 62 / 15 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | Absent | 1 · 3/15 charts (20%) | 1/3 | 62 / 15 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 1/15 charts (7%) | 1/3 | 62 / 15 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Descendant (7th House cusp)**: tier_score = 10 (n_juan_combos_total=62, n_marr_examples_total=15)  |  **Sun**: tier_score = 4 (n_juan_combos_total=62, n_marr_examples_total=15) — *looked up independently; no combined score is produced for this pairing.*
- **Descendant (7th House cusp)**: tier_score = 10 (n_juan_combos_total=62, n_marr_examples_total=15)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=62, n_marr_examples_total=15) — *looked up independently; no combined score is produced for this pairing.*
- **Imum Coeli (4th House cusp)**: tier_score = 10 (n_juan_combos_total=62, n_marr_examples_total=15)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=62, n_marr_examples_total=15) — *looked up independently; no combined score is produced for this pairing.*
- **Sun**: tier_score = 4 (n_juan_combos_total=62, n_marr_examples_total=15)  |  **5th House cusp**: tier_score = 4 (n_juan_combos_total=62, n_marr_examples_total=15) — *looked up independently; no combined score is produced for this pairing.*

---

## 24. Death of Husband or Male Friend

*Category: Death — Partnership (male)*

### 1. Event Overview

The mirror of Death of Wife for a female native: the Descendant or Midheaven combines with Saturn or the Sun as the core signature, with the same Uranus/Neptune manner-of-death coloring.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Sun, Mars, Saturn, Neptune, Pluto, Uranus
- Houses/Angles mentioned: Descendant (7th House cusp), Imum Coeli (4th House cusp), 8th House cusp, 5th House cusp, 12th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Sun, Mars, Saturn, Neptune, Pluto, Descendant (7th House cusp), Imum Coeli (4th House cusp), 8th House cusp, North Node (Ascending)
- **Secondary**: Uranus, 5th House cusp, 12th House cusp
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Saturn (13/61), Neptune (13/61), Pluto (12/61), Lunar Node (pole unspecified) (12/61), Mars (11/61), Uranus (10/61), Ascendant (1st House cusp) (9/61), Moon (8/61), Sun (7/61), Mercury (7/61)
- Total pairwise combinations catalogued for this event: 61
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: The mirror of Death of Wife for a female native: the Descendant or Midheaven combines with Saturn or the Sun as the core signature, with the same Uranus/Neptune manner-of-death coloring.
- Points referenced: Sun (strong), Saturn (strong), Midheaven (10th House cusp) (strong), Descendant (7th House cusp) (strong), Uranus (mentioned), Neptune (mentioned)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **13 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Saturn (10/13, 77%), Descendant (7th House cusp) (10/13, 77%), 8th House cusp (9/13, 69%), Mars (9/13, 69%), Neptune (8/13, 62%), 12th House cusp (6/13, 46%), Moon (6/13, 46%), Pluto (6/13, 46%)
- Node detail: North Node in 0, South Node in 1, unspecified-pole Node in 3 of 13 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- **Descendant (7th House cusp)** — supported by POLARIS, Other, Marr Aspects (score 10/10)

**Secondary Symbols**
- **Sun** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Saturn** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Neptune** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Uranus** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 6/10)
- **Mars** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Pluto** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Midheaven (10th House cusp)** — supported by Juan Combos, Other, Marr Aspects (score 6/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Imum Coeli (4th House cusp)** — supported by POLARIS, Marr Aspects (score 6/10)
- **8th House cusp** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **5th House cusp** — supported by POLARIS, Marr Aspects (score 4/10)
- **12th House cusp** — supported by POLARIS, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Moon** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Mercury** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Venus** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Ascendant (1st House cusp)** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Jupiter** — supported by Juan Combos (score 2/10)
- **3rd House cusp** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Sun, Saturn, Uranus, Neptune are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Mars, Pluto, Midheaven (10th House cusp), Descendant (7th House cusp), Lunar Node (North/South/unspecified) are supported by three of the four sources. 1 of these (Descendant (7th House cusp)) sits at the structural ceiling for its symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Moon, Mercury, Venus, Ascendant (1st House cusp), Imum Coeli (4th House cusp), 5th House cusp, 8th House cusp, 12th House cusp, Part of Fortune.

**Speculative / source-specific symbolism.** Jupiter (Juan Combos only), 3rd House cusp (Marr Aspects only), 9th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** Moon (in 6/13 example charts, 46%) recur in a substantial share of Marr's worked examples without being singled out in POLARIS's Primary/Secondary list. This is not a direct contradiction — POLARIS's list is a short, deliberately curated selection rather than an exhaustive one, and no case was found anywhere in the compendium of a POLARIS-Primary symbol being *absent* from a substantial Marr Aspects sample. Read it as an emphasis gap, not a disagreement about relevance.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Descendant (7th House cusp) | Primary | — (out of scope) | Strong emphasis | 2 · 10/13 charts (77%) | 3/3 † | 61 / 13 | 10 | Very Strong (Core Symbol) |
| Sun | Primary | 1 · 7/61 combos | Strong emphasis | 1 · 5/13 charts (38%) | 4/4 | 61 / 13 | 8 | Strong Symbol |
| Saturn | Primary | 1 · 13/61 combos | Strong emphasis | 2 · 10/13 charts (77%) | 4/4 | 61 / 13 | 8 | Strong Symbol |
| Neptune | Primary | 1 · 13/61 combos | Mentioned | 2 · 8/13 charts (62%) | 4/4 | 61 / 13 | 8 | Strong Symbol |
| Uranus | Secondary | 1 · 10/61 combos | Mentioned | 1 · 5/13 charts (38%) | 4/4 | 61 / 13 | 6 | Moderate (Relevant Symbol) |
| Mars | Primary | 1 · 11/61 combos | Absent | 2 · 9/13 charts (69%) | 3/4 | 61 / 13 | 6 | Moderate (Relevant Symbol) |
| Pluto | Primary | 1 · 12/61 combos | Absent | 1 · 6/13 charts (46%) | 3/4 | 61 / 13 | 6 | Moderate (Relevant Symbol) |
| Midheaven (10th House cusp) | Absent | 1 · 7/61 combos | Strong emphasis | 1 · 4/13 charts (31%) | 3/4 | 61 / 13 | 6 | Moderate (Relevant Symbol) |
| Lunar Node (North/South/unspecified) | Primary | 1 · 12/61 combos | Absent | 1 · 4/13 charts (31%) | 3/4 | 61 / 13 | 6 | Moderate (Relevant Symbol) |
| Imum Coeli (4th House cusp) | Primary | — (out of scope) | Absent | 1 · 6/13 charts (46%) | 2/3 | 61 / 13 | 6 | Moderate (Relevant Symbol) |
| 8th House cusp | Primary | — (out of scope) | Absent | 2 · 9/13 charts (69%) | 2/3 | 61 / 13 | 6 | Moderate (Relevant Symbol) |
| 5th House cusp | Secondary | — (out of scope) | Absent | 1 · 1/13 charts (8%) | 2/3 | 61 / 13 | 4 | Weak (Occasional Symbol) |
| 12th House cusp | Secondary | — (out of scope) | Absent | 1 · 6/13 charts (46%) | 2/3 | 61 / 13 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 5/61 combos | Absent | 1 · 3/13 charts (23%) | 2/3 | 61 / 13 | 4 | Weak (Occasional Symbol) |
| Moon | Absent | 1 · 8/61 combos | Absent | 1 · 6/13 charts (46%) | 2/4 | 61 / 13 | 2 | Very Weak (Speculative Symbol) |
| Mercury | Absent | 1 · 7/61 combos | Absent | 1 · 3/13 charts (23%) | 2/4 | 61 / 13 | 2 | Very Weak (Speculative Symbol) |
| Venus | Absent | 1 · 4/61 combos | Absent | 1 · 1/13 charts (8%) | 2/4 | 61 / 13 | 2 | Very Weak (Speculative Symbol) |
| Ascendant (1st House cusp) | Absent | 1 · 9/61 combos | Absent | 1 · 3/13 charts (23%) | 2/4 | 61 / 13 | 2 | Very Weak (Speculative Symbol) |
| Jupiter | Absent | 1 · 4/61 combos | Absent | 0 · 0/13 charts (0%) | 1/4 | 61 / 13 | 2 | Very Weak (Speculative Symbol) |
| 3rd House cusp | Absent | — (out of scope) | Absent | 1 · 1/13 charts (8%) | 1/3 | 61 / 13 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | Absent | 1 · 1/13 charts (8%) | 1/3 | 61 / 13 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 3/13 charts (23%) | 1/3 | 61 / 13 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Descendant (7th House cusp)**: tier_score = 10 (n_juan_combos_total=61, n_marr_examples_total=13)  |  **5th House cusp**: tier_score = 4 (n_juan_combos_total=61, n_marr_examples_total=13) — *looked up independently; no combined score is produced for this pairing.*
- **Descendant (7th House cusp)**: tier_score = 10 (n_juan_combos_total=61, n_marr_examples_total=13)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=61, n_marr_examples_total=13) — *looked up independently; no combined score is produced for this pairing.*
- **Sun**: tier_score = 8 (n_juan_combos_total=61, n_marr_examples_total=13)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=61, n_marr_examples_total=13) — *looked up independently; no combined score is produced for this pairing.*
- **5th House cusp**: tier_score = 4 (n_juan_combos_total=61, n_marr_examples_total=13)  |  **12th House cusp**: tier_score = 4 (n_juan_combos_total=61, n_marr_examples_total=13) — *looked up independently; no combined score is produced for this pairing.*

---

## 25. Death of Brother

*Category: Death — Family (sibling, male)*

### 1. Event Overview

The 3rd house cusp (or IC) afflicted by a malefic, and secondarily by Mercury, forms the core signature — the same house used for the sibling's birth, now shown in its adverse expression. The 8th house cusp adds an inheritance dimension.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Mercury, Mars, Saturn, Neptune, Pluto, Sun, Moon
- Houses/Angles mentioned: Ascendant (1st House cusp), Imum Coeli (4th House cusp), 8th House cusp, 3rd House cusp, 12th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Mercury, Mars, Saturn, Neptune, Pluto, Ascendant (1st House cusp), Imum Coeli (4th House cusp), 8th House cusp, North Node (Ascending)
- **Secondary**: Sun, Moon, 3rd House cusp, 12th House cusp
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Neptune (13/59), Pluto (13/59), Saturn (12/59), Lunar Node (pole unspecified) (12/59), Mars (11/59), Uranus (10/59), Ascendant (1st House cusp) (8/59), Moon (8/59), Midheaven (10th House cusp) (6/59), Mercury (6/59)
- Total pairwise combinations catalogued for this event: 59
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: The 3rd house cusp (or IC) afflicted by a malefic, and secondarily by Mercury, forms the core signature — the same house used for the sibling's birth, now shown in its adverse expression. The 8th house cusp adds an inheritance dimension.
- Points referenced: 8th House cusp (mentioned), Mercury (weak), Imum Coeli (4th House cusp) (weak), 3rd House cusp (weak)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **13 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Saturn (11/13, 85%), Mars (11/13, 85%), Mercury (10/13, 77%), 3rd House cusp (8/13, 62%), Uranus (8/13, 62%), 8th House cusp (8/13, 62%), Imum Coeli (4th House cusp) (6/13, 46%), Neptune (6/13, 46%)
- Node detail: North Node in 1, South Node in 2, unspecified-pole Node in 3 of 13 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Mercury** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **8th House cusp** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **Mars** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Saturn** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Neptune** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Pluto** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Imum Coeli (4th House cusp)** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **3rd House cusp** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Sun** — supported by POLARIS, Juan Combos, Marr Aspects (score 4/10)
- **Moon** — supported by POLARIS, Juan Combos, Marr Aspects (score 4/10)
- **Uranus** — supported by Juan Combos, Marr Aspects (score 4/10)
- **12th House cusp** — supported by POLARIS, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Venus** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Jupiter** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Midheaven (10th House cusp)** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Descendant (7th House cusp)** — supported by Marr Aspects (score 2/10)
- **5th House cusp** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Mercury is corroborated by every source able to speak to it, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Sun, Moon, Mars, Saturn, Neptune, Pluto, Ascendant (1st House cusp), Imum Coeli (4th House cusp), 3rd House cusp, 8th House cusp, Lunar Node (North/South/unspecified) are supported by three of the four sources. 3 of these (Imum Coeli (4th House cusp), 3rd House cusp, 8th House cusp) sit at the structural ceiling for their symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Venus, Jupiter, Uranus, Midheaven (10th House cusp), 12th House cusp, Part of Fortune.

**Speculative / source-specific symbolism.** Descendant (7th House cusp) (Marr Aspects only), 5th House cusp (Marr Aspects only), 9th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** Uranus (in 8/13 example charts, 62%) recur in a substantial share of Marr's worked examples without being singled out in POLARIS's Primary/Secondary list. This is not a direct contradiction — POLARIS's list is a short, deliberately curated selection rather than an exhaustive one, and no case was found anywhere in the compendium of a POLARIS-Primary symbol being *absent* from a substantial Marr Aspects sample. Read it as an emphasis gap, not a disagreement about relevance.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Mercury | Primary | 1 · 6/59 combos | Mentioned | 2 · 10/13 charts (77%) | 4/4 | 59 / 13 | 8 | Strong Symbol |
| 8th House cusp | Primary | — (out of scope) | Mentioned | 2 · 8/13 charts (62%) | 3/3 † | 59 / 13 | 8 | Strong Symbol |
| Mars | Primary | 1 · 11/59 combos | Absent | 2 · 11/13 charts (85%) | 3/4 | 59 / 13 | 6 | Moderate (Relevant Symbol) |
| Saturn | Primary | 1 · 12/59 combos | Absent | 2 · 11/13 charts (85%) | 3/4 | 59 / 13 | 6 | Moderate (Relevant Symbol) |
| Neptune | Primary | 1 · 13/59 combos | Absent | 1 · 6/13 charts (46%) | 3/4 | 59 / 13 | 6 | Moderate (Relevant Symbol) |
| Pluto | Primary | 1 · 13/59 combos | Absent | 1 · 4/13 charts (31%) | 3/4 | 59 / 13 | 6 | Moderate (Relevant Symbol) |
| Ascendant (1st House cusp) | Primary | 1 · 8/59 combos | Absent | 1 · 1/13 charts (8%) | 3/4 | 59 / 13 | 6 | Moderate (Relevant Symbol) |
| Imum Coeli (4th House cusp) | Primary | — (out of scope) | Mentioned | 1 · 6/13 charts (46%) | 3/3 † | 59 / 13 | 6 | Moderate (Relevant Symbol) |
| 3rd House cusp | Secondary | — (out of scope) | Mentioned | 2 · 8/13 charts (62%) | 3/3 † | 59 / 13 | 6 | Moderate (Relevant Symbol) |
| Lunar Node (North/South/unspecified) | Primary | 1 · 12/59 combos | Absent | 1 · 6/13 charts (46%) | 3/4 | 59 / 13 | 6 | Moderate (Relevant Symbol) |
| Sun | Secondary | 1 · 5/59 combos | Absent | 1 · 2/13 charts (15%) | 3/4 | 59 / 13 | 4 | Weak (Occasional Symbol) |
| Moon | Secondary | 1 · 8/59 combos | Absent | 1 · 3/13 charts (23%) | 3/4 | 59 / 13 | 4 | Weak (Occasional Symbol) |
| Uranus | Absent | 1 · 10/59 combos | Absent | 2 · 8/13 charts (62%) | 2/4 | 59 / 13 | 4 | Weak (Occasional Symbol) |
| 12th House cusp | Secondary | — (out of scope) | Absent | 1 · 2/13 charts (15%) | 2/3 | 59 / 13 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 5/59 combos | Absent | 1 · 4/13 charts (31%) | 2/3 | 59 / 13 | 4 | Weak (Occasional Symbol) |
| Venus | Absent | 1 · 5/59 combos | Absent | 1 · 2/13 charts (15%) | 2/4 | 59 / 13 | 2 | Very Weak (Speculative Symbol) |
| Jupiter | Absent | 1 · 4/59 combos | Absent | 1 · 1/13 charts (8%) | 2/4 | 59 / 13 | 2 | Very Weak (Speculative Symbol) |
| Midheaven (10th House cusp) | Absent | 1 · 6/59 combos | Absent | 1 · 3/13 charts (23%) | 2/4 | 59 / 13 | 2 | Very Weak (Speculative Symbol) |
| Descendant (7th House cusp) | Absent | — (out of scope) | Absent | 1 · 4/13 charts (31%) | 1/3 | 59 / 13 | 2 | Very Weak (Speculative Symbol) |
| 5th House cusp | Absent | — (out of scope) | Absent | 1 · 1/13 charts (8%) | 1/3 | 59 / 13 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | Absent | 1 · 2/13 charts (15%) | 1/3 | 59 / 13 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Mercury**: tier_score = 8 (n_juan_combos_total=59, n_marr_examples_total=13)  |  **Sun**: tier_score = 4 (n_juan_combos_total=59, n_marr_examples_total=13) — *looked up independently; no combined score is produced for this pairing.*
- **Mercury**: tier_score = 8 (n_juan_combos_total=59, n_marr_examples_total=13)  |  **9th House cusp**: tier_score = 2 (n_juan_combos_total=59, n_marr_examples_total=13) — *looked up independently; no combined score is produced for this pairing.*
- **8th House cusp**: tier_score = 8 (n_juan_combos_total=59, n_marr_examples_total=13)  |  **9th House cusp**: tier_score = 2 (n_juan_combos_total=59, n_marr_examples_total=13) — *looked up independently; no combined score is produced for this pairing.*
- **Sun**: tier_score = 4 (n_juan_combos_total=59, n_marr_examples_total=13)  |  **Moon**: tier_score = 4 (n_juan_combos_total=59, n_marr_examples_total=13) — *looked up independently; no combined score is produced for this pairing.*

---

## 26. Death of Sister

*Category: Death — Family (sibling, female)*

### 1. Event Overview

The gender-mirrored counterpart to Death of Brother: Venus replaces Mercury as the secondary afflicted planet, while the 3rd-house/IC-plus-8th-house (inheritance) pattern remains the same.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Moon, Mercury, Venus, Mars, Saturn, Neptune, Pluto
- Houses/Angles mentioned: Ascendant (1st House cusp), Imum Coeli (4th House cusp), 8th House cusp, 3rd House cusp, 12th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Moon, Mercury, Venus, Mars, Saturn, Neptune, Pluto, Ascendant (1st House cusp), Imum Coeli (4th House cusp), 8th House cusp, North Node (Ascending)
- **Secondary**: 3rd House cusp, 12th House cusp
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Neptune (13/59), Pluto (13/59), Saturn (12/59), Lunar Node (pole unspecified) (12/59), Mars (11/59), Uranus (10/59), Ascendant (1st House cusp) (8/59), Moon (8/59), Midheaven (10th House cusp) (6/59), Mercury (6/59)
- Total pairwise combinations catalogued for this event: 59
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: The gender-mirrored counterpart to Death of Brother: Venus replaces Mercury as the secondary afflicted planet, while the 3rd-house/IC-plus-8th-house (inheritance) pattern remains the same.
- Points referenced: 8th House cusp (mentioned), Venus (weak), Imum Coeli (4th House cusp) (weak), 3rd House cusp (weak)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **15 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: 3rd House cusp (13/15, 87%), Moon (12/15, 80%), Venus (11/15, 73%), 8th House cusp (9/15, 60%), Mars (9/15, 60%), Mercury (8/15, 53%), Uranus (8/15, 53%), Imum Coeli (4th House cusp) (8/15, 53%)
- Node detail: North Node in 1, South Node in 6, unspecified-pole Node in 3 of 15 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Venus** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Imum Coeli (4th House cusp)** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **8th House cusp** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **Moon** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Mercury** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Mars** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Saturn** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Neptune** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Pluto** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **3rd House cusp** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Uranus** — supported by Juan Combos, Marr Aspects (score 4/10)
- **12th House cusp** — supported by POLARIS, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Sun** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Jupiter** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Midheaven (10th House cusp)** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Descendant (7th House cusp)** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Venus is corroborated by every source able to speak to it, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Moon, Mercury, Mars, Saturn, Neptune, Pluto, Ascendant (1st House cusp), Imum Coeli (4th House cusp), 3rd House cusp, 8th House cusp, Lunar Node (North/South/unspecified) are supported by three of the four sources. 3 of these (Imum Coeli (4th House cusp), 3rd House cusp, 8th House cusp) sit at the structural ceiling for their symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Sun, Jupiter, Uranus, Midheaven (10th House cusp), 12th House cusp, Part of Fortune.

**Speculative / source-specific symbolism.** Descendant (7th House cusp) (Marr Aspects only), 9th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** Uranus (in 8/15 example charts, 53%), Descendant (7th House cusp) (in 6/15 example charts, 40%) recur in a substantial share of Marr's worked examples without being singled out in POLARIS's Primary/Secondary list. This is not a direct contradiction — POLARIS's list is a short, deliberately curated selection rather than an exhaustive one, and no case was found anywhere in the compendium of a POLARIS-Primary symbol being *absent* from a substantial Marr Aspects sample. Read it as an emphasis gap, not a disagreement about relevance.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Venus | Primary | 1 · 5/59 combos | Mentioned | 2 · 11/15 charts (73%) | 4/4 | 59 / 15 | 8 | Strong Symbol |
| Imum Coeli (4th House cusp) | Primary | — (out of scope) | Mentioned | 2 · 8/15 charts (53%) | 3/3 † | 59 / 15 | 8 | Strong Symbol |
| 8th House cusp | Primary | — (out of scope) | Mentioned | 2 · 9/15 charts (60%) | 3/3 † | 59 / 15 | 8 | Strong Symbol |
| Moon | Primary | 1 · 8/59 combos | Absent | 2 · 12/15 charts (80%) | 3/4 | 59 / 15 | 6 | Moderate (Relevant Symbol) |
| Mercury | Primary | 1 · 6/59 combos | Absent | 2 · 8/15 charts (53%) | 3/4 | 59 / 15 | 6 | Moderate (Relevant Symbol) |
| Mars | Primary | 1 · 11/59 combos | Absent | 2 · 9/15 charts (60%) | 3/4 | 59 / 15 | 6 | Moderate (Relevant Symbol) |
| Saturn | Primary | 1 · 12/59 combos | Absent | 1 · 5/15 charts (33%) | 3/4 | 59 / 15 | 6 | Moderate (Relevant Symbol) |
| Neptune | Primary | 1 · 13/59 combos | Absent | 2 · 8/15 charts (53%) | 3/4 | 59 / 15 | 6 | Moderate (Relevant Symbol) |
| Pluto | Primary | 1 · 13/59 combos | Absent | 1 · 6/15 charts (40%) | 3/4 | 59 / 15 | 6 | Moderate (Relevant Symbol) |
| Ascendant (1st House cusp) | Primary | 1 · 8/59 combos | Absent | 1 · 6/15 charts (40%) | 3/4 | 59 / 15 | 6 | Moderate (Relevant Symbol) |
| 3rd House cusp | Secondary | — (out of scope) | Mentioned | 2 · 13/15 charts (87%) | 3/3 † | 59 / 15 | 6 | Moderate (Relevant Symbol) |
| Lunar Node (North/South/unspecified) | Primary | 1 · 12/59 combos | Absent | 2 · 10/15 charts (67%) | 3/4 | 59 / 15 | 6 | Moderate (Relevant Symbol) |
| Uranus | Absent | 1 · 10/59 combos | Absent | 2 · 8/15 charts (53%) | 2/4 | 59 / 15 | 4 | Weak (Occasional Symbol) |
| 12th House cusp | Secondary | — (out of scope) | Absent | 1 · 2/15 charts (13%) | 2/3 | 59 / 15 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 5/59 combos | Absent | 1 · 4/15 charts (27%) | 2/3 | 59 / 15 | 4 | Weak (Occasional Symbol) |
| Sun | Absent | 1 · 5/59 combos | Absent | 1 · 1/15 charts (7%) | 2/4 | 59 / 15 | 2 | Very Weak (Speculative Symbol) |
| Jupiter | Absent | 1 · 4/59 combos | Absent | 1 · 3/15 charts (20%) | 2/4 | 59 / 15 | 2 | Very Weak (Speculative Symbol) |
| Midheaven (10th House cusp) | Absent | 1 · 6/59 combos | Absent | 1 · 2/15 charts (13%) | 2/4 | 59 / 15 | 2 | Very Weak (Speculative Symbol) |
| Descendant (7th House cusp) | Absent | — (out of scope) | Absent | 1 · 6/15 charts (40%) | 1/3 | 59 / 15 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | Absent | 1 · 1/15 charts (7%) | 1/3 | 59 / 15 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 1/15 charts (7%) | 1/3 | 59 / 15 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Venus**: tier_score = 8 (n_juan_combos_total=59, n_marr_examples_total=15)  |  **3rd House cusp**: tier_score = 6 (n_juan_combos_total=59, n_marr_examples_total=15) — *looked up independently; no combined score is produced for this pairing.*
- **Venus**: tier_score = 8 (n_juan_combos_total=59, n_marr_examples_total=15)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=59, n_marr_examples_total=15) — *looked up independently; no combined score is produced for this pairing.*
- **Imum Coeli (4th House cusp)**: tier_score = 8 (n_juan_combos_total=59, n_marr_examples_total=15)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=59, n_marr_examples_total=15) — *looked up independently; no combined score is produced for this pairing.*
- **3rd House cusp**: tier_score = 6 (n_juan_combos_total=59, n_marr_examples_total=15)  |  **Lunar Node (North/South/unspecified)**: tier_score = 6 (n_juan_combos_total=59, n_marr_examples_total=15) — *looked up independently; no combined score is produced for this pairing.*

---

## 27. Death

*Category: Death — the native's own mortality*

### 1. Event Overview

The native's own death, as distinct from the death of a relative. The sources differentiate by life stage: an angle conjunct or square the Sun for the elderly, an afflicted Ascendant for the young and middle-aged, and an afflicted IC for death in senility.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Sun, Saturn, Neptune, Pluto, Moon, Mars, Uranus
- Houses/Angles mentioned: Ascendant (1st House cusp), Midheaven (10th House cusp), 8th House cusp, 12th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Sun, Saturn, Neptune, Pluto, Ascendant (1st House cusp), Midheaven (10th House cusp), 8th House cusp, North Node (Ascending)
- **Secondary**: Moon, Mars, Uranus, 12th House cusp
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Neptune (8/30), Saturn (8/30), Pluto (8/30), Mars (8/30), Sun (6/30), Ascendant (1st House cusp) (5/30), Midheaven (10th House cusp) (5/30), Lunar Node (pole unspecified) (4/30), Moon (4/30), Uranus (2/30)
- Total pairwise combinations catalogued for this event: 30
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: The native's own death, as distinct from the death of a relative. The sources differentiate by life stage: an angle conjunct or square the Sun for the elderly, an afflicted Ascendant for the young and middle-aged, and an afflicted IC for death in senility.
- Points referenced: Sun (strong), Saturn (strong), Imum Coeli (4th House cusp) (strong), Ascendant (1st House cusp) (mentioned)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **72 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Saturn (62/72, 86%), Imum Coeli (4th House cusp) (51/72, 71%), Uranus (49/72, 68%), Mars (44/72, 61%), Ascendant (1st House cusp) (43/72, 60%), Neptune (42/72, 58%), Sun (41/72, 57%), Moon (38/72, 53%)
- Node detail: North Node in 0, South Node in 7, unspecified-pole Node in 9 of 72 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Sun** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Saturn** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Moon** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Mars** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Uranus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Neptune** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Pluto** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Midheaven (10th House cusp)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Imum Coeli (4th House cusp)** — supported by Other, Marr Aspects (score 6/10)
- **8th House cusp** — supported by POLARIS, Marr Aspects (score 6/10)
- **12th House cusp** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Mercury** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Venus** — supported by Marr Aspects (score 2/10)
- **Jupiter** — supported by Marr Aspects (score 2/10)
- **Descendant (7th House cusp)** — supported by Marr Aspects (score 2/10)
- **2nd House cusp** — supported by Marr Aspects (score 2/10)
- **3rd House cusp** — supported by Marr Aspects (score 2/10)
- **5th House cusp** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Sun, Saturn, Ascendant (1st House cusp) are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Moon, Mars, Uranus, Neptune, Pluto, Midheaven (10th House cusp), Lunar Node (North/South/unspecified) are supported by three of the four sources.

Supported by exactly two sources (moderate confidence): Mercury, Imum Coeli (4th House cusp), 8th House cusp, 12th House cusp, Part of Fortune.

**Speculative / source-specific symbolism.** Venus (Marr Aspects only), Jupiter (Marr Aspects only), Descendant (7th House cusp) (Marr Aspects only), 2nd House cusp (Marr Aspects only), 3rd House cusp (Marr Aspects only), 5th House cusp (Marr Aspects only), 9th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** Imum Coeli (4th House cusp) (in 51/72 example charts, 71%) recur in a substantial share of Marr's worked examples without being singled out in POLARIS's Primary/Secondary list. This is not a direct contradiction — POLARIS's list is a short, deliberately curated selection rather than an exhaustive one, and no case was found anywhere in the compendium of a POLARIS-Primary symbol being *absent* from a substantial Marr Aspects sample. Read it as an emphasis gap, not a disagreement about relevance.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Sun | Primary | 1 · 6/30 combos | Strong emphasis | 2 · 41/72 charts (57%) | 4/4 | 30 / 72 | 8 | Strong Symbol |
| Saturn | Primary | 1 · 8/30 combos | Strong emphasis | 2 · 62/72 charts (86%) | 4/4 | 30 / 72 | 8 | Strong Symbol |
| Ascendant (1st House cusp) | Primary | 1 · 5/30 combos | Mentioned | 2 · 43/72 charts (60%) | 4/4 | 30 / 72 | 8 | Strong Symbol |
| Moon | Secondary | 1 · 4/30 combos | Absent | 2 · 38/72 charts (53%) | 3/4 | 30 / 72 | 6 | Moderate (Relevant Symbol) |
| Mars | Secondary | 1 · 8/30 combos | Absent | 2 · 44/72 charts (61%) | 3/4 | 30 / 72 | 6 | Moderate (Relevant Symbol) |
| Uranus | Secondary | 1 · 2/30 combos | Absent | 2 · 49/72 charts (68%) | 3/4 | 30 / 72 | 6 | Moderate (Relevant Symbol) |
| Neptune | Primary | 1 · 8/30 combos | Absent | 2 · 42/72 charts (58%) | 3/4 | 30 / 72 | 6 | Moderate (Relevant Symbol) |
| Pluto | Primary | 1 · 8/30 combos | Absent | 2 · 30/72 charts (42%) | 3/4 | 30 / 72 | 6 | Moderate (Relevant Symbol) |
| Midheaven (10th House cusp) | Primary | 1 · 5/30 combos | Absent | 1 · 19/72 charts (26%) | 3/4 | 30 / 72 | 6 | Moderate (Relevant Symbol) |
| Lunar Node (North/South/unspecified) | Primary | 1 · 4/30 combos | Absent | 1 · 16/72 charts (22%) | 3/4 | 30 / 72 | 6 | Moderate (Relevant Symbol) |
| Imum Coeli (4th House cusp) | Absent | — (out of scope) | Strong emphasis | 2 · 51/72 charts (71%) | 2/3 | 30 / 72 | 6 | Moderate (Relevant Symbol) |
| 8th House cusp | Primary | — (out of scope) | Absent | 1 · 17/72 charts (24%) | 2/3 | 30 / 72 | 6 | Moderate (Relevant Symbol) |
| 12th House cusp | Secondary | — (out of scope) | Absent | 2 · 31/72 charts (43%) | 2/3 | 30 / 72 | 6 | Moderate (Relevant Symbol) |
| Part of Fortune | — (out of scope) | 1 · 1/30 combos | Absent | 1 · 12/72 charts (17%) | 2/3 | 30 / 72 | 4 | Weak (Occasional Symbol) |
| Mercury | Absent | 1 · 1/30 combos | Absent | 1 · 22/72 charts (31%) | 2/4 | 30 / 72 | 2 | Very Weak (Speculative Symbol) |
| Venus | Absent | 0 · 0/30 combos | Absent | 1 · 10/72 charts (14%) | 1/4 | 30 / 72 | 2 | Very Weak (Speculative Symbol) |
| Jupiter | Absent | 0 · 0/30 combos | Absent | 1 · 12/72 charts (17%) | 1/4 | 30 / 72 | 2 | Very Weak (Speculative Symbol) |
| Descendant (7th House cusp) | Absent | — (out of scope) | Absent | 1 · 12/72 charts (17%) | 1/3 | 30 / 72 | 2 | Very Weak (Speculative Symbol) |
| 2nd House cusp | Absent | — (out of scope) | Absent | 1 · 1/72 charts (1%) | 1/3 | 30 / 72 | 2 | Very Weak (Speculative Symbol) |
| 3rd House cusp | Absent | — (out of scope) | Absent | 1 · 5/72 charts (7%) | 1/3 | 30 / 72 | 2 | Very Weak (Speculative Symbol) |
| 5th House cusp | Absent | — (out of scope) | Absent | 1 · 1/72 charts (1%) | 1/3 | 30 / 72 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | Absent | 1 · 3/72 charts (4%) | 1/3 | 30 / 72 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 7/72 charts (10%) | 1/3 | 30 / 72 | 2 | Very Weak (Speculative Symbol) |

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Sun**: tier_score = 8 (n_juan_combos_total=30, n_marr_examples_total=72)  |  **8th House cusp**: tier_score = 6 (n_juan_combos_total=30, n_marr_examples_total=72) — *looked up independently; no combined score is produced for this pairing.*
- **Sun**: tier_score = 8 (n_juan_combos_total=30, n_marr_examples_total=72)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=30, n_marr_examples_total=72) — *looked up independently; no combined score is produced for this pairing.*
- **Saturn**: tier_score = 8 (n_juan_combos_total=30, n_marr_examples_total=72)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=30, n_marr_examples_total=72) — *looked up independently; no combined score is produced for this pairing.*
- **8th House cusp**: tier_score = 6 (n_juan_combos_total=30, n_marr_examples_total=72)  |  **12th House cusp**: tier_score = 6 (n_juan_combos_total=30, n_marr_examples_total=72) — *looked up independently; no combined score is produced for this pairing.*

---

## 28. Assasination or Suicide

*Category: Death — violent or self-inflicted*

### 1. Event Overview

A violent or self-inflicted death. This is one of the thinner entries in the compendium: both Juan Combos and Alexander Marr's short-form commentary record no data, leaving POLARIS and the worked examples as the only evidentiary base.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Mars, Saturn, Uranus, Neptune, Pluto, Moon
- Houses/Angles mentioned: Ascendant (1st House cusp), Midheaven (10th House cusp), 8th House cusp, 12th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Mars, Saturn, Uranus, Neptune, Pluto, Ascendant (1st House cusp), Midheaven (10th House cusp), 8th House cusp, North Node (Ascending)
- **Secondary**: Moon, 12th House cusp
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- *No data available from this source* (the compendium explicitly marks this entry “None”).

**Other (Alexander Marr — short-form notes)**
- *No data available from this source* (the compendium explicitly marks this entry “None”).

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **6 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- **Low sample size:** only 6 worked examples available for this event in total — frequencies quoted below (and the corresponding tier_score contributions) are drawn from a very small pool and should be read as suggestive rather than well-established (see `n_marr_examples_total` on each symbol record).
- Most frequent points: Mars (6/6, 100%), Moon (5/6, 83%), Neptune (4/6, 67%), Uranus (4/6, 67%), Imum Coeli (4th House cusp) (4/6, 67%), Ascendant (1st House cusp) (4/6, 67%), Sun (3/6, 50%), Saturn (3/6, 50%)
- Node detail: North Node in 0, South Node in 0, unspecified-pole Node in 1 of 6 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- **Mars** — supported by POLARIS, Marr Aspects (score 10/10)
- **Uranus** — supported by POLARIS, Marr Aspects (score 10/10)
- **Neptune** — supported by POLARIS, Marr Aspects (score 10/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Marr Aspects (score 10/10)

**Secondary Symbols**
- **Moon** — supported by POLARIS, Marr Aspects (score 8/10)
- **Saturn** — supported by POLARIS, Marr Aspects (score 8/10)
- **Pluto** — supported by POLARIS, Marr Aspects (score 8/10)
- **8th House cusp** — supported by POLARIS, Marr Aspects (score 8/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Marr Aspects (score 8/10)
- **Midheaven (10th House cusp)** — supported by POLARIS (score 6/10)
- **Imum Coeli (4th House cusp)** — supported by Marr Aspects (score 6/10)
- **Part of Fortune** — supported by Marr Aspects (score 6/10)

**Occasional Symbols**
- **Sun** — supported by Marr Aspects (score 2/10)
- **Jupiter** — supported by Marr Aspects (score 2/10)
- **Mercury** — supported by Marr Aspects (score 2/10)
- **Venus** — supported by Marr Aspects (score 2/10)
- **Descendant (7th House cusp)** — supported by Marr Aspects (score 2/10)
- **3rd House cusp** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **12th House cusp** — supported by POLARIS (score 2/10)

### 4. Consensus Analysis

Supported by exactly two sources (moderate confidence): Moon, Mars, Saturn, Uranus, Neptune, Pluto, Ascendant (1st House cusp), 8th House cusp, Lunar Node (North/South/unspecified). All of these are marked † in the table below: for each, only two sources could address the point at all (the other two are structurally out of scope for this event), and those two agree — a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

**Speculative / source-specific symbolism.** Sun (Marr Aspects only), Mercury (Marr Aspects only), Venus (Marr Aspects only), Jupiter (Marr Aspects only), Midheaven (10th House cusp) (POLARIS only), Descendant (7th House cusp) (Marr Aspects only), Imum Coeli (4th House cusp) (Marr Aspects only), 3rd House cusp (Marr Aspects only), 9th House cusp (Marr Aspects only), 12th House cusp (POLARIS only), Part of Fortune (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** No clear-cut contradictions were found for this event: the four sources differ in *emphasis* and *coverage* (which is discussed above) rather than making opposing claims about any single symbol.

**Incomplete information.** Juan Combos (marked “None”), Other (marked “None”) contribute no data to this event; the consolidated picture above rests on the remaining source(s) only.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Mars | Primary | — (out of scope) | — (no data) | 2 · 6/6 charts (100%) | 2/2 † | 0 / 6 | 10 | Very Strong (Core Symbol) |
| Uranus | Primary | — (out of scope) | — (no data) | 2 · 4/6 charts (67%) | 2/2 † | 0 / 6 | 10 | Very Strong (Core Symbol) |
| Neptune | Primary | — (out of scope) | — (no data) | 2 · 4/6 charts (67%) | 2/2 † | 0 / 6 | 10 | Very Strong (Core Symbol) |
| Ascendant (1st House cusp) | Primary | — (out of scope) | — (no data) | 2 · 4/6 charts (67%) | 2/2 † | 0 / 6 | 10 | Very Strong (Core Symbol) |
| Moon | Secondary | — (out of scope) | — (no data) | 2 · 5/6 charts (83%) | 2/2 † | 0 / 6 | 8 | Strong Symbol |
| Saturn | Primary | — (out of scope) | — (no data) | 1 · 3/6 charts (50%) | 2/2 † | 0 / 6 | 8 | Strong Symbol |
| Pluto | Primary | — (out of scope) | — (no data) | 1 · 1/6 charts (17%) | 2/2 † | 0 / 6 | 8 | Strong Symbol |
| 8th House cusp | Primary | — (out of scope) | — (no data) | 1 · 2/6 charts (33%) | 2/2 † | 0 / 6 | 8 | Strong Symbol |
| Lunar Node (North/South/unspecified) | Primary | — (out of scope) | — (no data) | 1 · 1/6 charts (17%) | 2/2 † | 0 / 6 | 8 | Strong Symbol |
| Midheaven (10th House cusp) | Primary | — (out of scope) | — (no data) | 0 · 0/6 charts (0%) | 1/2 | 0 / 6 | 6 | Moderate (Relevant Symbol) |
| Imum Coeli (4th House cusp) | Absent | — (out of scope) | — (no data) | 2 · 4/6 charts (67%) | 1/2 | 0 / 6 | 6 | Moderate (Relevant Symbol) |
| Part of Fortune | — (out of scope) | — (out of scope) | — (no data) | 1 · 1/6 charts (17%) | 1/1 † | 0 / 6 | 6 | Moderate (Relevant Symbol) |
| Sun | Absent | — (out of scope) | — (no data) | 1 · 3/6 charts (50%) | 1/2 | 0 / 6 | 2 | Very Weak (Speculative Symbol) |
| Jupiter | Absent | — (out of scope) | — (no data) | 1 · 3/6 charts (50%) | 1/2 | 0 / 6 | 2 | Very Weak (Speculative Symbol) |
| Mercury | Absent | — (out of scope) | — (no data) | 1 · 1/6 charts (17%) | 1/2 | 0 / 6 | 2 | Very Weak (Speculative Symbol) |
| Venus | Absent | — (out of scope) | — (no data) | 1 · 2/6 charts (33%) | 1/2 | 0 / 6 | 2 | Very Weak (Speculative Symbol) |
| Descendant (7th House cusp) | Absent | — (out of scope) | — (no data) | 1 · 2/6 charts (33%) | 1/2 | 0 / 6 | 2 | Very Weak (Speculative Symbol) |
| 3rd House cusp | Absent | — (out of scope) | — (no data) | 1 · 2/6 charts (33%) | 1/2 | 0 / 6 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | — (no data) | 1 · 1/6 charts (17%) | 1/2 | 0 / 6 | 2 | Very Weak (Speculative Symbol) |
| 12th House cusp | Secondary | — (out of scope) | — (no data) | 0 · 0/6 charts (0%) | 1/2 | 0 / 6 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Mars**: tier_score = 10 (n_juan_combos_total=0, n_marr_examples_total=6)  |  **Imum Coeli (4th House cusp)**: tier_score = 6 (n_juan_combos_total=0, n_marr_examples_total=6) — *looked up independently; no combined score is produced for this pairing.*
- **Mars**: tier_score = 10 (n_juan_combos_total=0, n_marr_examples_total=6)  |  **12th House cusp**: tier_score = 2 (n_juan_combos_total=0, n_marr_examples_total=6) — *looked up independently; no combined score is produced for this pairing.*
- **Uranus**: tier_score = 10 (n_juan_combos_total=0, n_marr_examples_total=6)  |  **12th House cusp**: tier_score = 2 (n_juan_combos_total=0, n_marr_examples_total=6) — *looked up independently; no combined score is produced for this pairing.*
- **Imum Coeli (4th House cusp)**: tier_score = 6 (n_juan_combos_total=0, n_marr_examples_total=6)  |  **Part of Fortune**: tier_score = 6 (n_juan_combos_total=0, n_marr_examples_total=6) — *looked up independently; no combined score is produced for this pairing.*

---

## 29. Failure or Defeat

*Category: Adversity — setback, disgrace, loss of standing*

### 1. Event Overview

The compendium's broadest adversity category, bundling together death sentences, executions, demotions, depression, hunger strikes, scandal and theft under one heading. Saturn is the connecting thread across nearly all of these sub-types, typically afflicting the Ascendant or Midheaven.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Sun, Mars, Saturn, Neptune, Moon, Mercury, Uranus, Pluto
- Houses/Angles mentioned: Ascendant (1st House cusp), Midheaven (10th House cusp), 3rd House cusp, 12th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Sun, Mars, Saturn, Neptune, Ascendant (1st House cusp), Midheaven (10th House cusp), 3rd House cusp, North Node (Ascending)
- **Secondary**: Moon, Mercury, Uranus, Pluto, 12th House cusp
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Mars (13/72), Saturn (13/72), Neptune (13/72), Pluto (12/72), Lunar Node (pole unspecified) (12/72), Sun (11/72), Moon (11/72), Ascendant (1st House cusp) (10/72), Uranus (10/72), Midheaven (10th House cusp) (10/72)
- Total pairwise combinations catalogued for this event: 72
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: The compendium's broadest adversity category, bundling together death sentences, executions, demotions, depression, hunger strikes, scandal and theft under one heading. Saturn is the connecting thread across nearly all of these sub-types, typically afflicting the Ascendant or Midheaven.
- Points referenced: Mercury (strong), Neptune (strong), Ascendant (1st House cusp) (strong), Midheaven (10th House cusp) (strong), 5th House cusp (strong), 12th House cusp (strong), Sun (mentioned), Moon (mentioned), Mars (mentioned), Jupiter (mentioned), Saturn (mentioned), Pluto (mentioned), 2nd House cusp (mentioned)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **79 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Saturn (55/79, 70%), Mars (54/79, 68%), Midheaven (10th House cusp) (53/79, 67%), Sun (48/79, 61%), Neptune (45/79, 57%), Ascendant (1st House cusp) (44/79, 56%), Uranus (40/79, 51%), Moon (39/79, 49%)
- Node detail: North Node in 6, South Node in 10, unspecified-pole Node in 5 of 79 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Sun** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Mercury** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Mars** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Saturn** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Neptune** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Midheaven (10th House cusp)** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Moon** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 6/10)
- **Pluto** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 6/10)
- **Uranus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **12th House cusp** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **3rd House cusp** — supported by POLARIS, Marr Aspects (score 6/10)
- **5th House cusp** — supported by Other, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Jupiter** — supported by Juan Combos, Other, Marr Aspects (score 4/10)
- **2nd House cusp** — supported by Other, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Venus** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Descendant (7th House cusp)** — supported by Marr Aspects (score 2/10)
- **Imum Coeli (4th House cusp)** — supported by Marr Aspects (score 2/10)
- **6th House cusp** — supported by Marr Aspects (score 2/10)
- **8th House cusp** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Sun, Moon, Mercury, Mars, Saturn, Neptune, Pluto, Ascendant (1st House cusp), Midheaven (10th House cusp) are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Jupiter, Uranus, 12th House cusp, Lunar Node (North/South/unspecified) are supported by three of the four sources. 1 of these (12th House cusp) sits at the structural ceiling for its symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Venus, 2nd House cusp, 3rd House cusp, 5th House cusp, Part of Fortune.

**Speculative / source-specific symbolism.** Descendant (7th House cusp) (Marr Aspects only), Imum Coeli (4th House cusp) (Marr Aspects only), 6th House cusp (Marr Aspects only), 8th House cusp (Marr Aspects only), 9th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** No clear-cut contradictions were found for this event: the four sources differ in *emphasis* and *coverage* (which is discussed above) rather than making opposing claims about any single symbol.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Sun | Primary | 1 · 11/72 combos | Mentioned | 2 · 48/79 charts (61%) | 4/4 | 72 / 79 | 8 | Strong Symbol |
| Mercury | Secondary | 1 · 9/72 combos | Strong emphasis | 2 · 39/79 charts (49%) | 4/4 | 72 / 79 | 8 | Strong Symbol |
| Mars | Primary | 1 · 13/72 combos | Mentioned | 2 · 54/79 charts (68%) | 4/4 | 72 / 79 | 8 | Strong Symbol |
| Saturn | Primary | 1 · 13/72 combos | Mentioned | 2 · 55/79 charts (70%) | 4/4 | 72 / 79 | 8 | Strong Symbol |
| Neptune | Primary | 1 · 13/72 combos | Strong emphasis | 2 · 45/79 charts (57%) | 4/4 | 72 / 79 | 8 | Strong Symbol |
| Ascendant (1st House cusp) | Primary | 1 · 10/72 combos | Strong emphasis | 2 · 44/79 charts (56%) | 4/4 | 72 / 79 | 8 | Strong Symbol |
| Midheaven (10th House cusp) | Primary | 1 · 10/72 combos | Strong emphasis | 2 · 53/79 charts (67%) | 4/4 | 72 / 79 | 8 | Strong Symbol |
| Moon | Secondary | 1 · 11/72 combos | Mentioned | 2 · 39/79 charts (49%) | 4/4 | 72 / 79 | 6 | Moderate (Relevant Symbol) |
| Pluto | Secondary | 1 · 12/72 combos | Mentioned | 2 · 34/79 charts (43%) | 4/4 | 72 / 79 | 6 | Moderate (Relevant Symbol) |
| Uranus | Secondary | 1 · 10/72 combos | Absent | 2 · 40/79 charts (51%) | 3/4 | 72 / 79 | 6 | Moderate (Relevant Symbol) |
| 12th House cusp | Secondary | — (out of scope) | Strong emphasis | 1 · 28/79 charts (35%) | 3/3 † | 72 / 79 | 6 | Moderate (Relevant Symbol) |
| Lunar Node (North/South/unspecified) | Primary | 1 · 12/72 combos | Absent | 1 · 21/79 charts (27%) | 3/4 | 72 / 79 | 6 | Moderate (Relevant Symbol) |
| 3rd House cusp | Primary | — (out of scope) | Absent | 1 · 29/79 charts (37%) | 2/3 | 72 / 79 | 6 | Moderate (Relevant Symbol) |
| 5th House cusp | Absent | — (out of scope) | Strong emphasis | 1 · 4/79 charts (5%) | 2/3 | 72 / 79 | 6 | Moderate (Relevant Symbol) |
| Jupiter | Absent | 1 · 4/72 combos | Mentioned | 1 · 22/79 charts (28%) | 3/4 | 72 / 79 | 4 | Weak (Occasional Symbol) |
| 2nd House cusp | Absent | — (out of scope) | Mentioned | 1 · 2/79 charts (3%) | 2/3 | 72 / 79 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 8/72 combos | Absent | 1 · 16/79 charts (20%) | 2/3 | 72 / 79 | 4 | Weak (Occasional Symbol) |
| Venus | Absent | 1 · 8/72 combos | Absent | 1 · 23/79 charts (29%) | 2/4 | 72 / 79 | 2 | Very Weak (Speculative Symbol) |
| Descendant (7th House cusp) | Absent | — (out of scope) | Absent | 1 · 10/79 charts (13%) | 1/3 | 72 / 79 | 2 | Very Weak (Speculative Symbol) |
| Imum Coeli (4th House cusp) | Absent | — (out of scope) | Absent | 1 · 3/79 charts (4%) | 1/3 | 72 / 79 | 2 | Very Weak (Speculative Symbol) |
| 6th House cusp | Absent | — (out of scope) | Absent | 1 · 4/79 charts (5%) | 1/3 | 72 / 79 | 2 | Very Weak (Speculative Symbol) |
| 8th House cusp | Absent | — (out of scope) | Absent | 1 · 5/79 charts (6%) | 1/3 | 72 / 79 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | Absent | 1 · 10/79 charts (13%) | 1/3 | 72 / 79 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 7/79 charts (9%) | 1/3 | 72 / 79 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Sun**: tier_score = 8 (n_juan_combos_total=72, n_marr_examples_total=79)  |  **3rd House cusp**: tier_score = 6 (n_juan_combos_total=72, n_marr_examples_total=79) — *looked up independently; no combined score is produced for this pairing.*
- **Sun**: tier_score = 8 (n_juan_combos_total=72, n_marr_examples_total=79)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=72, n_marr_examples_total=79) — *looked up independently; no combined score is produced for this pairing.*
- **Mercury**: tier_score = 8 (n_juan_combos_total=72, n_marr_examples_total=79)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=72, n_marr_examples_total=79) — *looked up independently; no combined score is produced for this pairing.*
- **3rd House cusp**: tier_score = 6 (n_juan_combos_total=72, n_marr_examples_total=79)  |  **5th House cusp**: tier_score = 6 (n_juan_combos_total=72, n_marr_examples_total=79) — *looked up independently; no combined score is produced for this pairing.*

---

## 30. Arrest

*Category: Legal — imprisonment / confinement*

### 1. Event Overview

Imprisonment specifically. The 12th house cusp (or Ascendant) is the core signature; Uranus colors a sudden arrest and Saturn a long or drawn-out confinement.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Mars, Saturn, Uranus, Neptune, Pluto, Sun, Mercury
- Houses/Angles mentioned: Ascendant (1st House cusp), Midheaven (10th House cusp), 12th House cusp, 3rd House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Mars, Saturn, Uranus, Neptune, Pluto, Ascendant (1st House cusp), Midheaven (10th House cusp), 12th House cusp, North Node (Ascending)
- **Secondary**: Sun, Mercury, 3rd House cusp
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Mars (4/8), Jupiter (3/8), Neptune (2/8), Lunar Node (pole unspecified) (2/8), Saturn (1/8), Ascendant (1st House cusp) (1/8), Sun (1/8), Uranus (1/8), Pluto (1/8)
- Total pairwise combinations catalogued for this event: 8
- **Low sample size:** only 8 combinations catalogued for this event in total — any single symbol's Juan Combos percentage here rests on very little underlying data, and the tier_score for symbols resting mainly on this source should be read with that in mind (see `n_juan_combos_total` on each symbol record).
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: Imprisonment specifically. The 12th house cusp (or Ascendant) is the core signature; Uranus colors a sudden arrest and Saturn a long or drawn-out confinement.
- Points referenced: Saturn (mentioned), Uranus (mentioned), Ascendant (1st House cusp) (mentioned), 12th House cusp (mentioned)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **18 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Saturn (15/18, 83%), Sun (13/18, 72%), Mars (12/18, 67%), 12th House cusp (12/18, 67%), Ascendant (1st House cusp) (11/18, 61%), Moon (10/18, 56%), Mercury (10/18, 56%), Midheaven (10th House cusp) (9/18, 50%)
- Node detail: North Node in 0, South Node in 1, unspecified-pole Node in 1 of 18 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Saturn** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Uranus** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **12th House cusp** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **Sun** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Mars** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Neptune** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Pluto** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Midheaven (10th House cusp)** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Mercury** — supported by POLARIS, Marr Aspects (score 4/10)
- **3rd House cusp** — supported by POLARIS, Marr Aspects (score 4/10)
- **Jupiter** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Moon** — supported by Marr Aspects (score 2/10)
- **Venus** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)
- **Part of Fortune** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Saturn, Uranus, Ascendant (1st House cusp) are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Sun, Mars, Neptune, Pluto, 12th House cusp, Lunar Node (North/South/unspecified) are supported by three of the four sources. 1 of these (12th House cusp) sits at the structural ceiling for its symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Mercury, Jupiter, Midheaven (10th House cusp), 3rd House cusp.

**Speculative / source-specific symbolism.** Moon (Marr Aspects only), Venus (Marr Aspects only), 9th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only), Part of Fortune (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** Moon (in 10/18 example charts, 56%) recur in a substantial share of Marr's worked examples without being singled out in POLARIS's Primary/Secondary list. This is not a direct contradiction — POLARIS's list is a short, deliberately curated selection rather than an exhaustive one, and no case was found anywhere in the compendium of a POLARIS-Primary symbol being *absent* from a substantial Marr Aspects sample. Read it as an emphasis gap, not a disagreement about relevance.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Saturn | Primary | 1 · 1/8 combos | Mentioned | 2 · 15/18 charts (83%) | 4/4 | 8 / 18 | 8 | Strong Symbol |
| Uranus | Primary | 1 · 1/8 combos | Mentioned | 2 · 9/18 charts (50%) | 4/4 | 8 / 18 | 8 | Strong Symbol |
| Ascendant (1st House cusp) | Primary | 1 · 1/8 combos | Mentioned | 2 · 11/18 charts (61%) | 4/4 | 8 / 18 | 8 | Strong Symbol |
| 12th House cusp | Primary | — (out of scope) | Mentioned | 2 · 12/18 charts (67%) | 3/3 † | 8 / 18 | 8 | Strong Symbol |
| Sun | Secondary | 1 · 1/8 combos | Absent | 2 · 13/18 charts (72%) | 3/4 | 8 / 18 | 6 | Moderate (Relevant Symbol) |
| Mars | Primary | 1 · 4/8 combos | Absent | 2 · 12/18 charts (67%) | 3/4 | 8 / 18 | 6 | Moderate (Relevant Symbol) |
| Neptune | Primary | 1 · 2/8 combos | Absent | 1 · 8/18 charts (44%) | 3/4 | 8 / 18 | 6 | Moderate (Relevant Symbol) |
| Pluto | Primary | 1 · 1/8 combos | Absent | 1 · 8/18 charts (44%) | 3/4 | 8 / 18 | 6 | Moderate (Relevant Symbol) |
| Lunar Node (North/South/unspecified) | Primary | 1 · 2/8 combos | Absent | 1 · 2/18 charts (11%) | 3/4 | 8 / 18 | 6 | Moderate (Relevant Symbol) |
| Midheaven (10th House cusp) | Primary | 0 · 0/8 combos | Absent | 2 · 9/18 charts (50%) | 2/4 | 8 / 18 | 6 | Moderate (Relevant Symbol) |
| Mercury | Secondary | 0 · 0/8 combos | Absent | 2 · 10/18 charts (56%) | 2/4 | 8 / 18 | 4 | Weak (Occasional Symbol) |
| 3rd House cusp | Secondary | — (out of scope) | Absent | 1 · 3/18 charts (17%) | 2/3 | 8 / 18 | 4 | Weak (Occasional Symbol) |
| Jupiter | Absent | 1 · 3/8 combos | Absent | 1 · 6/18 charts (33%) | 2/4 | 8 / 18 | 2 | Very Weak (Speculative Symbol) |
| Moon | Absent | 0 · 0/8 combos | Absent | 2 · 10/18 charts (56%) | 1/4 | 8 / 18 | 2 | Very Weak (Speculative Symbol) |
| Venus | Absent | 0 · 0/8 combos | Absent | 1 · 5/18 charts (28%) | 1/4 | 8 / 18 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | Absent | 1 · 5/18 charts (28%) | 1/3 | 8 / 18 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 2/18 charts (11%) | 1/3 | 8 / 18 | 2 | Very Weak (Speculative Symbol) |
| Part of Fortune | — (out of scope) | 0 · 0/8 combos | Absent | 1 · 3/18 charts (17%) | 1/3 | 8 / 18 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Saturn**: tier_score = 8 (n_juan_combos_total=8, n_marr_examples_total=18)  |  **Midheaven (10th House cusp)**: tier_score = 6 (n_juan_combos_total=8, n_marr_examples_total=18) — *looked up independently; no combined score is produced for this pairing.*
- **Saturn**: tier_score = 8 (n_juan_combos_total=8, n_marr_examples_total=18)  |  **Part of Fortune**: tier_score = 2 (n_juan_combos_total=8, n_marr_examples_total=18) — *looked up independently; no combined score is produced for this pairing.*
- **Uranus**: tier_score = 8 (n_juan_combos_total=8, n_marr_examples_total=18)  |  **Part of Fortune**: tier_score = 2 (n_juan_combos_total=8, n_marr_examples_total=18) — *looked up independently; no combined score is produced for this pairing.*
- **Midheaven (10th House cusp)**: tier_score = 6 (n_juan_combos_total=8, n_marr_examples_total=18)  |  **Mercury**: tier_score = 4 (n_juan_combos_total=8, n_marr_examples_total=18) — *looked up independently; no combined score is produced for this pairing.*

---

## 31. Losses

*Category: Material — financial setback*

### 1. Event Overview

Monetary loss through speculation, bankruptcy or theft. Uranus features in speculative losses, Neptune and Mercury in bankruptcy, and Mars or Neptune in theft — typically expressed through the 2nd house cusp or the angles.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Mercury, Mars, Saturn, Uranus, Neptune, Pluto
- Houses/Angles mentioned: Ascendant (1st House cusp), Midheaven (10th House cusp), 2nd House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Mercury, Mars, Saturn, Uranus, Neptune, Ascendant (1st House cusp), Midheaven (10th House cusp), 2nd House cusp
- **Secondary**: Pluto, North Node (Ascending)
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Venus (3/4), Neptune (1/4), Sun (1/4), Uranus (1/4), Pluto (1/4), Saturn (1/4)
- Total pairwise combinations catalogued for this event: 4
- **Low sample size:** only 4 combinations catalogued for this event in total — any single symbol's Juan Combos percentage here rests on very little underlying data, and the tier_score for symbols resting mainly on this source should be read with that in mind (see `n_juan_combos_total` on each symbol record).
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: Monetary loss through speculation, bankruptcy or theft. Uranus features in speculative losses, Neptune and Mercury in bankruptcy, and Mars or Neptune in theft — typically expressed through the 2nd house cusp or the angles.
- Points referenced: Mercury (mentioned), Mars (mentioned), Uranus (mentioned), Neptune (mentioned), Ascendant (1st House cusp) (mentioned), Midheaven (10th House cusp) (mentioned), 2nd House cusp (mentioned), 5th House cusp (mentioned)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **10 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Uranus (9/10, 90%), Saturn (7/10, 70%), 12th House cusp (7/10, 70%), Sun (7/10, 70%), Neptune (6/10, 60%), Pluto (6/10, 60%), 2nd House cusp (6/10, 60%), Mars (6/10, 60%)
- Node detail: North Node in 0, South Node in 1, unspecified-pole Node in 1 of 10 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Uranus** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Neptune** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **2nd House cusp** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **Mercury** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **Mars** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **Saturn** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Pluto** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **Midheaven (10th House cusp)** — supported by POLARIS, Other, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Sun** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Venus** — supported by Juan Combos, Marr Aspects (score 4/10)
- **12th House cusp** — supported by Marr Aspects (score 4/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Marr Aspects (score 2/10)
- **Moon** — supported by Marr Aspects (score 2/10)
- **Jupiter** — supported by Marr Aspects (score 2/10)
- **3rd House cusp** — supported by Marr Aspects (score 2/10)
- **Imum Coeli (4th House cusp)** — supported by Marr Aspects (score 2/10)
- **5th House cusp** — supported by Other (score 2/10)
- **6th House cusp** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)
- **Part of Fortune** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Uranus, Neptune are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Mercury, Mars, Saturn, Pluto, Ascendant (1st House cusp), Midheaven (10th House cusp), 2nd House cusp are supported by three of the four sources. 1 of these (2nd House cusp) sits at the structural ceiling for its symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Sun, Venus, Lunar Node (North/South/unspecified).

**Speculative / source-specific symbolism.** Moon (Marr Aspects only), Jupiter (Marr Aspects only), Imum Coeli (4th House cusp) (Marr Aspects only), 3rd House cusp (Marr Aspects only), 5th House cusp (Other only), 6th House cusp (Marr Aspects only), 9th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only), 12th House cusp (Marr Aspects only), Part of Fortune (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** Sun (in 7/10 example charts, 70%), 12th House cusp (in 7/10 example charts, 70%) recur in a substantial share of Marr's worked examples without being singled out in POLARIS's Primary/Secondary list. This is not a direct contradiction — POLARIS's list is a short, deliberately curated selection rather than an exhaustive one, and no case was found anywhere in the compendium of a POLARIS-Primary symbol being *absent* from a substantial Marr Aspects sample. Read it as an emphasis gap, not a disagreement about relevance.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Uranus | Primary | 1 · 1/4 combos | Mentioned | 2 · 9/10 charts (90%) | 4/4 | 4 / 10 | 8 | Strong Symbol |
| Neptune | Primary | 1 · 1/4 combos | Mentioned | 2 · 6/10 charts (60%) | 4/4 | 4 / 10 | 8 | Strong Symbol |
| 2nd House cusp | Primary | — (out of scope) | Mentioned | 2 · 6/10 charts (60%) | 3/3 † | 4 / 10 | 8 | Strong Symbol |
| Mercury | Primary | 0 · 0/4 combos | Mentioned | 1 · 5/10 charts (50%) | 3/4 | 4 / 10 | 6 | Moderate (Relevant Symbol) |
| Mars | Primary | 0 · 0/4 combos | Mentioned | 2 · 6/10 charts (60%) | 3/4 | 4 / 10 | 6 | Moderate (Relevant Symbol) |
| Saturn | Primary | 1 · 1/4 combos | Absent | 2 · 7/10 charts (70%) | 3/4 | 4 / 10 | 6 | Moderate (Relevant Symbol) |
| Pluto | Secondary | 1 · 1/4 combos | Absent | 2 · 6/10 charts (60%) | 3/4 | 4 / 10 | 6 | Moderate (Relevant Symbol) |
| Ascendant (1st House cusp) | Primary | 0 · 0/4 combos | Mentioned | 1 · 5/10 charts (50%) | 3/4 | 4 / 10 | 6 | Moderate (Relevant Symbol) |
| Midheaven (10th House cusp) | Primary | 0 · 0/4 combos | Mentioned | 1 · 5/10 charts (50%) | 3/4 | 4 / 10 | 6 | Moderate (Relevant Symbol) |
| Sun | Absent | 1 · 1/4 combos | Absent | 2 · 7/10 charts (70%) | 2/4 | 4 / 10 | 4 | Weak (Occasional Symbol) |
| Venus | Absent | 2 · 3/4 combos | Absent | 1 · 2/10 charts (20%) | 2/4 | 4 / 10 | 4 | Weak (Occasional Symbol) |
| 12th House cusp | Absent | — (out of scope) | Absent | 2 · 7/10 charts (70%) | 1/3 | 4 / 10 | 4 | Weak (Occasional Symbol) |
| Lunar Node (North/South/unspecified) | Secondary | 0 · 0/4 combos | Absent | 1 · 2/10 charts (20%) | 2/4 | 4 / 10 | 2 | Very Weak (Speculative Symbol) |
| Moon | Absent | 0 · 0/4 combos | Absent | 1 · 4/10 charts (40%) | 1/4 | 4 / 10 | 2 | Very Weak (Speculative Symbol) |
| Jupiter | Absent | 0 · 0/4 combos | Absent | 1 · 4/10 charts (40%) | 1/4 | 4 / 10 | 2 | Very Weak (Speculative Symbol) |
| 3rd House cusp | Absent | — (out of scope) | Absent | 1 · 4/10 charts (40%) | 1/3 | 4 / 10 | 2 | Very Weak (Speculative Symbol) |
| Imum Coeli (4th House cusp) | Absent | — (out of scope) | Absent | 1 · 1/10 charts (10%) | 1/3 | 4 / 10 | 2 | Very Weak (Speculative Symbol) |
| 5th House cusp | Absent | — (out of scope) | Mentioned | 0 · 0/10 charts (0%) | 1/3 | 4 / 10 | 2 | Very Weak (Speculative Symbol) |
| 6th House cusp | Absent | — (out of scope) | Absent | 1 · 1/10 charts (10%) | 1/3 | 4 / 10 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | Absent | 1 · 1/10 charts (10%) | 1/3 | 4 / 10 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 1/10 charts (10%) | 1/3 | 4 / 10 | 2 | Very Weak (Speculative Symbol) |
| Part of Fortune | — (out of scope) | 0 · 0/4 combos | Absent | 1 · 3/10 charts (30%) | 1/3 | 4 / 10 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Uranus**: tier_score = 8 (n_juan_combos_total=4, n_marr_examples_total=10)  |  **12th House cusp**: tier_score = 4 (n_juan_combos_total=4, n_marr_examples_total=10) — *looked up independently; no combined score is produced for this pairing.*
- **Uranus**: tier_score = 8 (n_juan_combos_total=4, n_marr_examples_total=10)  |  **Part of Fortune**: tier_score = 2 (n_juan_combos_total=4, n_marr_examples_total=10) — *looked up independently; no combined score is produced for this pairing.*
- **Neptune**: tier_score = 8 (n_juan_combos_total=4, n_marr_examples_total=10)  |  **Part of Fortune**: tier_score = 2 (n_juan_combos_total=4, n_marr_examples_total=10) — *looked up independently; no combined score is produced for this pairing.*
- **12th House cusp**: tier_score = 4 (n_juan_combos_total=4, n_marr_examples_total=10)  |  **Lunar Node (North/South/unspecified)**: tier_score = 2 (n_juan_combos_total=4, n_marr_examples_total=10) — *looked up independently; no combined score is produced for this pairing.*

---

## 32. Divorce or Separation

*Category: Relationship — rupture of partnership*

### 1. Event Overview

The separation preceding a divorce is marked by the Descendant afflicted by Mars or (if sudden) Uranus; an aspect from the Descendant to Jupiter is described as a frequent signature for the legal dimension of the divorce itself.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Mars, Saturn, Neptune, Pluto, Moon, Mercury, Venus, Uranus
- Houses/Angles mentioned: Descendant (7th House cusp), Imum Coeli (4th House cusp), 12th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Mars, Saturn, Neptune, Pluto, Descendant (7th House cusp), Imum Coeli (4th House cusp), North Node (Ascending)
- **Secondary**: Moon, Mercury, Venus, Uranus, 12th House cusp
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Saturn (9/29), Pluto (6/29), Neptune (6/29), Mars (6/29), Midheaven (10th House cusp) (5/29), Uranus (5/29), Lunar Node (pole unspecified) (5/29), Moon (4/29), Venus (4/29), Ascendant (1st House cusp) (2/29)
- Total pairwise combinations catalogued for this event: 29
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: The separation preceding a divorce is marked by the Descendant afflicted by Mars or (if sudden) Uranus; an aspect from the Descendant to Jupiter is described as a frequent signature for the legal dimension of the divorce itself.
- Points referenced: Mars (strong), Jupiter (strong), Uranus (strong), Ascendant (1st House cusp) (strong), Descendant (7th House cusp) (strong)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **19 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Sun (14/19, 74%), Saturn (14/19, 74%), Venus (13/19, 68%), Moon (13/19, 68%), Mars (13/19, 68%), Mercury (13/19, 68%), Descendant (7th House cusp) (12/19, 63%), Imum Coeli (4th House cusp) (12/19, 63%)
- Node detail: North Node in 0, South Node in 1, unspecified-pole Node in 4 of 19 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- **Descendant (7th House cusp)** — supported by POLARIS, Other, Marr Aspects (score 10/10)

**Secondary Symbols**
- **Mars** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Uranus** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Moon** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Mercury** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Venus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Jupiter** — supported by Juan Combos, Other, Marr Aspects (score 6/10)
- **Saturn** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Neptune** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Pluto** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Ascendant (1st House cusp)** — supported by Juan Combos, Other, Marr Aspects (score 6/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Imum Coeli (4th House cusp)** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Sun** — supported by Juan Combos, Marr Aspects (score 4/10)
- **12th House cusp** — supported by POLARIS, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Midheaven (10th House cusp)** — supported by Juan Combos, Marr Aspects (score 2/10)
- **5th House cusp** — supported by Marr Aspects (score 2/10)
- **2nd House cusp** — supported by Marr Aspects (score 2/10)
- **3rd House cusp** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Mars, Uranus are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Moon, Mercury, Venus, Jupiter, Saturn, Neptune, Pluto, Ascendant (1st House cusp), Descendant (7th House cusp), Lunar Node (North/South/unspecified) are supported by three of the four sources. 1 of these (Descendant (7th House cusp)) sits at the structural ceiling for its symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Sun, Midheaven (10th House cusp), Imum Coeli (4th House cusp), 12th House cusp, Part of Fortune.

**Speculative / source-specific symbolism.** 2nd House cusp (Marr Aspects only), 3rd House cusp (Marr Aspects only), 5th House cusp (Marr Aspects only), 9th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** Sun (in 14/19 example charts, 74%), Jupiter (in 10/19 example charts, 53%) recur in a substantial share of Marr's worked examples without being singled out in POLARIS's Primary/Secondary list. This is not a direct contradiction — POLARIS's list is a short, deliberately curated selection rather than an exhaustive one, and no case was found anywhere in the compendium of a POLARIS-Primary symbol being *absent* from a substantial Marr Aspects sample. Read it as an emphasis gap, not a disagreement about relevance.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Descendant (7th House cusp) | Primary | — (out of scope) | Strong emphasis | 2 · 12/19 charts (63%) | 3/3 † | 29 / 19 | 10 | Very Strong (Core Symbol) |
| Mars | Primary | 1 · 6/29 combos | Strong emphasis | 2 · 13/19 charts (68%) | 4/4 | 29 / 19 | 8 | Strong Symbol |
| Uranus | Secondary | 1 · 5/29 combos | Strong emphasis | 2 · 11/19 charts (58%) | 4/4 | 29 / 19 | 8 | Strong Symbol |
| Moon | Secondary | 1 · 4/29 combos | Absent | 2 · 13/19 charts (68%) | 3/4 | 29 / 19 | 6 | Moderate (Relevant Symbol) |
| Mercury | Secondary | 1 · 1/29 combos | Absent | 2 · 13/19 charts (68%) | 3/4 | 29 / 19 | 6 | Moderate (Relevant Symbol) |
| Venus | Secondary | 1 · 4/29 combos | Absent | 2 · 13/19 charts (68%) | 3/4 | 29 / 19 | 6 | Moderate (Relevant Symbol) |
| Jupiter | Absent | 1 · 2/29 combos | Strong emphasis | 2 · 10/19 charts (53%) | 3/4 | 29 / 19 | 6 | Moderate (Relevant Symbol) |
| Saturn | Primary | 1 · 9/29 combos | Absent | 2 · 14/19 charts (74%) | 3/4 | 29 / 19 | 6 | Moderate (Relevant Symbol) |
| Neptune | Primary | 1 · 6/29 combos | Absent | 1 · 5/19 charts (26%) | 3/4 | 29 / 19 | 6 | Moderate (Relevant Symbol) |
| Pluto | Primary | 1 · 6/29 combos | Absent | 2 · 11/19 charts (58%) | 3/4 | 29 / 19 | 6 | Moderate (Relevant Symbol) |
| Ascendant (1st House cusp) | Absent | 1 · 2/29 combos | Strong emphasis | 1 · 3/19 charts (16%) | 3/4 | 29 / 19 | 6 | Moderate (Relevant Symbol) |
| Lunar Node (North/South/unspecified) | Primary | 1 · 5/29 combos | Absent | 1 · 5/19 charts (26%) | 3/4 | 29 / 19 | 6 | Moderate (Relevant Symbol) |
| Imum Coeli (4th House cusp) | Primary | — (out of scope) | Absent | 2 · 12/19 charts (63%) | 2/3 | 29 / 19 | 6 | Moderate (Relevant Symbol) |
| Sun | Absent | 1 · 1/29 combos | Absent | 2 · 14/19 charts (74%) | 2/4 | 29 / 19 | 4 | Weak (Occasional Symbol) |
| 12th House cusp | Secondary | — (out of scope) | Absent | 1 · 6/19 charts (32%) | 2/3 | 29 / 19 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 2/29 combos | Absent | 1 · 1/19 charts (5%) | 2/3 | 29 / 19 | 4 | Weak (Occasional Symbol) |
| Midheaven (10th House cusp) | Absent | 1 · 5/29 combos | Absent | 1 · 6/19 charts (32%) | 2/4 | 29 / 19 | 2 | Very Weak (Speculative Symbol) |
| 5th House cusp | Absent | — (out of scope) | Absent | 1 · 7/19 charts (37%) | 1/3 | 29 / 19 | 2 | Very Weak (Speculative Symbol) |
| 2nd House cusp | Absent | — (out of scope) | Absent | 1 · 1/19 charts (5%) | 1/3 | 29 / 19 | 2 | Very Weak (Speculative Symbol) |
| 3rd House cusp | Absent | — (out of scope) | Absent | 1 · 4/19 charts (21%) | 1/3 | 29 / 19 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | Absent | 1 · 2/19 charts (11%) | 1/3 | 29 / 19 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 3/19 charts (16%) | 1/3 | 29 / 19 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Descendant (7th House cusp)**: tier_score = 10 (n_juan_combos_total=29, n_marr_examples_total=19)  |  **Lunar Node (North/South/unspecified)**: tier_score = 6 (n_juan_combos_total=29, n_marr_examples_total=19) — *looked up independently; no combined score is produced for this pairing.*
- **Descendant (7th House cusp)**: tier_score = 10 (n_juan_combos_total=29, n_marr_examples_total=19)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=29, n_marr_examples_total=19) — *looked up independently; no combined score is produced for this pairing.*
- **Mars**: tier_score = 8 (n_juan_combos_total=29, n_marr_examples_total=19)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=29, n_marr_examples_total=19) — *looked up independently; no combined score is produced for this pairing.*
- **Lunar Node (North/South/unspecified)**: tier_score = 6 (n_juan_combos_total=29, n_marr_examples_total=19)  |  **Imum Coeli (4th House cusp)**: tier_score = 6 (n_juan_combos_total=29, n_marr_examples_total=19) — *looked up independently; no combined score is produced for this pairing.*

---

## 33. Resign or Retire

*Category: Career — voluntary departure*

### 1. Event Overview

A voluntary departure from office or work. The Midheaven or Ascendant combined with Saturn (occasionally the Sun) is the stated signature — the same Saturn-angle pairing recurring across several career-ending categories.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Sun, Mars, Saturn, Neptune, Moon, Mercury, Uranus, Pluto
- Houses/Angles mentioned: Ascendant (1st House cusp), Midheaven (10th House cusp), 3rd House cusp, 12th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Sun, Mars, Saturn, Neptune, Ascendant (1st House cusp), Midheaven (10th House cusp), 3rd House cusp, 12th House cusp, North Node (Ascending)
- **Secondary**: Moon, Mercury, Uranus, Pluto
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Saturn (6/16), Neptune (6/16), Pluto (5/16), Midheaven (10th House cusp) (3/16), Uranus (3/16), Moon (2/16), Jupiter (2/16), Mars (2/16), Mercury (1/16), Venus (1/16)
- Total pairwise combinations catalogued for this event: 16
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: A voluntary departure from office or work. The Midheaven or Ascendant combined with Saturn (occasionally the Sun) is the stated signature — the same Saturn-angle pairing recurring across several career-ending categories.
- Points referenced: Sun (weak), Saturn (weak), Ascendant (1st House cusp) (weak), Midheaven (10th House cusp) (weak)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **33 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Saturn (24/33, 73%), Mars (22/33, 67%), Ascendant (1st House cusp) (22/33, 67%), Uranus (22/33, 67%), Midheaven (10th House cusp) (20/33, 61%), Neptune (17/33, 52%), Moon (17/33, 52%), Pluto (17/33, 52%)
- Node detail: North Node in 1, South Node in 5, unspecified-pole Node in 1 of 33 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Saturn** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Midheaven (10th House cusp)** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Sun** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **Moon** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Mars** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Uranus** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Neptune** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Pluto** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **3rd House cusp** — supported by POLARIS, Marr Aspects (score 6/10)
- **12th House cusp** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Mercury** — supported by POLARIS, Juan Combos, Marr Aspects (score 4/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Venus** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Jupiter** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Descendant (7th House cusp)** — supported by Marr Aspects (score 2/10)
- **Imum Coeli (4th House cusp)** — supported by Marr Aspects (score 2/10)
- **6th House cusp** — supported by Marr Aspects (score 2/10)
- **8th House cusp** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Saturn, Midheaven (10th House cusp) are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Sun, Moon, Mercury, Mars, Uranus, Neptune, Pluto, Ascendant (1st House cusp) are supported by three of the four sources.

Supported by exactly two sources (moderate confidence): Venus, Jupiter, 3rd House cusp, 12th House cusp, Lunar Node (North/South/unspecified), Part of Fortune.

**Speculative / source-specific symbolism.** Descendant (7th House cusp) (Marr Aspects only), Imum Coeli (4th House cusp) (Marr Aspects only), 6th House cusp (Marr Aspects only), 8th House cusp (Marr Aspects only), 9th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** No clear-cut contradictions were found for this event: the four sources differ in *emphasis* and *coverage* (which is discussed above) rather than making opposing claims about any single symbol.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Saturn | Primary | 1 · 6/16 combos | Mentioned | 2 · 24/33 charts (73%) | 4/4 | 16 / 33 | 8 | Strong Symbol |
| Midheaven (10th House cusp) | Primary | 1 · 3/16 combos | Mentioned | 2 · 20/33 charts (61%) | 4/4 | 16 / 33 | 8 | Strong Symbol |
| Sun | Primary | 0 · 0/16 combos | Mentioned | 1 · 14/33 charts (42%) | 3/4 | 16 / 33 | 6 | Moderate (Relevant Symbol) |
| Moon | Secondary | 1 · 2/16 combos | Absent | 2 · 17/33 charts (52%) | 3/4 | 16 / 33 | 6 | Moderate (Relevant Symbol) |
| Mars | Primary | 1 · 2/16 combos | Absent | 2 · 22/33 charts (67%) | 3/4 | 16 / 33 | 6 | Moderate (Relevant Symbol) |
| Uranus | Secondary | 1 · 3/16 combos | Absent | 2 · 22/33 charts (67%) | 3/4 | 16 / 33 | 6 | Moderate (Relevant Symbol) |
| Neptune | Primary | 1 · 6/16 combos | Absent | 2 · 17/33 charts (52%) | 3/4 | 16 / 33 | 6 | Moderate (Relevant Symbol) |
| Pluto | Secondary | 1 · 5/16 combos | Absent | 2 · 17/33 charts (52%) | 3/4 | 16 / 33 | 6 | Moderate (Relevant Symbol) |
| Ascendant (1st House cusp) | Primary | 0 · 0/16 combos | Mentioned | 2 · 22/33 charts (67%) | 3/4 | 16 / 33 | 6 | Moderate (Relevant Symbol) |
| 3rd House cusp | Primary | — (out of scope) | Absent | 1 · 12/33 charts (36%) | 2/3 | 16 / 33 | 6 | Moderate (Relevant Symbol) |
| 12th House cusp | Primary | — (out of scope) | Absent | 1 · 9/33 charts (27%) | 2/3 | 16 / 33 | 6 | Moderate (Relevant Symbol) |
| Mercury | Secondary | 1 · 1/16 combos | Absent | 1 · 12/33 charts (36%) | 3/4 | 16 / 33 | 4 | Weak (Occasional Symbol) |
| Lunar Node (North/South/unspecified) | Primary | 0 · 0/16 combos | Absent | 1 · 7/33 charts (21%) | 2/4 | 16 / 33 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 1/16 combos | Absent | 1 · 7/33 charts (21%) | 2/3 | 16 / 33 | 4 | Weak (Occasional Symbol) |
| Venus | Absent | 1 · 1/16 combos | Absent | 1 · 8/33 charts (24%) | 2/4 | 16 / 33 | 2 | Very Weak (Speculative Symbol) |
| Jupiter | Absent | 1 · 2/16 combos | Absent | 1 · 10/33 charts (30%) | 2/4 | 16 / 33 | 2 | Very Weak (Speculative Symbol) |
| Descendant (7th House cusp) | Absent | — (out of scope) | Absent | 1 · 1/33 charts (3%) | 1/3 | 16 / 33 | 2 | Very Weak (Speculative Symbol) |
| Imum Coeli (4th House cusp) | Absent | — (out of scope) | Absent | 1 · 2/33 charts (6%) | 1/3 | 16 / 33 | 2 | Very Weak (Speculative Symbol) |
| 6th House cusp | Absent | — (out of scope) | Absent | 1 · 1/33 charts (3%) | 1/3 | 16 / 33 | 2 | Very Weak (Speculative Symbol) |
| 8th House cusp | Absent | — (out of scope) | Absent | 1 · 2/33 charts (6%) | 1/3 | 16 / 33 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | Absent | 1 · 2/33 charts (6%) | 1/3 | 16 / 33 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 2/33 charts (6%) | 1/3 | 16 / 33 | 2 | Very Weak (Speculative Symbol) |

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Saturn**: tier_score = 8 (n_juan_combos_total=16, n_marr_examples_total=33)  |  **Mercury**: tier_score = 4 (n_juan_combos_total=16, n_marr_examples_total=33) — *looked up independently; no combined score is produced for this pairing.*
- **Saturn**: tier_score = 8 (n_juan_combos_total=16, n_marr_examples_total=33)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=16, n_marr_examples_total=33) — *looked up independently; no combined score is produced for this pairing.*
- **Midheaven (10th House cusp)**: tier_score = 8 (n_juan_combos_total=16, n_marr_examples_total=33)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=16, n_marr_examples_total=33) — *looked up independently; no combined score is produced for this pairing.*
- **Mercury**: tier_score = 4 (n_juan_combos_total=16, n_marr_examples_total=33)  |  **Lunar Node (North/South/unspecified)**: tier_score = 4 (n_juan_combos_total=16, n_marr_examples_total=33) — *looked up independently; no combined score is produced for this pairing.*

---

## 34. Mobilization

*Category: Military — call-up to service*

### 1. Event Overview

Being called into military service. The Midheaven or Ascendant with Mars is the core signature; the 12th house cusp and/or Saturn add a specifically difficult or psychologically hard mobilization.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Mars, Saturn, Pluto, Moon, Mercury
- Houses/Angles mentioned: Ascendant (1st House cusp), Midheaven (10th House cusp), 12th House cusp, 3rd House cusp
- Nodes/Points mentioned: none
- **Primary** (highest POLARIS confidence): Mars, Saturn, Pluto, Ascendant (1st House cusp), Midheaven (10th House cusp), 12th House cusp
- **Secondary**: Moon, Mercury, 3rd House cusp
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Moon (2/3), Saturn (1/3), Pluto (1/3), Jupiter (1/3), Neptune (1/3)
- Total pairwise combinations catalogued for this event: 3
- **Low sample size:** only 3 combinations catalogued for this event in total — any single symbol's Juan Combos percentage here rests on very little underlying data, and the tier_score for symbols resting mainly on this source should be read with that in mind (see `n_juan_combos_total` on each symbol record).
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: Being called into military service. The Midheaven or Ascendant with Mars is the core signature; the 12th house cusp and/or Saturn add a specifically difficult or psychologically hard mobilization.
- Points referenced: Saturn (strong), 12th House cusp (strong), Mars (weak), Ascendant (1st House cusp) (weak), Midheaven (10th House cusp) (weak)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **18 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Mars (14/18, 78%), 12th House cusp (13/18, 72%), Saturn (11/18, 61%), Sun (11/18, 61%), Uranus (10/18, 56%), Ascendant (1st House cusp) (10/18, 56%), Midheaven (10th House cusp) (10/18, 56%), Mercury (9/18, 50%)
- Node detail: North Node in 2, South Node in 4, unspecified-pole Node in 0 of 18 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- **12th House cusp** — supported by POLARIS, Other, Marr Aspects (score 10/10)

**Secondary Symbols**
- **Saturn** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Mars** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **Pluto** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **Midheaven (10th House cusp)** — supported by POLARIS, Other, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Moon** — supported by POLARIS, Juan Combos, Marr Aspects (score 4/10)
- **Mercury** — supported by POLARIS, Marr Aspects (score 4/10)
- **Jupiter** — supported by Juan Combos, Marr Aspects (score 4/10)
- **3rd House cusp** — supported by POLARIS, Marr Aspects (score 4/10)
- **Neptune** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Sun** — supported by Marr Aspects (score 2/10)
- **Uranus** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **Venus** — supported by Marr Aspects (score 2/10)
- **Imum Coeli (4th House cusp)** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)
- **Lunar Node (North/South/unspecified)** — supported by Marr Aspects (score 2/10)
- **Part of Fortune** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Saturn is corroborated by every source able to speak to it, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Moon, Mars, Pluto, Ascendant (1st House cusp), Midheaven (10th House cusp), 12th House cusp are supported by three of the four sources. 1 of these (12th House cusp) sits at the structural ceiling for its symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Mercury, Jupiter, Neptune, 3rd House cusp.

**Speculative / source-specific symbolism.** Sun (Marr Aspects only), Venus (Marr Aspects only), Uranus (Marr Aspects only), Imum Coeli (4th House cusp) (Marr Aspects only), 9th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only), Lunar Node (North/South/unspecified) (Marr Aspects only), Part of Fortune (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** Sun (in 11/18 example charts, 61%), Uranus (in 10/18 example charts, 56%) recur in a substantial share of Marr's worked examples without being singled out in POLARIS's Primary/Secondary list. This is not a direct contradiction — POLARIS's list is a short, deliberately curated selection rather than an exhaustive one, and no case was found anywhere in the compendium of a POLARIS-Primary symbol being *absent* from a substantial Marr Aspects sample. Read it as an emphasis gap, not a disagreement about relevance.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| 12th House cusp | Primary | — (out of scope) | Strong emphasis | 2 · 13/18 charts (72%) | 3/3 † | 3 / 18 | 10 | Very Strong (Core Symbol) |
| Saturn | Primary | 1 · 1/3 combos | Strong emphasis | 2 · 11/18 charts (61%) | 4/4 | 3 / 18 | 8 | Strong Symbol |
| Mars | Primary | 0 · 0/3 combos | Mentioned | 2 · 14/18 charts (78%) | 3/4 | 3 / 18 | 6 | Moderate (Relevant Symbol) |
| Pluto | Primary | 1 · 1/3 combos | Absent | 1 · 8/18 charts (44%) | 3/4 | 3 / 18 | 6 | Moderate (Relevant Symbol) |
| Ascendant (1st House cusp) | Primary | 0 · 0/3 combos | Mentioned | 2 · 10/18 charts (56%) | 3/4 | 3 / 18 | 6 | Moderate (Relevant Symbol) |
| Midheaven (10th House cusp) | Primary | 0 · 0/3 combos | Mentioned | 2 · 10/18 charts (56%) | 3/4 | 3 / 18 | 6 | Moderate (Relevant Symbol) |
| Moon | Secondary | 1 · 2/3 combos | Absent | 1 · 7/18 charts (39%) | 3/4 | 3 / 18 | 4 | Weak (Occasional Symbol) |
| Mercury | Secondary | 0 · 0/3 combos | Absent | 2 · 9/18 charts (50%) | 2/4 | 3 / 18 | 4 | Weak (Occasional Symbol) |
| Jupiter | Absent | 1 · 1/3 combos | Absent | 2 · 9/18 charts (50%) | 2/4 | 3 / 18 | 4 | Weak (Occasional Symbol) |
| 3rd House cusp | Secondary | — (out of scope) | Absent | 1 · 2/18 charts (11%) | 2/3 | 3 / 18 | 4 | Weak (Occasional Symbol) |
| Neptune | Absent | 1 · 1/3 combos | Absent | 1 · 5/18 charts (28%) | 2/4 | 3 / 18 | 2 | Very Weak (Speculative Symbol) |
| Sun | Absent | 0 · 0/3 combos | Absent | 2 · 11/18 charts (61%) | 1/4 | 3 / 18 | 2 | Very Weak (Speculative Symbol) |
| Uranus | Absent | 0 · 0/3 combos | Absent | 2 · 10/18 charts (56%) | 1/4 | 3 / 18 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | Absent | 1 · 8/18 charts (44%) | 1/3 | 3 / 18 | 2 | Very Weak (Speculative Symbol) |
| Venus | Absent | 0 · 0/3 combos | Absent | 1 · 4/18 charts (22%) | 1/4 | 3 / 18 | 2 | Very Weak (Speculative Symbol) |
| Imum Coeli (4th House cusp) | Absent | — (out of scope) | Absent | 1 · 3/18 charts (17%) | 1/3 | 3 / 18 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 6/18 charts (33%) | 1/3 | 3 / 18 | 2 | Very Weak (Speculative Symbol) |
| Lunar Node (North/South/unspecified) | Absent | 0 · 0/3 combos | Absent | 1 · 6/18 charts (33%) | 1/4 | 3 / 18 | 2 | Very Weak (Speculative Symbol) |
| Part of Fortune | — (out of scope) | 0 · 0/3 combos | Absent | 1 · 1/18 charts (6%) | 1/3 | 3 / 18 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **12th House cusp**: tier_score = 10 (n_juan_combos_total=3, n_marr_examples_total=18)  |  **3rd House cusp**: tier_score = 4 (n_juan_combos_total=3, n_marr_examples_total=18) — *looked up independently; no combined score is produced for this pairing.*
- **12th House cusp**: tier_score = 10 (n_juan_combos_total=3, n_marr_examples_total=18)  |  **Part of Fortune**: tier_score = 2 (n_juan_combos_total=3, n_marr_examples_total=18) — *looked up independently; no combined score is produced for this pairing.*
- **Saturn**: tier_score = 8 (n_juan_combos_total=3, n_marr_examples_total=18)  |  **Part of Fortune**: tier_score = 2 (n_juan_combos_total=3, n_marr_examples_total=18) — *looked up independently; no combined score is produced for this pairing.*
- **3rd House cusp**: tier_score = 4 (n_juan_combos_total=3, n_marr_examples_total=18)  |  **Neptune**: tier_score = 2 (n_juan_combos_total=3, n_marr_examples_total=18) — *looked up independently; no combined score is produced for this pairing.*

---

## 35. Accident

*Category: Physical — mishap or injury*

### 1. Event Overview

Physical accidents and injuries. The Ascendant combined with Mars or Uranus is the shared backbone across falls, wounds and injuries, with Saturn added for severe or painful cases and Pluto where amputation results.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Mercury, Mars, Saturn, Uranus, Moon, Neptune, Pluto
- Houses/Angles mentioned: Ascendant (1st House cusp), Midheaven (10th House cusp), 3rd House cusp, 12th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Mercury, Mars, Saturn, Uranus, Ascendant (1st House cusp), Midheaven (10th House cusp), 3rd House cusp, 12th House cusp
- **Secondary**: Moon, Neptune, Pluto, North Node (Ascending)
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Mars (10/34), Saturn (10/34), Neptune (8/34), Pluto (6/34), Ascendant (1st House cusp) (5/34), Midheaven (10th House cusp) (5/34), Moon (5/34), Uranus (4/34), Sun (4/34), Lunar Node (pole unspecified) (4/34)
- Total pairwise combinations catalogued for this event: 34
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: Physical accidents and injuries. The Ascendant combined with Mars or Uranus is the shared backbone across falls, wounds and injuries, with Saturn added for severe or painful cases and Pluto where amputation results.
- Points referenced: Mars (mentioned), Saturn (mentioned), Uranus (mentioned), Pluto (mentioned), Ascendant (1st House cusp) (mentioned)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **21 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Ascendant (1st House cusp) (16/21, 76%), Uranus (15/21, 71%), 12th House cusp (14/21, 67%), Saturn (14/21, 67%), Moon (12/21, 57%), Neptune (11/21, 52%), Sun (10/21, 48%), Pluto (10/21, 48%)
- Node detail: North Node in 1, South Node in 2, unspecified-pole Node in 0 of 21 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Mars** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Saturn** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Uranus** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Pluto** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 6/10)
- **Moon** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Mercury** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Neptune** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Midheaven (10th House cusp)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **3rd House cusp** — supported by POLARIS, Marr Aspects (score 6/10)
- **12th House cusp** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Lunar Node (North/South/unspecified)** — supported by POLARIS, Juan Combos, Marr Aspects (score 4/10)
- **Sun** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Jupiter** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Descendant (7th House cusp)** — supported by Marr Aspects (score 2/10)
- **Imum Coeli (4th House cusp)** — supported by Marr Aspects (score 2/10)
- **5th House cusp** — supported by Marr Aspects (score 2/10)
- **8th House cusp** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Mars, Saturn, Uranus, Pluto, Ascendant (1st House cusp) are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Moon, Mercury, Neptune, Midheaven (10th House cusp), Lunar Node (North/South/unspecified) are supported by three of the four sources.

Supported by exactly two sources (moderate confidence): Sun, Jupiter, 3rd House cusp, 12th House cusp, Part of Fortune.

**Speculative / source-specific symbolism.** Descendant (7th House cusp) (Marr Aspects only), Imum Coeli (4th House cusp) (Marr Aspects only), 5th House cusp (Marr Aspects only), 8th House cusp (Marr Aspects only), 9th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** Sun (in 10/21 example charts, 48%) recur in a substantial share of Marr's worked examples without being singled out in POLARIS's Primary/Secondary list. This is not a direct contradiction — POLARIS's list is a short, deliberately curated selection rather than an exhaustive one, and no case was found anywhere in the compendium of a POLARIS-Primary symbol being *absent* from a substantial Marr Aspects sample. Read it as an emphasis gap, not a disagreement about relevance.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Mars | Primary | 1 · 10/34 combos | Mentioned | 2 · 10/21 charts (48%) | 4/4 | 34 / 21 | 8 | Strong Symbol |
| Saturn | Primary | 1 · 10/34 combos | Mentioned | 2 · 14/21 charts (67%) | 4/4 | 34 / 21 | 8 | Strong Symbol |
| Uranus | Primary | 1 · 4/34 combos | Mentioned | 2 · 15/21 charts (71%) | 4/4 | 34 / 21 | 8 | Strong Symbol |
| Ascendant (1st House cusp) | Primary | 1 · 5/34 combos | Mentioned | 2 · 16/21 charts (76%) | 4/4 | 34 / 21 | 8 | Strong Symbol |
| Pluto | Secondary | 1 · 6/34 combos | Mentioned | 2 · 10/21 charts (48%) | 4/4 | 34 / 21 | 6 | Moderate (Relevant Symbol) |
| Moon | Secondary | 1 · 5/34 combos | Absent | 2 · 12/21 charts (57%) | 3/4 | 34 / 21 | 6 | Moderate (Relevant Symbol) |
| Mercury | Primary | 1 · 4/34 combos | Absent | 1 · 8/21 charts (38%) | 3/4 | 34 / 21 | 6 | Moderate (Relevant Symbol) |
| Neptune | Secondary | 1 · 8/34 combos | Absent | 2 · 11/21 charts (52%) | 3/4 | 34 / 21 | 6 | Moderate (Relevant Symbol) |
| Midheaven (10th House cusp) | Primary | 1 · 5/34 combos | Absent | 1 · 3/21 charts (14%) | 3/4 | 34 / 21 | 6 | Moderate (Relevant Symbol) |
| 3rd House cusp | Primary | — (out of scope) | Absent | 1 · 5/21 charts (24%) | 2/3 | 34 / 21 | 6 | Moderate (Relevant Symbol) |
| 12th House cusp | Primary | — (out of scope) | Absent | 2 · 14/21 charts (67%) | 2/3 | 34 / 21 | 6 | Moderate (Relevant Symbol) |
| Lunar Node (North/South/unspecified) | Secondary | 1 · 4/34 combos | Absent | 1 · 3/21 charts (14%) | 3/4 | 34 / 21 | 4 | Weak (Occasional Symbol) |
| Sun | Absent | 1 · 4/34 combos | Absent | 2 · 10/21 charts (48%) | 2/4 | 34 / 21 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 2/34 combos | Absent | 1 · 2/21 charts (10%) | 2/3 | 34 / 21 | 4 | Weak (Occasional Symbol) |
| Jupiter | Absent | 1 · 1/34 combos | Absent | 1 · 2/21 charts (10%) | 2/4 | 34 / 21 | 2 | Very Weak (Speculative Symbol) |
| Descendant (7th House cusp) | Absent | — (out of scope) | Absent | 1 · 1/21 charts (5%) | 1/3 | 34 / 21 | 2 | Very Weak (Speculative Symbol) |
| Imum Coeli (4th House cusp) | Absent | — (out of scope) | Absent | 1 · 7/21 charts (33%) | 1/3 | 34 / 21 | 2 | Very Weak (Speculative Symbol) |
| 5th House cusp | Absent | — (out of scope) | Absent | 1 · 1/21 charts (5%) | 1/3 | 34 / 21 | 2 | Very Weak (Speculative Symbol) |
| 8th House cusp | Absent | — (out of scope) | Absent | 1 · 1/21 charts (5%) | 1/3 | 34 / 21 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | Absent | 1 · 6/21 charts (29%) | 1/3 | 34 / 21 | 2 | Very Weak (Speculative Symbol) |

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Mars**: tier_score = 8 (n_juan_combos_total=34, n_marr_examples_total=21)  |  **12th House cusp**: tier_score = 6 (n_juan_combos_total=34, n_marr_examples_total=21) — *looked up independently; no combined score is produced for this pairing.*
- **Mars**: tier_score = 8 (n_juan_combos_total=34, n_marr_examples_total=21)  |  **9th House cusp**: tier_score = 2 (n_juan_combos_total=34, n_marr_examples_total=21) — *looked up independently; no combined score is produced for this pairing.*
- **Saturn**: tier_score = 8 (n_juan_combos_total=34, n_marr_examples_total=21)  |  **9th House cusp**: tier_score = 2 (n_juan_combos_total=34, n_marr_examples_total=21) — *looked up independently; no combined score is produced for this pairing.*
- **12th House cusp**: tier_score = 6 (n_juan_combos_total=34, n_marr_examples_total=21)  |  **Lunar Node (North/South/unspecified)**: tier_score = 4 (n_juan_combos_total=34, n_marr_examples_total=21) — *looked up independently; no combined score is produced for this pairing.*

---

## 36. Hospitalization or Illness

*Category: Health — medical crisis*

### 1. Event Overview

Hospitalization, surgery and related medical crises. The Ascendant (with the 12th house cusp) combined with Saturn is the general hospitalization signature; Mars marks surgery specifically, Uranus a sudden turn, and Mars-Neptune a case that fails to heal.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Mars, Saturn, Neptune, Moon, Pluto
- Houses/Angles mentioned: Ascendant (1st House cusp), Midheaven (10th House cusp), 12th House cusp
- Nodes/Points mentioned: none
- **Primary** (highest POLARIS confidence): Mars, Saturn, Neptune, Ascendant (1st House cusp), Midheaven (10th House cusp), 12th House cusp
- **Secondary**: Moon, Pluto
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Neptune (12/50), Saturn (11/50), Mars (10/50), Pluto (10/50), Sun (9/50), Moon (9/50), Ascendant (1st House cusp) (8/50), Midheaven (10th House cusp) (8/50), Uranus (7/50), Mercury (5/50)
- Total pairwise combinations catalogued for this event: 50
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: Hospitalization, surgery and related medical crises. The Ascendant (with the 12th house cusp) combined with Saturn is the general hospitalization signature; Mars marks surgery specifically, Uranus a sudden turn, and Mars-Neptune a case that fails to heal.
- Points referenced: Saturn (strong), Ascendant (1st House cusp) (strong), 12th House cusp (strong), Moon (mentioned), Mercury (mentioned), Mars (mentioned), Uranus (mentioned), Neptune (mentioned), Pluto (mentioned)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **68 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: 12th House cusp (50/68, 74%), Ascendant (1st House cusp) (49/68, 72%), Mars (48/68, 71%), Saturn (44/68, 65%), Sun (40/68, 59%), Moon (39/68, 57%), Neptune (36/68, 53%), Uranus (33/68, 49%)
- Node detail: North Node in 1, South Node in 1, unspecified-pole Node in 1 of 68 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- **12th House cusp** — supported by POLARIS, Other, Marr Aspects (score 10/10)

**Secondary Symbols**
- **Mars** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Saturn** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Neptune** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Moon** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 6/10)
- **Pluto** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 6/10)
- **Uranus** — supported by Juan Combos, Other, Marr Aspects (score 6/10)
- **Midheaven (10th House cusp)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Mercury** — supported by Juan Combos, Other, Marr Aspects (score 4/10)
- **Sun** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Imum Coeli (4th House cusp)** — supported by Marr Aspects (score 4/10)
- **Venus** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Jupiter** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Lunar Node (North/South/unspecified)** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Descendant (7th House cusp)** — supported by Marr Aspects (score 2/10)
- **3rd House cusp** — supported by Marr Aspects (score 2/10)
- **8th House cusp** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Moon, Mars, Saturn, Neptune, Pluto, Ascendant (1st House cusp) are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Mercury, Uranus, Midheaven (10th House cusp), 12th House cusp are supported by three of the four sources. 1 of these (12th House cusp) sits at the structural ceiling for its symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Sun, Venus, Jupiter, Lunar Node (North/South/unspecified), Part of Fortune.

**Speculative / source-specific symbolism.** Descendant (7th House cusp) (Marr Aspects only), Imum Coeli (4th House cusp) (Marr Aspects only), 3rd House cusp (Marr Aspects only), 8th House cusp (Marr Aspects only), 9th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** Sun (in 40/68 example charts, 59%), Uranus (in 33/68 example charts, 49%) recur in a substantial share of Marr's worked examples without being singled out in POLARIS's Primary/Secondary list. This is not a direct contradiction — POLARIS's list is a short, deliberately curated selection rather than an exhaustive one, and no case was found anywhere in the compendium of a POLARIS-Primary symbol being *absent* from a substantial Marr Aspects sample. Read it as an emphasis gap, not a disagreement about relevance.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| 12th House cusp | Primary | — (out of scope) | Strong emphasis | 2 · 50/68 charts (74%) | 3/3 † | 50 / 68 | 10 | Very Strong (Core Symbol) |
| Mars | Primary | 1 · 10/50 combos | Mentioned | 2 · 48/68 charts (71%) | 4/4 | 50 / 68 | 8 | Strong Symbol |
| Saturn | Primary | 1 · 11/50 combos | Strong emphasis | 2 · 44/68 charts (65%) | 4/4 | 50 / 68 | 8 | Strong Symbol |
| Neptune | Primary | 1 · 12/50 combos | Mentioned | 2 · 36/68 charts (53%) | 4/4 | 50 / 68 | 8 | Strong Symbol |
| Ascendant (1st House cusp) | Primary | 1 · 8/50 combos | Strong emphasis | 2 · 49/68 charts (72%) | 4/4 | 50 / 68 | 8 | Strong Symbol |
| Moon | Secondary | 1 · 9/50 combos | Mentioned | 2 · 39/68 charts (57%) | 4/4 | 50 / 68 | 6 | Moderate (Relevant Symbol) |
| Pluto | Secondary | 1 · 10/50 combos | Mentioned | 1 · 26/68 charts (38%) | 4/4 | 50 / 68 | 6 | Moderate (Relevant Symbol) |
| Uranus | Absent | 1 · 7/50 combos | Mentioned | 2 · 33/68 charts (49%) | 3/4 | 50 / 68 | 6 | Moderate (Relevant Symbol) |
| Midheaven (10th House cusp) | Primary | 1 · 8/50 combos | Absent | 1 · 12/68 charts (18%) | 3/4 | 50 / 68 | 6 | Moderate (Relevant Symbol) |
| Mercury | Absent | 1 · 5/50 combos | Mentioned | 1 · 24/68 charts (35%) | 3/4 | 50 / 68 | 4 | Weak (Occasional Symbol) |
| Sun | Absent | 1 · 9/50 combos | Absent | 2 · 40/68 charts (59%) | 2/4 | 50 / 68 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 3/50 combos | Absent | 1 · 10/68 charts (15%) | 2/3 | 50 / 68 | 4 | Weak (Occasional Symbol) |
| Imum Coeli (4th House cusp) | Absent | — (out of scope) | Absent | 2 · 28/68 charts (41%) | 1/3 | 50 / 68 | 4 | Weak (Occasional Symbol) |
| Venus | Absent | 1 · 4/50 combos | Absent | 1 · 17/68 charts (25%) | 2/4 | 50 / 68 | 2 | Very Weak (Speculative Symbol) |
| Jupiter | Absent | 1 · 1/50 combos | Absent | 1 · 12/68 charts (18%) | 2/4 | 50 / 68 | 2 | Very Weak (Speculative Symbol) |
| Lunar Node (North/South/unspecified) | Absent | 1 · 3/50 combos | Absent | 1 · 3/68 charts (4%) | 2/4 | 50 / 68 | 2 | Very Weak (Speculative Symbol) |
| Descendant (7th House cusp) | Absent | — (out of scope) | Absent | 1 · 4/68 charts (6%) | 1/3 | 50 / 68 | 2 | Very Weak (Speculative Symbol) |
| 3rd House cusp | Absent | — (out of scope) | Absent | 1 · 2/68 charts (3%) | 1/3 | 50 / 68 | 2 | Very Weak (Speculative Symbol) |
| 8th House cusp | Absent | — (out of scope) | Absent | 1 · 1/68 charts (1%) | 1/3 | 50 / 68 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | Absent | 1 · 1/68 charts (1%) | 1/3 | 50 / 68 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 2/68 charts (3%) | 1/3 | 50 / 68 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **12th House cusp**: tier_score = 10 (n_juan_combos_total=50, n_marr_examples_total=68)  |  **Sun**: tier_score = 4 (n_juan_combos_total=50, n_marr_examples_total=68) — *looked up independently; no combined score is produced for this pairing.*
- **12th House cusp**: tier_score = 10 (n_juan_combos_total=50, n_marr_examples_total=68)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=50, n_marr_examples_total=68) — *looked up independently; no combined score is produced for this pairing.*
- **Mars**: tier_score = 8 (n_juan_combos_total=50, n_marr_examples_total=68)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=50, n_marr_examples_total=68) — *looked up independently; no combined score is produced for this pairing.*
- **Sun**: tier_score = 4 (n_juan_combos_total=50, n_marr_examples_total=68)  |  **Part of Fortune**: tier_score = 4 (n_juan_combos_total=50, n_marr_examples_total=68) — *looked up independently; no combined score is produced for this pairing.*

---

## 37. Violence

*Category: Physical harm — assault, injury inflicted by others*

### 1. Event Overview

Violence directed at or by the native. Mars, Saturn and Uranus on the Ascendant form the core signature, with Pluto added for the most extreme cases; the compendium notes the same symbolism applies to both victim and perpetrator.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Mars, Saturn, Uranus, Pluto, Mercury
- Houses/Angles mentioned: Ascendant (1st House cusp), Midheaven (10th House cusp), 12th House cusp
- Nodes/Points mentioned: none
- **Primary** (highest POLARIS confidence): Mars, Saturn, Uranus, Pluto, Ascendant (1st House cusp), Midheaven (10th House cusp), 12th House cusp
- **Secondary**: Mercury
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Saturn (2/4), Mars (2/4), Pluto (2/4), Lunar Node (pole unspecified) (1/4), Part of Fortune (1/4)
- Total pairwise combinations catalogued for this event: 4
- **Low sample size:** only 4 combinations catalogued for this event in total — any single symbol's Juan Combos percentage here rests on very little underlying data, and the tier_score for symbols resting mainly on this source should be read with that in mind (see `n_juan_combos_total` on each symbol record).
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: Violence directed at or by the native. Mars, Saturn and Uranus on the Ascendant form the core signature, with Pluto added for the most extreme cases; the compendium notes the same symbolism applies to both victim and perpetrator.
- Points referenced: Sun (mentioned), Venus (mentioned), Mars (mentioned), Saturn (mentioned), Uranus (mentioned), Pluto (mentioned), Ascendant (1st House cusp) (mentioned), Midheaven (10th House cusp) (mentioned), 12th House cusp (weak)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **37 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Mars (28/37, 76%), Sun (26/37, 70%), Saturn (26/37, 70%), Neptune (22/37, 59%), Uranus (21/37, 57%), Midheaven (10th House cusp) (21/37, 57%), Mercury (20/37, 54%), Moon (19/37, 51%)
- Node detail: North Node in 1, South Node in 5, unspecified-pole Node in 4 of 37 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Mars** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Saturn** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **Pluto** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **12th House cusp** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **Uranus** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **Midheaven (10th House cusp)** — supported by POLARIS, Other, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Sun** — supported by Other, Marr Aspects (score 4/10)
- **Mercury** — supported by POLARIS, Marr Aspects (score 4/10)
- **Part of Fortune** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Venus** — supported by Other, Marr Aspects (score 2/10)
- **Lunar Node (North/South/unspecified)** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Moon** — supported by Marr Aspects (score 2/10)
- **Neptune** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **Jupiter** — supported by Marr Aspects (score 2/10)
- **Descendant (7th House cusp)** — supported by Marr Aspects (score 2/10)
- **Imum Coeli (4th House cusp)** — supported by Marr Aspects (score 2/10)
- **3rd House cusp** — supported by Marr Aspects (score 2/10)
- **6th House cusp** — supported by Marr Aspects (score 2/10)
- **8th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Mars, Saturn, Pluto are corroborated by every source able to speak to them, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Uranus, Ascendant (1st House cusp), Midheaven (10th House cusp), 12th House cusp are supported by three of the four sources. 1 of these (12th House cusp) sits at the structural ceiling for its symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Sun, Mercury, Venus, Lunar Node (North/South/unspecified), Part of Fortune.

**Speculative / source-specific symbolism.** Moon (Marr Aspects only), Jupiter (Marr Aspects only), Neptune (Marr Aspects only), Descendant (7th House cusp) (Marr Aspects only), Imum Coeli (4th House cusp) (Marr Aspects only), 3rd House cusp (Marr Aspects only), 6th House cusp (Marr Aspects only), 8th House cusp (Marr Aspects only), 9th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** Sun (in 26/37 example charts, 70%), Neptune (in 22/37 example charts, 59%) recur in a substantial share of Marr's worked examples without being singled out in POLARIS's Primary/Secondary list. This is not a direct contradiction — POLARIS's list is a short, deliberately curated selection rather than an exhaustive one, and no case was found anywhere in the compendium of a POLARIS-Primary symbol being *absent* from a substantial Marr Aspects sample. Read it as an emphasis gap, not a disagreement about relevance.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Mars | Primary | 1 · 2/4 combos | Mentioned | 2 · 28/37 charts (76%) | 4/4 | 4 / 37 | 8 | Strong Symbol |
| Saturn | Primary | 1 · 2/4 combos | Mentioned | 2 · 26/37 charts (70%) | 4/4 | 4 / 37 | 8 | Strong Symbol |
| Pluto | Primary | 1 · 2/4 combos | Mentioned | 2 · 16/37 charts (43%) | 4/4 | 4 / 37 | 8 | Strong Symbol |
| 12th House cusp | Primary | — (out of scope) | Mentioned | 2 · 16/37 charts (43%) | 3/3 † | 4 / 37 | 8 | Strong Symbol |
| Uranus | Primary | 0 · 0/4 combos | Mentioned | 2 · 21/37 charts (57%) | 3/4 | 4 / 37 | 6 | Moderate (Relevant Symbol) |
| Ascendant (1st House cusp) | Primary | 0 · 0/4 combos | Mentioned | 2 · 16/37 charts (43%) | 3/4 | 4 / 37 | 6 | Moderate (Relevant Symbol) |
| Midheaven (10th House cusp) | Primary | 0 · 0/4 combos | Mentioned | 2 · 21/37 charts (57%) | 3/4 | 4 / 37 | 6 | Moderate (Relevant Symbol) |
| Sun | Absent | 0 · 0/4 combos | Mentioned | 2 · 26/37 charts (70%) | 2/4 | 4 / 37 | 4 | Weak (Occasional Symbol) |
| Mercury | Secondary | 0 · 0/4 combos | Absent | 2 · 20/37 charts (54%) | 2/4 | 4 / 37 | 4 | Weak (Occasional Symbol) |
| Part of Fortune | — (out of scope) | 1 · 1/4 combos | Absent | 1 · 9/37 charts (24%) | 2/3 | 4 / 37 | 4 | Weak (Occasional Symbol) |
| Venus | Absent | 0 · 0/4 combos | Mentioned | 1 · 8/37 charts (22%) | 2/4 | 4 / 37 | 2 | Very Weak (Speculative Symbol) |
| Lunar Node (North/South/unspecified) | Absent | 1 · 1/4 combos | Absent | 1 · 10/37 charts (27%) | 2/4 | 4 / 37 | 2 | Very Weak (Speculative Symbol) |
| Moon | Absent | 0 · 0/4 combos | Absent | 2 · 19/37 charts (51%) | 1/4 | 4 / 37 | 2 | Very Weak (Speculative Symbol) |
| Neptune | Absent | 0 · 0/4 combos | Absent | 2 · 22/37 charts (59%) | 1/4 | 4 / 37 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | Absent | 1 · 15/37 charts (41%) | 1/3 | 4 / 37 | 2 | Very Weak (Speculative Symbol) |
| Jupiter | Absent | 0 · 0/4 combos | Absent | 1 · 12/37 charts (32%) | 1/4 | 4 / 37 | 2 | Very Weak (Speculative Symbol) |
| Descendant (7th House cusp) | Absent | — (out of scope) | Absent | 1 · 5/37 charts (14%) | 1/3 | 4 / 37 | 2 | Very Weak (Speculative Symbol) |
| Imum Coeli (4th House cusp) | Absent | — (out of scope) | Absent | 1 · 6/37 charts (16%) | 1/3 | 4 / 37 | 2 | Very Weak (Speculative Symbol) |
| 3rd House cusp | Absent | — (out of scope) | Absent | 1 · 9/37 charts (24%) | 1/3 | 4 / 37 | 2 | Very Weak (Speculative Symbol) |
| 6th House cusp | Absent | — (out of scope) | Absent | 1 · 1/37 charts (3%) | 1/3 | 4 / 37 | 2 | Very Weak (Speculative Symbol) |
| 8th House cusp | Absent | — (out of scope) | Absent | 1 · 4/37 charts (11%) | 1/3 | 4 / 37 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 2/37 charts (5%) | 1/3 | 4 / 37 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Mars**: tier_score = 8 (n_juan_combos_total=4, n_marr_examples_total=37)  |  **Lunar Node (North/South/unspecified)**: tier_score = 2 (n_juan_combos_total=4, n_marr_examples_total=37) — *looked up independently; no combined score is produced for this pairing.*
- **Mars**: tier_score = 8 (n_juan_combos_total=4, n_marr_examples_total=37)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=4, n_marr_examples_total=37) — *looked up independently; no combined score is produced for this pairing.*
- **Saturn**: tier_score = 8 (n_juan_combos_total=4, n_marr_examples_total=37)  |  **11th House cusp**: tier_score = 2 (n_juan_combos_total=4, n_marr_examples_total=37) — *looked up independently; no combined score is produced for this pairing.*
- **Lunar Node (North/South/unspecified)**: tier_score = 2 (n_juan_combos_total=4, n_marr_examples_total=37)  |  **Moon**: tier_score = 2 (n_juan_combos_total=4, n_marr_examples_total=37) — *looked up independently; no combined score is produced for this pairing.*

---

## 38. Intrigue

*Category: Deception — gossip, scandal, hidden dealings*

### 1. Event Overview

Gossip, intrigue and scandal. The 12th house cusp or the angles combined with Mercury or Neptune form the core signature, with Mars added when the scandal becomes public via the Midheaven.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Mercury, Neptune, Mars, Pluto
- Houses/Angles mentioned: Ascendant (1st House cusp), Midheaven (10th House cusp), 12th House cusp
- Nodes/Points mentioned: none
- **Primary** (highest POLARIS confidence): Mercury, Neptune, Ascendant (1st House cusp), Midheaven (10th House cusp), 12th House cusp
- **Secondary**: Mars, Pluto
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Uranus (1/1), Saturn (1/1)
- Total pairwise combinations catalogued for this event: 1
- **Low sample size:** only 1 combination catalogued for this event in total — any single symbol's Juan Combos percentage here rests on very little underlying data, and the tier_score for symbols resting mainly on this source should be read with that in mind (see `n_juan_combos_total` on each symbol record).
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: Gossip, intrigue and scandal. The 12th house cusp or the angles combined with Mercury or Neptune form the core signature, with Mars added when the scandal becomes public via the Midheaven.
- Points referenced: Mercury (strong), Neptune (strong), Ascendant (1st House cusp) (strong), Midheaven (10th House cusp) (strong), 5th House cusp (strong), 12th House cusp (strong), Mars (mentioned)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **11 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Uranus (10/11, 91%), Saturn (8/11, 73%), Mars (8/11, 73%), Midheaven (10th House cusp) (7/11, 64%), 3rd House cusp (7/11, 64%), 12th House cusp (7/11, 64%), Pluto (7/11, 64%), Venus (7/11, 64%)
- Node detail: North Node in 2, South Node in 0, unspecified-pole Node in 0 of 11 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- **12th House cusp** — supported by POLARIS, Other, Marr Aspects (score 10/10)

**Secondary Symbols**
- **Mercury** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **Neptune** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **Midheaven (10th House cusp)** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **Mars** — supported by POLARIS, Other, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Saturn** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Uranus** — supported by Juan Combos, Marr Aspects (score 4/10)
- **Pluto** — supported by POLARIS, Marr Aspects (score 4/10)
- **3rd House cusp** — supported by Marr Aspects (score 4/10)
- **5th House cusp** — supported by Other (score 4/10)
- **Sun** — supported by Marr Aspects (score 2/10)
- **Moon** — supported by Marr Aspects (score 2/10)
- **Venus** — supported by Marr Aspects (score 2/10)
- **Jupiter** — supported by Marr Aspects (score 2/10)
- **2nd House cusp** — supported by Marr Aspects (score 2/10)
- **9th House cusp** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)
- **Lunar Node (North/South/unspecified)** — supported by Marr Aspects (score 2/10)
- **Part of Fortune** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**Medium-confidence symbolism.** Mercury, Mars, Neptune, Ascendant (1st House cusp), Midheaven (10th House cusp), 12th House cusp are supported by three of the four sources. 1 of these (12th House cusp) sits at the structural ceiling for its symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Saturn, Uranus, Pluto.

**Speculative / source-specific symbolism.** Sun (Marr Aspects only), Moon (Marr Aspects only), Venus (Marr Aspects only), Jupiter (Marr Aspects only), 2nd House cusp (Marr Aspects only), 3rd House cusp (Marr Aspects only), 5th House cusp (Other only), 9th House cusp (Marr Aspects only), 11th House cusp (Marr Aspects only), Lunar Node (North/South/unspecified) (Marr Aspects only), Part of Fortune (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** Uranus (in 10/11 example charts, 91%), Saturn (in 8/11 example charts, 73%) recur in a substantial share of Marr's worked examples without being singled out in POLARIS's Primary/Secondary list. This is not a direct contradiction — POLARIS's list is a short, deliberately curated selection rather than an exhaustive one, and no case was found anywhere in the compendium of a POLARIS-Primary symbol being *absent* from a substantial Marr Aspects sample. Read it as an emphasis gap, not a disagreement about relevance.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| 12th House cusp | Primary | — (out of scope) | Strong emphasis | 2 · 7/11 charts (64%) | 3/3 † | 1 / 11 | 10 | Very Strong (Core Symbol) |
| Mercury | Primary | 0 · 0/1 combos | Strong emphasis | 2 · 6/11 charts (55%) | 3/4 | 1 / 11 | 8 | Strong Symbol |
| Neptune | Primary | 0 · 0/1 combos | Strong emphasis | 2 · 6/11 charts (55%) | 3/4 | 1 / 11 | 8 | Strong Symbol |
| Ascendant (1st House cusp) | Primary | 0 · 0/1 combos | Strong emphasis | 2 · 6/11 charts (55%) | 3/4 | 1 / 11 | 8 | Strong Symbol |
| Midheaven (10th House cusp) | Primary | 0 · 0/1 combos | Strong emphasis | 2 · 7/11 charts (64%) | 3/4 | 1 / 11 | 8 | Strong Symbol |
| Mars | Secondary | 0 · 0/1 combos | Mentioned | 2 · 8/11 charts (73%) | 3/4 | 1 / 11 | 6 | Moderate (Relevant Symbol) |
| Saturn | Absent | 1 · 1/1 combos | Absent | 2 · 8/11 charts (73%) | 2/4 | 1 / 11 | 4 | Weak (Occasional Symbol) |
| Uranus | Absent | 1 · 1/1 combos | Absent | 2 · 10/11 charts (91%) | 2/4 | 1 / 11 | 4 | Weak (Occasional Symbol) |
| Pluto | Secondary | 0 · 0/1 combos | Absent | 2 · 7/11 charts (64%) | 2/4 | 1 / 11 | 4 | Weak (Occasional Symbol) |
| 3rd House cusp | Absent | — (out of scope) | Absent | 2 · 7/11 charts (64%) | 1/3 | 1 / 11 | 4 | Weak (Occasional Symbol) |
| 5th House cusp | Absent | — (out of scope) | Strong emphasis | 0 · 0/11 charts (0%) | 1/3 | 1 / 11 | 4 | Weak (Occasional Symbol) |
| Sun | Absent | 0 · 0/1 combos | Absent | 2 · 6/11 charts (55%) | 1/4 | 1 / 11 | 2 | Very Weak (Speculative Symbol) |
| Moon | Absent | 0 · 0/1 combos | Absent | 1 · 5/11 charts (45%) | 1/4 | 1 / 11 | 2 | Very Weak (Speculative Symbol) |
| Venus | Absent | 0 · 0/1 combos | Absent | 2 · 7/11 charts (64%) | 1/4 | 1 / 11 | 2 | Very Weak (Speculative Symbol) |
| Jupiter | Absent | 0 · 0/1 combos | Absent | 2 · 7/11 charts (64%) | 1/4 | 1 / 11 | 2 | Very Weak (Speculative Symbol) |
| 2nd House cusp | Absent | — (out of scope) | Absent | 1 · 1/11 charts (9%) | 1/3 | 1 / 11 | 2 | Very Weak (Speculative Symbol) |
| 9th House cusp | Absent | — (out of scope) | Absent | 1 · 3/11 charts (27%) | 1/3 | 1 / 11 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 2/11 charts (18%) | 1/3 | 1 / 11 | 2 | Very Weak (Speculative Symbol) |
| Lunar Node (North/South/unspecified) | Absent | 0 · 0/1 combos | Absent | 1 · 2/11 charts (18%) | 1/4 | 1 / 11 | 2 | Very Weak (Speculative Symbol) |
| Part of Fortune | — (out of scope) | 0 · 0/1 combos | Absent | 1 · 2/11 charts (18%) | 1/3 | 1 / 11 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **12th House cusp**: tier_score = 10 (n_juan_combos_total=1, n_marr_examples_total=11)  |  **5th House cusp**: tier_score = 4 (n_juan_combos_total=1, n_marr_examples_total=11) — *looked up independently; no combined score is produced for this pairing.*
- **12th House cusp**: tier_score = 10 (n_juan_combos_total=1, n_marr_examples_total=11)  |  **Part of Fortune**: tier_score = 2 (n_juan_combos_total=1, n_marr_examples_total=11) — *looked up independently; no combined score is produced for this pairing.*
- **Mercury**: tier_score = 8 (n_juan_combos_total=1, n_marr_examples_total=11)  |  **Part of Fortune**: tier_score = 2 (n_juan_combos_total=1, n_marr_examples_total=11) — *looked up independently; no combined score is produced for this pairing.*
- **5th House cusp**: tier_score = 4 (n_juan_combos_total=1, n_marr_examples_total=11)  |  **Sun**: tier_score = 2 (n_juan_combos_total=1, n_marr_examples_total=11) — *looked up independently; no combined score is produced for this pairing.*

---

## 39. Gambling Loss

*Category: Fortune — loss through chance or speculation*

### 1. Event Overview

The negative counterpart to Gambling Gain, sharing a 'Losses'-style signature: Uranus in speculative loss, Neptune and Mercury in bankruptcy-type loss. As with Gambling Gain, only one worked example survives, so the empirical base is thin.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Mars, Saturn, Uranus, Neptune, Pluto
- Houses/Angles mentioned: Ascendant (1st House cusp), Midheaven (10th House cusp), 2nd House cusp, 5th House cusp
- Nodes/Points mentioned: North Node (Ascending)
- **Primary** (highest POLARIS confidence): Mars, Saturn, Uranus, Neptune, Ascendant (1st House cusp), Midheaven (10th House cusp), 2nd House cusp, 5th House cusp
- **Secondary**: Pluto, North Node (Ascending)
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- *No data available from this source* (the compendium explicitly marks this entry “None”).

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: The negative counterpart to Gambling Gain, sharing a 'Losses'-style signature: Uranus in speculative loss, Neptune and Mercury in bankruptcy-type loss. As with Gambling Gain, only one worked example survives, so the empirical base is thin.
- Points referenced: Mercury (mentioned), Uranus (mentioned), Neptune (mentioned), Ascendant (1st House cusp) (mentioned), Midheaven (10th House cusp) (mentioned), 2nd House cusp (mentioned), 5th House cusp (mentioned)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **1 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- **Low sample size:** only 1 worked example available for this event in total — frequencies quoted below (and the corresponding tier_score contributions) are drawn from a very small pool and should be read as suggestive rather than well-established (see `n_marr_examples_total` on each symbol record).
- Most frequent points: Neptune (1/1, 100%), Venus (1/1, 100%), Pluto (1/1, 100%), 2nd House cusp (1/1, 100%), Uranus (1/1, 100%), Jupiter (1/1, 100%), 12th House cusp (1/1, 100%)

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Uranus** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **Neptune** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **2nd House cusp** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Other (score 6/10)
- **Midheaven (10th House cusp)** — supported by POLARIS, Other (score 6/10)
- **5th House cusp** — supported by POLARIS, Other (score 6/10)

**Occasional Symbols**
- **Pluto** — supported by POLARIS, Marr Aspects (score 4/10)
- **Mars** — supported by POLARIS (score 4/10)
- **Saturn** — supported by POLARIS (score 4/10)
- **Venus** — supported by Marr Aspects (score 2/10)
- **Jupiter** — supported by Marr Aspects (score 2/10)
- **12th House cusp** — supported by Marr Aspects (score 2/10)
- **Mercury** — supported by Other (score 2/10)
- **Lunar Node (North/South/unspecified)** — supported by POLARIS (score 2/10)

### 4. Consensus Analysis

**Medium-confidence symbolism.** Uranus, Neptune, 2nd House cusp are supported by three of the four sources. All of these sit at the structural ceiling for their symbol type — marked † in the table below — because Juan Combos carries no data at all for this event, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Pluto, Ascendant (1st House cusp), Midheaven (10th House cusp), 5th House cusp.

**Speculative / source-specific symbolism.** Mercury (Other only), Venus (Marr Aspects only), Mars (POLARIS only), Jupiter (Marr Aspects only), Saturn (POLARIS only), 12th House cusp (Marr Aspects only), Lunar Node (North/South/unspecified) (POLARIS only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** No clear-cut contradictions were found for this event: the four sources differ in *emphasis* and *coverage* (which is discussed above) rather than making opposing claims about any single symbol.

**Incomplete information.** Juan Combos (marked “None”) contribute no data to this event; the consolidated picture above rests on the remaining source(s) only.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Uranus | Primary | — (out of scope) | Mentioned | 1 · 1/1 charts (100%) | 3/3 † | 0 / 1 | 6 | Moderate (Relevant Symbol) |
| Neptune | Primary | — (out of scope) | Mentioned | 1 · 1/1 charts (100%) | 3/3 † | 0 / 1 | 6 | Moderate (Relevant Symbol) |
| 2nd House cusp | Primary | — (out of scope) | Mentioned | 1 · 1/1 charts (100%) | 3/3 † | 0 / 1 | 6 | Moderate (Relevant Symbol) |
| Ascendant (1st House cusp) | Primary | — (out of scope) | Mentioned | 0 · 0/1 charts (0%) | 2/3 | 0 / 1 | 6 | Moderate (Relevant Symbol) |
| Midheaven (10th House cusp) | Primary | — (out of scope) | Mentioned | 0 · 0/1 charts (0%) | 2/3 | 0 / 1 | 6 | Moderate (Relevant Symbol) |
| 5th House cusp | Primary | — (out of scope) | Mentioned | 0 · 0/1 charts (0%) | 2/3 | 0 / 1 | 6 | Moderate (Relevant Symbol) |
| Pluto | Secondary | — (out of scope) | Absent | 1 · 1/1 charts (100%) | 2/3 | 0 / 1 | 4 | Weak (Occasional Symbol) |
| Mars | Primary | — (out of scope) | Absent | 0 · 0/1 charts (0%) | 1/3 | 0 / 1 | 4 | Weak (Occasional Symbol) |
| Saturn | Primary | — (out of scope) | Absent | 0 · 0/1 charts (0%) | 1/3 | 0 / 1 | 4 | Weak (Occasional Symbol) |
| Venus | Absent | — (out of scope) | Absent | 1 · 1/1 charts (100%) | 1/3 | 0 / 1 | 2 | Very Weak (Speculative Symbol) |
| Jupiter | Absent | — (out of scope) | Absent | 1 · 1/1 charts (100%) | 1/3 | 0 / 1 | 2 | Very Weak (Speculative Symbol) |
| 12th House cusp | Absent | — (out of scope) | Absent | 1 · 1/1 charts (100%) | 1/3 | 0 / 1 | 2 | Very Weak (Speculative Symbol) |
| Mercury | Absent | — (out of scope) | Mentioned | 0 · 0/1 charts (0%) | 1/3 | 0 / 1 | 2 | Very Weak (Speculative Symbol) |
| Lunar Node (North/South/unspecified) | Secondary | — (out of scope) | Absent | 0 · 0/1 charts (0%) | 1/3 | 0 / 1 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Uranus**: tier_score = 6 (n_juan_combos_total=0, n_marr_examples_total=1)  |  **Mars**: tier_score = 4 (n_juan_combos_total=0, n_marr_examples_total=1) — *looked up independently; no combined score is produced for this pairing.*
- **Uranus**: tier_score = 6 (n_juan_combos_total=0, n_marr_examples_total=1)  |  **Lunar Node (North/South/unspecified)**: tier_score = 2 (n_juan_combos_total=0, n_marr_examples_total=1) — *looked up independently; no combined score is produced for this pairing.*
- **Neptune**: tier_score = 6 (n_juan_combos_total=0, n_marr_examples_total=1)  |  **Lunar Node (North/South/unspecified)**: tier_score = 2 (n_juan_combos_total=0, n_marr_examples_total=1) — *looked up independently; no combined score is produced for this pairing.*
- **Mars**: tier_score = 4 (n_juan_combos_total=0, n_marr_examples_total=1)  |  **Saturn**: tier_score = 4 (n_juan_combos_total=0, n_marr_examples_total=1) — *looked up independently; no combined score is produced for this pairing.*

---

## 40. Negative Travel

*Category: Travel — unfavorable journey*

### 1. Event Overview

The unfavorable counterpart to Positive Travel, sharing the same base symbolism (3rd/9th house cusp with the Moon, Mercury or Uranus; Jupiter for duration; Neptune for overseas/flight) but expressed through afflicted rather than harmonious aspects.

### 2. Source Summary

**POLARIS (Isaac Starkman)**
- Planets mentioned: Mercury, Mars, Saturn, Uranus, Neptune, Pluto
- Houses/Angles mentioned: Ascendant (1st House cusp), Midheaven (10th House cusp), 9th House cusp, 12th House cusp
- Nodes/Points mentioned: none
- **Primary** (highest POLARIS confidence): Mercury, Mars, Saturn, Uranus, Neptune, Pluto, Ascendant (1st House cusp), Midheaven (10th House cusp), 9th House cusp
- **Secondary**: 12th House cusp
- Unique observation: POLARIS never uses the Part of Fortune or a South-Node-specific point anywhere in the compendium, and this event follows that pattern.

**Juan Combos (Juan Estadella)**
- Planets/points referenced (by combination count): Neptune (1/3), Ascendant (1st House cusp) (1/3), Moon (1/3), Lunar Node (pole unspecified) (1/3), Jupiter (1/3), Saturn (1/3)
- Total pairwise combinations catalogued for this event: 3
- **Low sample size:** only 3 combinations catalogued for this event in total — any single symbol's Juan Combos percentage here rests on very little underlying data, and the tier_score for symbols resting mainly on this source should be read with that in mind (see `n_juan_combos_total` on each symbol record).
- Scope reminder: Juan Combos' method is a fixed roster of 14 points (Ascendant, Midheaven, the ten planets, the Lunar Node, and the Part of Fortune) tested pairwise; it never references the Descendant, the IC, or any minor house cusp for *any* event in the compendium, so silence on those points is a scope limit, not a finding.

**Other (Alexander Marr — short-form notes)**
- Paraphrased summary: The unfavorable counterpart to Positive Travel, sharing the same base symbolism (3rd/9th house cusp with the Moon, Mercury or Uranus; Jupiter for duration; Neptune for overseas/flight) but expressed through afflicted rather than harmonious aspects.
- Points referenced: Moon (mentioned), Mercury (mentioned), Jupiter (mentioned), Uranus (mentioned), Neptune (mentioned), 3rd House cusp (mentioned), 9th House cusp (mentioned)

**Marr Aspects (Alexander Marr — worked example charts)**
- Based on **16 worked example** directions/aspects drawn from named natal charts (not an authorial rule statement, but observed frequency across real cases).
- Most frequent points: Mars (12/16, 75%), Ascendant (1st House cusp) (11/16, 69%), Moon (11/16, 69%), Sun (10/16, 62%), 9th House cusp (10/16, 62%), Saturn (10/16, 62%), Uranus (10/16, 62%), Jupiter (9/16, 56%)
- Node detail: North Node in 0, South Node in 1, unspecified-pole Node in 5 of 16 examples.

### 3. Consolidated Symbolism

**Primary Symbols**
- *(none at this level for this event)*

**Secondary Symbols**
- **Neptune** — supported by POLARIS, Juan Combos, Other, Marr Aspects (score 8/10)
- **9th House cusp** — supported by POLARIS, Other, Marr Aspects (score 8/10)
- **Moon** — supported by Juan Combos, Other, Marr Aspects (score 6/10)
- **Mercury** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **Jupiter** — supported by Juan Combos, Other, Marr Aspects (score 6/10)
- **Saturn** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Uranus** — supported by POLARIS, Other, Marr Aspects (score 6/10)
- **Ascendant (1st House cusp)** — supported by POLARIS, Juan Combos, Marr Aspects (score 6/10)
- **Mars** — supported by POLARIS, Marr Aspects (score 6/10)
- **12th House cusp** — supported by POLARIS, Marr Aspects (score 6/10)

**Occasional Symbols**
- **Pluto** — supported by POLARIS, Marr Aspects (score 4/10)
- **Midheaven (10th House cusp)** — supported by POLARIS, Marr Aspects (score 4/10)
- **3rd House cusp** — supported by Other, Marr Aspects (score 4/10)
- **Lunar Node (North/South/unspecified)** — supported by Juan Combos, Marr Aspects (score 2/10)
- **Sun** — supported by Marr Aspects (score 2/10)
- **Venus** — supported by Marr Aspects (score 2/10)
- **Imum Coeli (4th House cusp)** — supported by Marr Aspects (score 2/10)
- **11th House cusp** — supported by Marr Aspects (score 2/10)
- **Part of Fortune** — supported by Marr Aspects (score 2/10)

### 4. Consensus Analysis

**High-confidence symbolism.** Neptune is corroborated by every source able to speak to it, and represent the least disputable symbolism for this event.

**Medium-confidence symbolism.** Moon, Mercury, Jupiter, Saturn, Uranus, Ascendant (1st House cusp), 9th House cusp are supported by three of the four sources. 1 of these (9th House cusp) sits at the structural ceiling for its symbol type — marked † in the table below — because Juan Combos' fixed roster never tests house cusps other than the Ascendant/Midheaven, a structural gap in what that source could test, not a comment on how strongly the remaining sources agree — check each symbol's tier_score above for that.

Supported by exactly two sources (moderate confidence): Mars, Pluto, Midheaven (10th House cusp), 3rd House cusp, 12th House cusp, Lunar Node (North/South/unspecified).

**Speculative / source-specific symbolism.** Sun (Marr Aspects only), Venus (Marr Aspects only), Imum Coeli (4th House cusp) (Marr Aspects only), 11th House cusp (Marr Aspects only), Part of Fortune (Marr Aspects only) — each resting on a single source and best treated as a minor refinement rather than load-bearing symbolism.

**Where the sources pull apart.** Moon (in 11/16 example charts, 69%), Sun (in 10/16 example charts, 62%) recur in a substantial share of Marr's worked examples without being singled out in POLARIS's Primary/Secondary list. This is not a direct contradiction — POLARIS's list is a short, deliberately curated selection rather than an exhaustive one, and no case was found anywhere in the compendium of a POLARIS-Primary symbol being *absent* from a substantial Marr Aspects sample. Read it as an emphasis gap, not a disagreement about relevance.

### 5. Evaluation Rules (Individual Symbol Scores)

| Symbol | POLARIS | Juan Combos | Other (Marr prose) | Marr Aspects (examples) | Sources | n (Juan combos / Marr examples) | Tier Score | Tier |
|---|---|---|---|---|---|---|---|---|
| Neptune | Primary | 1 · 1/3 combos | Mentioned | 2 · 8/16 charts (50%) | 4/4 | 3 / 16 | 8 | Strong Symbol |
| 9th House cusp | Primary | — (out of scope) | Mentioned | 2 · 10/16 charts (62%) | 3/3 † | 3 / 16 | 8 | Strong Symbol |
| Moon | Absent | 1 · 1/3 combos | Mentioned | 2 · 11/16 charts (69%) | 3/4 | 3 / 16 | 6 | Moderate (Relevant Symbol) |
| Mercury | Primary | 0 · 0/3 combos | Mentioned | 2 · 8/16 charts (50%) | 3/4 | 3 / 16 | 6 | Moderate (Relevant Symbol) |
| Jupiter | Absent | 1 · 1/3 combos | Mentioned | 2 · 9/16 charts (56%) | 3/4 | 3 / 16 | 6 | Moderate (Relevant Symbol) |
| Saturn | Primary | 1 · 1/3 combos | Absent | 2 · 10/16 charts (62%) | 3/4 | 3 / 16 | 6 | Moderate (Relevant Symbol) |
| Uranus | Primary | 0 · 0/3 combos | Mentioned | 2 · 10/16 charts (62%) | 3/4 | 3 / 16 | 6 | Moderate (Relevant Symbol) |
| Ascendant (1st House cusp) | Primary | 1 · 1/3 combos | Absent | 2 · 11/16 charts (69%) | 3/4 | 3 / 16 | 6 | Moderate (Relevant Symbol) |
| Mars | Primary | 0 · 0/3 combos | Absent | 2 · 12/16 charts (75%) | 2/4 | 3 / 16 | 6 | Moderate (Relevant Symbol) |
| 12th House cusp | Secondary | — (out of scope) | Absent | 2 · 8/16 charts (50%) | 2/3 | 3 / 16 | 6 | Moderate (Relevant Symbol) |
| Pluto | Primary | 0 · 0/3 combos | Absent | 1 · 2/16 charts (12%) | 2/4 | 3 / 16 | 4 | Weak (Occasional Symbol) |
| Midheaven (10th House cusp) | Primary | 0 · 0/3 combos | Absent | 1 · 4/16 charts (25%) | 2/4 | 3 / 16 | 4 | Weak (Occasional Symbol) |
| 3rd House cusp | Absent | — (out of scope) | Mentioned | 1 · 4/16 charts (25%) | 2/3 | 3 / 16 | 4 | Weak (Occasional Symbol) |
| Lunar Node (North/South/unspecified) | Absent | 1 · 1/3 combos | Absent | 1 · 6/16 charts (38%) | 2/4 | 3 / 16 | 2 | Very Weak (Speculative Symbol) |
| Sun | Absent | 0 · 0/3 combos | Absent | 2 · 10/16 charts (62%) | 1/4 | 3 / 16 | 2 | Very Weak (Speculative Symbol) |
| Venus | Absent | 0 · 0/3 combos | Absent | 1 · 7/16 charts (44%) | 1/4 | 3 / 16 | 2 | Very Weak (Speculative Symbol) |
| Imum Coeli (4th House cusp) | Absent | — (out of scope) | Absent | 1 · 6/16 charts (38%) | 1/3 | 3 / 16 | 2 | Very Weak (Speculative Symbol) |
| 11th House cusp | Absent | — (out of scope) | Absent | 1 · 3/16 charts (19%) | 1/3 | 3 / 16 | 2 | Very Weak (Speculative Symbol) |
| Part of Fortune | — (out of scope) | 0 · 0/3 combos | Absent | 1 · 2/16 charts (12%) | 1/3 | 3 / 16 | 2 | Very Weak (Speculative Symbol) |

† *Full agreement among applicable sources: every source able to address this symbol at all scored it 1 or 2 (see §3.2a of the Methodology). This is a statement about breadth of agreement, not strength — a daggered symbol can still carry a low tier_score if the sources that did weigh in did so weakly (all scoring 1 rather than 2). Always read the tier_score and the per-source 0/1/2 values above alongside this mark, not in place of it.*

### 6. Independent Symbol Lookup — Worked Examples

*Full framework: Methodology §3.5. This document reports each symbol's own tier_score independently and performs **no aspect-level combination of any kind**. The pairs below demonstrate looking up two symbols side by side — nothing here combines them into a single aspect-level number; a consumer of this data looks up each point separately for its own purposes.*

- **Neptune**: tier_score = 8 (n_juan_combos_total=3, n_marr_examples_total=16)  |  **12th House cusp**: tier_score = 6 (n_juan_combos_total=3, n_marr_examples_total=16) — *looked up independently; no combined score is produced for this pairing.*
- **Neptune**: tier_score = 8 (n_juan_combos_total=3, n_marr_examples_total=16)  |  **Part of Fortune**: tier_score = 2 (n_juan_combos_total=3, n_marr_examples_total=16) — *looked up independently; no combined score is produced for this pairing.*
- **9th House cusp**: tier_score = 8 (n_juan_combos_total=3, n_marr_examples_total=16)  |  **Part of Fortune**: tier_score = 2 (n_juan_combos_total=3, n_marr_examples_total=16) — *looked up independently; no combined score is produced for this pairing.*
- **12th House cusp**: tier_score = 6 (n_juan_combos_total=3, n_marr_examples_total=16)  |  **Pluto**: tier_score = 4 (n_juan_combos_total=3, n_marr_examples_total=16) — *looked up independently; no combined score is produced for this pairing.*
