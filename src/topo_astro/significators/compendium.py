"""
Compendium data-access layer for the PSSR window-narrowing feature.

Architectural layer: significator data/lookup (per the migration manual's
post-Phase-8 layout - significator data and lookups live under
significators/). This module is genuinely new (there was no compendium
loader before); it owns nothing else and relocates nothing.

Responsibilities (spec: docs/pssr_window_narrowing_design_v5.md section
5.1, lookup contracts in sections 4.2 and 4.3):

    - Load the two committed reference artifacts:
        compendium_reference/compendium_scoring_export_v2.json  (per-symbol
        tier data, the source of `tier_score`)
        compendium_reference/juan_combos_pairs_v1.json          (the Juan
        Combos pairwise table, the source of `pair_strength`)
      from a configurable base directory. The default resolves
      compendium_reference/ relative to the repository root (three levels
      up from this package), with an override parameter for tests.
    - `Compendium.event_title_for(event_id)`  - EventType -> compendium
      title mapping (spec 4.2): 40 EventTypes map to a compendium event,
      11 have no compendium event and map to None.
    - `Compendium.tier_score(event_id, symbol)` - per-symbol tier from the
      scoring JSON; None for absent keys (no data). Absent is never
      synthesized into a 0.
    - `Compendium.pair_strength(event_id, point_a, point_b)` - unordered
      canonical lookup into the pairwise table; returns
      "strong" | "weak" | "excluded" | None (None = absent / no data for
      that event, including the three marked-none events).
    - `SYMBOL_MAP_NAMED` - the codebase-named -> compendium-symbol mapping
      (spec 4.3). The two lookup methods accept either form: codebase
      named labels (e.g. 'Mean_Node', 'H1') are translated first, and
      compendium symbols (e.g. 'NODE_ANY', 'ASC') pass through.

Design notes:
    - Pure functions and immutable module constants only - no module-level
      mutable state (Phase 7 discipline). The loaded data lives on a
      Compendium instance created by Compendium.load(), so tests inject
      their own base directory and the pipeline holds one instance.
    - Fail-closed everywhere: an unknown event id, an unknown symbol, an
      absent symbol key, an unlisted pair, and the marked-none events all
      return None, never a guessed value. `absent` is distinct from
      `excluded` (the pairwise table's explicit counter-indicative tier).
    - 'Mean_Node' -> 'NODE_ANY' is the one genuinely lossy mapping in
      SYMBOL_MAP_NAMED (the codebase does not specify the node pole - v5
      finding F15) and is stated as such.
    - The angle/house entries are retained in SYMBOL_MAP_NAMED for future
      research (v5 section 9.1) even though the narrowing stages consume
      only planet/Node and data-side Sun/POF pairs.
"""

import json
import os

from topo_astro.significators.rules_data import EventType

# ---------------------------------------------------------------------------
# EventType -> compendium-title mapping (spec v5 section 4.2)
# ---------------------------------------------------------------------------

