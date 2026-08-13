"""
Step 3 (config module) tests: pssr_window_config.py integrity and drift
guards (spec docs/pssr_window_narrowing_design_v5.md sections 5.6, 6.1,
6.2).

Every knob in the section-6.2 table is pinned here, so a future edit to
either the config module or one of its source constants cannot silently
change the research control panel. Where the config imports an existing
codebase value, the test also asserts identity (`is`) with the source, not
just value equality, to keep the complete-by-reference rule (section 6.1)
from being violated by a copy-paste.
"""

from topo_astro.batch import pssr_window_config as cfg
from topo_astro.core.aspects import MAJOR_ASPECTS, PSSR_MOON_ORB_DEG, PSSR_PLANET_ORB_DEG
from topo_astro.significators.rules_data import Planet


def test_sweep_step_seconds():
    assert cfg.STEP_SECONDS == 60


def test_aspect_classes_are_majors_by_identity():
    assert cfg.ASPECT_CLASSES is MAJOR_ASPECTS


def test_orb_knobs_import_existing_constants_by_identity():
    assert cfg.ORB_FAST_SLOW_DEG is PSSR_PLANET_ORB_DEG
    assert cfg.ORB_MOON_CONJ_OPP_DEG is PSSR_MOON_ORB_DEG


def test_orb_knob_values():
    assert cfg.ORB_FAST_SLOW_DEG == 12 / 60
    assert cfg.ORB_MOON_CONJ_OPP_DEG == 32 / 60
    assert cfg.ORB_MOON_GENERAL_ARC_MIN == 18.0


def test_speed_floor_knobs():
    assert cfg.SPEED_FLOOR_ARC_MIN_PER_DAY == 30.0
    assert cfg.SPEED_FLOOR_USE_ABSOLUTE is True


def test_point_sets():
    assert cfg.FAST_SET == frozenset({Planet.MER, Planet.VEN, Planet.MAR})
    assert cfg.SLOW_SET == frozenset({Planet.JUP, Planet.SAT, Planet.URA, Planet.NEP, Planet.PLU, Planet.NNO})
    assert cfg.FAST_FAST_SET == frozenset({Planet.MER, Planet.VEN, Planet.MAR, Planet.MON})
    assert cfg.MOON == Planet.MON


def test_relevance_knobs():
    assert cfg.PAIR_RELEVANCE_MIN == "strong"
    assert cfg.STAGE2_TIER_FLOOR == 6


def test_consensus_and_margin_knobs():
    assert cfg.SAFETY_MARGIN_MINUTES == 30
    assert cfg.SINGLE_EVENT_FINE_RANGE_MINUTES == 60
    assert cfg.MAX_ASPECTS_PER_EVENT == "all"
    assert cfg.CONSENSUS_MAX_CARDINALITY is True
    assert cfg.CONSENSUS_TIE_BREAK == "earliest_start"


def test_planet_codes_are_the_string_names_used_by_aspect_finders():
    # Pins the convention that Planet.* are string names matching the
    # (p1/p2) names find_pssr_swiss_aspects and the compendium symbols use,
    # so the fast/slow/fast-fast sets line up with real aspect output.
    assert isinstance(Planet.MER, str)
    assert Planet.MON == "Moon"
    assert Planet.NNO == "Mean_Node"
    assert cfg.FAST_FAST_SET <= frozenset(Planet.__dict__.values()) | {Planet.MON}