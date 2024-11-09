# constants.py
import swisseph as swe

ZODIAC_SIGNS = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
]

PLANETS = [
    'Sun', 'Moon', 'Mercury', 'Venus', 'Mars',
    'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Mean_Node'
]

HOUSES = ['H1','H2','H3','H4','H5','H6','H7','H8','H9','H10','H11','H12']    

def calc_planets_labelled(jd_radix, label):
    planets = []
    
    for planet in range(0, len(PLANETS)):
        xx, _ = swe.calc_ut(jd_radix, planet)
        long = xx[0]

        planets.append((PLANETS[planet], long, label))    

    return planets

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
    for i in range(0, 12):
        planets_houses.append((f"H{i+1}", houses[i], label))
      
    return planets_houses

def calc_planets_pof_houses_labelled(jd_radix, geopos):
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

    for house_no in range(0,11):
        rad_planets.append((f'H{house_no+1}',houses[0][house_no],'(r)'))

    return rad_planets

def get_precession(jd1, jd2):
    """Give the jd of the 2 dates you want the precession between"""
    aya1 = swe.get_ayanamsa_ut(jd1)
    aya2 = swe.get_ayanamsa_ut(jd2)
    
    return abs(aya1 - aya2)