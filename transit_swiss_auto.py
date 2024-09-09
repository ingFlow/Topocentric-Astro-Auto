import swisseph as swe
import julian
from datetime import datetime, timedelta
import aspects_base as aspects

PLANETS = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Mean_Node']


def calc_planets_labelled(jd_radix, label):
    planets = []
    
    for planet in range(0, len(PLANETS)):
        xx, _ = swe.calc_ut(jd_radix, planet)
        long = xx[0]

        planets.append((PLANETS[planet], long, label))    
    return planets

def calc_transits_for_date(jd_radix, jd_event, rad_planets):
    """returns tuple with 2 str of aspects rad to direct and conv trans"""
    jd_rad_event_diff = abs(jd_radix - jd_event)
    jd_conv_event = jd_radix - jd_rad_event_diff
    
    dir_planets = calc_planets_labelled(jd_event, '(p)')
    conv_planets = calc_planets_labelled(jd_conv_event, '(c)')

    str_rad_direct_aspects = aspects.find_trans_swiss_aspects(rad_planets,dir_planets)
    str_rad_conv_aspects = aspects.find_trans_swiss_aspects(rad_planets, conv_planets)
    
    return str_rad_direct_aspects, str_rad_conv_aspects

