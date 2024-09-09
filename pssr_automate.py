import julian
from datetime import datetime, timedelta
import astro_seek_read 
import swisseph as swe

ZODIAC_SIGNS = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", 
                "scorpio","sagittarius", "capricorn", "aquarius", "pisces"]

def calc_natal_planets_labelled(jd_radix, label):
    rad_planets = []
    for planet in range(0, len(PLANETS)):
        xx, _ = swe.calc_ut(jd_radix, planet)
        long = xx[0]

        rad_planets.append((PLANETS[planet], long, label))    
    return rad_planets

def convert_full_dec_degrees_to_zod_min_sec(full_dec_degrees):
    zod, deg = convert_dec_degrees_to_zod(full_dec_degrees)
    deg = convert_dec_degrees_to_deg_min_sec(deg)
    return (zod,deg)

def get_prenatal_trans_date(radix_datetime, event_datetime):
    jd_rad = julian.to_jd(radix_datetime)
    jd_event = julian.to_jd(event_datetime)
    jd_prenatal = jd_rad - abs(jd_event - jd_rad) 
    print(jd_rad, jd_event, jd_prenatal, julian.from_jd(jd_prenatal))
    return julian.from_jd(jd_prenatal)

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


def parse_longitude(longitude_str):
    # Example input: '82  18   54      '
    #returns deg,min,sec
    import re

    # Regular expression to extract degrees, minutes, and seconds
    match = re.match(r'(\d+)  (\d+)   (\d+)      ', longitude_str)
    if match:
        degrees = int(match.group(1))
        minutes = int(match.group(2))
        seconds = int(match.group(3))
        return degrees, minutes, seconds
    else:
        raise ValueError("Invalid longitude format")

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
    radix_month_day = (radix_datetime.month, radix_datetime.day)
    event_month_day = (event_datetime.month, event_datetime.day)
    if event_month_day < radix_month_day:
        direct_year = event_datetime.year - 1
    else:
        direct_year = event_datetime.year
    return direct_year

def get_ayanamsa(datetime):
    try:
        str_rad_month = datetime.strftime("%B").lower()
    except ValueError:
        raise ValueError("Month number must be between 1 and 12")
    aya_degrees, aya_minutes = astro_seek_read.m_get_astro_emphemeris_ayanam\
    (str_rad_month,datetime.year)
    decimal_aya_degrees = get_decimal_degrees(aya_degrees, aya_minutes, 0)
    return decimal_aya_degrees

def accumulate_output():
    output = []

    def log(msg):
        output.append(msg)

    return output, log

