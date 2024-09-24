import swisseph as swe
import julian
from datetime import datetime, timedelta
import aspects_base as aspects
import pssr_swiss_auto as ps

class LunarType:
    LUNAR = 0
    KINETIC = 1
    AS_LUNAR = 2

ZODIAC_SIGNS = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", 
                "scorpio","sagittarius", "capricorn", "aquarius", "pisces"]
PLANETS = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Mean_Node']

def calc_bija_days(secondary_days_dec):
    base_bija_seconds_per_year = 3*60 + 55.9
    bija_seconds = secondary_days_dec * base_bija_seconds_per_year
    bija_days = bija_seconds / 86400
    return bija_days

def calc_kinetic_dir_conv(jd_radix, jd_event, precession, conv_precession):
    jd_diff = abs(jd_radix - jd_event)
    days_diff = jd_diff / 365.2422
    jd_prog_prelim = jd_radix + days_diff
    xx, _ = swe.calc_ut(jd_prog_prelim, swe.MOON)
    prog_moon_prelim = xx[0]
    jd_search_date = julian.to_jd(julian.from_jd(jd_event) - timedelta(days=30))
    jd_return_direct = swe.mooncross_ut(prog_moon_prelim, jd_search_date)
    jd_return_after_first_direct = swe.mooncross_ut(prog_moon_prelim, jd_search_date)
    #rare case where it reaches degree literally that day or something
    if jd_return_after_first_direct <= jd_event:
        jd_return_direct = jd_return_after_first_direct
    jd_return_direct = int(jd_return_direct) #make it midday of whatever jd
    
    sidt_radix = swe.sidtime(int(jd_radix))
    sidt_event = swe.sidtime(jd_return_direct)
    st_diff = (sidt_event - sidt_radix)/24
    days_years_diff = julian.from_jd(jd_event).year - julian.from_jd(jd_radix).year
    days_years_diff += st_diff

    bija_days = calc_bija_days(days_diff)
    days_years_diff -= bija_days

    jd_prog = jd_radix + days_years_diff
    xx, _ = swe.calc_ut(jd_prog, swe.MOON)
    prog_moon_long = xx[0] + precession

    jd_reg = jd_radix - days_years_diff
    xx, _ = swe.calc_ut(jd_reg, swe.MOON)
    reg_moon_long = xx[0] - conv_precession

    return prog_moon_long, reg_moon_long

def get_point_long_dir_conv(ltype: LunarType, jd_radix, jd_event, geopos, geopos_natal):
    jd_conv_event = jd_radix - (abs(jd_radix-jd_event))
    xx, _ = swe.calc_ut(jd_radix, swe.MOON)
    moon_long = xx[0]    
    rad_aya = swe.get_ayanamsa_ut(jd_radix)
    event_aya = swe.get_ayanamsa_ut(jd_event)
    precession = abs(rad_aya - event_aya)
    moon_precessed_long = moon_long + precession

    event_aya = swe.get_ayanamsa_ut(jd_conv_event)
    conv_precession = abs(rad_aya - event_aya)
    moon_conv_precessed_long = moon_long - conv_precession

    #jd_new_rad_dir = swe.mooncross_ut(moon_precessed_long, jd_radix)
    #jd_shifted_rad_dir = julian.to_jd(julian.from_jd(jd_radix) - timedelta(days=10))
    #jd_new_rad_conv = swe.mooncross_ut(moon_conv_precessed_long, jd_shifted_rad_dir)

    if ltype == LunarType.LUNAR:
        #radical moon
        return moon_precessed_long, moon_conv_precessed_long
    if ltype == LunarType.KINETIC:
        #radical progressed moon
        return calc_kinetic_dir_conv(jd_radix,jd_event,precession,conv_precession)

    if ltype == LunarType.AS_LUNAR:
        #radical ac
        houses = swe.houses(jd_radix, geopos_natal[0], geopos_natal[1], b'T')
        ac_dir = houses[0][0] + precession
        
        houses = swe.houses(jd_radix, geopos_natal[0], geopos_natal[1], b'T')
        ac_conv = houses[0][0] - precession
        return ac_dir, ac_conv
        
