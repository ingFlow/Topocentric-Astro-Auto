import swisseph as swe
import julian
import pd_base as pd
import pssr_automate as pssr
import math
import aspects_base as aspects
from datetime import datetime, timedelta

class EventType:
    BIRTH_BROTHER = 0
    BIRTH_SISTER = 1
    BIRTH_SON = 2
    BIRTH_DAUGHTER = 3
    DEATH_FATHER_GRAND = 4
    DEATH_MOTHER_GRAND = 5
    SUCCESS = 6
    FAILURE = 7
    TRAVEL_POSITIVE = 8
    TRAVEL_NEGATIVE = 9
    ARREST = 10
    LOSSES = 11
    GRADUATION = 12
    MOVE_HOME = 13
    BIRTH_GRANDSON = 14
    BIRTH_GRANDDAUGHTER = 15
    MARRIAGE_FOR_MALE = 16
    MARRIAGE_FOR_FEMALE = 17
    CHILDS_MARRIAGE = 18
    DIVORCE_SEPARATION = 19
    DEATH_SON = 20
    DEATH_DAUGHTER = 21
    DEATH_WIFE = 22
    DEATH_HUSn]BAND = 23
    DEATH_BROTHER = 24
    DEATH_SISTER = 25
    DEATH = 26
    ASSASINATION_SUICIDE = 27
    PROMOTION_JOB = 28
    RESIGN_RETIRE = 29
    TRAVEL_OVERSEAS_POSITIVE = 30
    MOBILIZATION = 31
    DEMOBILIZATION_RELEASE = 32
    ACCIDENT = 33
    HOSPITALIZATION_ILLNESS = 34
    VIOLENCE = 35
    INTRIGUE = 36
    GAMBLING_LOSS = 37
    GAMBLING_GAIN = 38
    ARMY_PROMOTION = 39

class Planet:
    SUN = 'Sun'
    MON = 'Moon'
    MER = 'Mercury'
    VEN = 'Venus'
    MAR = 'Mars'
    JUP = 'Jupiter'
    SAT = 'Saturn'
    URA = 'Uranus'
    NEP = 'Neptune'
    PLU = 'Pluto'
    NNO = 'Mean_Node'

PLANETS = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Mean_Node']

