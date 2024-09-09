import swisseph as swe
import julian
import pd_base as pd
import math
import aspects_base as aspects
from datetime import timedelta
import secondary_automate as secondary

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
    DEATH_HUSBAND = 23
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
i_level = 0

event_rules = {
    EventType.BIRTH_BROTHER: (('H4', 'H7'), (Planet.MER, Planet.JUP)),
    EventType.BIRTH_SISTER: (('H4', 'H7'), (Planet.MON, Planet.MER, Planet.VEN)),
    EventType.BIRTH_SON: (('H4', 'H1'), (Planet.MAR, Planet.SUN, Planet.JUP, Planet.NNO)),
    EventType.BIRTH_DAUGHTER: (('H4', 'H1'), (Planet.VEN, Planet.MON, Planet.JUP, Planet.NNO)),
    EventType.DEATH_FATHER_GRAND: (('H10','H1'), (Planet.SAT, Planet.SUN, Planet.NEP, Planet.PLU, Planet.MAR, Planet.NNO)),
    EventType.DEATH_MOTHER_GRAND: (('H4','H1'), (Planet.MON, Planet.VEN, Planet.SAT, Planet.NEP, Planet.PLU, Planet.MAR, Planet.NNO)),
    EventType.SUCCESS: (('H10','H1'), (Planet.SUN, Planet.JUP, Planet.MON, Planet.MER, Planet.URA, Planet.VEN)),
    EventType.FAILURE: (('H10','H1'), (Planet.SAT, Planet.NEP, Planet.NNO, Planet.MAR, Planet.SUN)),
    EventType.TRAVEL_POSITIVE: (('H10','H1'), (Planet.MON, Planet.MER, Planet.URA, Planet.JUP)),
    EventType.TRAVEL_NEGATIVE: (('H10','H1'), (Planet.SAT, Planet.MAR, Planet.NEP, Planet.PLU, Planet.MER, Planet.URA)),
    EventType.ARREST: (('H10','H1'), (Planet.SAT, Planet.URA, Planet.NEP, Planet.MAR, Planet.PLU, Planet.NNO)),
    EventType.LOSSES: (('H10','H1'), (Planet.NEP, Planet.URA, Planet.MER, Planet.MAR, Planet.SAT)),
    EventType.GRADUATION: (('H10','H1'), (Planet.MER, Planet.MON, Planet.JUP, Planet.SUN, Planet.URA, Planet.VEN)),
    EventType.MOVE_HOME: (('H4','H1'), (Planet.MER, Planet.MON, Planet.NNO, Planet.JUP, Planet.SUN, Planet.VEN)),
    EventType.BIRTH_GRANDSON:(('H4','H1'),(Planet.MAR, Planet.SUN, Planet.JUP, Planet.NNO)),
    EventType.BIRTH_GRANDDAUGHTER:(('H4','H1'),(Planet.VEN,Planet.MON, Planet.JUP,Planet.NNO)),
    EventType.MARRIAGE_FOR_MALE:(('H10','H7'),(Planet.VEN,Planet.MON,Planet.NNO,Planet.JUP)),
    EventType.MARRIAGE_FOR_FEMALE:(('H10','H7'),(Planet.SUN,Planet.JUP,Planet.MAR,Planet.NNO)),
    EventType.CHILDS_MARRIAGE:(('H10','H7'),(Planet.MER,Planet.VEN,Planet.MON,Planet.NNO,Planet.JUP,Planet.SUN)),
    EventType.DIVORCE_SEPARATION:(('H4','H7'),(Planet.MAR,Planet.SAT,Planet.NEP,Planet.NNO,Planet.PLU)),
    EventType.DEATH_SON:(('H4','H7'),(Planet.MAR,Planet.SAT,Planet.NEP,Planet.PLU,Planet.NNO)),
    EventType.DEATH_DAUGHTER:(('H4','H7'),(Planet.VEN,Planet.MON,Planet.NEP,Planet.PLU,Planet.NNO)),
    EventType.DEATH_WIFE:(('H4','H7'),(Planet.MON,Planet.VEN,Planet.SAT,Planet.NEP,Planet.PLU,Planet.NNO,Planet.MAR)),
    EventType.DEATH_HUSBAND:(('H4','H7'),(Planet.SAT,Planet.SUN,Planet.NEP,Planet.PLU,Planet.NNO,Planet.MAR)),
    EventType.DEATH_BROTHER:(('H4','H1'),(Planet.MER,Planet.MAR,Planet.SAT,Planet.NEP,Planet.PLU,Planet.NNO)),
    EventType.DEATH_SISTER:(('H4','H1'),(Planet.MON,Planet.MER,Planet.VEN,Planet.MAR,Planet.SAT,Planet.NEP,Planet.PLU,Planet.NNO)),
    EventType.DEATH:(('H10','H1'),(Planet.SAT,Planet.PLU,Planet.NEP,Planet.NNO,Planet.SUN)),
    EventType.ASSASINATION_SUICIDE:(('H10','H1'),(Planet.SAT,Planet.PLU,Planet.URA,Planet.NEP,Planet.NNO,Planet.MAR)),
    EventType.PROMOTION_JOB:(('H10','H1'),(Planet.SUN,Planet.JUP,Planet.MON,Planet.MER,Planet.URA,Planet.VEN)),
    EventType.RESIGN_RETIRE:(('H10','H1'),(Planet.SAT,Planet.NEP,Planet.SUN,Planet.MAR,Planet.NNO)),
    EventType.TRAVEL_OVERSEAS_POSITIVE:(('H10','H1'),(Planet.MON,Planet.MER,Planet.URA,Planet.JUP)),
    EventType.MOBILIZATION:(('H10','H1'),(Planet.MAR,Planet.SAT,Planet.PLU)),
    EventType.DEMOBILIZATION_RELEASE:(('H10','H1'),(Planet.JUP,Planet.VEN,Planet.URA)),
    EventType.ACCIDENT:(('H10','H1'),(Planet.MAR,Planet.URA,Planet.SAT,Planet.MER)),
    EventType.HOSPITALIZATION_ILLNESS:(('H10','H1'),(Planet.SAT,Planet.NEP,Planet.MAR)),
    EventType.VIOLENCE:(('H10','H1'),(Planet.MAR,Planet.PLU,Planet.SAT,Planet.URA)),
    EventType.INTRIGUE:(('H10','H1'),(Planet.NEP,Planet.MER)),
    EventType.GAMBLING_LOSS:(('H10','H1'),(Planet.NEP,Planet.SAT,Planet.URA,Planet.MAR)),
    EventType.GAMBLING_GAIN:(('H10','H1'),(Planet.JUP,Planet.VEN,Planet.URA)),
    EventType.ARMY_PROMOTION:(('H10','H1'),(Planet.SUN,Planet.MAR,Planet.PLU,Planet.JUP,Planet.MON,Planet.MER,Planet.URA))
}

