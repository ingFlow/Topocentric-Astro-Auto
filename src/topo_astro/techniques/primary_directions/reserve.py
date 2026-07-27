"""
techniques/primary_directions/reserve.py - a preserved, currently-unwired
alternate Primary Directions calculation path.

get_directed_from_data implements the same MD > SA quadrant-shift
correction as PD_Base.set_directed_data (trig.py), but takes already-
computed intermediate values (GEO_LAT, DECL, RA, RAMC, mc, house_pos, ac,
long, e) directly as parameters, rather than deriving them internally
from a radix/event pair on every call. Not currently wired into
PD_Automate's active call path - kept because it's a genuinely different,
lower-level, composable entry point that could be useful for a future
caching/bulk-optimization pathway (e.g. reusing RA/DECL/RAMC across many
events for one radix without recomputing them from the ephemeris each
time), not a worse or older copy of the same thing.
"""
import swisseph as swe
from julian import from_jd

from .trig import (
    get_quadrant_from_house_pos,
    calc_md_to_oa_data,
    calc_left_right_angles,
    shift_point_to_closest_next_quad,
    calc_arc,
    calc_long_from_OA,
)


def get_directed_from_data(jd_radix, jd_event, GEO_LAT, DECL, RA, RAMC, mc, flag_direct, house_pos, ac, long, e):
    quadrant = get_quadrant_from_house_pos(house_pos)
    MD, _, SA, phi, _, OA_OD, FLAG_ASCEN = calc_md_to_oa_data(RA, RAMC, quadrant, GEO_LAT, DECL, ac, long)

    if (MD > SA):
        left_angle, right_angle = calc_left_right_angles(ac, mc, quadrant)
        new_quadrant = shift_point_to_closest_next_quad(long, left_angle, right_angle, quadrant)
        MD, _, SA, phi, _, OA_OD, FLAG_ASCEN = calc_md_to_oa_data(RA, RAMC, new_quadrant, GEO_LAT, DECL, ac, long)
        
        if (MD > SA):
            with open("log_md_sa.txt", "a") as file:
                    file.write(f"before \t{from_jd(jd_radix)} ra: {RA} md: {MD} sa: {SA} : oad {OA_OD} {FLAG_ASCEN} \n")

            new_quadrant = shift_point_to_closest_next_quad(long, left_angle, right_angle, quadrant)
            MD, _, SA, phi, _, OA_OD, FLAG_ASCEN = calc_md_to_oa_data(RA, RAMC, new_quadrant, GEO_LAT, DECL, ac, long)
            
            with open("log_md_sa.txt", "a") as file:
                    file.write(f"mid \t{from_jd(jd_radix)} md: {MD} sa: {SA} : oad {OA_OD} {FLAG_ASCEN} \n")

            if (MD > SA):
                with open("log_md_sa.txt", "a") as file:
                    file.write(f"last \t{from_jd(jd_radix)} md: {MD} sa: {SA} : oad {OA_OD} {FLAG_ASCEN} \n")

    arc = calc_arc(jd_radix, jd_event)
    dir_OA = OA_OD + arc if flag_direct else OA_OD - arc
    dir_OA = swe.degnorm(dir_OA)

    LONG_deg = calc_long_from_OA(dir_OA, phi, e, FLAG_ASCEN)
    '''print(f"arc: {arc}")
    print(f"directed OA/OD: {dir_OA}")
    print(f"long directed: {LONG_deg}")'''
    
    return LONG_deg
