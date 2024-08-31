import swisseph as swe
import julian
import pd_base as pd
import pssr_automate as pssr
import math
import aspects_base as aspects

PLANETS = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Mean_Node']

event_rules = {
    1: (('MC', 'DC'),('Saturn', 'Uranus', 'Neptune')),
    2: (('IC', 'DC'),('Sun', 'Moon', 'POF')),
    3: (('IC', 'AC'),('Mars', 'Mercury', 'Venus')),
}

def is_acceptable_angular_aspect(event_id, str_aspect):
    """input the event id corresponding to dictionary and string with aspect as printed to textfile like this
    (Uranus,55.5 52,(r)) (Hmd1,325.600,(d)) (square,3')"""
    
    aspect_rules = event_rules[event_id]
    if not aspect_rules:
        return False  

    p1_d1_s1, p2_d2_s2, asp_orb = str_aspect.split(' ')
    p1, _, _ = p1_d1_s1.split(',')
    p1 = p1[1:]
    p2, _, _ = p2_d2_s2.split(',')
    p2 = p2[1:]

    angle_accept = aspect_rules[0]
    planet_accept = aspect_rules[1]

    if ((p1 in angle_accept) and (p2 in planet_accept)) or ((p2 in angle_accept) and (p1 in planet_accept)):
        return True
    
def count_all_acceptable_angles(event_id, str_all_aspects):
    "returns a string of only acceptable angular direction aspects"
    list_aspects = str_all_aspects.split('\n')
    str_acceptable_aspects = ""

    for i in range(0, len(list_aspects)):
        if (list_aspects[i] != ''):
            aspect = list_aspects[i]
            if is_acceptable_angular_aspect(event_id, aspect):
                str_acceptable_aspects += aspect + '\n'

    return str_acceptable_aspects
    

def calc_all_pd_houses(JD_RADIX, jd_event, geo_latitude, geo_longitude):
    
    arc = pd.calc_arc(JD_RADIX, jd_event)
    houses_ret = swe.houses(JD_RADIX, geo_latitude, geo_longitude, b'T')
    ramc = houses_ret [1][2]

    radix = pd.calc_houses_with_ramc(ramc, JD_RADIX, geo_latitude, "(r)")
    directed = pd.calc_houses_with_ramc(ramc+arc, JD_RADIX, geo_latitude, "(d)")
    converse = pd.calc_houses_with_ramc(ramc-arc, JD_RADIX, geo_latitude, "(c)")
    
    return radix, directed, converse
 
def calc_all_pd_planets(JD_RADIX, jd_event, geo_latitude, geo_longitude):
    dir_planets = []
    conv_planets = []
    rad_planets = []

    for i in range(0, len(PLANETS)):
        planet = i
        #print(f"planet: {PLANETS[planet]}")
        xx, _ = swe.calc_ut(JD_RADIX, planet)
        xx1, _ = swe.calc_ut(JD_RADIX, planet, swe.FLG_EQUATORIAL)
        long = xx[0]
        ra = xx1[0]
        decl = xx1[1]

        ac, mc, ramc = calc_radix_ac_mc_ramc(JD_RADIX,geo_latitude, geo_longitude)

        quadrant = pd.get_point_quadrant(ac,mc,long)

        rad_planets.append((PLANETS[planet], long, "(r)"))    

        long_directed = pd.get_directed_from_data(JD_RADIX, jd_event, geo_latitude, decl, ra, ramc, True, quadrant, ac, long)
        dir_planets.append((PLANETS[planet], long_directed, "(d)"))
        
        long_conv = pd.get_directed_from_data(JD_RADIX, jd_event, geo_latitude, decl, ra, ramc, False, quadrant, ac, long)
        conv_planets.append((PLANETS[planet], long_conv, "(c)"))

    return rad_planets, dir_planets, conv_planets