def m_auto_pssr(r_day, r_month, r_year, r_hour, r_minute, r_second, e_day, e_month, 
                e_year, e_hour, e_minute, e_second, timezone):
    output, log = accumulate_output()
    #have radix and event datetimes
    radix_datetime = datetime(r_year, r_month, r_day, r_hour, r_minute, r_second)
    event_datetime = datetime(e_year, e_month, e_day, e_hour, e_minute, e_second)
    log(f"Radix datetime#{radix_datetime}")
    log(f"Event datetime#{event_datetime}")

    #get pssr direct year
    pssr_direct_year = calc_pssr_direct_year(radix_datetime, event_datetime)
    log(f"PSSR direct year#{pssr_direct_year}")

    #get radix ayanamsa
    radix_aya_dec_degrees = get_ayanamsa(radix_datetime)
    log(f"Radix ayanamsa#{radix_aya_dec_degrees}")

    #get event ayanamsa
    event_aya_dec_degrees = get_ayanamsa(event_datetime)
    log(f"Event ayanamsa#{event_aya_dec_degrees}")

    #get precession
    precession_dec_degrees = abs(radix_aya_dec_degrees - event_aya_dec_degrees)
    log(f"Precession#{precession_dec_degrees}")

    #get radix sun
    str_positions, detailed_positions = \
    astro_seek_read.m_get_astro_chart_positions(r_day, r_month, r_year, \
                                                r_hour, r_minute, r_second)
    str_sun_longitude = astro_seek_read.m_get_sun_longitude(detailed_positions)
    sun_degrees,sun_minutes,sun_seconds = parse_longitude(str_sun_longitude)
    sun_dec_degrees = get_decimal_degrees(sun_degrees, sun_minutes, sun_seconds)
    log(f"Sun's longitude#{sun_dec_degrees}")

    #get precessed sun
    precessed_sun_dec_degrees = sun_dec_degrees + precession_dec_degrees
    log(f"Precessed sun's longitude#{precessed_sun_dec_degrees}")

    #get sign and degree of precessed sun
    precessed_sun_sign, precessed_sun_zod_degrees = convert_dec_degrees_to_zod\
    (precessed_sun_dec_degrees)
    log(f"Precessed sun's sign and zodiac degree#{precessed_sun_sign},{precessed_sun_zod_degrees}")

    #get datetime of precessed sun radix
    pre_sun_degree, pre_sun_minute, pre_sun_second = convert_dec_degrees_to_deg_min_sec\
    (precessed_sun_zod_degrees)
    log(f"Precessed sun's position#{pre_sun_degree} {pre_sun_minute}\'{pre_sun_second}\'\'")

    precessed_radix_datetime = astro_seek_read.m_get_astro_sun_return(pre_sun_degree,\
                                    pre_sun_minute, pre_sun_second, precessed_sun_sign,\
                                    radix_datetime.year, timezone)
    log(f"Precessed radix datetime#{precessed_radix_datetime}")

    #get pssr dir datetime
    pssr_direct_datetime = astro_seek_read.m_get_astro_sun_return(pre_sun_degree,\
    pre_sun_minute, pre_sun_second, precessed_sun_sign,\
    pssr_direct_year, timezone)
    log(f"PSSR direct datetime#{pssr_direct_datetime}")

    #JD calculations
    jd_radix = dt_gregorian_to_julian(radix_datetime)
    jd_event = dt_gregorian_to_julian(event_datetime)
    jd_rad_event_diff = abs(jd_event - jd_radix)
    jd_pssr = dt_gregorian_to_julian(pssr_direct_datetime)
    jd_pssr_event_diff = abs(jd_pssr - jd_event)
    jd_converse = jd_radix - jd_rad_event_diff
    log(f"jd_radix#{jd_radix}, jd_event#{jd_event}, jd_rad_event_diff#{jd_rad_event_diff}, jd_pssr#{jd_pssr}, jd_pssr_event_diff#{jd_pssr_event_diff},jd_converse#{jd_converse}")


    #get event to pssr time lapse
    direct_dec_timelapse = jd_pssr_event_diff / 15.218425 
    time_timelapse = decimal_to_time(direct_dec_timelapse)
    dt_reg_pssr_dir = pssr_direct_datetime - time_timelapse
    dt_prog_pssr_dir = pssr_direct_datetime + time_timelapse
    log(f"Regressed pssr datetime#{dt_reg_pssr_dir}")
    log(f"Progressed pssr datetime#{dt_prog_pssr_dir}")

    #get converse event datetime
    converse_datetime = julian_to_gregorian(jd_converse)
    log(f"Converse datetime#{converse_datetime}")

    #get converse pssr year
    if (pssr_direct_year == event_datetime.year):
        pssr_converse_year = converse_datetime.year
    else:
        pssr_converse_year = converse_datetime.year + 1
    log(f"PSSR converse year#{pssr_converse_year}")

    #get converse ayanamsa
    converse_aya_dec_degrees = get_ayanamsa(converse_datetime)
    log(f"Converse ayanamsa#{converse_aya_dec_degrees}")

    #get converse precession
    conv_precession_dec_degrees = abs(radix_aya_dec_degrees - converse_aya_dec_degrees)
    log(f"Converse precession#{conv_precession_dec_degrees}")

    #get converse precessed sun
    conv_precessed_sun_dec_degrees = sun_dec_degrees - conv_precession_dec_degrees
    log(f"Converse precessed sun's longitude#{conv_precessed_sun_dec_degrees}")

    #get converse sign and degree of precessed sun
    conv_precessed_sun_sign, conv_precessed_sun_zod_degrees = \
    convert_dec_degrees_to_zod(conv_precessed_sun_dec_degrees)
    log(f"Converse precessed sun's sign and zodiac degree#{conv_precessed_sun_sign},{conv_precessed_sun_zod_degrees}")

    #get datetime of converse precessed sun radix
    conv_pre_sun_degree, conv_pre_sun_minute, conv_pre_sun_second =\
    convert_dec_degrees_to_deg_min_sec(conv_precessed_sun_zod_degrees)
    log(f"Converse precessed sun's position#{conv_pre_sun_degree}{conv_pre_sun_minute}\'{conv_pre_sun_second}\'\'")

    conv_precessed_radix_datetime = astro_seek_read.m_get_astro_sun_return(\
        conv_pre_sun_degree,conv_pre_sun_minute, \
        conv_pre_sun_second, conv_precessed_sun_sign,radix_datetime.year, timezone)
    log(f"Precessed radix datetime#{conv_precessed_radix_datetime}")

    #get converse pssr dir datetime
    pssr_converse_datetime = astro_seek_read.m_get_astro_sun_return(
        conv_pre_sun_degree,conv_pre_sun_minute, conv_pre_sun_second,
        conv_precessed_sun_sign, pssr_converse_year, timezone)
    log(f"Converse PSSR direct datetime#{pssr_converse_datetime}")

    #jds converse
    jd_conv_pssr = dt_gregorian_to_julian(pssr_converse_datetime)
    jd_conv_pssr_event_diff = abs(jd_conv_pssr - jd_converse)
    log(f"jd_conv_pssr#{jd_conv_pssr}, jd_conv_pssr_event_diff#{jd_conv_pssr_event_diff}")

    #get converse event to pssr time lapse
    converse_dec_timelapse = jd_conv_pssr_event_diff / 15.218425 
    time_timelapse = decimal_to_time(converse_dec_timelapse)
    dt_reg_pssr_conv = pssr_converse_datetime - time_timelapse
    dt_prog_pssr_conv = pssr_converse_datetime + time_timelapse
    log(f"Regressed pssr converse datetime#{dt_reg_pssr_conv}")
    log(f"Progressed pssr converse datetime#{dt_prog_pssr_conv}")
    log("*****************************************************\n\n")

    '''with open("output_auto_pssr.txt", "a") as f:
        f.write("\n".join(output))
        print("done writing log to file")'''

    return (dt_reg_pssr_dir, dt_prog_pssr_dir, dt_reg_pssr_conv, dt_prog_pssr_conv)
    
