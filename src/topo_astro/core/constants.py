"""
core/constants.py - shared domain constants and low-level calculation
helpers used across every technique module and both operating modes (the
interactive Flask app and the offline batch/rectification tooling).

Responsibilities:
    - Domain vocabulary: PLANETS, ZODIAC_SIGNS, ALL_ASPECTS (the aspect
      angle/orb table), aTechniqueType (the canonical technique-type
      enum - see the note in batch/grid_engine.py for why this is the
      one and only technique-type enum that should ever be defined).
    - Radix-position calculation helpers used by every technique class:
      calc_planets_labelled, calc_planets_pof_houses_labelled,
      calc_planets_houses_labelled.
    - The altitude/geocoding cache (get_altitude), backed by a local
      altitudes.json file with a live network fallback.

This module has no knowledge of Flask, the batch-orchestration layer, or
any specific technique's internals - it is pure, reusable domain logic,
and every other module in this project either imports from here directly
or (in the case of the technique modules) builds directly on top of it.

Recent change (mechanical-move phase): parse_selection_file moved to
persistence/selections.py - it's the one thing this module used to hold
that wasn't really a "constant" or a calculation helper, and it deserved
its own clearly-labeled home.
"""
import swisseph as swe
import requests
import json
import os
import logging

ZODIAC_SIGNS = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
]

PLANETS = [
    'Sun', 'Moon', 'Mercury', 'Venus', 'Mars',
    'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Mean_Node'
]

HOUSES = ['H1','H2','H3','H4','H5','H6','H7','H8','H9','H10','H11','H12']    

ALT_FILE_PATH = "altitudes.json"
DATA_INPUT_DIR = "data/data_input"
SELECTIONS_DIR = "data/saved_selections"
CHARTS_DIR = "static/charts"

ALL_ASPECTS = {
    "sextile": (60,300),
    "conjunction": (0,360),
    "trine": (120,240),
    "square": (90, 270),
    "opposition": (180, 180),
    "45-semisquare": (45,315),
    "135-sesquisquare": (135,225),
    "30-semisextile": (30,330),
    "150-quincunx": (150, 210)
}

PLANET_ABBREVIATIONS = {
    "Sun": "SUN",
    "Moon": "MON",
    "Mercury": "MER",
    "Venus": "VEN",
    "Mars": "MAR",
    "Jupiter": "JUP",
    "Saturn": "SAT",
    "Uranus": "URA",
    "Neptune": "NEP",
    "Pluto": "PLU",
    "Mean_Node": "NNO", 
}

class aTechniqueType:
    PRIMARY_DIRECT = 0  #diff order of technique type specific to index.html
    SECONDARY_DIRECT = 1
    PSSR = 2
    TRANSIT = 3
    LUNAR = 4
    SRA = 5
    HARMONICS = 6
    NATAL = 7
    
    # For easily getting names or iterating
    @classmethod
    def get_all_techniques(cls):
        return {
            cls.PRIMARY_DIRECT: "PD",
            cls.SECONDARY_DIRECT: "Secondary",
            cls.PSSR: "PSSR",
            cls.TRANSIT: "Transit",
            cls.LUNAR: "Lunar",
            cls.SRA: "SRA",
            cls.HARMONICS: "Harmonics",
            cls.NATAL: "Natal",
        }

def get_technique_name(technique_index):
    return aTechniqueType.get_all_techniques().get(technique_index, "Unknown")

def calc_planets_labelled(jd_radix, label):
    planets = []
    
    for planet in range(0, len(PLANETS)):
        xx, _ = swe.calc_ut(jd_radix, planet)
        long = xx[0]

        planets.append((PLANETS[planet], long, label))    

    return planets

def calc_planets_houses_labelled(jd, label, planets_indexes_to_exclude, geopos):
    planets_houses = []
    
    for planet in range(0, len(PLANETS)):
        if (planet in planets_indexes_to_exclude):
            pass
        else:
            xx, _ = swe.calc_ut(jd, planet)
            long = xx[0]

            planets_houses.append((PLANETS[planet], long, label))  
   
    houses = swe.houses(jd, geopos[0], geopos[1], b'T')[0]
    for i in range(0, 12):
        planets_houses.append((f"H{i+1}", houses[i], label))
      
    return planets_houses

def calc_planets_pof_houses_labelled(jd_radix, geopos):
    rad_planets = []
    geo_latitude = geopos[0]
    geo_longitude = geopos[1]
    for planet in range(0, len(PLANETS)):
        xx, _ = swe.calc_ut(jd_radix, planet)
        long = xx[0]

        rad_planets.append((PLANETS[planet], long, "(r)")) 
    
    houses = swe.houses(jd_radix, geo_latitude, geo_longitude, b'T')
    ac = houses[0][0]
    sun_long = rad_planets[PLANETS.index('Sun')][1]
    moon_long = rad_planets[PLANETS.index('Moon')][1]
    pof_long = swe.degnorm(ac + moon_long - sun_long)
    rad_planets.append(('POF',pof_long,'(r)'))

    for house_no in range(0,11):
        rad_planets.append((f'H{house_no+1}',houses[0][house_no],'(r)'))

    return rad_planets

def get_precession(jd1, jd2):
    """Give the jd of the 2 dates you want the precession between"""
    aya1 = swe.get_ayanamsa_ut(jd1)
    aya2 = swe.get_ayanamsa_ut(jd2)
    
    return abs(aya1 - aya2)

def get_altitude(lat, lon):
    """Load stored altitude data from a JSON file."""
    if lat == None or lon == None:
        return None
    rlat = round(lat, 6)
    rlon = round(lon, 6)
    data = {}
    if os.path.exists(ALT_FILE_PATH):
        with open(ALT_FILE_PATH, "r") as f:
            data = json.load(f)
    key = f"{rlat},{rlon}"
    
    if key in data:
        return data[key]
    else:
        """Get altitude data from the Open-Elevation API."""
        url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
        response = requests.get(url)
        altitude = None
        if response.status_code == 200:
            altitude = response.json()["results"][0]["elevation"]
        data[key] = altitude
        
        """Save new altitude data to a JSON file."""
        with open(ALT_FILE_PATH, "w") as f:
            json.dump(data, f, indent=4)
            
        return data[key]