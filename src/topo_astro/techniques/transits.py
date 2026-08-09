"""
techniques/transits.py - the Transit technique: Transit_Auto (radix
positions checked against a fresh ephemeris query at the event date
itself, direct and converse via get_str_aspects). The only technique that
queries the ephemeris fresh at the event date with no arc/derivation step
in between - see test_techniques_golden.py's notes on cross-environment
ephemeris precision if this technique's golden values ever look
unexpectedly sensitive to the environment they were generated in.

Phase 6 update: added get_aspects()/get_info() as thin additive wrappers
around get_str_aspects()/get_dict_info() (see the class body below).
Transit_Auto is one of the five techniques (with PD, Secondary, PSSR,
SRA) unified under this common two-method shape by techniques/base.py's
dispatcher. The original get_str_aspects()/get_dict_info() names are left
in place unchanged; nothing that already calls them needs to change.
Note: Transit is the one uniform technique whose constructor takes the
*event's* geopos rather than the natal one (see calc_transits_for_date's
`geopos` parameter, used only to compute `rad_planets` when none is
supplied) - the Phase 6 dispatcher in techniques/base.py preserves this
distinction explicitly rather than normalizing all five techniques onto
a single geopos value.
"""
import swisseph as swe
import julian
from topo_astro.core.aspects import find_trans_swiss_aspects
from topo_astro.core.constants import PLANETS, calc_planets_labelled, calc_planets_pof_houses_labelled

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

    # --- Phase 6: additive uniform-interface wrappers (see module docstring) ---
    def get_aspects(self):
        """Thin wrapper over get_str_aspects() - part of the 5-technique
        uniform (direct, converse) contract introduced in Phase 6. Does
        not replace get_str_aspects(), which remains available unchanged."""
        return self.get_str_aspects()

    def get_info(self):
        """Thin wrapper over get_dict_info() - part of the 5-technique
        uniform info-dict contract introduced in Phase 6. Does not
        replace get_dict_info(), which remains available unchanged."""
        return self.get_dict_info()