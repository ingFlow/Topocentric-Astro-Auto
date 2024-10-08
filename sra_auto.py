import swisseph as swe
import julian
from datetime import datetime, timedelta
import aspects_base as aspects

ZODIAC_SIGNS = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", 
                "scorpio","sagittarius", "capricorn", "aquarius", "pisces"]
PLANETS = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Mean_Node']


def calc_planets_houses_labelled(jd, label, planets_indexes_to_exclude, geopos):
    planets_houses = []
    
    for planet in range(0, len(PLANETS)):
        if (planet in planets_indexes_to_exclude):
            pass
        else:
            xx, _ = swe.calc_ut(jd, planet)
            long = xx[0]

            planets_houses.append((PLANETS[planet], long, label))  
   
    houses = swe.houses(jd, geopos[0], geopos[1], b'T')[0]
    for i in range(0, len(houses)):
        planets_houses.append((f"H{i}", houses[i], label))
      
    return planets_houses


def convert_full_dec_degrees_to_zod_min_sec(full_dec_degrees):
    zod, deg = convert_dec_degrees_to_zod(full_dec_degrees)
    deg = convert_dec_degrees_to_deg_min_sec(deg)
    return (zod,deg)

def julian_to_gregorian(julian_day):
    return julian.from_jd(julian_day)

def gregorian_to_julian(year, month, day, hour=12, minute=0, second=0):
    dt = datetime(year, month, day, hour, minute, second)
    return julian.to_jd(dt)

def dt_gregorian_to_julian(dt):
    return julian.to_jd(dt)

def decimal_to_time(decimal_time):
    hours, minutes, seconds = convert_dec_degrees_to_deg_min_sec(decimal_time)
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)

def get_decimal_degrees(degrees, minutes, seconds):
    return int(degrees) + int(minutes) / 60 + int(seconds) / 3600