secondary_and_house_rules = {
EventType.BIRTH_BROTHER: (('H3'),(Planet.SUN, Planet.MON, Planet.VEN, Planet.NNO, Planet.URA, Planet.PLU)),
EventType.BIRTH_SISTER: (('H3'), (Planet.SUN, Planet.JUP, Planet.NNO, Planet.URA, Planet.PLU)),
EventType.BIRTH_SON: (('H5'), (Planet.PLU, Planet.URA, Planet.MON, Planet.VEN, Planet.MER)),
EventType.BIRTH_DAUGHTER: (('H5'), (Planet.MAR, Planet.URA, Planet.PLU, Planet.SUN, Planet.MER)),
EventType.DEATH_FATHER_GRAND: (('H8', 'H12'), (Planet.URA, Planet.MON)),
EventType.DEATH_MOTHER_GRAND: (('H8','H12'), (Planet.SUN, Planet.URA)),
EventType.SUCCESS: (('H3'), (Planet.NNO)),
EventType.FAILURE: (('H3', 'H12'), (Planet.URA, Planet.MON, Planet.MER, Planet.PLU)),
EventType.TRAVEL_POSITIVE: (('H9'), (Planet.VEN, Planet.SUN, Planet.NNO)),
EventType.TRAVEL_NEGATIVE: (('H9','H12'), ()),
EventType.ARREST: (('H12','H3'), (Planet.SUN,Planet.MER)),
EventType.LOSSES: (('H2'), (Planet.PLU, Planet.NNO)),
EventType.GRADUATION: (('H3'), (Planet.NNO)),
EventType.MOVE_HOME: (('H3'), (Planet.URA)),
EventType.BIRTH_GRANDSON:(('H5','H9'), (Planet.PLU, Planet.URA,Planet.MON,Planet.VEN,Planet.MER)),
EventType.BIRTH_GRANDDAUGHTER:(('H5','H9'), (Planet.MAR,Planet.URA,Planet.PLU,Planet.SUN,Planet.MER)),
EventType.MARRIAGE_FOR_MALE:(('H5'), (Planet.MER,Planet.URA,Planet.MAR,Planet.SUN)),
EventType.MARRIAGE_FOR_FEMALE:(('H5'), (Planet.MER,Planet.URA,Planet.VEN,Planet.MON,Planet.PLU)),
EventType.CHILDS_MARRIAGE:(('H5'), (Planet.URA,Planet.MAR,Planet.PLU)),
EventType.DIVORCE_SEPARATION:(('H12'), (Planet.MER,Planet.URA,Planet.VEN,Planet.MON,Planet.PLU)),
EventType.DEATH_SON:(('H5','H8','H12'), (Planet.SUN,Planet.MER,Planet.URA)),
EventType.DEATH_DAUGHTER:(('H5','H8','H12'), (Planet.MAR, Planet.URA,Planet.MER)),
EventType.DEATH_WIFE:(('H5','H8','H12'), (Planet.URA)),
EventType.DEATH_HUSBAND:(('H5','H8','H12'), (Planet.URA)),
EventType.DEATH_BROTHER:(('H3','H8','H12'), (Planet.MON,Planet.SUN)),
EventType.DEATH_SISTER:(('H3','H8','H12'), ()),
EventType.DEATH:(('H8','H12'), (Planet.URA,Planet.MAR,Planet.MON)),
EventType.ASSASINATION_SUICIDE:(('H8','H12'), (Planet.MON)),
EventType.PROMOTION_JOB:(('H2','H3','H11'), (Planet.PLU,Planet.NNO)),
EventType.RESIGN_RETIRE:(('H3','H12'), (Planet.URA,Planet.MON,Planet.MER,Planet.PLU)),
EventType.TRAVEL_OVERSEAS_POSITIVE:(('H9'), (Planet.VEN,Planet.NEP,Planet.SUN,Planet.NNO)),
EventType.MOBILIZATION:(('H3','H12'), (Planet.MON,Planet.MER)),
EventType.DEMOBILIZATION_RELEASE:(('H3','H12'), (Planet.MON,Planet.MER,Planet.NNO)),
EventType.ACCIDENT:(('H3','H12'), (Planet.NEP,Planet.NNO,Planet.PLU,Planet.MON)),
EventType.HOSPITALIZATION_ILLNESS:(('H12'), (Planet.PLU,Planet.MON)),
EventType.VIOLENCE:(('H12'), (Planet.MER)),
EventType.INTRIGUE:(('H12'), (Planet.PLU,Planet.MAR)),
EventType.GAMBLING_LOSS:(('H2','H5'), (Planet.PLU,Planet.NNO)),
EventType.GAMBLING_GAIN:(('H2','H5'), (Planet.PLU)),
EventType.ARMY_PROMOTION:(('H2','H3','H11'), (Planet.VEN,Planet.NNO))
}