# The 40 EventTypes that have a compendium event, keyed by EventType member
# name. Verified against both reference files; see the spec's mapping table.
EVENT_TITLE_BY_NAME = {
    "BIRTH_BROTHER": "Birth of Brother",
    "BIRTH_SISTER": "Birth of Sister",
    "BIRTH_SON": "Birth of Son",
    "BIRTH_DAUGHTER": "Birth of Daughter",
    "BIRTH_GRANDSON": "Birth of Grandson",
    "BIRTH_GRANDDAUGHTER": "Birth of Granddaughter",
    "MARRIAGE_ENGAGEMENT_FOR_MALE": "Marriage for Male",
    "MARRIAGE_ENGAGEMENT_FOR_FEMALE": "Marriage for Female",
    "CHILDS_MARRIAGE": "Child's Marriage",
    "DIVORCE_SEPARATION": "Divorce or Separation",
    "DEATH_FATHER_GRAND": "Death of Father or Grandfather",
    "DEATH_MOTHER_GRAND": "Death of Mother or Grandmother",
    "DEATH_SON": "Death of Son",
    "DEATH_DAUGHTER": "Death of Daughter",
    "DEATH_WIFE_FRIEND": "Death of Wife or Female Friend",
    "DEATH_HUSBAND_FRIEND": "Death of Husband or Male Friend",
    "DEATH_BROTHER": "Death of Brother",
    "DEATH_SISTER": "Death of Sister",
    "DEATH": "Death",
    "ASSASINATION_SUICIDE": "Assasination or Suicide",
    "SUCCESS_ELECTED": "Success or Elected",
    "PROMOTION_JOB": "Job Promotion",
    "FAILURE_DEFEATED": "Failure or Defeat",
    "RESIGN_RETIRE": "Resign or Retire",
    "TRAVEL_OVERSEAS_POSITIVE": "Positive Travel Overseas",
    "TRAVEL_POSITIVE": "Positive Travel",
    "TRAVEL_NEGATIVE": "Negative Travel",
    "MOBILIZATION": "Mobilization",
    "DEMOBILIZATION_RELEASE": "Demobilization or Release",
    "ARREST": "Arrest",
    "ACCIDENT": "Accident",
    "HOSPITALIZATION_ILLNESS": "Hospitalization or Illness",
    "VIOLENCE": "Violence",
    "INTRIGUE": "Intrigue",
    "LOSSES": "Losses",
    "GAMBLING_LOSS": "Gambling Loss",
    "GAMBLING_GAIN": "Gambling Gain",
    "GRADUATION_PUBLICATION": "Graduation or Publication",
    "MOVE_HOME": "Move Home",
    "ARMY_PROMOTION": "Army Promotion",
}

# The 11 EventTypes with no compendium event - they cannot contribute any
# stage by construction and must resolve to None, never to a title.
NO_DATA_EVENT_NAMES = frozenset(
    {
        "POSITIVE_AC_MC",
        "NEGATIVE_AC_MC",
        "POSITIVE_2_8",
        "NEGATIVE_2_8",
        "POSITIVE_3_9",
        "NEGATIVE_3_9",
        "POSITIVE_5_11",
        "NEGATIVE_5_11",
        "POSITIVE_6_12",
        "NEGATIVE_6_12",
        "BLANK",
    }
)

# event_id (EventType value) -> EventType member name, built once from the
# rules_data class. Ints only; the pipeline passes EventType values.
_EVENT_TYPE_ID_TO_NAME = {
    value: name
    for name, value in vars(EventType).items()
    if isinstance(value, int) and name.isupper()
}

# ---------------------------------------------------------------------------
# Symbol-name mapping, codebase named labels -> compendium symbols
# (spec v5 section 4.3)
# ---------------------------------------------------------------------------

SYMBOL_MAP_NAMED = {
    "Sun": "SUN",
    "Moon": "MOON",
    "Mercury": "MERCURY",
    "Venus": "VENUS",
    "Mars": "MARS",
    "Jupiter": "JUPITER",
    "Saturn": "SATURN",
    "Uranus": "URANUS",
    "Neptune": "NEPTUNE",
    "Pluto": "PLUTO",
    "Mean_Node": "NODE_ANY",  # the one genuinely lossy mapping (v5 F15)
    "Node": "NODE_ANY",       # aspects.py's SLOW_PLANETS spelling
    "POF": "POF",
    "Fortune": "POF",         # aspects.py's RECEPTIVE_POINTS spelling
    "H1": "ASC",
    "H4": "IC",
    "H7": "DESC",
    "H10": "MC",
    "H2": "H2",
    "H3": "H3",
    "H5": "H5",
    "H6": "H6",
    "H8": "H8",
    "H9": "H9",
    "H11": "H11",
    "H12": "H12",
    # Identity entries for compendium-side names that also appear as
    # codebase labels (aspects.py's HOUSES / primary-directions code).
    "ASC": "ASC",
    "MC": "MC",
    "DESC": "DESC",
    "IC": "IC",
}

SCORING_FILE_NAME = "compendium_scoring_export_v2.json"
PAIRS_FILE_NAME = "juan_combos_pairs_v1.json"


def to_compendium_symbol(name):
    """Translate a codebase named label to its compendium symbol.

    Compendium symbols (e.g. 'MOON', 'NODE_ANY', 'ASC') pass through
    unchanged; unknown names also pass through - the lookups fail closed on
    them naturally (the symbol simply won't be found in the data).
    """
    return SYMBOL_MAP_NAMED.get(name, name)