event_rules = {
    EventType.BIRTH_BROTHER: (('MC', 'ASC'), (Planet.MER, Planet.JUP)),
    EventType.BIRTH_SISTER: (('MC', 'ASC'), (Planet.MON, Planet.MER, Planet.VEN)),
    EventType.BIRTH_SON: (('MC', 'ASC'), (Planet.MAR, Planet.SUN, Planet.JUP, Planet.NNO)),
    EventType.BIRTH_DAUGHTER: (('MC', 'ASC'), (Planet.VEN, Planet.MON, Planet.JUP, Planet.NNO)),
    EventType.DEATH_FATHER_GRAND: (('MC', 'ASC'), (Planet.SAT, Planet.SUN, Planet.NEP, Planet.PLU, Planet.MAR, Planet.NNO)),
    EventType.DEATH_MOTHER_GRAND: (('MC', 'ASC'), (Planet.MON, Planet.VEN, Planet.SAT, Planet.NEP, Planet.PLU, Planet.MAR, Planet.NNO)),
    EventType.SUCCESS: (('MC', 'ASC'), (Planet.SUN, Planet.JUP, Planet.MON, Planet.MER, Planet.URA, Planet.VEN)),
    EventType.FAILURE: (('MC', 'ASC'), (Planet.SAT, Planet.NEP, Planet.NNO, Planet.MAR, Planet.SUN)),
    EventType.TRAVEL_POSITIVE: (('MC', 'ASC'), (Planet.MON, Planet.MER, Planet.URA, Planet.JUP)),
    EventType.TRAVEL_NEGATIVE: (('MC', 'ASC'), (Planet.SAT, Planet.MAR, Planet.NEP, Planet.PLU, Planet.MER, Planet.URA)),
    EventType.ARREST: (('MC', 'ASC'), (Planet.SAT, Planet.URA, Planet.NEP, Planet.MAR, Planet.PLU, Planet.NNO)),
    EventType.LOSSES: (('MC', 'ASC'), (Planet.NEP, Planet.URA, Planet.MER, Planet.MAR, Planet.SAT)),
    EventType.GRADUATION: (('MC', 'ASC'), (Planet.MER, Planet.MON, Planet.JUP, Planet.SUN, Planet.URA, Planet.VEN)),
    EventType.MOVE_HOME: (('MC', 'ASC'), (Planet.MER, Planet.MON, Planet.NNO, Planet.JUP, Planet.SUN, Planet.VEN)),
    EventType.BIRTH_GRANDSON:(('MC','ASC'),(Planet.MAR, Planet.SUN, Planet.JUP, Planet.NNO)),
    EventType.BIRTH_GRANDDAUGHTER:(('MC','ASC'),(Planet.VEN,Planet.MON, Planet.JUP,Planet.NNO)),
    EventType.MARRIAGE_FOR_MALE:(('MC','ASC'),(Planet.VEN,Planet.MON,Planet.NNO,Planet.JUP)),
    EventType.MARRIAGE_FOR_FEMALE:(('MC','ASC'),(Planet.SUN,Planet.JUP,Planet.MAR,Planet.NNO)),
    EventType.CHILDS_MARRIAGE:(('MC','ASC'),(Planet.MER,Planet.VEN,Planet.MON,Planet.NNO,Planet.JUP,Planet.SUN)),
    EventType.DIVORCE_SEPARATION:(('MC','ASC'),(Planet.MAR,Planet.SAT,Planet.NEP,Planet.NNO,Planet.PLU)),
    EventType.DEATH_SON:(('MC','ASC'),(Planet.MAR,Planet.SAT,Planet.NEP,Planet.PLU,Planet.NNO)),
    EventType.DEATH_DAUGHTER:(('MC','ASC'),(Planet.VEN,Planet.MON,Planet.NEP,Planet.PLU,Planet.NNO)),
    EventType.DEATH_WIFE:(('MC','ASC'),(Planet.MON,Planet.VEN,Planet.SAT,Planet.NEP,Planet.PLU,Planet.NNO,Planet.MAR)),
    EventType.DEATH_HUSBAND:(('MC','ASC'),(Planet.SAT,Planet.SUN,Planet.NEP,Planet.PLU,Planet.NNO,Planet.MAR)),
    EventType.DEATH_BROTHER:(('MC','ASC'),(Planet.MER,Planet.MAR,Planet.SAT,Planet.NEP,Planet.PLU,Planet.NNO)),
    EventType.DEATH_SISTER:(('MC','ASC'),(Planet.MON,Planet.MER,Planet.VEN,Planet.MAR,Planet.SAT,Planet.NEP,Planet.PLU,Planet.NNO)),
    EventType.DEATH:(('MC','ASC'),(Planet.SAT,Planet.PLU,Planet.NEP,Planet.NNO,Planet.SUN)),
    EventType.ASSASINATION_SUICIDE:(('MC','ASC'),(Planet.SAT,Planet.PLU,Planet.URA,Planet.NEP,Planet.NNO,Planet.MAR)),
    EventType.PROMOTION_JOB:(('MC','ASC'),(Planet.SUN,Planet.JUP,Planet.MON,Planet.MER,Planet.URA,Planet.VEN)),
    EventType.RESIGN_RETIRE:(('MC','ASC'),(Planet.SAT,Planet.NEP,Planet.SUN,Planet.MAR,Planet.NNO)),
    EventType.TRAVEL_OVERSEAS_POSITIVE:(('MC','ASC'),(Planet.MON,Planet.MER,Planet.URA,Planet.JUP)),
    EventType.MOBILIZATION:(('MC','ASC'),(Planet.MAR,Planet.SAT,Planet.PLU)),
    EventType.DEMOBILIZATION_RELEASE:(('MC','ASC'),(Planet.JUP,Planet.VEN,Planet.URA)),
    EventType.ACCIDENT:(('MC','ASC'),(Planet.MAR,Planet.URA,Planet.SAT,Planet.MER)),
    EventType.HOSPITALIZATION_ILLNESS:(('MC','ASC'),(Planet.SAT,Planet.NEP,Planet.MAR)),
    EventType.VIOLENCE:(('MC','ASC'),(Planet.MAR,Planet.PLU,Planet.SAT,Planet.URA)),
    EventType.INTRIGUE:(('MC','ASC'),(Planet.NEP,Planet.MER)),
    EventType.GAMBLING_LOSS:(('MC','ASC'),(Planet.NEP,Planet.SAT,Planet.URA,Planet.MAR)),
    EventType.GAMBLING_GAIN:(('MC','ASC'),(Planet.JUP,Planet.VEN,Planet.URA)),
    EventType.ARMY_PROMOTION:(('MC','ASC'),(Planet.SUN,Planet.MAR,Planet.PLU,Planet.JUP,Planet.MON,Planet.MER,Planet.URA))
}

grid_acceptable_aspects = []

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
    
def count_all_acceptable_angles(event_id, str_all_aspects, count):
    "returns a couunt string of only acceptable angular direction aspects"
    list_aspects = str_all_aspects.split('\n')
    str_acceptable_aspects = ""

    for i in range(0, len(list_aspects)):
        if (list_aspects[i] != ''):
            aspect = list_aspects[i]
            if is_acceptable_angular_aspect(event_id, aspect):
                str_acceptable_aspects += aspect + '\n'
                count += 1

    return count, str_acceptable_aspects.rstrip()
    
