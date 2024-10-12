import swisseph as swe
import julian
from datetime import timedelta
from aspects_base import calculate_aspect, convert_full_dec_degrees_to_zod_min_sec, convert_dec_degrees_to_deg_min_sec
from constants import PLANETS

class LunarType:
    LUNAR = 0
    KINETIC = 1
    AS_LUNAR = 2

    @classmethod
    def get_name(cls, value):
        """Returns the name of the lunar type for the given value."""
        for attr in dir(cls):
            if not attr.startswith("__") and getattr(cls, attr) == value:
                return attr
        return 'Unknown Lunar Type'

class Lunar_Auto:
    def __init__(self, dt_radix, dt_event, geopos, geopos_natal, orb):
        self.__dict_info = {}

        list1 = self.calc_lunar_for_date(dt_radix,dt_event,geopos,geopos_natal,LunarType.LUNAR,orb)
        list2 = self.calc_lunar_for_date(dt_radix,dt_event,geopos,geopos_natal,LunarType.KINETIC,orb)
        list3 = self.calc_lunar_for_date(dt_radix,dt_event,geopos,geopos_natal,LunarType.AS_LUNAR,orb)
        list = [*list1, *list2, *list3]

        self.__all_lunars = list

    def calc_lunar_for_date(self, dt_radix, dt_event, geopos, geopos_natal, ltype: LunarType, orb):
        """returns list of (name_cyclic, [list_planets_near_angles])
        list_planets_near_angles format is (planet, aspect, orb)"""
        jd_radix = julian.to_jd(dt_radix)
        jd_event = julian.to_jd(dt_event)
        
        #lunar computation
        point_long_dir, point_long_conv, dict_calc_info = get_point_long_dir_conv(ltype,jd_radix,jd_event, geopos_natal)
        jd_search_date = julian.to_jd(dt_event - timedelta(days=30))
        
        jd_return_direct = swe.mooncross_ut(point_long_dir, jd_search_date)
        jd_return_after_first_direct = swe.mooncross_ut(point_long_dir, jd_return_direct)
        #rare case where it reaches degree literally that day or something
        if jd_return_after_first_direct <= jd_event:
            jd_return_direct = jd_return_after_first_direct

        #DEMI
        if abs(jd_return_direct - jd_event) > 14:
            point_long_dir_demi = swe.degnorm(point_long_dir + 180)
            if ltype == LunarType.KINETIC:
                point_long_dir_demi,_ = calc_kinetic_demi_dir_conv(jd_radix, jd_event)
            jd_demi_return_direct = swe.mooncross_ut(point_long_dir_demi, jd_return_direct)
            
        else:
            jd_demi_return_direct = None
        
        #kinetics handled different acc too marr/fagan method
        if ltype == LunarType.KINETIC:
            jd_conv_date = jd_radix - abs(jd_return_direct - jd_radix)
        else:
            jd_conv_date = jd_radix - abs(jd_event - jd_radix)

        jd_conv_date = int(jd_conv_date) + 0.5
        jd_return_converse = swe.mooncross_ut(point_long_conv, jd_conv_date)

        jd_conv_event_exact = jd_radix - (abs(jd_radix - jd_event))
        #DEMI
        if abs(jd_return_converse - jd_conv_event_exact) > 14:
            point_long_conv_demi = swe.degnorm(point_long_conv + 180)
            if ltype == LunarType.KINETIC:
                _, point_long_conv_demi = calc_kinetic_demi_dir_conv(jd_radix, jd_event)
            jd_search_date = julian.to_jd(julian.from_jd(jd_return_converse) - timedelta(days=16))
            jd_demi_return_conv = swe.mooncross_ut(point_long_conv_demi, jd_search_date)
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

        all_charts.append((f"{str_label}",main_direct_planets))
        if jd_demi_return_direct:
            demi_direct_positions = calc_planets_ac_mc(jd_demi_return_direct, geopos)
            demi_direct_planets = calc_planets_near_angles(demi_direct_positions,orb)
            all_charts.append((f"D{str_label}",demi_direct_planets))    

        all_charts.append((f"{str_label}C",main_conv_planets))
        if jd_demi_return_conv:
            demi_conv_positions = calc_planets_ac_mc(jd_demi_return_conv, geopos)
            demi_conv_planets = calc_planets_near_angles(demi_conv_positions,orb)
            all_charts.append((f"D{str_label}C",demi_conv_planets))    

        key_str = LunarType.get_name(ltype)
        self.__dict_info[key_str] = dict_calc_info
        self.__dict_info[key_str].update({"dt_return_direct": julian.from_jd(jd_return_direct)})
        self.__dict_info[key_str].update({"dt_return_converse": julian.from_jd(jd_return_converse)})
        if jd_demi_return_direct is not None:
            self.__dict_info[key_str].update({"point_long_direct_demi": convert_full_dec_degrees_to_zod_min_sec(point_long_dir_demi)})
            self.__dict_info[key_str].update({"dt_return_demi_direct": julian.from_jd(jd_demi_return_direct)})
        if jd_demi_return_conv is not None:
            self.__dict_info[key_str].update({"point_long_converse_demi": convert_full_dec_degrees_to_zod_min_sec(point_long_conv_demi)})
            self.__dict_info[key_str].update({"dt_return_demi_converse": julian.from_jd(jd_demi_return_conv)})
        temp_dict = {
            "direct_positions": main_direct_positions,
            "converse_positions": main_conv_positions,
        }
        if jd_demi_return_direct != None:
            temp_dict.update({"direct_demi_positions": demi_direct_positions})
        if jd_demi_return_conv != None:
            temp_dict.update({"converse_demi_positions": demi_conv_positions})
        self.__dict_info[key_str].update(temp_dict)

        return all_charts

    def get_all_lunars(self):
        return self.__all_lunars
    
    def get_info(self):
        return self.__dict_info