def calc_planets_ac_mc(jd_radix, geopos):
    """returns list starting with ac them mc then rest of planets"""
    planets = []

    houses = swe.houses(jd_radix, geopos[0], geopos[1], b'T')
    ac = houses[0][0]
    mc = houses[1][1]
    planets.append(('ac',ac))
    planets.append(('mc',mc))
    
    for planet in range(0, len(PLANETS)):
        xx, _ = swe.calc_ut(jd_radix, planet)
        long = xx[0]

        planets.append((PLANETS[planet], long))    

    return planets

def calc_planets_near_angles(list_planets, orb):
    """returns list of tuple like ac, conj, jup, 3
    ac, opp, sat, 4
    mc, conj, ven, 5 etc."""
    planets_near_angle = []
    ac = list_planets[0][1]
    mc = list_planets[1][1]
    planets = list_planets[2:]

    for p, d in planets:
        aspect = aspects.calculate_aspect(ac, d, orb, True)
        if aspect:
            asp, asp_orb = aspect
            if asp == 'conjunction' or asp == 'opposition':
                str = (f'(ac,{ac:.2f}) ({p},{d:.2f}) ({asp},{asp_orb * 60:.0f}\')\n')
                planets_near_angle.append(str)
    for p, d in planets:
        aspect = aspects.calculate_aspect(mc, d, orb, True)
        if aspect:
            asp, asp_orb = aspect
            if asp == 'conjunction' or asp == 'opposition':
                str = (f'(mc,{mc:.2f}) ({p},{d:.2f}) ({asp},{asp_orb * 60:.0f}\')\n')
                planets_near_angle.append(str)
    return planets_near_angle

def calc_lunar_for_date(dt_radix, dt_event, geopos, geopos_natal, ltype: LunarType, orb):
    """returns list of (name_cyclic, [list_planets_near_angles])
    list_planets_near_angles format is (planet, aspect, orb)"""
    jd_radix = julian.to_jd(dt_radix)
    jd_event = julian.to_jd(dt_event)
    
    #lunar computation
    point_long_dir, point_long_conv = get_point_long_dir_conv(ltype,jd_radix,jd_event,geopos, geopos_natal)
    jd_search_date = julian.to_jd(dt_event - timedelta(days=30))
    
    jd_return_direct = swe.mooncross_ut(point_long_dir, jd_search_date)
    jd_return_after_first_direct = swe.mooncross_ut(point_long_dir, jd_return_direct)
    #rare case where it reaches degree literally that day or something
    if jd_return_after_first_direct <= jd_event:
        jd_return_direct = jd_return_after_first_direct

    #DEMI
    if abs(jd_return_direct - jd_event) > 14:
        point_long_dir = swe.degnorm(point_long_dir + 180)
        jd_demi_return_direct = swe.mooncross_ut(point_long_dir, jd_return_direct)
    else:
        jd_demi_return_direct = None
    
    jd_conv_date = jd_radix - abs(jd_return_direct - jd_radix)
    dt_conv_date = julian.from_jd(jd_conv_date)
    jd_conv_date = julian.to_jd(datetime(dt_conv_date.year, dt_conv_date.month, dt_conv_date.day, 0, 0 ,0))
    jd_return_converse = swe.mooncross_ut(point_long_conv, jd_conv_date)

    jd_conv_event_exact = jd_radix - (abs(jd_radix - jd_event))
    #DEMI
    if abs(jd_return_converse - jd_conv_event_exact) > 14:
        point_long_conv = swe.degnorm(point_long_conv + 180)
        jd_search_date = julian.to_jd(julian.from_jd(jd_return_converse) - timedelta(days=16))
        jd_demi_return_conv = swe.mooncross_ut(point_long_conv, jd_search_date)
    else:
        jd_demi_return_conv = None

    all_charts = []
    str_label = ''
    if ltype == LunarType.LUNAR:
        str_label = 'L'
    elif ltype == LunarType.KINETIC:
        str_label = 'K'
    elif ltype == LunarType.AS_LUNAR:
        str_label = 'A'

    main_direct_positions = calc_planets_ac_mc(jd_return_direct,geopos)
    main_conv_positions = calc_planets_ac_mc(jd_return_converse, geopos)
    main_direct_planets = calc_planets_near_angles(main_direct_positions,orb)
    main_conv_planets = calc_planets_near_angles(main_conv_positions,orb)

    print(f"mainD-ac {ps.convert_full_dec_degrees_to_zod_min_sec(main_direct_positions[0][1])}  mc {ps.convert_full_dec_degrees_to_zod_min_sec(main_direct_positions[1][1])}  moon {ps.convert_full_dec_degrees_to_zod_min_sec(main_direct_positions[3][1])}")
    print(f"mainC-ac {ps.convert_full_dec_degrees_to_zod_min_sec(main_conv_positions[0][1])}  mc {ps.convert_full_dec_degrees_to_zod_min_sec(main_conv_positions[1][1])}  moon {ps.convert_full_dec_degrees_to_zod_min_sec(main_conv_positions[3][1])}")

    all_charts.append((f"{str_label}",main_direct_planets))
    if jd_demi_return_direct:
        demi_direct_positions = calc_planets_ac_mc(jd_demi_return_direct, geopos)
        demi_direct_planets = calc_planets_near_angles(demi_direct_positions,orb)
        all_charts.append((f"D{str_label}",demi_direct_planets))    
        print(f"demiD-ac {ps.convert_full_dec_degrees_to_zod_min_sec(demi_direct_positions[0][1])}  mc {ps.convert_full_dec_degrees_to_zod_min_sec(demi_direct_positions[1][1])}  moon {ps.convert_full_dec_degrees_to_zod_min_sec(demi_direct_positions[3][1])}")


    all_charts.append((f"{str_label}C",main_conv_planets))
    if jd_demi_return_conv:
        demi_conv_positions = calc_planets_ac_mc(jd_demi_return_conv, geopos)
        demi_conv_planets = calc_planets_near_angles(demi_conv_positions,orb)
        all_charts.append((f"D{str_label}C",demi_conv_planets))    
        print(f"demiC-ac {ps.convert_full_dec_degrees_to_zod_min_sec(demi_conv_positions[0][1])}  mc {ps.convert_full_dec_degrees_to_zod_min_sec(demi_conv_positions[1][1])}  moon {ps.convert_full_dec_degrees_to_zod_min_sec(demi_conv_positions[3][1])}")


    dtj = julian.from_jd(jd_demi_return_direct) if jd_demi_return_direct else 'none'
    dtjj = julian.from_jd(jd_demi_return_conv) if jd_demi_return_conv else 'none'
    
    print(f"mainD {julian.from_jd(jd_return_direct)}\nmainC {julian.from_jd(jd_return_converse)} \ndemiD {dtj} \ndemiC {dtjj}")
    return all_charts

