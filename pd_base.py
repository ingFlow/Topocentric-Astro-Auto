import math
import swisseph as swe
from aspects_base import convert_dec_degrees_to_deg_min_sec

class PD_Base:
    def  __init__(self, jd_radix, jd_event, GEO_LAT, DECL, RA, RAMC, mc, flag_direct, house_pos, ac, long):
        self.set_directed_data(jd_radix, jd_event, GEO_LAT, DECL, RA, RAMC, mc, flag_direct, house_pos, ac, long)

    def set_directed_data(self, jd_radix, jd_event, GEO_LAT, DECL, RA, RAMC, mc, flag_direct, house_pos, ac, long):
        E = calculate_obliquity(jd_radix)
        quadrant = get_quadrant_from_house_pos(house_pos)
        MD, AD, SA, phi, ADP, OA_OD, FLAG_ASCEN = calc_md_to_oa_data(RA, RAMC, quadrant, GEO_LAT, DECL, ac, long)

        if (MD > SA):
            left_angle, right_angle = calc_left_right_angles(ac, mc, quadrant)
            new_quadrant = shift_point_to_closest_next_quad(long, left_angle, right_angle, quadrant)
            MD, AD, SA, phi, ADP, OA_OD, FLAG_ASCEN = calc_md_to_oa_data(RA, RAMC, new_quadrant, GEO_LAT, DECL, ac, long)
            
            if (MD > SA):
                with open("log_md_sa_4SEP24.txt", "a") as file:
                    file.write(f"{jd_radix} still got error... not okay \n")

        arc = calc_arc(jd_radix, jd_event)
        dir_OA = OA_OD + arc if flag_direct else OA_OD - arc

        LONG_deg = calc_long_from_OA(dir_OA, phi, E, FLAG_ASCEN)

        self.QUADRANT = quadrant
        self.ARC = arc
        self.MD = MD
        self.AD = AD
        self.SA = SA
        self.phi = phi
        self.ADP = ADP
        self.OA_OD = OA_OD 
        self.FLAG_ASCENSION = FLAG_ASCEN
        self.LONG = LONG_deg
        self.MDO = (MD/SA)*90

    def get_long_directed(self):
        return self.LONG

    def get_extended_planet_info(self):
        dict_info = {
            "QUADRANT": self.QUADRANT,
            "ARC": (convert_dec_degrees_to_deg_min_sec(self.ARC),self.ARC),
            "MD": (convert_dec_degrees_to_deg_min_sec(self.MD),self.MD),
            "AD": (convert_dec_degrees_to_deg_min_sec(self.AD),self.AD),
            "SA": (convert_dec_degrees_to_deg_min_sec(self.SA),self.SA),
            "phi": (convert_dec_degrees_to_deg_min_sec(self.phi),self.phi),
            "ADP": (convert_dec_degrees_to_deg_min_sec(self.ADP),self.ADP),
            "OA_OD": (convert_dec_degrees_to_deg_min_sec(self.OA_OD),self.OA_OD),
            "FLAG_ASCENSION": self.FLAG_ASCENSION,
            "MDO": (convert_dec_degrees_to_deg_min_sec(self.MDO),self.MDO)
        }

        return dict_info

def calculate_obliquity(JD):
    '''this obliquity is not the true one that takes into account the nutation and stuff'''

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

def calculate_longitude(E, phi, OA):
    '''based on juan's formula in pred astro p69 pdf'''

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

def has_wraparound(start, end):
        return start > end

def get_quadrant_from_house_pos(house):
    if house in (1, 2, 3):
        return 2
    if house in (4, 5, 6):
        return 3
    if house in (7, 8, 9):
        return 4
    if house in (10, 11, 12):
        return 1
    else:
        return 'ERROR HOUSE NOT HANDLED!'

def get_housepos_manual(long, cusps):
    house_pos = None
    for i in range(12):
        if cusps[i] <= long < cusps[(i + 1) % 12]:
            house_pos = i +1      
        if cusps[(i + 1) % 12] < cusps[i]:
            if (long < cusps[(i+1)%12]) or (long > cusps[i]):
                house_pos = ((i+1)%12) 
                if house_pos == 0:
                    house_pos = 12
    return house_pos