def calc_bija_days(secondary_days_dec):
    base_bija_seconds_per_year = 3*60 + 55.9
    bija_seconds = secondary_days_dec * base_bija_seconds_per_year
    bija_days = bija_seconds / 86400
    return bija_days

def calc_kinetic_demi_dir_conv(jd_radix, jd_event):
    jd_diff = abs(jd_radix - jd_event)
    days_diff = jd_diff / 365.2422
    jd_prog_prelim = jd_radix + days_diff
    xx, _ = swe.calc_ut(jd_prog_prelim, swe.MOON)
    prog_moon_prelim = swe.degnorm(xx[0] + 180)
    jd_search_date = julian.to_jd(julian.from_jd(jd_event) - timedelta(days=30))
    jd_return_direct = swe.mooncross_ut(prog_moon_prelim, jd_search_date)
    jd_return_after_first_direct = swe.mooncross_ut(prog_moon_prelim, jd_search_date)
    #rare case where it reaches degree literally that day or something
    if jd_return_after_first_direct <= jd_event:
        jd_return_direct = jd_return_after_first_direct
    jd_return_direct = int(jd_return_direct)+1 #make it midday of whatever jd
    
    sidt_radix = swe.sidtime(int(jd_radix)+1)
    sidt_event = swe.sidtime(jd_return_direct)
    st_diff = (sidt_event - sidt_radix)/24
    days_years_diff = julian.from_jd(jd_event).year - julian.from_jd(jd_radix).year
    days_years_diff += st_diff

    bija_days = calc_bija_days(days_diff)
    days_years_diff -= bija_days

    rad_aya = swe.get_ayanamsa_ut(jd_radix)
    event_aya = swe.get_ayanamsa_ut(jd_event)
    precession = abs(rad_aya - event_aya)
    jd_conv_event = jd_radix - (abs(jd_radix-jd_event))
    event_aya = swe.get_ayanamsa_ut(jd_conv_event)
    conv_precession = abs(rad_aya - event_aya)

    jd_prog = jd_radix + days_years_diff
    xx, _ = swe.calc_ut(jd_prog, swe.MOON)
    prog_moon_long = swe.degnorm(xx[0]+180) + precession

    jd_reg = jd_radix - days_years_diff
    xx, _ = swe.calc_ut(jd_reg, swe.MOON)
    reg_moon_long = swe.degnorm(xx[0]+180) - conv_precession

    return prog_moon_long, reg_moon_long

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
    jd_return_direct = int(jd_return_direct)+1 #make it midday of whatever jd
    
    sidt_radix = swe.sidtime(int(jd_radix)+1)
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

