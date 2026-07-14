import swisseph as swe
from aspects_base import find_secondary_swiss_aspects, remove_duplicates, format_house_list, convert_dec_degrees_to_deg_min_sec
import julian
from constants import PLANETS, calc_planets_labelled, calc_planets_pof_houses_labelled 
        
class Secondary_Auto:
    def __init__(self, jd_radix, jd_event, geo_lat, geo_long, e, ramc=None, rad_planets=None):
        self.__dict_info = {}
        self.secondary_for_event(jd_radix, jd_event, geo_lat, geo_long, e, ramc, rad_planets)

    def secondary_for_event(self, jd_radix, jd_event, geo_lat, geo_long, e, ramc=None, rad_positions=None):
        if rad_positions is None:
            rad_positions = calc_planets_pof_houses_labelled(jd_radix,[geo_lat,geo_long])
            houses = swe.houses(jd_radix, geo_lat, geo_long, b'T')
            ramc = houses[1][2]

        prog_positions, reg_positions, self.__dict_info = get_all_secondary_positions(jd_radix, jd_event, geo_lat, geo_long, e, ramc, rad_positions)
        
        str_aspects_rad_prog =  find_secondary_swiss_aspects(rad_positions, prog_positions)
        str_aspects_rad_reg =  find_secondary_swiss_aspects(rad_positions, reg_positions)
        str_aspects_prog_prog =  find_secondary_swiss_aspects(prog_positions, prog_positions)
        str_aspects_reg_reg =  find_secondary_swiss_aspects(reg_positions, reg_positions)
        str_aspects_prog_prog =  remove_duplicates(str_aspects_prog_prog)
        str_aspects_reg_reg =  remove_duplicates(str_aspects_reg_reg)

        self.__str_rad_n_prog = str_aspects_rad_prog + str_aspects_prog_prog
        self.__str_rad_n_reg = str_aspects_rad_reg + str_aspects_reg_reg

    def get_str_aspects(self):
        return self.__str_rad_n_prog, self.__str_rad_n_reg

    def get_dict_info(self):
        return self.__dict_info

def get_all_secondary_positions(jd_radix, jd_event, geo_lat, geo_long, e, ramc, rad_planets):
    """returns tuple rad_pos, prog_pos, reg_pos, dict_info"""
    dict_info = {}
    jd_diff = abs(jd_radix-jd_event)
    days_diff = jd_diff / 365.2422
    jd_prog = jd_radix + days_diff
    jd_reg = jd_radix - days_diff

    #getting prog/reg arc
    xx, _ = swe.calc_ut(jd_radix, swe.SUN, swe.FLG_EQUATORIAL)
    ra_rad = xx[0]
    xx, _ = swe.calc_ut(jd_prog, swe.SUN, swe.FLG_EQUATORIAL)
    ra_prog = xx[0]    
    xx, _ = swe.calc_ut(jd_reg, swe.SUN, swe.FLG_EQUATORIAL)
    ra_reg = xx[0]

    arc_prog = ra_prog - ra_rad
    arc_reg = ra_reg - ra_rad

    #directed houses 
    houses_prog = swe.houses_armc(swe.degnorm(ramc+arc_prog), geo_lat, e, b'T')[0] 
    houses_reg = swe.houses_armc(swe.degnorm(ramc+arc_reg), geo_lat, e, b'T')[0] 
    houses_prog =  format_house_list(houses_prog, '(p)')
    houses_reg =  format_house_list(houses_reg, '(c)')

    planets_prog = calc_planets_labelled(jd_prog, "(p)")
    planets_reg = calc_planets_labelled(jd_reg, "(c)")
    #add POF
    pof_prog = calc_POF(planets_prog, houses_prog[0][1])
    pof_reg = calc_POF(planets_reg, houses_reg[0][1])
    planets_prog.append(('POF', pof_prog,"(p)"))
    planets_reg.append(('POF', pof_reg,"(c)"))

    dict_info = {
        "dt_radix": julian.from_jd(jd_radix),
        "dt_event": julian.from_jd(jd_event),
        "geopos": [geo_lat, geo_long],
        "days_diff_radix_event": days_diff,
        "dt_progressed": julian.from_jd(jd_prog),
        "dt_regressed": julian.from_jd(jd_reg),
        "RA_sun_rad": convert_dec_degrees_to_deg_min_sec(ra_rad),
        "RA_sun_prog": convert_dec_degrees_to_deg_min_sec(ra_prog),
        "RA_sun_reg": convert_dec_degrees_to_deg_min_sec(ra_reg),
        "arc_progressed": convert_dec_degrees_to_deg_min_sec(arc_prog),
        "arc_regregressed": convert_dec_degrees_to_deg_min_sec(arc_reg),
        "RAMC": convert_dec_degrees_to_deg_min_sec(ramc),
        "e": convert_dec_degrees_to_deg_min_sec(e),
        "rad_positions": rad_planets,
        "progressed_positions": [*planets_prog, *houses_prog],
        "regressed_positions": [*planets_reg, * houses_reg]
    }

    return [*planets_prog, *houses_prog], [*planets_reg, * houses_reg], dict_info

def calc_POF(planets, ac):
    sun_index = PLANETS.index('Sun')
    moon_index = PLANETS.index('Moon')
    long_sun = planets[sun_index][1]
    long_moon = planets[moon_index][1]

    return swe.degnorm(ac + long_moon - long_sun)

