"""
Fixture manifest for the Phase 2 characterization test suite.

Defines, for each of the four reference people, which candidate radix
datetimes and which events are exercised by the golden-master tests.
This file is the single source of truth for "what gets tested" - both
the golden-file generator and the pytest test modules import from here,
so the two can never drift apart.

Person selection rationale (each targets a distinct timezone/DST scenario):
    - winston        Historical Local Mean Time, England (pre-standard-time)
    - richard_wagner  Historical Local Mean Time, Germany (pre-standard-time)
    - jacqui_onassis  Modern-era US Eastern time WITH Daylight Saving (July 1929)
    - beyonce         Modern IANA timezone, no DST (US Central, Houston)

For each person, "candidates" lists the specific radix datetimes tested
(the "left-hand list" entries a person would pick from in the interactive
app). "events" lists a representative subset of that person's real events,
chosen to span multiple EventType/GoodBadFlag categories rather than
testing every event x every technique x every candidate combinatorially.
"""

import os

FIXTURES_DIR = os.path.dirname(os.path.abspath(__file__))
BIRTH_DATA_DIR = os.path.join(FIXTURES_DIR, "birth_data")
GOLDEN_DIR = os.path.join(FIXTURES_DIR, "golden")
SAVED_SELECTIONS_DIR = os.path.join(FIXTURES_DIR, "saved_selections")

PEOPLE = {
    "beyonce": {
        "file": os.path.join(BIRTH_DATA_DIR, "beyonce.json"),
        "timezone_scenario": "modern_no_dst",
        "candidates": {
            # zero-width window -> the accepted DOB is the only meaningful candidate
            "actual_dob": "1981-09-04T02:28:44",
        },
        "event_datetimes": [
            "2012-01-07T12:00:00",  # BIRTH_DAUGHTER
            "2004-02-08T12:00:00",  # SUCCESS_ELECTED
            "2005-09-10T12:00:00",  # DIVORCE_SEPARATION
        ],
    },
    "winston": {
        "file": os.path.join(BIRTH_DATA_DIR, "winston.json"),
        "timezone_scenario": "historical_lmt_england",
        "candidates": {
            "actual_dob": "1874-11-30T01:04:00",
            "radix_start": "1874-11-30T00:00:00",
            "radix_end": "1874-11-30T03:00:00",
        },
        "event_datetimes": [
            "1911-05-28T12:00:00",  # BIRTH_SON
            "1963-10-19T12:00:00",  # DEATH_SISTER
            "1899-11-15T12:00:00",  # ARREST
        ],
    },
    "jacqui_onassis": {
        "file": os.path.join(BIRTH_DATA_DIR, "jacqui_onassis.json"),
        "timezone_scenario": "modern_dst_active",
        "candidates": {
            "actual_dob": "1929-07-27T20:00:00",
            "radix_end": "1929-07-28T20:00:00",
        },
        "event_datetimes": [
            "1953-09-12T12:00:00",  # MARRIAGE_ENGAGEMENT_FOR_FEMALE
            "1963-11-22T12:00:00",  # DEATH_HUSBAND_FRIEND
            "1960-11-25T12:00:00",  # BIRTH_SON
        ],
    },
    "richard_wagner": {
        "file": os.path.join(BIRTH_DATA_DIR, "richard_wagner.json"),
        "timezone_scenario": "historical_lmt_germany",
        "candidates": {
            "actual_dob": "1813-05-22T02:53:28",
            # dt_radix_start (1813-05-22T02:00:00, ~53 min before dt_actual_dob) is
            # included deliberately, not just for completeness: it is the ONE
            # candidate across all four people's full event lists (2,706
            # planet-direction checks searched) confirmed to naturally trigger
            # PD_Base's MD > SA quadrant-shift correction (Pluto, house 12) -
            # see test_pd_md_sa_correction.py. This is real "Bug #1" territory
            # per the Developer Manual, and this is the only known real-data
            # case that exercises it, so it stays in the fixture set even
            # though dt_actual_dob is technically the "more correct" birth time.
            "radix_start": "1813-05-22T02:00:00",
        },
        "event_datetimes": [
            "1836-07-07T12:00:00",  # MARRIAGE_ENGAGEMENT_FOR_MALE
            "1866-01-25T12:00:00",  # DEATH_WIFE_FRIEND
            "1865-04-10T12:00:00",  # BIRTH_SON
        ],
    },
}

# Every technique the golden-capture script exercises, by its aTechniqueType value
TECHNIQUES = [
    "PRIMARY_DIRECT",
    "SECONDARY_DIRECT",
    "PSSR",
    "TRANSIT",
    "SRA",
    "LUNAR",
    "HARMONICS",
    "NATAL",
]