def get_point_long_dir_conv(ltype: LunarType, jd_radix, jd_event, geopos_natal):
    jd_conv_event = jd_radix - (abs(jd_radix-jd_event))
    xx, _ = swe.calc_ut(jd_radix, swe.MOON)
    moon_long = xx[0]    
    rad_aya = swe.get_ayanamsa_ut(jd_radix)
    event_aya = swe.get_ayanamsa_ut(jd_event)
    dir_precession = abs(rad_aya - event_aya)
    moon_precessed_long = moon_long + dir_precession

    event_aya = swe.get_ayanamsa_ut(jd_conv_event)
    conv_precession = abs(rad_aya - event_aya)
    moon_conv_precessed_long = moon_long - conv_precession

    dir_long, conv_long = None, None

    if ltype == LunarType.LUNAR:
        #radical moon
        dir_long, conv_long = moon_precessed_long, moon_conv_precessed_long
    if ltype == LunarType.KINETIC:
        #radical progressed moon
        dir_long, conv_long = calc_kinetic_dir_conv(jd_radix,jd_event,dir_precession,conv_precession)

    if ltype == LunarType.AS_LUNAR:
        #radical ac
        houses = swe.houses(jd_radix, geopos_natal[0], geopos_natal[1], b'T')
        ac_dir = houses[0][0] + dir_precession
        
        houses = swe.houses(jd_radix, geopos_natal[0], geopos_natal[1], b'T')
        ac_conv = houses[0][0] - conv_precession
        dir_long, conv_long = ac_dir, ac_conv

    dict_info = {
        "dt_radix": julian.from_jd(jd_radix),
        "dt_event": julian.from_jd(jd_event),
        "dt_converse_event": julian.from_jd(jd_conv_event),
        "rad_moon": convert_full_dec_degrees_to_zod_min_sec(moon_long),
        "direct_precession": convert_dec_degrees_to_deg_min_sec(dir_precession),
        "converse_precession": convert_dec_degrees_to_deg_min_sec(conv_precession),
        "point_long_direct": convert_full_dec_degrees_to_zod_min_sec(dir_long),
        "point_long_converse": convert_full_dec_degrees_to_zod_min_sec(conv_long),
    }

    return dir_long, conv_long, dict_info
        
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
        aspect = calculate_aspect(ac, d, orb, True)
        if aspect:
            asp, asp_orb = aspect
            if asp == 'conjunction' or asp == 'opposition':
                str = (f'(ac,{ac:.2f}) ({p},{d:.2f}) ({asp},{asp_orb * 60:.0f}\')\n')
                planets_near_angle.append(str)
    for p, d in planets:
        aspect = calculate_aspect(mc, d, orb, True)
        if aspect:
            asp, asp_orb = aspect
            if asp == 'conjunction' or asp == 'opposition':
                str = (f'(mc,{mc:.2f}) ({p},{d:.2f}) ({asp},{asp_orb * 60:.0f}\')\n')
                planets_near_angle.append(str)
    return planets_near_angle

def get_str_only_aspects_from_data(dt_radix, dt_event, geopos, geopos_natal, ltype: LunarType, orb):
    lunar_obj = Lunar_Auto(dt_radix, dt_event, geopos, geopos_natal, ltype, orb)
    all_charts = lunar_obj.get_all_lunars()
    aspects_only_list = get_str_only_aspects_from_array(all_charts)
    return aspects_only_list

def get_str_labelled_aspects_from_array(all_charts):
    '''gives the aspects keeping which chart it came from'''
    aspects_only_list = ""
    for key, aspects in all_charts:
        processed_aspects = key + '\n'
        for aspect in aspects:
            # Split by \n and remove empty lines
            split_aspects = [a.strip() for a in aspect.split('\n') if a.strip()]
            try:
                for s in split_aspects:
                    processed_aspects = processed_aspects + s +'\n'
            except:
                processed_aspects += split_aspects
        
        if processed_aspects != key + '\n':  # Add only if there's content
            aspects_only_list = aspects_only_list + processed_aspects + "\n" 
    aspects_only_list = aspects_only_list.replace('\n\n', '\n')
    return aspects_only_list

def get_str_only_aspects_from_array(all_charts):
    aspects_only_list = ""
    for key, aspects in all_charts:
        processed_aspects = ""
        for aspect in aspects:
            # Split by \n and remove empty lines
            split_aspects = [a.strip() for a in aspect.split('\n') if a.strip()]
            try:
                for s in split_aspects:
                    processed_aspects = processed_aspects + s +'\n'
            except:
                processed_aspects += split_aspects
        
        if processed_aspects:  # Add only if there's content
            aspects_only_list = aspects_only_list + processed_aspects + "\n" 
    aspects_only_list = aspects_only_list.replace('\n\n', '\n')
    return aspects_only_list

