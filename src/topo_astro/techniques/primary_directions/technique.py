"""
techniques/primary_directions/technique.py - Primary Directions
orchestration: the PD_Automate class (builds a directed chart for one
radix/event pair, direct and converse), calc_directed_pd_houses,
calc_directed_pd_planets, calc_directed_POF, calc_radix_ac_mc_ramc,
calc_rad_planets_equatorial, and calc_planet_house_pos.

Phase 5 update: the significator/scoring engine that used to live in this
file (Planet, EventType, AspectType, GoodBadFlag, PRIMARY_RULES,
SECONDARY_RULES, PLANETARY_COMBO, and the
is_acceptable_*/count_*_acceptable_aspects/get_accept_lists/
appropriate_base/good_bad_flag_match_aspect/is_aspect_conj_opp call graph)
has moved to significators/rules_data.py and significators/scoring.py
respectively, since - per the Developer Manual's Section 7.2 - that engine
is reused by five of the seven techniques (Primary Directions, Secondary,
Transit, SRA, Harmonics), not specific to Primary Directions. This module
now contains PD-specific directed-position orchestration only.

Every function/class that remains below (PD_Automate,
calc_directed_pd_houses, calc_directed_pd_planets, calc_rad_planets_equatorial,
calc_directed_POF, calc_planet_house_pos, calc_radix_ac_mc_ramc) has zero
direct reference to the moved symbols - confirmed by direct source
inspection before the move, not assumed. Callers that need both PD
orchestration and significator/scoring together (webapp/app.py,
batch/grid_engine.py, batch/entrypoints.py) now import from both this
module and significators/ separately; see each call site's own updated
imports for the exact mapping.

Recent change (de-duplication/mechanical-move phases): add_suffix_to_tuples,
calc_alt, and calc_lst were relocated to core/reserve.py - they're general
astronomy utilities, not PD-specific, and had no caller anywhere in this
file's own logic.
"""
import swisseph as swe
import julian
import math

from topo_astro.techniques.primary_directions import trig as pd
from topo_astro.core.aspects import calculate_obliquity, find_pd_swiss_aspects, format_house_list
from topo_astro.core.constants import PLANETS, calc_planets_pof_houses_labelled

class PD_Automate:
    def __init__(self,jd_rad : julian, jd : julian, geo_positions: list, rad_planets_labelled=None, rad_planets_equatorial=None, rad_houses_info=None, e=None):
        self.__dict_planets_extended_info = {}
        self.pd_for_time_event(jd_rad, jd, geo_positions, rad_planets_labelled, rad_planets_equatorial, rad_houses_info, e)

    def pd_for_time_event(self,jd_rad : julian, jd : julian, geo_positions: list, rad_planets_labelled=None, rad_planets_equatorial=None, rad_houses_info=None, e=None):
        if rad_planets_labelled == None: #ie there is only event info
            rad_houses_info = swe.houses(jd_rad, geo_positions[0], geo_positions[1], b'T')
            rad_planets_labelled = calc_planets_pof_houses_labelled(jd_rad)
            rad_planets_equatorial = calc_rad_planets_equatorial(jd_rad)
            e = calculate_obliquity(jd_rad)

        dir_houses, conv_houses = calc_directed_pd_houses(jd_rad,jd, geo_positions[0], rad_houses_info, e)
        dir_houses = format_house_list(dir_houses, '(d)')
        conv_houses = format_house_list(conv_houses, '(c)')
        dir_planets, conv_planets, dict_extended = calc_directed_pd_planets(jd_rad,jd, geo_positions[0], geo_positions[1], rad_houses_info, rad_planets_equatorial, e)

        #add POF  DATA
        dir_pof, conv_pof, dict_pof_info = calc_directed_POF(rad_planets_labelled, jd_rad, jd, geo_positions[0], rad_houses_info, e)
        dir_planets.append(('POF', dir_pof, "(d)"))
        conv_planets.append(('POF',conv_pof, "(c)"))
        #JOIN ARRAYS
        rad_positions = rad_planets_labelled
        dir_positions = [*dir_planets, *dir_houses]
        conv_positions = [*conv_planets, *conv_houses]

        self.__dict_planets_extended_info["base"] = {
            "dt_radix": julian.from_jd(jd_rad),
            "dt_event": julian.from_jd(jd),
            "geopos": geo_positions,
            "rad_positions": rad_positions,
            "rad_equatorial": rad_planets_equatorial,
            "directed_positions": dir_positions,
            "converse_positions": conv_positions
        }
        dict_extended.update(dict_pof_info)
        self.__dict_planets_extended_info["planets_extended"] = dict_extended
        self.__dict_planets_extended_info["MDOs"] = self.get_mdos_natal()
        self.__str_aspects_rad_dir = find_pd_swiss_aspects(rad_positions, dir_positions)
        self.__str_aspects_rad_conv = find_pd_swiss_aspects(rad_positions, conv_positions)
        

    def get_aspects_str(self):
        return self.__str_aspects_rad_dir, self.__str_aspects_rad_conv

    def get_extended_information(self):
        return self.__dict_planets_extended_info
    
    def get_mdos_natal(self):
        mdo_list = []
        extended_planets = self.__dict_planets_extended_info["planets_extended"]
        for key, value in extended_planets.items():
            mdo = value['MDO']
            mdo_list.append((key,mdo[0]))
        return mdo_list
    