def convert_dec_degrees_to_zod(decimal_degrees):
    segment_size = 30
    index = int(decimal_degrees // segment_size)
    zodiac_degree = decimal_degrees - index * segment_size
    return ZODIAC_SIGNS[index], zodiac_degree

def convert_dec_degrees_to_deg_min_sec(decimal_degrees):
    degrees = int(decimal_degrees)
    fractional_degrees = abs(decimal_degrees - degrees)
    minutes = int(fractional_degrees * 60)
    seconds = int(round((fractional_degrees * 60 - minutes) * 60, 2))

    return degrees, minutes, seconds

def calc_direct_year(radix_datetime, event_datetime):
    """give the year for the solar return corresponding to an event """
    radix_month_day = (radix_datetime.month, radix_datetime.day)
    event_month_day = (event_datetime.month, event_datetime.day)
    if event_month_day < radix_month_day:
        direct_year = event_datetime.year - 1
    else:
        direct_year = event_datetime.year
    return direct_year

def sra_for_date_event_norad(jd_radix, jd_event, geopos):
    """returns tuple of str_dir aspects and str_conv aspects"""
    rad_planets = []
    geo_latitude = geopos[0]
    geo_longitude = geopos[1]
    for planet in range(0, len(PLANETS)):
        xx, _ = swe.calc_ut(jd_radix, planet)
        long = xx[0]

        rad_planets.append((PLANETS[planet], long, "(r)")) 
    houses = swe.houses(jd_radix, geo_latitude, geo_longitude, b'T')
    ac = houses[0][0]
    sun_long = rad_planets[PLANETS.index('Sun')][1]
    moon_long = rad_planets[PLANETS.index('Moon')][1]
    pof_long = swe.degnorm(ac + moon_long - sun_long)
    rad_planets.append(('POF',pof_long,'(r)'))
    for house_no in range(0,len(houses[0])):
        rad_planets.append((f'H{house_no+1}',houses[0][house_no],'(r)'))

    str_rad_sra_aspects, str_sra_sra_aspects = calc_sra_for_date(julian.from_jd(jd_radix),julian.from_jd(jd_event),rad_planets, geopos)

    return str_rad_sra_aspects, str_sra_sra_aspects

def calc_sra_for_date(dt_radix, dt_event, rad_planets, geopos):
    """returns tuple with 2 str of aspects td/tc tropical direct/converse and pd/pc precessed equiv."""
    jd_radix = julian.to_jd(dt_radix)
    jd_event = julian.to_jd(dt_event)

    direct_year = calc_direct_year(dt_radix, dt_event)
    jd_dir_start = julian.to_jd(datetime(direct_year,1,1,0,0,0))
    rad_aya = swe.get_ayanamsa_ut(jd_radix)
    event_aya = swe.get_ayanamsa_ut(jd_event)
    dir_precession = abs(rad_aya - event_aya)
    xx, _ = swe.calc_ut(jd_radix, swe.SUN)
    rad_sun_long = xx[0]
    dir_sun_long_precessed = rad_sun_long + dir_precession
    
    #PRENATAL
    jd_conv_event = jd_radix - abs(jd_radix - jd_event)
    year_diff = abs(dt_radix.year - dt_event.year)
    if (direct_year == dt_event.year):
        converse_year = dt_radix.year - year_diff
    else:
        converse_year = (dt_radix.year - year_diff) + 1
    jd_conv_start = julian.to_jd(datetime(converse_year,1,1,0,0,0))
    
    event_aya = swe.get_ayanamsa_ut(jd_conv_event)
    conv_precession = abs(rad_aya - event_aya)
    conv_sun_long_precessed = rad_sun_long - conv_precession
    
    jd_dir_return = swe.solcross_ut(rad_sun_long, jd_dir_start)
    jd_dir_return_precessed = swe.solcross_ut(dir_sun_long_precessed, jd_dir_start)
    jd_conv_return = swe.solcross_ut(rad_sun_long, jd_conv_start)
    jd_conv_return_precessed = swe.solcross_ut(conv_sun_long_precessed, jd_conv_start)
    
    planets_to_exclude = []
    trop_dir_planets = calc_planets_houses_labelled(jd_dir_return, '(td)', planets_to_exclude, geopos)
    trop_conv_planets = calc_planets_houses_labelled(jd_conv_return, '(tc)', planets_to_exclude, geopos)
    precessed_dir_planets = calc_planets_houses_labelled(jd_dir_return_precessed, '(pd)', planets_to_exclude, geopos)
    precessed_conv_planets = calc_planets_houses_labelled(jd_conv_return_precessed, '(pc)', planets_to_exclude, geopos)
    sra_planets = [*trop_dir_planets, *trop_conv_planets, *precessed_dir_planets, *precessed_conv_planets]
 
    str_rad_sra_aspects = aspects.find_sra_swiss_aspects(rad_planets,sra_planets) 
    str_td_td_aspects = aspects.find_sra_swiss_aspects(trop_dir_planets, trop_dir_planets)
    str_tc_tc_aspects = aspects.find_sra_swiss_aspects(trop_conv_planets, trop_conv_planets)
    str_pd_pd_aspects = aspects.find_sra_swiss_aspects(precessed_dir_planets, precessed_dir_planets)
    str_pc_pc_aspects = aspects.find_sra_swiss_aspects(precessed_conv_planets, precessed_conv_planets)
    str_sra_sra_aspects = [*str_td_td_aspects, *str_tc_tc_aspects, *str_pd_pd_aspects, *str_pc_pc_aspects]
    str_rad_sra_aspects = aspects.remove_duplicates(str_rad_sra_aspects)

    return str_rad_sra_aspects, str_sra_sra_aspects

jd_radix = julian.to_jd(datetime(1926,4,21,1,38,12))
jd_event = julian.to_jd(datetime(1953,6,6,12,00,00))
geopos = [51.5166667, -0.111666667, 15.0]

jd_radix = julian.to_jd(datetime(1940,10,9,17,24,13))
jd_event = julian.to_jd(datetime(1980,12,8,12,00,00))
geopos = [53.733333, -2.9833333, 15.0]
print(sra_for_date_event_norad(jd_radix,jd_event,geopos))