def count_mal_ben_from_str_aspects(str_aspects):
    planet_counts = count_each_planet_lunars(str_aspects)
    malefic_count = planet_counts[PLANETS.index('Saturn')] + planet_counts[PLANETS.index('Neptune')] + planet_counts[PLANETS.index('Mars')] + planet_counts[PLANETS.index('Pluto')]
    benefic_count = planet_counts[PLANETS.index('Venus')] + planet_counts[PLANETS.index('Jupiter')] + planet_counts[PLANETS.index('Sun')] + planet_counts[PLANETS.index('Moon')]
    
    return malefic_count, benefic_count


def count_mal_ben_all_lunars(dt_radix, dt_event, geopos, geopos_natal, orb):
    """return tuple (mal count, ben count)"""
    lunar_obj = Lunar_Auto(dt_radix,dt_event,geopos,geopos_natal,orb)
    all_charts = lunar_obj.get_all_lunars()
    all_aspects = get_str_labelled_aspects_from_array(all_charts)
    
    planet_counts = count_each_planet_lunars(all_aspects)
    malefic_count = planet_counts[PLANETS.index('Saturn')] + planet_counts[PLANETS.index('Neptune')] + planet_counts[PLANETS.index('Mars')] + planet_counts[PLANETS.index('Pluto')]
    benefic_count = planet_counts[PLANETS.index('Venus')] + planet_counts[PLANETS.index('Jupiter')] + planet_counts[PLANETS.index('Sun')] + planet_counts[PLANETS.index('Moon')]
    
    return malefic_count, benefic_count

def count_each_planet_lunars(all_aspects_str):
    split_aspects_str = all_aspects_str.split('\n')
    planet_counts = [0,0,0,0,0,0,0,0,0,0,0]
    for i in range(0,11):
        planet = PLANETS[i]
        for aspect in split_aspects_str:
            if planet in aspect:
                planet_counts[i] =  planet_counts[i] + 1
    return planet_counts    

def get_str_planet_counts(counts):
    return_str = ""
    for i in range(0,11):
        return_str += f"{PLANETS[i]}: {counts[i]}, "
    return return_str

swe.set_ephe_path('/usr/share/swisseph/ephe')
'''dt_radix = datetime(1926,4,21,1,12,50)
dt_event = datetime(1948,11,14,12,00,00)
geopos = [51.5266667, -0.00852778, 15.0]
geopos_natal = [51.5266667, -0.00852778, 15.0]

dt_radix = datetime(1924,6,12,15,31,15)
#dt_event = datetime(1988,11,8,12,00,00)
dt_event = datetime(1992,11,4,12,00,00)
geopos = [38.9, -77.0333333, 15.0]
geopos_natal = [42.25, -71.0833, 10.0]

ltype = LunarType.KINETIC
orb = 9
lunar_obj = Lunar_Auto(dt_radix,dt_event,geopos, geopos_natal,orb)
all_charts =lunar_obj.get_all_lunars()
all_charts = get_str_only_aspects_from_array(all_charts)
#print(all_charts)
inf = lunar_obj.get_info()
print(inf)
counts = count_each_planet_lunars(all_charts)
#print(get_str_counts(counts))

#print(count_mal_ben_all_lunars(dt_radix,dt_event,geopos,geopos_natal,orb))
#GETTING MOON AC MC FOR 2 DATES 
jd1 = julian.to_jd(datetime(1948,11,3,15,3,00))
xx, _ = swe.calc_ut(jd1, swe.MOON)
houses = swe.houses(jd1, geopos[0], geopos[1], b'T')
ac = houses[0][0]
mc = houses[1][1]
print(f"moon dirNQL {convert_full_dec_degrees_to_zod_min_sec(xx[0])}  ac {convert_full_dec_degrees_to_zod_min_sec(ac)}  mc {convert_full_dec_degrees_to_zod_min_sec(mc)}")
jd2 = julian.to_jd(datetime(1903,10,6,10,22,00))
xx, _ = swe.calc_ut(jd2, swe.MOON)
houses = swe.houses(jd2, geopos[0], geopos[1], b'T')
ac = houses[0][0]
mc = houses[1][1]
print(f"moon convNQL {convert_full_dec_degrees_to_zod_min_sec(xx[0])}  ac {convert_full_dec_degrees_to_zod_min_sec(ac)}  mc {convert_full_dec_degrees_to_zod_min_sec(mc)}")'''