def get_point_quadrant(ac, mc, longitude):
    longitude %= 360
    mc %= 360
    ac %= 360
    ic = swe.degnorm(mc+180)
    dc = swe.degnorm(ac+180)

    if (has_wraparound(mc, ac) and (longitude >= mc or longitude < ac)) or (not has_wraparound(mc, ac) and mc <= longitude < ac):
        return 1

    if (has_wraparound(ac, ic) and (longitude >= ac or longitude < ic)) or (not has_wraparound(ac, ic) and ac <= longitude < ic):
        return 2

    if (has_wraparound(ic, dc) and (longitude >= ic or longitude < dc)) or (not has_wraparound(ic, dc) and ic <= longitude < dc):
        return 3

    if (has_wraparound(dc, mc) and (longitude >= dc or longitude < mc)) or (not has_wraparound(dc, mc) and dc <= longitude < mc):
        return 4

    return "Error: Unable to determine quadrant"

def calculate_MD(RA, RAMC, quadrant):
    RA = swe.degnorm(RA)
    RAIC = swe.degnorm(RAMC-180)

    '''    dist_ramc = abs(swe.difdeg2n(RAMC,RA))
    dist_raic = abs(swe.difdeg2n(RAIC,RA))

    print(dist_ramc, dist_raic, RA, RAMC, quadrant)
    return dist_ramc if (dist_ramc < dist_raic) else dist_raic
'''
    if quadrant == 4:
        return abs(swe.difdeg2n(RAMC,RA))
    if quadrant == 3:
        return abs(swe.difdeg2n(RA,RAIC))
    if quadrant == 2:
        return abs(swe.difdeg2n(RAIC,RA))
    if quadrant == 1:
        return abs(swe.difdeg2n(RA,RAMC))
    #{CHECK IF THIS IS FINE THAT I PUT ABSOLUTE}


'''make sure input lat is negative or positive for N vs S(-ve)'''
def calculate_AD(GEO_LAT, DECL):
    sin_AD = math.tan(math.radians(GEO_LAT)) * math.tan(math.radians(DECL))
    
    if (sin_AD < -1) or (sin_AD > 1):
        raise ValueError(f"Value out of domain for arcsin function: must be between -1 and 1 - IN AD CALCULATION: GEO_LAT {GEO_LAT} DECL {DECL}")

    return math.degrees(math.asin(sin_AD))

'''GEO_LAT MUST BE DECIMAL FORM, all calculations are in degrees'''
def calculate_SA(AD, ac, long, GEO_LAT, quadrant):
    #FIND OUT IF ABOVE OR BELOW HORIZON IF ABOVE/BELOW AC/DC AXIS
    NS_indicator = 1
    dc = swe.degnorm(ac + 180)
    
    if (quadrant in (2, 3)):
        NS_indicator = -1
        
    SA = 90 + AD if (GEO_LAT*NS_indicator > 0) else 90 - AD
    
    return SA

def calculate_Pole_phi(MD, SA, GEO_LAT):
    try:
        tan_phi = (MD / SA) * math.tan(math.radians(GEO_LAT))
        return math.degrees(math.atan(tan_phi))
    except TypeError as e:
        print(f"An error occurred: {e}")
        print(f"MD: {MD}, SA: {SA}, GEO_LAT: {GEO_LAT}")                                                                 
        return
        
def calculate_ADP(phi, DECL):
    sin_ADP  = math.tan(math.radians(phi)) * math.tan(math.radians(DECL))
            
    if (sin_ADP < -1) or (sin_ADP > 1):
        print(f"Value out of domain for arcsin function: must be between -1 and 1 - IN ADP CALCULATION: DECL {DECL} phi {phi}")
        return 0
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

def calc_arc(jd_radix, jd_event):
    naibod = (0+ 59/60 + 8.33/3600)
    naibod_day = 0.00269861
    jd_diff = abs(jd_radix-jd_event)
    arc = jd_diff*naibod_day
    return arc

def calc_house_pole(house_no, GEO_LAT):
    """FOR H1/H2 (NOT HOUSES) USE mdpt1 or 2"""
    tan_phi = 0.0
    if house_no in (3, 9, 5, 11):
        tan_phi = (1/3) * math.tan(math.radians(GEO_LAT))
    elif house_no in (2, 8, 6, 12):
        tan_phi = (2/3) * math.tan(math.radians(GEO_LAT))
    elif house_no in (1, 7):
        tan_phi = math.tan(math.radians(GEO_LAT))
    elif house_no in (4, 10):
        tan_phi = 0
    elif house_no in ('mdpt1', 'mdpt2'):
        tan_phi = 0.5 * math.tan(math.radians(GEO_LAT))
    else:
        print(f"House number {house_no} is not handled.")

    return math.degrees(math.atan(tan_phi))