swe.set_ephe_path('/usr/share/swisseph/ephe')
'''dt_radix = datetime(1926,4,21,1,12,50)
dt_event = datetime(1948,11,14,12,00,00)
geopos = [51.5266667, -0.00852778, 15.0]
geopos_natal = [51.5266667, -0.00852778, 15.0]
'''
dt_radix = datetime(1924,6,12,15,31,15)
#dt_event = datetime(1988,11,8,12,00,00)
dt_event = datetime(1992,11,4,12,00,00)
geopos = [38.9, -77.0333333, 15.0]
geopos_natal = [42.25, -71.0833, 10.0]

ltype = LunarType.KINETIC
orb = 3
all_charts = calc_lunar_for_date(dt_radix,dt_event,geopos, geopos_natal,ltype,orb)
print(all_charts)

'''GETTING MOON AC MC FOR 2 DATES 
jd1 = julian.to_jd(datetime(1948,11,3,15,3,00))
xx, _ = swe.calc_ut(jd1, swe.MOON)
houses = swe.houses(jd1, geopos[0], geopos[1], b'T')
ac = houses[0][0]
mc = houses[1][1]
print(f"moon dirNQL {ps.convert_full_dec_degrees_to_zod_min_sec(xx[0])}  ac {ps.convert_full_dec_degrees_to_zod_min_sec(ac)}  mc {ps.convert_full_dec_degrees_to_zod_min_sec(mc)}")
jd2 = julian.to_jd(datetime(1903,10,6,10,22,00))
xx, _ = swe.calc_ut(jd2, swe.MOON)
houses = swe.houses(jd2, geopos[0], geopos[1], b'T')
ac = houses[0][0]
mc = houses[1][1]
print(f"moon convNQL {ps.convert_full_dec_degrees_to_zod_min_sec(xx[0])}  ac {ps.convert_full_dec_degrees_to_zod_min_sec(ac)}  mc {ps.convert_full_dec_degrees_to_zod_min_sec(mc)}")
'''