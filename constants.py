# constants.py
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
DATA_INPUT_DIR = 'data_input'
SELECTIONS_DIR = 'saved_selections'
CHARTS_DIR = 'static/charts'

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

def parse_selection_file(filepath):
    """Reads a saved selection file and parses it into a dictionary."""
    if not os.path.exists(filepath):
        logging.info(f"Selection file not found: {filepath}")
        return None

    loaded_selections = {}
    current_event = None
    current_technique = None
    line_number = 0

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_content in f:
                line_number += 1
                processed_line = line_content.rstrip()

                if not processed_line.startswith(' ') and processed_line.startswith("Event: "):
                    current_event = processed_line[len("Event: "):].strip()
                    if not current_event: # Handle empty event string if it occurs
                        logging.warning(f"Empty event string found at line {line_number} in {filepath}")
                        current_event = f"UNKNOWN_EVENT_{line_number}" # Placeholder
                    loaded_selections[current_event] = {}
                    current_technique = None
                elif processed_line.startswith("  ") and not processed_line.startswith("   ") and "Technique: " in processed_line:
                    if current_event:
                        try:
                            technique_part = processed_line.split("Technique: ", 1)[1]
                            current_technique = technique_part.strip()
                            if not current_technique: # Handle empty technique string
                                logging.warning(f"Empty technique string for event '{current_event}' at line {line_number} in {filepath}")
                                current_technique = f"UNKNOWN_TECHNIQUE_{line_number}" # Placeholder
                            loaded_selections[current_event][current_technique] = []
                        except IndexError:
                            logging.warning(f"Malformed Technique line for event '{current_event}' at line {line_number} in {filepath}: {processed_line}")
                            current_technique = None
                    else:
                        logging.warning(f"Found Technique line without preceding Event at line {line_number} in {filepath}: {processed_line}")
                        current_technique = None
                elif processed_line.startswith("    - "): # No need for 'not startswith("     ")' if structure is consistent
                    if current_event and current_technique:
                        # Ensure the technique key and list exist
                        if current_technique not in loaded_selections[current_event]:
                            logging.warning(f"Aspect found for event '{current_event}' but technique '{current_technique}' not initialized at line {line_number} in {filepath}. Initializing.")
                            loaded_selections[current_event][current_technique] = []

                        if isinstance(loaded_selections[current_event].get(current_technique), list):
                            aspect = processed_line[len("    - "):].strip()
                            if aspect: # Only add non-empty aspects
                                loaded_selections[current_event][current_technique].append(aspect)
                        else: # Should not happen if initialized correctly
                            logging.error(f"Critical parsing error: Technique list for '{current_event}' -> '{current_technique}' is not a list at line {line_number} in {filepath}.")
                    # else: Ignore aspect lines found out of proper context

        logging.info(f"Successfully parsed selections from {filepath}")
        # print("Parsed Dictionary:", loaded_selections) # Keep for debugging if needed
        return loaded_selections

    except Exception as e:
        logging.error(f"Error parsing selection file {filepath} at line ~{line_number}: {e}")
        return None