def calc_directed_pd_houses(jd_radix, jd_event, geo_latitude, rad_houses, e):
    """returns 2 tuples with house cusps 1 to 12 dir, conv
    removed functionality for Hmd1 and Hmd2 (H1/H2)"""
    arc = pd.calc_arc(jd_radix, jd_event)
    ramc = rad_houses[1][2]

    directed = swe.houses_armc(swe.degnorm(ramc+arc), geo_latitude, e, b'T')[0]
    converse = swe.houses_armc(swe.degnorm(ramc-arc), geo_latitude, e, b'T')[0]
    #print(f"dirHouse ----- {directed} \nconvHouse------- {converse}")
    return directed, converse

def calc_directed_pd_planets(jd_radix, jd_event, geo_latitude, geo_longitude, houses_info, rad_planets_equatorial, e):
    """returns tuple (dir_planets, conv_planets, extended_planet_info)"""
    dir_planets = []
    conv_planets = []
    dict_extended_info = {}

    for planet in range(0, len(PLANETS)):
        long, ra, decl = rad_planets_equatorial[planet]
        cusps = houses_info[0]
        p_house = pd.get_housepos_manual(long, cusps)
        ac, mc, ramc = calc_radix_ac_mc_ramc(houses_info)

        direct_pd_obj = pd.PD_Base(jd_radix, jd_event, geo_latitude, decl, ra, ramc, mc, True, p_house, ac, long, e)
        long_directed = direct_pd_obj.get_long_directed()
        dir_planets.append((PLANETS[planet], long_directed, "(d)"))
        
        converse_pd_obj = pd.PD_Base(jd_radix, jd_event, geo_latitude, decl, ra, ramc, mc, False, p_house, ac, long, e)
        long_conv = converse_pd_obj.get_long_directed()
        conv_planets.append((PLANETS[planet], long_conv, "(c)"))

        #append planets md,sa,adp etc to dict information
        dict_extended_info[PLANETS[planet]] = direct_pd_obj.get_extended_planet_info()

    return dir_planets, conv_planets, dict_extended_info

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

def calc_directed_POF(rad_planets, jd_radix, jd_event, geo_latitude, houses_info, e):
    """returns tuple (pof_rad, pof_directed, pof_converse)"""
    ac, mc, ramc = calc_radix_ac_mc_ramc(houses_info)
    cusps = houses_info[0]
    pof_long = rad_planets[11][1]
    p_house = pd.get_housepos_manual(pof_long, cusps)
    
    ra, decl, _ = swe.cotrans((pof_long, 0.0, 1), e)
    decl = -decl
    
    direct_pof_obj = pd.PD_Base(jd_radix, jd_event, geo_latitude, decl, ra, ramc, mc, True, p_house, ac, pof_long, e)
    long_directed = direct_pof_obj.get_long_directed()

    converse_pof_obj = pd.PD_Base(jd_radix, jd_event, geo_latitude, decl, ra, ramc, mc, False, p_house, ac, pof_long, e)
    long_conv = converse_pof_obj.get_long_directed()

    dict_info = {}
    dict_info["POF"] = direct_pof_obj.get_extended_planet_info()
    
    return long_directed, long_conv, dict_info

def calc_planet_house_pos(ramc, geo_lat, e, long, lat):
    hpos = swe.house_pos(ramc, geo_lat, e, (long,lat), b'T')
    
    return int(hpos)

def calc_radix_ac_mc_ramc(houses_info):
    """returns tuple of radix (ac, mc, ramc)"""
    ac = houses_info[0][0]
    mc = houses_info[1][1]
    ramc = houses_info[1][2]
    
    return (ac, mc, ramc)