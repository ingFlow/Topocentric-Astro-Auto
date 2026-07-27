"""
core/reserve.py - preserved, currently-unwired general-purpose astronomy
utilities, relocated out of the primary-directions technique module they
used to live in (pd_automate.py) since they aren't PD-specific.

None of these have a current caller anywhere in the application. They are
kept, not deleted, because they represent real, working formulas that
would be costly to reconstruct if a future feature needs them (e.g.
calc_alt/calc_lst for a visibility/rise-set feature, or if the reserved
kerykeion charting work in webapp/reserve/ is ever revisited).
"""
import math
import swisseph as swe


def add_suffix_to_tuples(tuples_list, suffix):
    return tuple(list(t) + [suffix] for t in tuples_list)


def calc_alt(lst_hours, ra_deg, decl_deg, latitude_deg):
    """
    Calculate the altitude of an astronomical object given LST, RA, Dec, and Latitude.

    Parameters:
    lst_str (str): Local Sidereal Time in HH:MM:SS format.
    ra_deg (float): Right Ascension in degrees.
    dec_deg (float): Declination in degrees.
    latitude_deg (float): Latitude of the observer in degrees.

    Returns:
    float: Altitude in degrees.
    """    
    lst_deg = lst_hours * 15.0
    h = lst_deg - ra_deg
    h = swe.degnorm(h)    #normalize degree

    lat_rad = math.radians(latitude_deg)
    decl_rad = math.radians(decl_deg)
    h_rad = math.radians(h)

    alt_rad = math.asin(math.sin(decl_rad) * math.sin(lat_rad) + 
                        math.cos(decl_rad) * math.cos(lat_rad) * math.cos(h_rad))

    alt_deg = math.degrees(alt_rad)

    return alt_deg


def calc_lst(jd, longitude):
    """
    Calculate the Local Sidereal Time (LST) and Greenwich Mean Sidereal Time (GMST)
    from Julian Date (JD) and longitude.

    Parameters:
    jd (float): Julian Date.
    longitude (float): Longitude of the location in degrees.

    Prints:
    - Julian Date
    - Greenwich Mean Sidereal Time
    - Local Sidereal Time
    """

    # Convert longitude to degrees, minutes, seconds format for display
    hemisphere = 'E' if longitude > 0 else 'W'
    longitude_deg = int(abs(longitude))
    longitude_min = int((abs(longitude) - longitude_deg) * 60)
    longitude_sec = int(((abs(longitude) - longitude_deg) * 60 - longitude_min) * 60)

    # Calculate Greenwich Mean Sidereal Time (GMST)
    gmst = 18.697374558 + 24.06570982441908 * (jd - 2451545)
    gmst = gmst % 24  # Convert to 24-hour format

    # Convert longitude to sidereal hours
    longitude_hours = longitude / 15.0

    # Calculate Local Sidereal Time (LST)
    lst = gmst + longitude_hours
    if lst < 0:
        lst += 24
    elif lst >= 24:
        lst -= 24
    
    return lst
