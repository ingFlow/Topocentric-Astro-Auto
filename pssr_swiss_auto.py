import swisseph as swe
import julian
from datetime import datetime, timedelta
from aspects_base import convert_dec_degrees_to_deg_min_sec, find_pssr_swiss_aspects, convert_full_dec_degrees_to_zod_min_sec
from constants import PLANETS, get_precession, calc_planets_labelled, calc_planets_pof_houses_labelled

class PSSR_Auto:
    def __init__(self, dt_radix, dt_event, rad_planets=None, geopos=None):
        self.__dict_info = {}
        self.calc_pssr_for_date(dt_radix, dt_event, rad_planets, geopos)


    def calc_pssr_for_date(self, dt_radix, dt_event, rad_planets=None, geopos=None):
        """returns tuple with 2 str of aspects rad to direct and conv pssr (prog/reg)
        if no radplanetsyou need to also give geopos natal"""
        jd_radix = julian.to_jd(dt_radix)
        jd_event = julian.to_jd(dt_event)

        if rad_planets == None:
            rad_planets = calc_planets_pof_houses_labelled(julian.to_jd(dt_radix), geopos)
        
        pssr_direct_year = calc_pssr_direct_year(dt_radix, dt_event)
        jd_pssr_start = julian.to_jd(datetime(pssr_direct_year,1,1,0,0,0))
        dir_precession = get_precession(jd_radix, jd_event)
        sun_long = rad_planets[0][1]
        dir_sun_long_precessed = swe.degnorm(sun_long + dir_precession)
        
        jd_pssr_dir = swe.solcross_ut(dir_sun_long_precessed, jd_pssr_start)
        jd_rad_event_diff = abs(jd_radix - jd_event)
        jd_pssr_event_diff_dir = abs(jd_pssr_dir - jd_event)
        jd_conv_event = jd_radix - jd_rad_event_diff

        timelapse = timedelta(hours=jd_pssr_event_diff_dir / 15.218425)
        jd_prog_pssr_dir = julian.to_jd(julian.from_jd(jd_pssr_dir) + timelapse)
        jd_reg_pssr_dir = julian.to_jd(julian.from_jd(jd_pssr_dir) - timelapse)

        year_diff = abs(dt_radix.year - dt_event.year)
        if (pssr_direct_year == dt_event.year):
            pssr_converse_year = dt_radix.year - year_diff
        else:
            pssr_converse_year = (dt_radix.year - year_diff) + 1
        jd_pssr_start = julian.to_jd(datetime(pssr_converse_year,1,1,0,0,0))
        
        conv_precession = get_precession(jd_radix, jd_conv_event)
        conv_sun_long_precessed = swe.degnorm(sun_long - conv_precession)
        jd_pssr_conv = swe.solcross_ut(conv_sun_long_precessed, jd_pssr_start)
        
        jd_pssr_event_diff_conv = abs(jd_pssr_conv - jd_conv_event)
        
        timelapse = timedelta(hours=jd_pssr_event_diff_conv / 15.218425)
        jd_prog_pssr_conv = julian.to_jd(julian.from_jd(jd_pssr_conv) + timelapse)
        jd_reg_pssr_conv = julian.to_jd(julian.from_jd(jd_pssr_conv) - timelapse)
        
        planets_to_exclude = ['Sun']
        prog_dir_planets = exclude_planets(calc_planets_labelled(jd_prog_pssr_dir, '(dp)'),planets_to_exclude)
        prog_conv_planets = exclude_planets(calc_planets_labelled(jd_prog_pssr_conv, '(cp)'),planets_to_exclude)
        reg_dir_planets = exclude_planets(calc_planets_labelled(jd_reg_pssr_dir, '(dr)'),planets_to_exclude)
        reg_conv_planets = exclude_planets(calc_planets_labelled(jd_reg_pssr_conv, '(cr)'),planets_to_exclude)
        direct_planets = [*prog_dir_planets, *reg_dir_planets]
        conv_planets = [*prog_conv_planets, *reg_conv_planets]

        self.__dict_info = {
            "dt_radix": dt_radix,
            "dt_event": dt_event,
            "direct_year": pssr_direct_year,
            "direct_precession": convert_dec_degrees_to_deg_min_sec(dir_precession),
            "rad_sun": convert_full_dec_degrees_to_zod_min_sec(sun_long),
            "sun_direct_precessed": convert_full_dec_degrees_to_zod_min_sec(dir_sun_long_precessed),
            "dt_direct_return": julian.from_jd(jd_pssr_dir),
            "jd_diff_pssr_event": jd_pssr_event_diff_dir,
            "dt_prog_pssr_direct": julian.from_jd(jd_prog_pssr_dir),
            "dt_reg_pssr_direct": julian.from_jd(jd_reg_pssr_dir),
            "converse_year": pssr_converse_year,
            "converse_precession": convert_dec_degrees_to_deg_min_sec(conv_precession),
            "converse_sun_precessed": convert_full_dec_degrees_to_zod_min_sec(conv_sun_long_precessed),
            "dt_converse_return": julian.from_jd(jd_pssr_conv),
            "jd_diff_pssr_event_converse": jd_pssr_event_diff_conv,
            "dt_prog_pssr_converse": julian.from_jd(jd_prog_pssr_conv),
            "dt_reg_pssr_converse": julian.from_jd(jd_reg_pssr_conv),
            "rad_positions": rad_planets,
            "direct_planets": direct_planets,
            "converse_planets": conv_planets
        }

        self.__str_rad_direct_aspects =  find_pssr_swiss_aspects(rad_planets,direct_planets)
        self.__str_rad_conv_aspects =  find_pssr_swiss_aspects(rad_planets, conv_planets)
        
    def get_str_aspects(self):
        return self.__str_rad_direct_aspects, self.__str_rad_conv_aspects

    def get_dict_info(self):
        return self.__dict_info
    
def exclude_planets(planets_list, exclude_planets):
    temp_planets = []

    for planet in planets_list:
        p = planet[0]
        if not(p in exclude_planets):
            temp_planets.append(planet)
    
    return temp_planets

def calc_pssr_direct_year(radix_datetime, event_datetime):
    """give the year for the solar return corresponding to an event """
    radix_month_day = (radix_datetime.month, radix_datetime.day)
    event_month_day = (event_datetime.month, event_datetime.day)
    if event_month_day < radix_month_day:
        direct_year = event_datetime.year - 1
    else:
        direct_year = event_datetime.year
    return direct_year
