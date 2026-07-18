"""
Shared pytest configuration for the Phase 2 characterization suite.

Puts the application source on sys.path (controlled by the
TOPO_ASTRO_SOURCE_ROOT environment variable so this suite keeps working
unchanged across Phase 3's in-place edits and Phase 4's package move -
only the environment variable needs to change, not this file or any
test module), and provides small shared fixtures used across test files.
"""

import json
import os
import sys

import pytest

# --------------------------------------------------------------------
# Same convention as fixtures/generate_golden_files.py: point this at
# wherever the source currently lives. Defaults to the pre-Phase-4 flat
# layout; export TOPO_ASTRO_SOURCE_ROOT=/path/to/src/topo_astro (or run
# `pip install -e .` on the new package and delete this insert entirely)
# once Phase 4 lands.
# --------------------------------------------------------------------
SOURCE_ROOT = os.environ.get("TOPO_ASTRO_SOURCE_ROOT", "/home/claude/repo_extracted")
if SOURCE_ROOT not in sys.path:
    sys.path.insert(0, SOURCE_ROOT)

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
BIRTH_DATA_DIR = os.path.join(FIXTURES_DIR, "birth_data")
GOLDEN_DIR = os.path.join(FIXTURES_DIR, "golden")
SAVED_SELECTIONS_DIR = os.path.join(FIXTURES_DIR, "saved_selections")

sys.path.insert(0, FIXTURES_DIR)  # so `import fixture_manifest` works from test modules


@pytest.fixture(scope="session")
def source_root():
    return SOURCE_ROOT


@pytest.fixture(scope="session")
def golden_dir():
    return GOLDEN_DIR


def load_golden(person_key):
    """Loads the golden JSON captured by generate_golden_files.py for one person."""
    path = os.path.join(GOLDEN_DIR, f"{person_key}_techniques.json")
    with open(path) as f:
        return json.load(f)


def load_birth_data(person_key):
    path = os.path.join(BIRTH_DATA_DIR, f"{person_key}.json")
    with open(path) as f:
        return json.load(f)


@pytest.fixture(scope="session")
def all_golden():
    """All four people's golden data, keyed by person_key."""
    from tests.fixtures.fixture_manifest import PEOPLE
    return {p: load_golden(p) for p in PEOPLE}
