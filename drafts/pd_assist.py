import pd_base 
import pd_automate
import swisseph as swe
from constants import calc_planets_pof_houses_labelled
from aspects_base import calculate_obliquity

def get_natal_arc(jd_rad, geo_positions, planet1, planet2):
    """planet1/2 is name of planet"""
    houses_info = swe.houses(jd_rad, geo_positions[0], geo_positions[1], b'T')
    rad_planets_labelled = calc_planets_pof_houses_labelled(jd_rad)
    rad_planets_equatorial = pd_automate.calc_rad_planets_equatorial(jd_rad)
    e = calculate_obliquity(jd_rad)

    long, ra, decl = rad_planets_equatorial[planet1]
    cusps = houses_info[0]
    p_house = pd_base.get_housepos_manual(long, cusps)
    ac, mc, ramc = pd_automate.calc_radix_ac_mc_ramc(houses_info)

    jd_event = jd_rad + 20

    planet1_pd_obj = pd_base.PD_Base(jd_rad, jd_event, geo_positions[0], decl, ra, ramc, mc, True, p_house, ac, long, e)
    
    long, ra, decl = rad_planets_equatorial[planet2]
    cusps = houses_info[0]
    p_house = pd_base.get_housepos_manual(long, cusps)
    ac, mc, ramc = pd_automate.calc_radix_ac_mc_ramc(houses_info)

    jd_event = jd_rad + 20

    planet2_pd_obj = pd_base.PD_Base(jd_rad, jd_event, geo_positions[0], decl, ra, ramc, mc, True, p_house, ac, long, e)
    
    planet1_OA = planet1_pd_obj.OA_OD
    planet2_OA = planet2_pd_obj.OA_OD
    arc = abs(planet1_OA - planet2_OA)
    naibod = (0+ 59/60 + 8.33/3600)
    years_elapsed = arc/naibod
    days_elapsed = years_elapsed * 365
    jd_mature = jd_rad +