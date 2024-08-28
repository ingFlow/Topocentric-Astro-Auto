import math
import pssr_automate as pssr
import astro_seek_read 
from datetime import datetime

'''this obliquity is not the true one that takes into account the nutation and stuff'''
def calculate_obliquity(JD):
  t = (JD - 2451545.0) / 3652500

  e = (84381.448 - 
       4680.93 * t - 
       1.55 * t**2 + 
       1999.25 * t**3 - 
       51.38 * t**4 - 
       249.67 * t**5 - 
       39.05 * t**6 + 
       7.12 * t**7 + 
       27.87 * t**8 + 
       5.79 * t**9 + 
       2.45 * t**10)

  return e/3600

'''based on juan's formula in pred astro p69 pdf'''
def calculate_longitude(E, phi, OA):
    E_rad = math.radians(E)
    phi_rad = math.radians(phi)
    OA_rad = math.radians(OA)

     #if the OA is OD then the obliquity is negative
    tan_long =  (math.sin(E_rad) * math.tan(phi_rad) - 
                math.cos(E_rad) * math.cos(OA_rad)) / math.sin(OA_rad)

     #get tan-1(long)
    LONG_rad = math.atan(tan_long)

    # Convert radians to degrees
    LONG_deg = math.degrees(LONG_rad)

    '''Adjust the result based on the value of OA - if OA is is less than 180 then add 90, if bigger than 180 add 270'''
    if OA < 180:
        LONG_deg += 90
    else:
        LONG_deg += 270

    # Ensure the longitude is within the range [0, 360) degrees
    LONG_deg = LONG_deg % 360

    return LONG_deg

def get_point_quadrant(ac, mc, long):
    quadrant = 0
    dc = (ac + 180) % 360
    ic = (mc - 180) % 360
    
    if (mc <= long):
        quadrant = 1
    elif (ac <= long < ic):
        quadrant = 2
    elif (ic <= long < dc):
        quadrant = 3
    elif (dc <= long):
        quadrant = 4

    print(f"ac {ac}, mc {mc}, long {long}, quadrant {quadrant}")
    return quadrant

def calculate_MD(RA, RAMC, quadrant):
    #make sure RA is not larger than 360 
    MD = 0.00
    RA = RA % 360
    RAIC = (RAMC-180) % 360

    if quadrant in (1,4):
        MD = abs(RAMC - RA)
    elif quadrant in (2,3):
        MD = abs(RAIC - RA)

    return MD

'''make sure input lat is negative or positive for N vs S(-ve)'''
def calculate_AD(GEO_LAT, DECL):
    sin_AD = math.tan(math.radians(GEO_LAT)) * math.tan(math.radians(DECL))
    
    if (sin_AD < -1) or (sin_AD > 1):
        raise ValueError(f"Value out of domain for arcsin function: must be between -1 and 1 - IN AD CALCULATION: GEO_LAT {GEO_LAT} DECL {DECL}")

    return math.degrees(math.asin(sin_AD))

'''GEO_LAT MUST BE DECIMAL FORM, all calculations are in degrees'''
def calculate_SA(AD, ac, long, GEO_LAT):
    #FIND OUT IF ABOVE OR BELOW HORIZON IF ABOVE/BELOW AC/DC AXIS
    NS_indicator = 1
    dc = (ac + 180) % 360
    
    if (ac <= long < dc):
        NS_indicator = -1
        
    SA = 90 + AD if (GEO_LAT*NS_indicator > 0) else 90 - AD
    
    return SA

def calculate_Pole_phi(MD, SA, GEO_LAT):
    tan_phi = (MD/SA) * math.tan(math.radians(GEO_LAT))
        
    return math.degrees(math.atan(tan_phi))

def calculate_ADP(phi, DECL):
    sin_ADP  = math.tan(math.radians(phi)) * math.tan(math.radians(DECL))
            
    if (sin_ADP < -1) or (sin_ADP > 1):
        raise ValueError(f"Value out of domain for arcsin function: must be between -1 and 1 - IN ADP CALCULATION: DECL {DECL} phi {phi}")

    return math.degrees(math.asin(sin_ADP))

def calculate_OA_OD(RA, ADP, GEO_LAT, quadrant):
    # if north/south calculation changes
    OA_OD = 0.0
    FLAG_ASCEN = None
    
    if (GEO_LAT >= 0):
        OA_OD = RA - ADP if (quadrant in (1,2)) else RA + ADP
        FLAG_ASCEN = True if (quadrant in (1,2)) else False
    else:
        OA_OD = RA + ADP if (quadrant in (1,2)) else RA - ADP
        FLAG_ASCEN = False if (quadrant in (1,2)) else True


    return OA_OD, FLAG_ASCEN
        
def calculate_MDO(MD, SA):
    return MD/SA*90

def get_data_for_planet(date, event_date, planet):
    '''need to return: GEO_LAT, DECL, RA, RAMC, LST'''
    GEO_LAT = astro_seek_read.m_get_GEO_LAT(event_date)
    RAMC, RA, DECL = astro_seek_read.m_get_RAMC_RA_DECL_point(event_date,'Saturn')
    LST = astro_seek_read.m_get_LST(event_date)
    
    data = (GEO_LAT, DECL, RA, RAMC, LST)
    return data

def calc_arc(jd_radix, jd_event):
    naibod = (0+ 59/60 + 8.33/3600)
    naibod_day = 0.00269861
    jd_diff = abs(jd_radix-jd_event)
    arc = jd_diff*naibod_day
    return arc

