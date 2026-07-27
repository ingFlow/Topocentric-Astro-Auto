"""
techniques/transits.py - the Transit technique: Transit_Auto (radix
positions checked against a fresh ephemeris query at the event date
itself, direct and converse via get_str_aspects). The only technique that
queries the ephemeris fresh at the event date with no arc/derivation step
in between - see test_techniques_golden.py's notes on cross-environment
ephemeris precision if this technique's golden values ever look
unexpectedly sensitive to the environment they were generated in.
"""
import swisseph as swe
import julian
from core.aspects import find_trans_swiss_aspects
from core.constants import PLANETS, calc_planets_labelled, calc_planets_pof_houses_labelled

class Transit_Auto:
    def __init__(self, jd_radix, jd_event, geopos, rad_planets=None):
        self.__dict_info = {}
        self.calc_transits_for_date(jd_radix, jd_event, geopos, rad_planets)
    
    def calc_transits_for_date(self, jd_radix, jd_event, geopos, rad_planets=None):
        """If noradixplanets then make rad_planets=None and give geopos
        returns tuple with 2 str of aspects rad to direct and conv trans"""
        if rad_planets is None:
            rad_planets = calc_planets_pof_houses_labelled(jd_radix, geopos)
        
        jd_rad_event_diff = abs(jd_radix - jd_event)
        jd_conv_event = jd_radix - jd_rad_event_diff
        
        dir_planets = calc_planets_labelled(jd_event, '(p)')
        conv_planets = calc_planets_labelled(jd_conv_event, '(c)')

        self.__dict_info = {
            "dt_radix": julian.from_jd(jd_radix),
            "dt_event": julian.from_jd(jd_event),
            "dt_converse_event": julian.from_jd(jd_conv_event),
            "rad_positions": rad_planets,
            "direct_planets": dir_planets,
            "converse_planets": conv_planets
        }

        self.__str_rad_direct_aspects = find_trans_swiss_aspects(rad_planets,dir_planets)
        self.__str_rad_conv_aspects = find_trans_swiss_aspects(rad_planets, conv_planets)
        
    def get_str_aspects(self):
        return self.__str_rad_direct_aspects, self.__str_rad_conv_aspects

    def get_dict_info(self):
        return self.__dict_info