grid_acceptable_aspects = []
flag_pd_sec = None

def is_acceptable_angular_aspect(event_id, str_aspect):
    """input the event id corresponding to dictionary and string with aspect as printed to textfile like this
    (Uranus,55.5 52,(r)) (Hmd1,325.600,(d)) (square,3')"""
    
    aspect_rules = event_rules[event_id]
    house_aspect_rules = secondary_and_house_rules[event_id]
    if not aspect_rules:
        return False  
    
    p1_d1_s1, p2_d2_s2, asp_orb = str_aspect.split(' ')
    p1, _, _ = p1_d1_s1.split(',')
    p1 = p1[1:]
    p2, _, _ = p2_d2_s2.split(',')
    p2 = p2[1:]

    angle_accept = aspect_rules[0]
    planet_accept = aspect_rules[1]
    house_accept = house_aspect_rules[0]
    secondary_planets = house_aspect_rules[1]
    
    if i_level == 1:
        #angles to primary planets
        if ((p1 in angle_accept) and (p2 in planet_accept)) or ((p1 in planet_accept) and (p2 in angle_accept)):
            return True
    if i_level == 2:
        #house/angles to primary planets
        if (p1 in angle_accept) or (p1 in house_accept):
            if (p2 in planet_accept):
                return True
        if (p2 in angle_accept) or (p2 in house_accept):
            if (p1 in planet_accept):
                return True
    if i_level == 3:
        #house/angles to secondary planets
        if (p1 in angle_accept) or (p1 in house_accept):
            if (p2 in planet_accept) or (p2 in secondary_planets):
                return True
        if (p2 in angle_accept) or (p2 in house_accept):
            if (p1 in planet_accept) or (p1 in secondary_planets):
                return True
    if i_level == 4:
        #planets to planets primary
        if  (p1 in planet_accept) and (p2 in planet_accept):
            return True
    if i_level == 5:
        #planets to planets secondary
        if  (p1 in planet_accept) or (p1 in secondary_planets):
            if (p2 in planet_accept) or (p2 in secondary_planets):
                return True 

