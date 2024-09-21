import swisseph as swe
import math
import aspects_base as aspects

PLANETS = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Mean_Node']
        
def get_all_secondary_positions(jd_radix, jd_event, geo_lat, geo_long):
    jd_diff = abs(jd_radix-jd_event)
    days_diff = jd_diff / 365.2422
    jd_prog = jd_radix + days_diff
    jd_reg = jd_radix - days_diff
    #print(f"{julian.from_jd(jd_radix)}, event: {julian.from_jd(jd_event)}, dt_prog: {julian.from_jd(jd_prog)}, dt_reg: {julian.from_jd(jd_reg)}")

    #getting prog/reg arc
    xx, _ = swe.calc_ut(jd_radix, swe.SUN, swe.FLG_EQUATORIAL)
    ra_rad = xx[0]
    xx, _ = swe.calc_ut(jd_prog, swe.SUN, swe.FLG_EQUATORIAL)
    ra_prog = xx[0]    
    xx, _ = swe.calc_ut(jd_reg, swe.SUN, swe.FLG_EQUATORIAL)
    ra_reg = xx[0]
    arc_prog = ra_prog - ra_rad
    arc_reg = ra_reg - ra_rad
    houses = swe.houses(jd_radix, geo_lat, geo_long, b'T')
    ramc = houses[1][2]
    e = calculate_obliquity(jd_radix)

    #directed houses and rad houses
    houses_rad = houses[0]
    houses_prog = swe.houses_armc(ramc+arc_prog, geo_lat, e, b'T')[0] 
    houses_reg = swe.houses_armc(ramc+arc_reg, geo_lat, e, b'T')[0] 
    houses_rad = aspects.format_house_list(houses_rad, '(r)')
    houses_prog = aspects.format_house_list(houses_prog, '(p)')
    houses_reg = aspects.format_house_list(houses_reg, '(c)')

    planets_rad = calc_all_planets(jd_radix, "(r)")
    planets_prog = calc_all_planets(jd_prog, "(p)")
    planets_reg = calc_all_planets(jd_reg, "(c)")
    #add POF
    pof_rad = calc_POF(planets_rad, houses_rad[2][1])
    pof_prog = calc_POF(planets_prog, houses_prog[2][1])
    pof_reg = calc_POF(planets_reg, houses_reg[2][1])
    planets_rad.append(('POF', pof_rad, "(r)"))
    planets_prog.append(('POF', pof_prog,"(p)"))
    planets_reg.append(('POF', pof_reg,"(c)"))

    return  [*planets_rad, *houses_rad], [*planets_prog, *houses_prog], [*planets_reg, * houses_reg]


def calc_houses_with_ramc(RAMC, jd, GEO_LAT, label):   
    longitudes = []
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

        longitudes.append((house_name, long, label))
        count +=1
    
    long = calc_long_from_OA(RAMC, 0.0, E, True)
    longitudes.append(('MC',long, label))

    #calculating H1 AND H2
    phi = calc_house_pole('Hmd1', GEO_LAT)
    #OA DIFF BETWEEN ASC AND MC IS ALWAYS 90 SO PLUS 45
    OA = (RAMC + 45) % 360
    long = calc_long_from_OA(OA,phi, E, True)
    longitudes.append(('Hmd1', long, label))
    OA = ((RAMC + 90) + 45) %  360
    long = calc_long_from_OA(OA,phi, E, True)
    longitudes.append(('Hmd2', long, label))

    return longitudes

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

def calc_house_pole(house_no, GEO_LAT):
    tan_phi = 0.0
    if house_no in (3, 9, 5, 11):
        tan_phi = (1/3) * math.tan(math.radians(GEO_LAT))
    elif house_no in (2, 8, 6, 12):
        tan_phi = (2/3) * math.tan(math.radians(GEO_LAT))
    elif house_no == 'ASC':
        tan_phi = math.tan(math.radians(GEO_LAT))
    elif house_no in ('Hmd1', 'Hmd2'):
        tan_phi = 0.5 * math.tan(math.radians(GEO_LAT))
    else:
        print(f"House number {house_no} is not handled.")

    return math.degrees(math.atan(tan_phi))

def calc_all_planets(jd, label):
    planets = []

    for planet in range(0, len(PLANETS)):
        xx, _ = swe.calc_ut(jd, planet)
        long = xx[0]
        
        planets.append((PLANETS[planet], long, label))    

    return planets        

def calc_POF(planets, ac):
    """returns tuple (pof_rad, pof_directed, pof_converse)"""
    sun_index = PLANETS.index('Sun')
    moon_index = PLANETS.index('Moon')
    long_sun = planets[sun_index][1]
    long_moon = planets[moon_index][1]
    return (ac + long_moon - long_sun) % 360

def secondary_for_event(jd_radix, jd_event, geo_lat, geo_long):
    swe.set_ephe_path('ephe')
    rad_positions, prog_positions, reg_positions = get_all_secondary_positions(jd_radix, jd_event, geo_lat, geo_long)
    
    str_aspects_rad_prog = aspects.find_secondary_swiss_aspects(rad_positions, prog_positions)
    str_aspects_rad_reg = aspects.find_secondary_swiss_aspects(rad_positions, reg_positions)
    str_aspects_prog_prog = aspects.find_secondary_swiss_aspects(prog_positions, prog_positions)
    str_aspects_reg_reg = aspects.find_secondary_swiss_aspects(reg_positions, reg_positions)
    str_aspects_prog_prog = aspects.remove_duplicates(str_aspects_prog_prog)
    str_aspects_reg_reg = aspects.remove_duplicates(str_aspects_reg_reg)

    str_rad_n_prog = str_aspects_rad_prog + str_aspects_prog_prog
    str_rad_n_reg = str_aspects_rad_reg + str_aspects_reg_reg

    return str_rad_n_prog, str_rad_n_reg