def calc_houses_with_ramc(RAMC, jd, GEO_LAT, label):   
    directed_longitudes = []
    E = calculate_obliquity(jd)
    #print(f"RAMC: {RAMC}, E: {E}, GEO_LAT: {GEO_LAT}")
    
    houses = [11, 12, 'ASC', 2, 3]
    count = 1

    for house in houses:
        OA = (RAMC + (30*count)) % 360
        phi = calc_house_pole(house, GEO_LAT)
        long = calc_long_from_OA(OA, phi, E, True)
        #print(f"HOUSE: {house}, OA: {OA}, phi: {phi}, long: {long}")
        
        if house == 'ASC':
            house_name = 'ASC'
        else:
            house_name = 'H' + str(house) 

        directed_longitudes.append((house_name, long, label))
        count +=1
    
    long = calc_long_from_OA(RAMC, 0.0, E, True)
    directed_longitudes.append(('MC',long, label))

    #calculating H1 AND H2
    phi = calc_house_pole('mdpt1', GEO_LAT)
    #OA DIFF BETWEEN ASC AND MC IS ALWAYS 90 SO PLUS 45
    OA = (RAMC + 45) % 360
    long = calc_long_from_OA(OA,phi, E, True)
    directed_longitudes.append(('Hmd1', long, label))
    OA = ((RAMC + 90) + 45) %  360
    long = calc_long_from_OA(OA,phi, E, True)
    directed_longitudes.append(('Hmd2', long, label))

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

def shift_point_to_closest_next_quad(point_angle, left, right, current_quadrant):
    """will return new shifted quadrant based on which angle it is closer to (left or right of the point)
    Q1:  left is mc and right is ac
    Q2: left is ac and right is ic
    Q3: left is ic and right is dc
    Q4: left is dc and right is mc"""

    dist_to_left = abs(swe.difdeg2n(point_angle,left))
    dist_to_right = abs(swe.difdeg2n(point_angle,right))
    
    new_quadrant = current_quadrant - 1 if (dist_to_left < dist_to_right) else current_quadrant + 1
    if (new_quadrant == 0):
        new_quadrant = 4
    elif (new_quadrant == 5):
        new_quadrant = 1
    return new_quadrant

def calc_left_right_angles(ac, mc, quadrant):
    """returns tuple (left_angle, right_angle)"""
    ic = (mc + 180) % 360
    dc = (ac + 180) % 360

    if (quadrant == 1):
        return mc, ac
    if (quadrant == 2):
        return ac, ic
    if (quadrant == 3):
        return ic, dc
    if (quadrant == 4):
        return dc, mc

def calc_md_to_oa_data(RA, RAMC, quadrant, GEO_LAT,DECL, ac, long):
    MD = calculate_MD(RA, RAMC, quadrant)
    #print(f"MD {MD}, RAMC {RAMC} RA {RA} house {house_pos} quad {quadrant}")
    AD = calculate_AD(GEO_LAT, DECL)
    SA = calculate_SA(AD, ac, long, GEO_LAT, quadrant)
    phi = calculate_Pole_phi(MD, SA, GEO_LAT)
    ADP = calculate_ADP(phi, DECL)
    OA_OD, FLAG_ASCEN = calculate_OA_OD(RA, ADP, GEO_LAT, quadrant)

    return MD, AD, SA, phi, ADP, OA_OD, FLAG_ASCEN

def get_directed_from_data(jd_radix, jd_event, GEO_LAT, DECL, RA, RAMC, mc, flag_direct, house_pos, ac, long):
    E = calculate_obliquity(jd_radix)
    quadrant = get_quadrant_from_house_pos(house_pos)
    MD, AD, SA, phi, ADP, OA_OD, FLAG_ASCEN = calc_md_to_oa_data(RA, RAMC, quadrant, GEO_LAT, DECL, ac, long)

    if (MD > SA):
        left_angle, right_angle = calc_left_right_angles(ac, mc, quadrant)
        new_quadrant = shift_point_to_closest_next_quad(long, left_angle, right_angle, quadrant)
        MD, AD, SA, phi, ADP, OA_OD, FLAG_ASCEN = calc_md_to_oa_data(RA, RAMC, new_quadrant, GEO_LAT, DECL, ac, long)
        
        if (MD > SA):
            with open("log_md_sa_4SEP24.txt", "a") as file:
                file.write(f"{jd_radix} still got error... not okay \n")

    arc = calc_arc(jd_radix, jd_event)
    dir_OA = OA_OD + arc if flag_direct else OA_OD - arc

    LONG_deg = calc_long_from_OA(dir_OA, phi, E, FLAG_ASCEN)
    '''print(f"arc: {arc}")
    print(f"directed OA/OD: {dir_OA}")
    print(f"long directed: {LONG_deg}")'''
    
    return LONG_deg