def calc_house_pole(house_no, GEO_LAT):
    tan_phi = 0.0
    if house_no in (3, 9, 5, 11):
        tan_phi = (1/3) * math.tan(math.radians(GEO_LAT))
    elif house_no in (2, 8, 6, 12):
        tan_phi = (2/3) * math.tan(math.radians(GEO_LAT))
    elif house_no == 1:
        tan_phi = math.tan(math.radians(GEO_LAT))
    else:
        print(f"House number {house_no} is not handled.")

    return math.degrees(math.atan(tan_phi))
    

def calc_houses_with_ramc(RAMC, jd, GEO_LAT, label):   
    directed_longitudes = []
    E = calculate_obliquity(jd)
    print(f"RAMC: {RAMC}, E: {E}, GEO_LAT: {GEO_LAT}")
    
    houses = [11, 12, 1, 2, 3]
    count = 1
    for house in houses:
        OA = (RAMC + (30*count)) % 360
        phi = calc_house_pole(house, GEO_LAT)
        long = calc_long_from_OA(OA, phi, E, True)
        print(f"HOUSE: {house}, OA: {OA}, phi: {phi}, long: {long}")

        house_name = 'H' + str(house) 
        directed_longitudes.append((house_name, long, label))
        count +=1

    long = calc_long_from_OA(RAMC, 0.0, E, True)
    directed_longitudes.append(('MC',long, label))
    
    return directed_longitudes

def calc_long_from_OA(OA, phi, E, flag_ascen):
    if not(flag_ascen):
        E *= -1
    tan_long = (math.sin(math.radians(E)) * math.tan(math.radians(phi)) - math.cos(math.radians(E)) * math.cos(math.radians(OA))) / math.sin(math.radians(OA))
    LONG_deg = math.degrees(math.atan(tan_long))

    if (OA < 180):
        LONG_deg += 90
    else:
        LONG_deg += 270
    return LONG_deg % 360

def get_directed_from_data(jd_radix, jd_event, GEO_LAT, DECL, RA, RAMC, flag_direct, quadrant, ac, long):
    E = calculate_obliquity(jd_radix)

    MD = calculate_MD(RA, RAMC, quadrant)
    AD = calculate_AD(GEO_LAT, DECL)
    SA = calculate_SA(AD, ac, long, GEO_LAT)
    if (MD > SA):
        print('\nTHIS HAPPENED MD>SA PAY ATTENTION!!!!!!\n') # see solution in marr
    phi = calculate_Pole_phi(MD, SA, GEO_LAT)
    ADP = calculate_ADP(phi, DECL)

    OA_OD, FLAG_ASCEN = calculate_OA_OD(RA, ADP, GEO_LAT, quadrant)


    print('planet_data:')
    print('LONG', long)
    print('AC', ac)
    print(f'RA: {RA}')
    print(f'RAMC: {RAMC}')
    print(f'DECL: {DECL}')
    print(f'GEO_LAT: {GEO_LAT}')
    print('QUADRANT: ', quadrant)
    print(f'MD: {MD}')
    print(f'AD: {AD}')
    print(f'SA: {SA}')
    print(f'PHI: {phi}')
    print(f'ADP: {ADP}')
    print(f'OA/OD: {OA_OD}{FLAG_ASCEN}')
    print(f'E: {E}')
    
    arc = calc_arc(jd_radix, jd_event)
    dir_OA = OA_OD + arc if flag_direct else OA_OD - arc

    LONG_deg = calc_long_from_OA(dir_OA, phi, E, FLAG_ASCEN)
    print(f"arc: {arc}")
    print(f"directed OA/OD: {dir_OA}")
    print(f"long directed: {LONG_deg}")
    
    return LONG_deg
    

'''flag_direct is to know if its dir/conv dir to know whether to add/minus the arc'''
def get_directed_from_date(date_event, date_radix, point_to_direct, flag_direct):
     #get arc of direction from event date using Naibod
     naibod_dec = pssr.get_decimal_degrees(0,59,8.33)
     jd_event = pssr.dt_gregorian_to_julian(date_event)
     jd_radix = pssr.dt_gregorian_to_julian(date_radix)
     jd_diff = abs(jd_event-jd_radix)
     arc_decimal = jd_diff*naibod_dec
     arc_degrees = pssr.convert_dec_degrees_to_deg_min_sec(arc_decimal)

     #GETTING LONG OF DIRECTED POINT STARTING FROM NATAL INFO
     #calculating e at radix date(check that  this is sound) {TODO}
     e_radix_decimal = calculate_obliquity(jd_radix)
    
     #need OA of the point to direct
     GEO_LAT, DECL, RA, RAMC, LST = get_data_for_planet(date_event, point_to_direct)
     MD = calculate_MD(RA, RAMC)
     AD = calculate_AD(GEO_LAT, DECL)
     SA = calculate_SA(AD, LST, RA, GEO_LAT, DECL)
     phi = calculate_Pole_phi(MD, SA, GEO_LAT)
     ADP = calculate_ADP(phi, DECL)
    

     #OA_OD = calculate_OA_OD(RA, ADP, GEO_LAT)


     directed_long = calculate_longitude(e_radix_decimal, phi, None)
     directed_long_sign, directed_long_dec = pssr.convert_dec_degrees_to_zod(directed_long)
     directed_long_deg_min_sec = pssr.convert_dec_degrees_to_deg_min_sec(directed_long_dec)
     print(f"Longitude: {directed_long_sign} degrees {directed_long_deg_min_sec}")

radix_date = datetime(2018, 2, 19, 12, 00, 00)
event_date = datetime(2000, 12, 19, 17, 00, 00)
#pn, ps = astro_seek_read.m_get_astro_chart_positions(event_date.day, event_date.month, event_date.year, event_date.hour, event_date.minute, event_date.second)
#print(astro_seek_read.m_get_RA_point(event_date, 'Node'))
