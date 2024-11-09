import swisseph as swe
import julian
from datetime import datetime
from aspects_base import find_trans_swiss_aspects
from constants import PLANETS, calc_planets_labelled, calc_planets_pof_houses_labelled

class Harmonics_Auto:
    def __init__(self, jd_radix, jd_event, geopos, rad_planets=None):
        self.__dict_info = {}
        self.calc_harmonics_for_date(jd_radix, jd_event, geopos, rad_planets)
    
    def calc_harmonics_for_date(self, jd_radix, jd_event, geopos, rad_planets=None):
        
        if rad_planets is None:
            rad_planets = calc_planets_pof_houses_labelled(jd_radix, geopos)
        
        jd_rad_event_diff = abs(jd_radix - jd_event)
        years_elapsed = jd_rad_event_diff / 365.2422
        
        harmonic_planets = []
        for obj in rad_planets:
            planet = obj[0]
            if (planet in PLANETS) or (planet == 'POF'):
                obj_degree = obj[1]
                harmonic_degree = years_elapsed * obj_degree
                harmonic_degree = swe.degnorm(harmonic_degree)
                harmonic_planets.append((planet,harmonic_degree,'(h)'))

        self.__dict_info = {
            "dt_radix": julian.from_jd(jd_radix),
            "dt_event": julian.from_jd(jd_event),
            "rad_positions": rad_planets,
            "harmonic_planets": harmonic_planets
        }

        self.__str_rad_harmonic_aspects = find_trans_swiss_aspects(rad_planets,harmonic_planets)
        
    def get_str_aspects(self):
        return self.__str_rad_harmonic_aspects

    def get_dict_info(self):
        return self.__dict_info

