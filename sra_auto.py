import swisseph as swe
import julian
from datetime import datetime, timedelta
from aspects_base import find_sra_swiss_aspects, remove_duplicates, convert_dec_degrees_to_deg_min_sec, convert_full_dec_degrees_to_zod_min_sec
from constants import get_precession, calc_planets_houses_labelled, calc_planets_pof_houses_labelled, PLANETS 

class SRA_Auto:
    def __init__(self, dt_radix, dt_event, geopos, rad_planets=None):
        self.__dict_info = {}
        self.calc_sra_for_date(dt_radix, dt_event, geopos, rad_planets)

    def calc_sra_for_date(self, dt_radix, dt_event, geopos, rad_planets=None):
        """returns tuple with 2 str of aspects td/tc tropical direct/converse and pd/pc precessed equiv."""
        jd_radix = julian.to_jd(dt_radix)
        jd_event = julian.to_jd(dt_event)

        if rad_planets == None:
            rad_planets = calc_planets_pof_houses_labelled(jd_radix, geopos)

        direct_year = calc_direct_year(dt_radix, dt_event)
        jd_dir_start = julian.to_jd(datetime(direct_year,1,1,0,0,0))
        dir_precession = get_precession(jd_radix, julian.to_jd(datetime(direct_year, dt_radix.month, dt_radix.day, 12, 00, 00)))
        dir_precession = get_precession(jd_radix, jd_event)
        rad_sun_long = rad_planets[0][1]
        dir_sun_long_precessed = swe.degnorm(rad_sun_long + dir_precession)
        
        #PRENATAL
        jd_conv_event = jd_radix - abs(jd_radix - jd_event)
        year_diff = abs(dt_radix.year - dt_event.year)
        if (direct_year == dt_event.year):
            converse_year = dt_radix.year - year_diff
        else:
            converse_year = (dt_radix.year - year_diff) + 1
        jd_conv_start = julian.to_jd(datetime(converse_year,1,1,0,0,0))
        
        conv_precession = get_precession(jd_radix, julian.to_jd(datetime(converse_year, dt_radix.month, dt_radix.day, 12, 00, 00)))
        conv_precession = get_precession(jd_radix, jd_event)
        conv_sun_long_precessed = swe.degnorm(rad_sun_long - conv_precession)
        
        jd_dir_return = swe.solcross_ut(rad_sun_long, jd_dir_start)
        jd_dir_return_precessed = swe.solcross_ut(dir_sun_long_precessed, jd_dir_start)
        jd_conv_return = swe.solcross_ut(rad_sun_long, jd_conv_start)
        jd_conv_return_precessed = swe.solcross_ut(conv_sun_long_precessed, jd_conv_start)
        
        planets_to_exclude = []
        trop_dir_planets = calc_planets_houses_labelled(jd_dir_return, '(td)', planets_to_exclude, geopos)
        trop_conv_planets = calc_planets_houses_labelled(jd_conv_return, '(tc)', planets_to_exclude, geopos)
        precessed_dir_planets = calc_planets_houses_labelled(jd_dir_return_precessed, '(pd)', planets_to_exclude, geopos)
        precessed_conv_planets = calc_planets_houses_labelled(jd_conv_return_precessed, '(pc)', planets_to_exclude, geopos)
        sra_planets = [*trop_dir_planets, *trop_conv_planets] #rad-to-trop more effective than rad to precessed
    
        str_rad_sra_aspects = find_sra_swiss_aspects(rad_planets,sra_planets) 
        str_td_td_aspects = find_sra_swiss_aspects(trop_dir_planets, trop_dir_planets)
        str_tc_tc_aspects = find_sra_swiss_aspects(trop_conv_planets, trop_conv_planets)
        str_pd_pd_aspects = find_sra_swiss_aspects(precessed_dir_planets, precessed_dir_planets)
        str_pc_pc_aspects = find_sra_swiss_aspects(precessed_conv_planets, precessed_conv_planets)
        str_sra_sra_aspects = str_td_td_aspects + '\n' + str_tc_tc_aspects + '\n' + str_pd_pd_aspects + '\n' + str_pc_pc_aspects
        str_rad_sra_aspects = remove_duplicates(str_rad_sra_aspects)

        self.__dict_info = {
            "dt_radix": julian.from_jd(jd_radix),
            "dt_event": dt_event,
            "direct_year": direct_year,
            "direct_precession": convert_dec_degrees_to_deg_min_sec(dir_precession),
            "radix_sun_long": convert_full_dec_degrees_to_zod_min_sec(rad_sun_long),
            "directed_sun_long_precessed": convert_full_dec_degrees_to_zod_min_sec(dir_sun_long_precessed),
            "dt_conv_event": julian.from_jd(jd_conv_event),
            "converse_year": converse_year,
            "converse_precession": convert_dec_degrees_to_deg_min_sec(conv_precession),
            "converse_sun_long_precessed": convert_full_dec_degrees_to_zod_min_sec(conv_sun_long_precessed),
            "dt_return_direct": julian.from_jd(jd_dir_return),
            "dt_return_converse": julian.from_jd(jd_conv_return),
            "dt_return_direct_precessed": julian.from_jd(jd_dir_return_precessed),
            "dt_return_converse_precessed": julian.from_jd(jd_conv_return_precessed),
            "tropical_direct_planets": trop_dir_planets,
            "tropical_converse_planets": trop_conv_planets,
            "precessed_direct_planets": precessed_dir_planets,
            "precessed_converse_planets": precessed_conv_planets
        }

        self.__str_sra_sra_aspects = str_sra_sra_aspects
        self.__str_rad_sra_aspects = str_rad_sra_aspects

    def get_str_aspects(self):
        return self.__str_rad_sra_aspects, self.__str_sra_sra_aspects

    def get_info(self):
        return self.__dict_info

def calc_direct_year(radix_datetime, event_datetime):
    """give the year for the solar return corresponding to an event """
    radix_month_day = (radix_datetime.month, radix_datetime.day)
    event_month_day = (event_datetime.month, event_datetime.day)
    if event_month_day < radix_month_day:
        direct_year = event_datetime.year - 1
    else:
        direct_year = event_datetime.year
    return direct_year


'''jd_radix = julian.to_jd(datetime(1940,10,9,17,24,13))
jd_event = julian.to_jd(datetime(1980,12,8,12,00,00))
geopos = [53.733333, -2.9833333, 15.0]

jd_radix = julian.to_jd(datetime(1948,11,14,21,13,37))
jd_event = julian.to_jd(datetime(1958,7,26,12,00,00))
geopos = [51.5166667, -0.111666667, 15.0]

jd_radix = julian.to_jd(datetime(1926,4,21,1,12,48))
jd_event = julian.to_jd(datetime(1948,11,14,12,00,00))
geopos = [51.5166667, -0.111666667, 15.0]
'''