def count_event_acceptable_aspects(event_id, str_all_aspects, count):
    "returns a (count, string) of only acceptable angular direction aspects"
    list_aspects = str_all_aspects.split('\n')
    str_acceptable_aspects = ""

    for i in range(0, len(list_aspects)):
        if (list_aspects[i] != ''):
            aspect = list_aspects[i]
            if is_acceptable_angular_aspect(event_id, aspect):
                str_acceptable_aspects += aspect + '\n'
                count += 1

    return count, str_acceptable_aspects.rstrip()
    
def generate_grid_angular_aspects(filename, start_time, end_time, increment_seconds, list_dt_events, geo_positions: list[3], level: int, flag_pd_sec_in):
    """flag is true for pd false for sec
    level 1 = angles to prim planets
    level 2 = angles/houses to prim planets
    level 3 = angles/houses to prim/second planets
    level 4 = prim planets to prim planets
    level 5 = prim/second planets to prim/second planets"""

    global grid_acceptable_aspects, i_level, flag_pd_sec
    i_level = level
    flag_pd_sec = flag_pd_sec_in
    temp_list_event = ['Time']

    for i in range(0,len(list_dt_events)):
        temp_list_event.append(f"{i}: {list_dt_events[i][0].strftime('%Y-%m-%d')}")
    temp_list_event.append('Count')
    grid_acceptable_aspects.append(temp_list_event)
    
    current_time = start_time
    increment = timedelta(seconds=increment_seconds)
    
    while current_time <= end_time:
        print(f"working on: {current_time}....")
        append_grid_acceptable_angles(list_dt_events, julian.to_jd(current_time),geo_positions)
        current_time += increment

    # Handle the case where the last increment might exceed the end time
    if current_time > end_time:
        append_grid_acceptable_angles(list_dt_events, julian.to_jd(current_time),geo_positions)
    
    with open(f"{filename}", "w") as file:
        for time in grid_acceptable_aspects:
            file.write(f"{str(time)}\n")
    