def calc_directed_POF(rad_planets, JD_RADIX, jd_event, geo_latitude, geo_longitude):
    """returns tuple (pof_rad, pof_directed, pof_converse)"""
    sun_index = PLANETS.index('Sun')
    moon_index = PLANETS.index('Moon')
    long_sun = rad_planets[sun_index][1]
    long_moon = rad_planets[moon_index][1]
    ac, mc, ramc = calc_radix_ac_mc_ramc(JD_RADIX, geo_latitude, geo_longitude)
    
    pof_long = (ac + long_moon - long_sun) % 360
    quadrant = pd.get_point_quadrant(ac, mc, pof_long)

    e = pd.calculate_obliquity(JD_RADIX)
    ra, decl, _ = swe.cotrans((pof_long, 0.0, 1), e)
    
    long_directed = pd.get_directed_from_data(JD_RADIX, jd_event, geo_latitude, decl, ra, ramc, True, quadrant, ac, pof_long)
    long_conv = pd.get_directed_from_data(JD_RADIX, jd_event, geo_latitude, decl, ra, ramc, False, quadrant, ac, pof_long)
    

    return pof_long, long_directed, long_conv

def calc_radix_ac_mc_ramc(JD_RADIX, geo_latitude, geo_longitude):
    """returns tuple of radix (ac, mc, ramc)"""
    houses = swe.houses(JD_RADIX, geo_latitude, geo_longitude, b'T')

    ac = houses[0][0]
    mc = houses[1][1]
    ramc = houses[1][2]
    
    return (ac, mc, ramc)

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

def pd_for_time_event(jd_radix : julian, jd : julian, geo_positions: list[3]):
    """
    Calculate the primary directions for all planets and houses

    Parameters:
    jd_radix (Julian): date and time (UT) of birth
    jd (Julian): date of event
    geo_positions (list[float]): [geo_lat, geo_long, altitude] of birth place, South/West negative pls
    orb (float): degrees decimal of orb allowed

    Returns:
    2 str with rad-dir and rad-conv aspects
    """
    JD_RADIX = jd_radix
    jd_event = jd
    geo_latitude = geo_positions[0]
    geo_longitude = geo_positions[1]

    swe.set_ephe_path('ephe')
    rad_houses, dir_houses, conv_houses = calc_all_pd_houses(JD_RADIX,jd_event, geo_latitude, geo_longitude)
    rad_planets, dir_planets, conv_planets = calc_all_pd_planets(JD_RADIX,jd_event, geo_latitude, geo_longitude)
    #add POF DATA
    rad_pof, dir_pof, conv_pof = calc_directed_POF(rad_planets, JD_RADIX, jd_event, geo_latitude, geo_longitude)
    rad_planets.append(('POF', rad_pof, "(r)"))
    dir_planets.append(('POF', dir_pof, "(d)"))
    conv_planets.append(('POF',conv_pof, "(c)"))
    #JOIN ARRAYS
    rad_positions = [*rad_planets, *rad_houses]
    dir_positions = [*dir_planets, *dir_houses]
    conv_positions = [*conv_planets, *conv_houses]

    str_aspects_rad_dir = aspects.find_pd_swiss_aspects(rad_positions, dir_positions)
    str_aspects_rad_conv = aspects.find_pd_swiss_aspects(rad_positions, conv_positions)
    
    return str_aspects_rad_dir, str_aspects_rad_conv

def pd_for_time_event_write_to_file(jd_radix : julian, jd : julian, geo_positions: list[3]):
    ARC_P = pd.calc_arc(jd_radix, jd)
    str_aspects_rad_dir, str_aspects_rad_conv =  pd_for_time_event(jd_radix, jd, geo_positions)

    with open("sweee_ephem_output.txt", "a") as file:
        #file.write(f"Event Date: {str(julian.from_jd(jd))}, \tARC: {pssr.convert_dec_degrees_to_deg_min_sec(ARC_P)} \nRad Positions: {rad_planets}{rad_houses} \nDir Positions: {dir_planets}{dir_houses} \nCon Positions: {conv_planets}{conv_houses}")
        file.write(f"\nRAD-DIR ASPECTS: \n{str_aspects_rad_dir}")
        file.write(f"RAD-CONV ASPECTS: \n{str_aspects_rad_conv}\n")