def normalize_title(title):
    """Normalize a compendium title for matching (curly vs straight
    apostrophe - the reference files use a curly one in "Child's Marriage"
    while the spec table and this module use a straight one)."""
    return title.replace("\u2019", "'").replace("\u2018", "'")


def default_base_dir():
    """Resolve the default compendium_reference/ directory.

    Anchored to this file (src/topo_astro/significators/compendium.py):
    three levels up is the repository root, where compendium_reference/
    lives (it sits outside the installable package by design - v5 Step 0).
    """
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, os.pardir, os.pardir, os.pardir, "compendium_reference"))


class Compendium:
    """Immutable holder for the two compendium artifacts plus the lookups.

    Created via Compendium.load(base_dir) - the constructor takes the
    already-loaded JSON data so instances can be built in tests without
    touching the filesystem. Lookups are pure functions of the instance's
    data; there is no module-level mutable state.
    """

    def __init__(self, scoring_data, pairs_data):
        # Titles are normalized on load (curly vs straight apostrophe) so
        # the mapping's straight-apostrophe titles always match the data.
        self._scoring_by_title = {
            normalize_title(event["title"]): event for event in scoring_data["events"]
        }
        self._pairs_by_title = {
            normalize_title(title): entry for title, entry in pairs_data["events"].items()
        }

    @classmethod
    def load(cls, base_dir=None):
        """Load both artifacts from base_dir (default: default_base_dir()).

        Raises FileNotFoundError with a clear message if either artifact is
        missing, and ValueError if either file does not have the expected
        top-level shape.
        """
        base = base_dir if base_dir is not None else default_base_dir()
        scoring_path = os.path.join(base, SCORING_FILE_NAME)
        pairs_path = os.path.join(base, PAIRS_FILE_NAME)
        for path in (scoring_path, pairs_path):
            if not os.path.isfile(path):
                raise FileNotFoundError(f"compendium artifact not found: {path}")
        with open(scoring_path, encoding="utf-8") as f:
            scoring_data = json.load(f)
        with open(pairs_path, encoding="utf-8") as f:
            pairs_data = json.load(f)
        if "events" not in scoring_data or not isinstance(scoring_data["events"], list):
            raise ValueError(f"{SCORING_FILE_NAME}: expected top-level 'events' list")
        if "events" not in pairs_data or not isinstance(pairs_data["events"], dict):
            raise ValueError(f"{PAIRS_FILE_NAME}: expected top-level 'events' dict")
        return cls(scoring_data, pairs_data)

    def event_title_for(self, event_id):
        """Map an EventType value to its compendium title.

        Returns None for the 11 no-data EventTypes and for any event id
        that is not an EventType value (fail closed - a caller can never
        accidentally get a title for an event that has no compendium data).
        """
        name = _EVENT_TYPE_ID_TO_NAME.get(event_id)
        if name is None:
            return None
        return EVENT_TITLE_BY_NAME.get(name)

    def tier_score(self, event_id, symbol):
        """Per-symbol tier (0-10 int) for an event, or None for no data.

        None covers: a no-data/unknown event id, an unknown symbol, and an
        absent symbol key for that event in the scoring JSON. An absent key
        is 'no data', never synthesized into a 0 (v5 section 4.2).
        """
        title = self.event_title_for(event_id)
        if title is None:
            return None
        event = self._scoring_by_title.get(title)
        if event is None:
            return None
        record = event["symbols"].get(to_compendium_symbol(symbol))
        if record is None:
            return None
        return record["tier_score"]

    def pair_strength(self, event_id, point_a, point_b):
        """Juan Combos pair tier for an event: strong | weak | excluded.

        Lookup is unordered (the table's canonical A:B keys are sorted).
        Returns None when the event has no data (no-data EventType, the
        three marked-none events, or the pair simply isn't catalogued for
        that event). None means 'absent', which is distinct from the
        'excluded' tier.
        """
        title = self.event_title_for(event_id)
        if title is None:
            return None
        entry = self._pairs_by_title.get(title)
        if entry is None:
            return None
        a = to_compendium_symbol(point_a)
        b = to_compendium_symbol(point_b)
        a, b = sorted((a, b))
        pair = entry["pairs"].get(f"{a}:{b}")
        if pair is None:
            return None
        return pair["strength"]