def append_grid_acceptable_angles(list_dt_events, jd_radix : julian, geo_positions: list[3]):
    formatted_time = julian.from_jd(jd_radix).strftime('%H:%M:%S')
    temp_list_event = [formatted_time] 
    count = 0
    
    rad_houses_info = swe.houses(jd_radix, geo_positions[0], geo_positions[1], b'T')
    rad_planets_labelled = calc_natal_planets_labelled(jd_radix)
    rad_planets_equatorial = calc_rad_planets_equatorial(jd_radix)
    
    event_index = 0
    for dt_event, event_id in list_dt_events:
        if flag_pd_sec:
            str_rad_dir_aspects, str_rad_conv_aspects = pd_for_time_event(jd_radix, julian.to_jd(dt_event), geo_positions, rad_planets_labelled, rad_planets_equatorial, rad_houses_info)
            str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects   
        else:
            str_rad_n_prog_aspects, str_rad_n_reg_aspects = secondary.secondary_for_event(jd_radix, julian.to_jd(dt_event), geo_positions[0], geo_positions[1])
            str_all_directed_aspects = str_rad_n_prog_aspects + '\n' + str_rad_n_reg_aspects

        #count is incremented in next line 
        count, str_acceptable_aspects = count_event_acceptable_aspects(event_id, str_all_directed_aspects, count)

        if count > 0:
            temp_list_event.append(str_acceptable_aspects)
        else:
            temp_list_event.append(f"{str(event_index)}")
        event_index += 1

    temp_list_event.append(count)

    global grid_acceptable_aspects
    grid_acceptable_aspects.append(temp_list_event)    
    return

def calc_directed_pd_houses(JD_RADIX, jd_event, geo_latitude, rad_houses):
    """returns 2 tuples with house cusps 1 to 12 dir, conv
    removed functionality for Hmd1 and Hmd2 (H1/H2)"""
    arc = pd.calc_arc(JD_RADIX, jd_event)
    ramc = rad_houses[1][2]
    e = pd.calculate_obliquity(JD_RADIX)

    directed = swe.houses_armc(ramc+arc, geo_latitude, e, b'T')[0]
    converse = swe.houses_armc(ramc-arc, geo_latitude, e, b'T')[0]

    return directed, converse
 
def calc_directed_pd_planets(JD_RADIX, jd_event, geo_latitude, geo_longitude, rad_planets_equatorial):
    dir_planets = []
    conv_planets = []

    for planet in range(0, len(PLANETS)):
        long, ra, decl = rad_planets_equatorial[planet]
        cusps = swe.houses(JD_RADIX, geo_latitude, geo_longitude, b'T')[0]
        p_house = pd.get_housepos_manual(long, cusps)
        ac, mc, ramc = calc_radix_ac_mc_ramc(JD_RADIX,geo_latitude, geo_longitude)

        long_directed = pd.get_directed_from_data(JD_RADIX, jd_event, geo_latitude, decl, ra, ramc, mc, True, p_house, ac, long)
        dir_planets.append((PLANETS[planet], long_directed, "(d)"))
        
        long_conv = pd.get_directed_from_data(JD_RADIX, jd_event, geo_latitude, decl, ra, ramc, mc, False, p_house, ac, long)
        conv_planets.append((PLANETS[planet], long_conv, "(c)"))

    return dir_planets, conv_planets

def calc_natal_planets_labelled(jd_radix):
    rad_planets = []
    for planet in range(0, len(PLANETS)):
        xx, _ = swe.calc_ut(jd_radix, planet)
        long = xx[0]

        rad_planets.append((PLANETS[planet], long, "(r)"))    
    return rad_planets

