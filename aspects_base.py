from enum import Enum

class ProcessType(Enum):
    PSSR = "PSSR"
    TRANSIT = "TRANSIT"
    
# Define the constants for aspects and zodiac signs
ASPECTS = {
    "sextile": (60,300),
    "conjunction": (0,360),
    "trine": (120,240),
    "square": (90, 270),
    "opposition": (180, 180),
    "45": (45,315),
    "135": (135,225)
}

ZODIAC_START_DEGREES = {
    "Aries": 0,
    "Taurus": 30,
    "Gemini": 60,
    "Cancer": 90,
    "Leo": 120,
    "Virgo": 150,
    "Libra": 180,
    "Scorpio": 210,
    "Sagittarius": 240,
    "Capricorn": 270,
    "Aquarius": 300,
    "Pisces": 330,
}

FAST_PLANETS = {'Mars', 'Mercury', 'Venus', 'Moon'}
SLOW_PLANETS = {'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Node'}
HOUSES = {'ASC', 'H2', 'MC', 'H3', 'H5', 'H6'}
RECEPTIVE_POINTS = HOUSES.union({'Moon', 'Sun', 'Fortune'})
ALL_PLANETS = FAST_PLANETS.union(SLOW_PLANETS)
ALL_PLANET_TRANS = ALL_PLANETS.union({'Sun'})

def zodiac_to_degrees(sign, degrees):
    """Convert zodiac sign and degrees to total degrees."""
    return ZODIAC_START_DEGREES[sign] + degrees


def split_position(position):
    """Parse a position string into a dictionary of planet, sign, and degrees, speed."""
    planet, sign, degrees_minutes, speed = position.split(",")
    degrees, minutes = map(int, degrees_minutes.split("  "))
    total_degrees = int(degrees) + (int(minutes) / 60)
    return {"planet": planet, "sign": sign, "degrees": total_degrees, "speed": speed}

def calculate_POF(sun, moon, ac):
    return ac + moon - sun

def calculate_aspect(first_degrees, second_degrees, orb):
    """Determine the aspect between two planetary positions."""
    difference = abs(first_degrees - second_degrees) % 360
    for aspect, ideal in ASPECTS.items():
        forward_ideal, backward_ideal = ideal
        
        lower_bound = forward_ideal - orb
        upper_bound = forward_ideal + orb
        if lower_bound <= difference <= upper_bound:
            return aspect, abs(forward_ideal - difference)
            
        lower_bound = backward_ideal - orb
        upper_bound = backward_ideal + orb
        if lower_bound <= difference <= upper_bound:
            return aspect, abs(backward_ideal - difference)
    return None

def find_trans_aspects(planet_set1, planet_set2, orb):
    aspects_str = ''
    
    for item in planet_set1:
        print('I1\t', item)
        p1, d1, s1 = item
        for item2 in planet_set2:
            print('IT2 \t',item2)
            p2, d2, s2 = item2
            if (
                (p1 in ALL_PLANET_TRANS and p2 in ALL_PLANET_TRANS) or
                (p1 in HOUSES and p2 in ALL_PLANET_TRANS) or
                (p1 in ALL_PLANET_TRANS and p2 in HOUSES)
            ):
                aspect = calculate_aspect(d1, d2, orb)
                if aspect:
                    aspect_name, aspect_orb = aspect
                    aspect_str = (f'({p1},{d1:.3f},{s1}) ({p2},{d2:.3f},{s2}) '
                                  f'({aspect_name},{aspect_orb * 60:.0f}\')\n')
                    aspects_str += aspect_str
    return aspects_str


