import swisseph as swe
import julian
from datetime import datetime, timedelta
import aspects_base as aspects

ZODIAC_SIGNS = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", 
                "scorpio","sagittarius", "capricorn", "aquarius", "pisces"]
PLANETS = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Mean_Node']


def calc_planets_labelled(jd_radix, label, planets_indexes_to_exclude):
    planets = []
    
    for planet in range(0, len(PLANETS)):
        if (planet in planets_indexes_to_exclude):
            pass
        else:
            xx, _ = swe.calc_ut(jd_radix, planet)
            long = xx[0]

            planets.append((PLANETS[planet], long, label))    
    return planets


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

def calc_pssr_direct_year(radix_datetime, event_datetime):
    """give the year for the solar return corresponding to an event """
    radix_month_day = (radix_datetime.month, radix_datetime.day)
    event_month_day = (event_datetime.month, event_datetime.day)
    if event_month_day < radix_month_day:
        direct_year = event_datetime.year - 1
    else:
        direct_year = event_datetime.year
    return direct_year


def calc_pssr_for_date(dt_radix, dt_event, geo_latitude, geo_longitude):
    """returns tuple with 2 str of aspects rad to direct and conv pssr (prog/reg)"""
    jd_radix = julian.to_jd(dt_radix)
    jd_event = julian.to_jd(dt_event)

    pssr_direct_year = calc_pssr_direct_year(dt_radix, dt_event)
    jd_pssr_start = julian.to_jd(datetime(pssr_direct_year,1,1,0,0,0))
    rad_aya = swe.get_ayanamsa_ut(jd_radix)
    event_aya = swe.get_ayanamsa_ut(jd_event)
    precession = abs(rad_aya - event_aya)
    xx, _ = swe.calc_ut(jd_radix, swe.SUN)
    sun_long = xx[0]
    sun_long_precessed = sun_long + precession
    
    jd_pssr = swe.solcross_ut(sun_long_precessed, jd_pssr_start)
    jd_rad_event_diff = abs(jd_radix - jd_event)
    jd_pssr_event_diff = abs(jd_pssr - jd_event)
    jd_conv_event = jd_radix - jd_rad_event_diff

    timelapse = timedelta(hours=jd_pssr_event_diff / 15.218425)
    jd_prog_pssr_dir = julian.to_jd(julian.from_jd(jd_pssr) + timelapse)
    jd_reg_pssr_dir = julian.to_jd(julian.from_jd(jd_pssr) - timelapse)

    year_diff = abs(dt_radix.year - dt_event.year)
    if (pssr_direct_year == dt_event.year):
        pssr_converse_year = dt_radix.year - year_diff
    else:
        pssr_converse_year = (dt_radix.year - year_diff) + 1
    jd_pssr_start = julian.to_jd(datetime(pssr_converse_year,1,1,0,0,0))
    
    event_aya = swe.get_ayanamsa_ut(jd_conv_event)
    precession = abs(rad_aya - event_aya)
    sun_long_precessed = sun_long - precession
    jd_pssr = swe.solcross_ut(sun_long_precessed, jd_pssr_start)
    
    jd_pssr_event_diff = abs(jd_pssr - jd_conv_event)
    
    timelapse = timedelta(hours=jd_pssr_event_diff / 15.218425)
    jd_prog_pssr_conv = julian.to_jd(julian.from_jd(jd_pssr) + timelapse)
    jd_reg_pssr_conv = julian.to_jd(julian.from_jd(jd_pssr) - timelapse)
    
    planets_to_exclude = [PLANETS.index('Sun')]
    prog_dir_planets = calc_planets_labelled(jd_prog_pssr_dir, '(dp)', planets_to_exclude)
    prog_conv_planets = calc_planets_labelled(jd_prog_pssr_conv, '(cp)', planets_to_exclude)
    reg_dir_planets = calc_planets_labelled(jd_reg_pssr_dir, '(dr)', planets_to_exclude)
    reg_conv_planets = calc_planets_labelled(jd_reg_pssr_conv, '(cr)', planets_to_exclude)
    direct_planets = [*prog_dir_planets, *reg_dir_planets]
    conv_planets = [*prog_conv_planets, *reg_conv_planets]

    rad_planets = calc_planets_labelled(jd_radix, '(r)', [])
    houses = swe.houses(jd_radix, geo_latitude, geo_longitude, b'T')
    ac = houses[0][0]
    sun_long = rad_planets[PLANETS.index('Sun')][1]
    moon_long = rad_planets[PLANETS.index('Moon')][1]
    pof_long = swe.degnorm(ac + moon_long - sun_long)
    rad_planets.append(('POF',pof_long,'(r)'))
    for house_no in range(0,len(houses[0])):
        rad_planets.append((f'H{house_no+1}',houses[0][house_no],'(r)'))

    str_rad_direct_aspects = aspects.find_pssr_swiss_aspects(rad_planets,direct_planets)
    str_rad_conv_aspects = aspects.find_pssr_swiss_aspects(rad_planets, conv_planets)
    
    return str_rad_direct_aspects, str_rad_conv_aspects

asp1,asp2 = calc_pssr_for_date(datetime(1889,4,20,17,30,37),datetime(1903,1,3,12,0,0), 48.25, 13.05)
print(asp1)
print(asp2)