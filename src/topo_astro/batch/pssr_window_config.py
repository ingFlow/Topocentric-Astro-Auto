"""
batch/pssr_window_config.py - the complete research control panel for the
PSSR window-narrowing feature.

Architectural layer: batch/ (the narrowing pipeline's configuration, new
for this feature). This module contains NO logic - only named constants,
imports and provenance comments - so a researcher sees the full decision
surface at a glance (spec: docs/pssr_window_narrowing_design_v5.md section
6).

Two sourcing rules (spec section 6.1):
    1. Where a value already exists in the codebase, this module imports
       it rather than duplicating it (complete-by-reference): dependency
       flows one way only - config -> existing code, pipeline -> config.
       Existing modules never import this module.
    2. Where a value is genuinely new (a v5 decision), it is defined here
       with a `# NEW - <section>, v5` comment and a one-line rationale.

Unit convention: orb knobs that import existing constants are expressed in
degrees; genuinely new orb knobs are expressed in arcminutes. The pipeline
converts internally to a single unit and never re-derives these values.
"""

from topo_astro.core.aspects import MAJOR_ASPECTS, PSSR_MOON_ORB_DEG, PSSR_PLANET_ORB_DEG
from topo_astro.significators.rules_data import Planet

# --- sweep (spec section 3.2) -------------------------------------------------

STEP_SECONDS = 60  # NEW - section 3.2, v5: sweep step over the window.

# --- aspect classes (spec section 3.4) ----------------------------------------

# EXISTING - core/aspects.py (majors table); applied via
# calculate_aspect(..., flag_major=True). Minors never gate; they are
# recorded in the near-miss ledger (spec section 9.4).
ASPECT_CLASSES = MAJOR_ASPECTS

# --- orbs (spec section 3.4) --------------------------------------------------

# EXISTING - inline literal in find_pssr_swiss_aspects, named & imported
# per spec section 5.5. Fast-to-slow orb for the coarse stage (degrees).
ORB_FAST_SLOW_DEG = PSSR_PLANET_ORB_DEG  # = 12/60

# EXISTING - same source. Moon orb for conjunctions/oppositions (degrees).
ORB_MOON_CONJ_OPP_DEG = PSSR_MOON_ORB_DEG  # = 32/60

# NEW - book section 1.5, v5: the Moon's general (non-conj/opp) orb, in
# arcminutes. Book p. 108: "For the Moon, a larger orb of 18' of arc is
# allowed (32' in conjunctions and oppositions)". The existing finder has
# no 18' value (it applies 32' to all Moon aspects), so this is a
# first-class new decision.
ORB_MOON_GENERAL_ARC_MIN = 18.0

# --- speed gate (spec section 3.5) --------------------------------------------

# NEW - book's 30-35'/day range, lower bound (book p. 117); user-confirmed
# (decision D1). The floor gates specificity, not correctness.
SPEED_FLOOR_ARC_MIN_PER_DAY = 30.0

# NEW - section 3.5, v5: retrograde handled by magnitude; a retrograde
# point at |speed| >= floor clears the gate.
SPEED_FLOOR_USE_ABSOLUTE = True

# --- point sets (spec section 3.3) --------------------------------------------

# EXISTING convention - Planet codes imported from significators.rules_data;
# membership per book section 1.8 (Moon excluded from the fast set).
FAST_SET = frozenset({Planet.MER, Planet.VEN, Planet.MAR})

# EXISTING convention - same import; membership per book section 1.8.
SLOW_SET = frozenset({Planet.JUP, Planet.SAT, Planet.URA, Planet.NEP, Planet.PLU, Planet.NNO})

# NEW - book section 1.10a + decision D6: fast-to-fast pairings are removed
# from stage 1 entirely and folded into the fine stage. Moon belongs here
# (it is fast in the fine-stage sense) even though it is not in FAST_SET.
FAST_FAST_SET = frozenset({Planet.MER, Planet.VEN, Planet.MAR, Planet.MON})

# EXISTING convention.
MOON = Planet.MON

# --- relevance (spec section 4.1 / decisions D3, D4) --------------------------

# NEW - user-confirmed (decision D3): only `strong` pairs gate stage 1;
# `weak` pairs are recorded in the near-miss ledger, never gating, and
# `excluded` pairs never gate.
PAIR_RELEVANCE_MIN = "strong"

# NEW - book section 1.10 proposal; decision D4: the fine stage's Moon arm
# requires the slow point's tier_score >= 6 (Moderate); an absent key
# fails closed.
STAGE2_TIER_FLOOR = 6

# --- consensus, margin and corroboration (spec sections 3.7-3.10) -------------

# NEW - sections 3.8/3.9, v5: the "window buffer" added around consensus
# ranges, clamped to the input window.
SAFETY_MARGIN_MINUTES = 30

# NEW - section 3.10, v5: corroboration tier boundary, measured pre-margin:
# a single corroborating event is `usable` only if its pre-margin range is
# <= this; otherwise the tier is `weak`.
SINGLE_EVENT_FINE_RANGE_MINUTES = 60

# NEW - section 3.7, v5: how many aspects per event the fine sweep
# consumes. "all" uses every hit; "1" reproduces the book's single-aspect
# practice.
MAX_ASPECTS_PER_EVENT = "all"

# NEW - sections 3.8/3.9, v5: max-cardinality partial-consensus fallback
# on/off (an empty full consensus falls back to the largest agreeing
# subset instead of the full window).
CONSENSUS_MAX_CARDINALITY = True

# NEW - section 3.8, v5: tie-break among equally large consensus subsets.
CONSENSUS_TIE_BREAK = "earliest_start"