def find_aspects(planet_set1, planet_set2, orb, house_check, rad_sr_check):
    """Find and format aspects between two sets of planets."""
    ''' if the planet is fast set 1 and slow set 2
        if the planet is fast set 2 and slow set 1
        if the planet is any planet and set 2 is any planet - if housecheck true
        if the planet in set1 is sun or POF and set 2 any planet
        if set 1 is house cusp and set 2 is any planet
        rad/sr check is basically so that the aspects from sr to sr are not done for recep. pts
        '''
        
    
    aspects_str = ''
    
    for p1, d1, s1 in planet_set1:
        for p2, d2, s2 in planet_set2:
            if (
                (house_check and (p1 in ALL_PLANETS and p2 in ALL_PLANETS)) or
                (p1 in FAST_PLANETS and p2 in SLOW_PLANETS) or
                (p1 in SLOW_PLANETS and p2 in FAST_PLANETS) or
                (house_check and rad_sr_check and (p1 in RECEPTIVE_POINTS and p2 in ALL_PLANETS))
            ):

                aspect = calculate_aspect(d1, d2, orb)
                if aspect:
                    aspect_name, aspect_orb = aspect
                    aspect_str = (f'({p1},{d1:.3f},{s1}) ({p2},{d2:.3f},{s2}) '
                                  f'({aspect_name},{aspect_orb * 60:.0f}\')\n')
                    aspects_str += aspect_str
    return aspects_str
#needs an array wof planet name str and degrees decimal
def calc_all_aspects(set1, set2, orb):

    aspects_str = ''

    for p1, d1 in set1:
        for p2, d2 in set2:
            aspect = calculate_aspect(d1, d2, orb)
            if aspect:
                aspect_name, aspect_orb = aspect
                aspect_str = (f'({p1},{d1:.3f}) ({p2},{d2:.3f}) '
                              f'({aspect_name},{aspect_orb * 60:.0f}\')\n')
                aspects_str += aspect_str
    return aspects_str

    
def process_file(file_name):
    """Read planetary positions from a file and convert to degrees."""
    with open(file_name, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
    return process_list(lines)
    

def process_list(list_positions):
    planets = []
    for line in list_positions:
        if line.endswith(',R'):
            line = line[:-2]
        line = line[:-1]
        position = split_position(line)
        full_degrees = zodiac_to_degrees(position["sign"], position["degrees"])
        planets.append((position["planet"], full_degrees, position["speed"]))
    return planets

def remove_duplicates(str_planets_aspects):
    list_aspects = str_planets_aspects.split('\n')
    str_return = ""
    list_no_repeats = []

    for i in range(0, len(list_aspects)):
        if (list_aspects[i] != ''):
            aspect = list_aspects[i]
            p1, p2, asp = aspect.split(' ')
            str_check = f'{p2} {p1} {asp}'
            if (str_check in list_no_repeats) or (list_aspects[i] in list_no_repeats) or (p1==p2):
                pass
            else:
                list_no_repeats.append(list_aspects[i])

    return '\n'.join(list_no_repeats)

def m_aspects_between_two_sets_positions(first_set, second_set, str_label_planet_sets, orb, house_check, process_type: ProcessType):
    """Main function to process planetary data and find aspects.
    legacy from using textfiles to get positions
    file_name = start_filename if start_time_flag else end_filename
    set1 = process_file(file_name)
    set2 = process_file(check_filename)"""

    set1 = process_list(first_set)
    set2 = process_list(second_set)

    if process_type == ProcessType.PSSR:
        str_write_both_sets = find_aspects(set1, set2, orb, house_check, rad_sr_check=True)
        str_write_second_set_only = find_aspects(set2, set2, orb, house_check, rad_sr_check=False)
    elif process_type == ProcessType.TRANSIT:
        str_write_both_sets = find_trans_aspects(set1, set2, orb)
        str_write_second_set_only = ''

    str_write_second_set_only = remove_duplicates(str_write_second_set_only)

    str_output = f"\n{str_label_planet_sets}\n"
    if (str_write_both_sets == '' and str_write_second_set_only == ''):
      print('no aspects within acceptable orb')
      str_output += 'no aspects within acceptable orb + \n'
    elif (str_write_both_sets == '' and str_write_second_set_only != ''):
      str_output += 'These are the aspects within the second set only:\n'
      str_output += str_write_second_set_only + '\n'
    elif (str_write_both_sets != '' and str_write_second_set_only != ''):
      str_output += str_write_both_sets + '\n'
      str_output += 'These are the aspects among within the second set only:\n'
      str_output += str_write_second_set_only + '\n'
    elif (str_write_both_sets != '' and str_write_second_set_only == ''):
      str_output += str_write_both_sets + '\n'

    return str_output

# Example call to main function
#main('planet_rad_start.txt', None, 'planet_check-pos.txt', 'output.txt', 
#'20h30m32s insert_date_refactor', orb=0.6, start_time_flag=True)