def calc_rad_planets_equatorial(jd_radix):
    """returns array with (long, ra, decl) for each of PLANETS(list) following PLANETS INDEXING"""
    planet_info = [] 
    for planet in range(0, len(PLANETS)):
        xx, _ = swe.calc_ut(jd_radix, planet)
        xx1, _ = swe.calc_ut(jd_radix, planet, swe.FLG_EQUATORIAL)
        long = xx[0]
        ra = xx1[0]
        decl = xx1[1]
        planet_info.append((long, ra, decl))

    return planet_info

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

def pd_for_time_event(jd_radix : julian, jd : julian, geo_positions: list[3], rad_planets_labelled, rad_planets_equatorial, rad_houses_info):
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
    dir_houses, conv_houses = calc_directed_pd_houses(JD_RADIX,jd_event, geo_latitude, rad_houses_info)
    rad_houses = rad_houses_info[0]
    
    rad_houses = aspects.format_house_list(rad_houses, '(r)')
    dir_houses = aspects.format_house_list(dir_houses, '(d)')
    conv_houses = aspects.format_house_list(conv_houses, '(c)')
    dir_planets, conv_planets = calc_directed_pd_planets(JD_RADIX,jd_event, geo_latitude, geo_longitude, rad_planets_equatorial)
    #add POF  DATA
    rad_pof, dir_pof, conv_pof = calc_directed_POF(rad_planets_labelled, JD_RADIX, jd_event, geo_latitude, geo_longitude)
    rad_planets_labelled.append(('POF', rad_pof, "(r)"))
    dir_planets.append(('POF', dir_pof, "(d)"))
    conv_planets.append(('POF',conv_pof, "(c)"))
    #JOIN ARRAYS
    rad_positions = [*rad_planets_labelled, *rad_houses]
    dir_positions = [*dir_planets, *dir_houses]
    conv_positions = [*conv_planets, *conv_houses]

    str_aspects_rad_dir = aspects.find_pd_swiss_aspects(rad_positions, dir_positions)
    str_aspects_rad_conv = aspects.find_pd_swiss_aspects(rad_positions, conv_positions)
    
    return str_aspects_rad_dir, str_aspects_rad_conv

def count_aspect_groups_txt(filename):
    opp_conj = ['opposition', 'conjunction']
    sqr_tri_sext = ['square', 'trine', 'sextile']
    results = []

    with open(filename, 'r') as infile:
        for line in infile:
            parts = eval(line.strip())
            time = parts[0]
            aspects = parts[1:-1]
            count = parts[-1]

            opp_conj_count = 0
            sqr_tri_sext_count = 0
            minor_count = 0

            for all_aspect in aspects:
                if all_aspect:
                    aspect = all_aspect.split(', ')
                    for asp in aspect:
                        if asp[0] == '(':
                            if '\n' in asp:
                                asp_lines = asp.split('\n')
                                for line in asp_lines:
                                    asp = line.split(' ')[2]

                                    if ('sesquisquare' in asp) or ('semisquare' in asp) or ('semisextile' in asp) or ('quincunx' in asp):
                                        minor_count += 1
                                    elif ('opposition' in asp) or ('conjunction' in asp):
                                        opp_conj_count += 1
                                    elif ('square' in asp) or ('sextile' in asp) or ('trine' in asp):
                                        sqr_tri_sext_count += 1
                            else:
                                asp = asp.split(' ')[2]

                                if ('sesquisquare' in asp) or ('semisquare' in asp) or ('semisextile' in asp) or ('quincunx' in asp):
                                    minor_count += 1
                                elif ('opposition' in asp) or ('conjunction' in asp):
                                    opp_conj_count += 1
                                elif ('square' in asp) or ('sextile' in asp) or ('trine' in asp):
                                    sqr_tri_sext_count += 1

            results.append([f"{time}, {count}, opp/conj: {opp_conj_count}", f"sqr/tri/sext: {sqr_tri_sext_count}", f"major: {sqr_tri_sext_count+opp_conj_count}", f"minor: {minor_count}"])                
    print(results)
    with open(f"{filename}COUNTASCMC.txt", 'w') as outfile:
        for result in results:
            outfile.write(str(result) + '\n')