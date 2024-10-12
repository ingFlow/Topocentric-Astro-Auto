import swisseph as swe
import julian
from datetime import datetime, timedelta
import aspects_base as aspects

PLANETS = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Mean_Node']

class Transit_Auto:
    def __init__(self, jd_radix, jd_event, rad_planets):
        self.__dict_info = {}
        self.calc_transits_for_date(jd_radix, jd_event, rad_planets)
    
    def calc_transits_for_date(self, jd_radix, jd_event, rad_planets):
        """returns tuple with 2 str of aspects rad to direct and conv trans"""
        jd_rad_event_diff = abs(jd_radix - jd_event)
        jd_conv_event = jd_radix - jd_rad_event_diff
        
        dir_planets = calc_planets_labelled(jd_event, '(p)')
        conv_planets = calc_planets_labelled(jd_conv_event, '(c)')

        self.__dict_info = {
            "dt_radix": julian.from_jd(jd_radix),
            "dt_event": julian.from_jd(jd_event),
            "rad_positions": rad_planets,
            "dt_converse_event": julian.from_jd(jd_conv_event),
            "direct_planets": dir_planets,
            "converse_planets": conv_planets
        }


        self.__str_rad_direct_aspects = aspects.find_trans_swiss_aspects(rad_planets,dir_planets)
        self.__str_rad_conv_aspects = aspects.find_trans_swiss_aspects(rad_planets, conv_planets)
        
    def get_str_aspects(self):
        return self.__str_rad_direct_aspects, self.__str_rad_conv_aspects

    def get_dict_info(self):
        return self.__dict_info


def calc_planets_labelled(jd_radix, label):
    planets = []
    
    for planet in range(0, len(PLANETS)):
        xx, _ = swe.calc_ut(jd_radix, planet)
        long = xx[0]

        planets.append((PLANETS[planet], long, label))    

    return planets