def generate_grid_angular_aspects(start_time, end_time, increment_seconds, list_dt_events, jd_radix : julian, geo_positions: list[3]):
    global grid_acceptable_aspects
    temp_list_event = ['Time']
    for i in range(0,len(list_dt_events)):
        temp_list_event.append(f"Event{i}")
    temp_list_event.append('Count')
    grid_acceptable_aspects.append(temp_list_event)

    current_time = start_time
    increment = timedelta(seconds=increment_seconds)
    
    while current_time <= end_time:
        append_grid_acceptable_angles(list_dt_events, pssr.dt_gregorian_to_julian(current_time),geo_positions)
        current_time += increment
        with open("log_md_sa.txt", "a") as file:
            file.write(f"{current_time.strftime('%H:%M:%S')}---------------------------")

    # Handle the case where the last increment might exceed the end time
    if current_time > end_time:
        append_grid_acceptable_angles(list_dt_events, pssr.dt_gregorian_to_julian(current_time),geo_positions)
    with open("gridddd.txt", "w") as file:
        for time in grid_acceptable_aspects:
            file.write(f"{str(time)}\n")
    
def append_grid_acceptable_angles(list_dt_events, jd_radix : julian, geo_positions: list[3]):
    formatted_time = pssr.julian_to_gregorian(jd_radix).strftime('%H:%M:%S')
    temp_list_event = [formatted_time] 
    count = 0
    for dt_event, event_id in list_dt_events:
        str_rad_dir_aspects, str_rad_conv_aspects = pd_for_time_event(jd_radix, pssr.dt_gregorian_to_julian(dt_event), geo_positions)
        str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects
        count, str_acceptable_aspects = count_all_acceptable_angles(event_id, str_all_directed_aspects, count)

        if count > 0:
            temp_list_event.append(str_acceptable_aspects)
        else:
            temp_list_event.append('')
    temp_list_event.append(count)

    global grid_acceptable_aspects
    grid_acceptable_aspects.append(temp_list_event)
    
    return


def calc_all_pd_houses(JD_RADIX, jd_event, geo_latitude, geo_longitude):
    """returns 3 tuples with house cusps 1 to 12
    removed functionality for Hmd1 and Hmd2 (H1/H2)"""
    arc = pd.calc_arc(JD_RADIX, jd_event)
    radix = swe.houses(JD_RADIX, geo_latitude, geo_longitude, b'T')
    ramc = radix[1][2]
    radix = radix[0]
    e = pd.calculate_obliquity(JD_RADIX)

    directed = swe.houses_armc(ramc+arc, geo_latitude, e, b'T')[0]
    converse = swe.houses_armc(ramc-arc, geo_latitude, e, b'T')[0]

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
        lat = xx[1]
        ra = xx1[0]
        decl = xx1[1]
        
        cusps = swe.houses(JD_RADIX, geo_latitude, geo_longitude, b'T')[0]
        p_house = pd.get_housepos_manual(long, cusps)

        ac, mc, ramc = calc_radix_ac_mc_ramc(JD_RADIX,geo_latitude, geo_longitude)
        #quadrant = pd.get_point_quadrant(ac,mc,long)

        rad_planets.append((PLANETS[planet], long, "(r)"))    

        long_directed = pd.get_directed_from_data(JD_RADIX, jd_event, geo_latitude, decl, ra, ramc, mc, True, p_house, ac, long)
        dir_planets.append((PLANETS[planet], long_directed, "(d)"))
        
        long_conv = pd.get_directed_from_data(JD_RADIX, jd_event, geo_latitude, decl, ra, ramc, mc, False, p_house, ac, long)
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
    
    long_directed = pd.get_directed_from_data(JD_RADIX, jd_event, geo_latitude, decl, ra, ramc, mc, True, quadrant, ac, pof_long)
    long_conv = pd.get_directed_from_data(JD_RADIX, jd_event, geo_latitude, decl, ra, ramc, mc, False, quadrant, ac, pof_long)
    

    return pof_long, long_directed, long_conv

def calc_planet_house_pos(ramc, geo_lat, e, long, lat):
    hpos = swe.house_pos(ramc, geo_lat, e, (long,lat), b'T')
    
    return int(hpos)

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
    rad_houses = aspects.format_house_list(rad_houses, '(r)')
    dir_houses = aspects.format_house_list(dir_houses, '(d)')
    conv_houses = aspects.format_house_list(conv_houses, '(c)')
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
        file.write(f"Event Date: {str(julian.from_jd(jd))}, \tARC: {pssr.convert_dec_degrees_to_deg_min_sec(ARC_P)} \nRad Positions: {rad_planets}{rad_houses} \nDir Positions: {dir_planets}{dir_houses} \nCon Positions: {conv_planets}{conv_houses}")
        file.write(f"\nRAD-DIR ASPECTS: \n{str_aspects_rad_dir}")
        file.write(f"RAD-CONV ASPECTS: \n{str_aspects_rad_conv}\n")
