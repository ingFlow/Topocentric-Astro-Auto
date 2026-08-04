"""
significators/scoring.py - the acceptance/scoring engine that decides
whether a computed aspect is astrologically meaningful for a given
EventType, and (for Primary Directions and its five sibling techniques)
how many points it contributes to a candidate birth time's running score.

Relocated here (Phase 5 of the migration plan) from
techniques/primary_directions/technique.py, alongside significators/rules_data.py
(the data tables this file reads from). Per the Developer Manual's Section
7.2 and Section 8, these functions are reused by five of the seven
techniques - Primary Directions, Secondary, Transit, SRA, and Harmonics -
not specific to Primary Directions; only PSSR uses a different acceptance
function (count_event_acceptable_aspects, which is itself defined here and
shared across PSSR and the other techniques' non-PD-score acceptance
checks - see the call-site table below). Lunar and Natal apply no
scoring filter at all (a real, pre-existing gap in feature coverage
documented in the Developer Manual, not something this move changes).

This move is a pure code relocation - extraction and re-import only. Every
function body below is copied verbatim, character-for-character, from its
previous location in technique.py, including the still-open TODO comment
that used to sit directly above get_accept_lists (preserved here exactly
as it was, since the underlying logic issue it flags has not been
resolved).

Contents (the full acceptance/scoring call graph, in dependency order):
    - get_accept_lists(event_id): pulls the angle/house/planet accept
      lists and GoodBadFlag out of PRIMARY_RULES/SECONDARY_RULES for one
      EventType.
    - good_bad_flag_match_aspect(good_bad_flag, aspect): does this
      aspect's polarity (conjunction/trine/sextile vs. square/opposition)
      match the event's GOOD/BAD orientation?
    - appropriate_base(...): the core "is this directed aspect
      thematically appropriate for this event" check, layering the
      table-driven accept lists with a number of hardcoded, event-specific
      exceptions (see the Developer Manual's Section 6.4 for the specific
      EventTypes this affects, e.g. HOSPITALIZATION_ILLNESS,
      ASSASINATION_SUICIDE).
    - is_acceptable_planet_combo(event_id, p1, p2): checks a planet pair
      against PLANETARY_COMBO, handling that table's four different value
      shapes (plain list of pairs; single-int alias to another event;
      int-plus-extra-pairs; bare int).
    - is_acceptable_angular_aspect(event_id, str_aspect, type): the
      general-purpose acceptance check parameterized by AspectType
      granularity - used by count_event_acceptable_aspects (PSSR's own
      scoring path, and the batch grid engine's per-technique acceptance
      filtering).
    - is_aspect_conj_opp(str_aspect): a small helper - is this aspect
      string a conjunction or opposition?
    - count_event_acceptable_aspects(...): filters a full aspect-string
      block down to only the acceptable ones for one event, returning
      (count, filtered_string). This is the function PSSR's "Show
      Accepted" path uses (via AspectType.FAST_TO_SLOW_COMBO), and also
      what the batch grid engine calls for every technique's acceptance
      column.
    - count_pd_score_acceptable_aspects(...): the weighted numeric scoring
      rubric (25/20/16/14/12/10/8/6/3 points by aspect class x point-type
      combination) - despite the "pd" in the name, this is the function
      the interactive GUI uses for Primary Directions, Secondary, Transit,
      SRA, and Harmonics's "Show Accepted" filter (see
      webapp/app.py's update_content route).
    - is_acceptable_pd_aspect(event_id, str_aspect): the per-aspect
      scoring lookup that count_pd_score_acceptable_aspects calls in a
      loop.

Depends on significators/rules_data.py for the data tables (PRIMARY_RULES,
SECONDARY_RULES, PLANETARY_COMBO, EventType, AspectType, GoodBadFlag,
Planet) and on core/constants.py for PLANETS/HOUSES (used only inside
is_acceptable_angular_aspect's ANGLE_HOUSE_ANY_PLANET branch). Has no
dependency on techniques/primary_directions/technique.py or on any other
technique module - callers reach this module directly, not through PD's
namespace.
"""
from topo_astro.significators.rules_data import (
    Planet,
    EventType,
    AspectType,
    GoodBadFlag,
    PRIMARY_RULES,
    SECONDARY_RULES,
    PLANETARY_COMBO,
)
from topo_astro.core.constants import PLANETS, HOUSES

#{TODO the logic here of the angle_rules and house_aspect_rules is not correct, need to fix}
def get_accept_lists(event_id):    
    aspect_rules = PRIMARY_RULES[event_id]
    house_aspect_rules = SECONDARY_RULES[event_id]
    if not aspect_rules:
        #if event_id doesn't exist
        return False  
    
    angle_house_accept = aspect_rules[0] #these are primary angle/houses
    angle_accept = []
    house_accept = []
    planet_accept = aspect_rules[1] #these are primary planets
    pre_house_accept = house_aspect_rules[0] #these are secondary houses
    secondary_planets = house_aspect_rules[1] #these are secondary planets
    primary_houses = []
    good_bad_flag = aspect_rules[2] 
    
    if isinstance(pre_house_accept, str): #there are no angles in secondary rules so these are just houses handling
        house_accept = [pre_house_accept]
    elif isinstance(pre_house_accept, tuple):
        for h in pre_house_accept:
            house_accept.append(h)

    for angle_house in angle_house_accept:
        if angle_house in ['H1','H4','H7','H10']:
            angle_accept.append(angle_house)
        else:
            primary_houses.append(angle_house) #these are primary houses only
            house_accept.append(angle_house) #these are primary houses plus the secondary houses

    return angle_accept, house_accept, planet_accept, secondary_planets, primary_houses, good_bad_flag

def good_bad_flag_match_aspect(good_bad_flag, aspect):
    if good_bad_flag == GoodBadFlag.GOOD:
        if aspect in ['conjunction', 'sextile', 'trine', 'opposition']:
            return True
    if good_bad_flag == GoodBadFlag.BAD:
        if aspect in ['square', 'opposition', 'conjunction']:
            return True
    return False

def appropriate_base(good_bad_flag, aspect, p1, p2, event_id):
    angle_accept, house_accept, planet_accept, secondary_planets, primary_houses, good_bad_flag = get_accept_lists(event_id)
    
    good_bad_aspect_flag = good_bad_flag_match_aspect(good_bad_flag,aspect)
    if not good_bad_aspect_flag:
        return False
        
    #these are for the rectification process: DIRECTED house to prim/sec planets then DIRECTED angle to prim (plus extra planets) assuming p2 is directed factor
    if (p2 in primary_houses) and ((p1 in planet_accept) or (p1 in secondary_planets)):
        return True
    if (p2 in angle_accept) and (p1 in planet_accept):
        return True
    
    #These are the extra planet allowed with angles that are not primary planets
    flag_angle_pof = False
    if (p2 in angle_accept) or (p2 == "POF"):
        flag_angle_pof = True
    if ((event_id == EventType.BIRTH_BROTHER) and flag_angle_pof and (p1 in [Planet.URA, Planet.SUN, Planet.NNO])):
        return True
    if ((event_id == EventType.BIRTH_SISTER) and flag_angle_pof and (p1 in [Planet.URA, Planet.NNO])):
        return True
    if ((event_id == EventType.BIRTH_SON) and flag_angle_pof and (p1 in [Planet.URA])):
        return True
    if ((event_id == EventType.BIRTH_DAUGHTER) and flag_angle_pof and (p1 in [Planet.URA])):
        return True
    if ((event_id == EventType.TRAVEL_POSITIVE) and flag_angle_pof and (p1 in [Planet.VEN])):
        return True
    if ((event_id == EventType.ARREST) and flag_angle_pof and (p1 in [Planet.MER])):
        return True
    if ((event_id == EventType.BIRTH_GRANDSON) and flag_angle_pof and (p1 in [Planet.MER])):
        return True
    if ((event_id == EventType.BIRTH_GRANDDAUGHTER) and flag_angle_pof and (p1 in [Planet.MER,])):
        return True
    if ((event_id == EventType.MARRIAGE_ENGAGEMENT_FOR_MALE) and flag_angle_pof and (p1 in [Planet.MER])):
        return True
    if ((event_id == EventType.MARRIAGE_ENGAGEMENT_FOR_FEMALE) and flag_angle_pof and (p1 in [Planet.MER, Planet.MON, Planet.VEN])):
        return True
    if ((event_id == EventType.DEATH_SON) and flag_angle_pof and (p1 in [Planet.URA, Planet.SUN])):
        return True
    if ((event_id == EventType.DEATH_DAUGHTER) and flag_angle_pof and (p1 in [Planet.URA, Planet.MAR])):
        return True
    if ((event_id == EventType.DEATH_WIFE_FRIEND) and flag_angle_pof and (p1 in [Planet.URA])):
        return True
    if ((event_id == EventType.DEATH_HUSBAND_FRIEND) and flag_angle_pof and (p1 in [Planet.URA])):
        return True
    if ((event_id == EventType.DEATH) and flag_angle_pof and (p1 in [Planet.URA, Planet.MAR])):
        return True
    if ((event_id == EventType.RESIGN_RETIRE) and flag_angle_pof and (p1 in [Planet.MON, Planet.PLU])):
        return True
    if ((event_id == EventType.TRAVEL_OVERSEAS_POSITIVE) and flag_angle_pof and (p1 in [Planet.VEN])):
        return True
    if ((event_id == EventType.HOSPITALIZATION_ILLNESS) and flag_angle_pof and (p1 in [Planet.MON])):
        return True
    if ((event_id == EventType.ASSASINATION_SUICIDE) and (aspect == 'conjunction') and flag_angle_pof and (p1 == 'H12')):
        return True
    
    #house and angle conjunctions
    if (aspect == 'conjunction'):
        if ((p2 in angle_accept) and (p1 in primary_houses)):
            return True
        if ((p2 in primary_houses) and (p1 in angle_accept)):
            return True
        
    if (aspect in ['conjunction', 'opposition']) :
        if ((p2 == 'POF') and (p1 in planet_accept)):       #allow for directed POF to primary planets
            return True
        
    #here we are allowing POF directed to appropriate cusp/angle conj/opp and vice versa
    if (((p1 in angle_accept) or (p1 in house_accept)) and (p2 == "POF")) or ((p1 == "POF") and ((p2 in angle_accept) or (p2 in house_accept))):
        if good_bad_flag == GoodBadFlag.GOOD:
            if aspect == "conjunction":
                return True
        elif good_bad_flag == GoodBadFlag.BAD:
            if aspect == "opposition":
                return True
    
def is_acceptable_planet_combo(event_id, p1, p2):
    planetary_combos_list = []
    combos_value_prelim = PLANETARY_COMBO[event_id]
    if isinstance(combos_value_prelim, tuple):
        if isinstance(combos_value_prelim[0], int) and len(combos_value_prelim) == 1: #if there is only one value in the list (eventid)
            planetary_combos_list = PLANETARY_COMBO[combos_value_prelim[0]]
        else:
            if not isinstance(combos_value_prelim[0], int): #there is only planet combos
                planetary_combos_list = combos_value_prelim
            else:
                planetary_combos_list = PLANETARY_COMBO[combos_value_prelim[0]] #first element is reference to other event_id and then a bunch of tuples
                planetary_combos_list = list(planetary_combos_list)
                planetary_combos_list.extend(combos_value_prelim[1:])
                planetary_combos_list = tuple(planetary_combos_list)
    else:
        planetary_combos_list = PLANETARY_COMBO[combos_value_prelim]
            
    p1_p2_combo = (p1, p2)
    p2_p1_combo = (p2, p1)
    if p1_p2_combo in planetary_combos_list:
        return True
    if p2_p1_combo in planetary_combos_list:
        return True

    return False

def is_acceptable_angular_aspect(event_id, str_aspect, type):
    """input the event id corresponding to dictionary and string with aspect as printed to textfile like this
    (Uranus,55.5 52,(r)) (Hmd1,325.600,(d)) (square,3')"""
    angle_accept, house_accept, planet_accept, secondary_planets, primary_houses, good_bad_flag = get_accept_lists(event_id)
    
    p1_d1_s1, p2_d2_s2, asp_deg = str_aspect.split(' ')
    p1, _, _ = p1_d1_s1.split(',')
    p1 = p1[1:]
    p2, _, _ = p2_d2_s2.split(',')
    p2 = p2[1:]
    aspect, _ = asp_deg.split(',')
    aspect = aspect[1:]
    
    if type == AspectType.FAST_TO_SLOW_COMBO:
        '''flag_appropriate_combo = is_acceptable_planet_combo(event_id,p1,p2)
        if not flag_appropriate_combo:
            return False'''
        if aspect not in ["conjunction", "opposition", "sextile", "trine", "square"]:
            return False
        if (p2 in [Planet.MAR, Planet.MER, Planet.VEN, Planet.MON]) and (p1 in [Planet.JUP, Planet.SAT, Planet.URA, Planet.NEP, Planet.PLU, Planet.NNO]):
            return True
        if (p1 in [Planet.MAR, Planet.MER, Planet.VEN, Planet.MON]) and (p2 in [Planet.JUP, Planet.SAT, Planet.URA, Planet.NEP, Planet.PLU, Planet.NNO]):
            return True
        #sun as receptor where combo is allowed
        if (p2 in [Planet.SUN]) and (p1 in [Planet.MAR, Planet.MER, Planet.VEN, Planet.MON]):
            if p1 in [Planet.MON]:
                if p2 in planet_accept:
                    return True
            if (p1 in planet_accept) and (p2 in planet_accept):
                return True
    
    if type == AspectType.APPROPRIATE_DIRECTED_CUSP_ONLY:
        return appropriate_base(good_bad_flag, aspect, p1, p2, event_id)
    if type == AspectType.APPROPRIATE_DIRECTED_CUSP_PLANET_TO_CUSP:
        flag_appropriate_directed_cusp = appropriate_base(good_bad_flag, aspect, p1, p2, event_id)
        flag_appropriate_directed_cusp_planet_to_cusp = appropriate_base(good_bad_flag, aspect, p2, p1, event_id) #just swap the 2 to check if the angle/house to planets are the other way same rules
        return flag_appropriate_directed_cusp or flag_appropriate_directed_cusp_planet_to_cusp
    if type == AspectType.APPROPRIATE_INCLUDING_PLANET_COMBOS:
        flag_appropriate_directed_cusp = appropriate_base(good_bad_flag, aspect, p1, p2, event_id)
        flag_appropriate_directed_cusp_planet_to_cusp = appropriate_base(good_bad_flag, aspect, p2, p1, event_id)
        if flag_appropriate_directed_cusp or flag_appropriate_directed_cusp_planet_to_cusp:
            return True
        good_bad_aspect_flag = good_bad_flag_match_aspect(good_bad_flag,aspect)
        if not good_bad_aspect_flag:
            return False
        
        return is_acceptable_planet_combo(event_id,p1,p2)
    
    if type == AspectType.ANGLE_PRIMARY:
        #angles to primary planets
        if ((p1 in angle_accept) and (p2 in planet_accept)) or ((p1 in planet_accept) and (p2 in angle_accept)):
            return True
    if type == AspectType.ANGLE_SECONDARY:
        #angles to primary/secondary planets
        if ((p1 in angle_accept) and (p2 in planet_accept)) or ((p1 in planet_accept) and (p2 in angle_accept)):
            return True
        if ((p1 in angle_accept) and (p2 in secondary_planets)) or ((p1 in secondary_planets) and (p2 in angle_accept)):
            return True
    if type == AspectType.ANGLE_HOUSE_PRIMARY:
        #house/angles to primary planets
        if (p1 in angle_accept) or (p1 in house_accept):
            if (p2 in planet_accept):
                return True
        if (p2 in angle_accept) or (p2 in house_accept):
            if (p1 in planet_accept):
                return True
    if type == AspectType.ANGLE_HOUSE_SECONDARY:
        #house/angles to secondary planets
        if (p1 in angle_accept) or (p1 in house_accept):
            if (p2 in planet_accept) or (p2 in secondary_planets):
                return True
        if (p2 in angle_accept) or (p2 in house_accept):
            if (p1 in planet_accept) or (p1 in secondary_planets):
                return True
    if type == AspectType.PLANETS_PRIMARY:
        #planets to planets primary or angles/houses to primary
        if  (p1 in planet_accept) and (p2 in planet_accept):
            return True
        if (p1 in angle_accept) or (p1 in house_accept):
            if (p2 in planet_accept):
                return True
        if (p2 in angle_accept) or (p2 in house_accept):
            if (p1 in planet_accept):
                return True
    if type == AspectType.PLANETS_SECONDARY:
        #planets to planets secondary or angle/house to secondary
        if  (p1 in planet_accept) or (p1 in secondary_planets):
            if (p2 in planet_accept) or (p2 in secondary_planets):
                return True 
        if (p1 in angle_accept) or (p1 in house_accept):
            if (p2 in planet_accept) or (p2 in secondary_planets):
                return True
        if (p2 in angle_accept) or (p2 in house_accept):
            if (p1 in planet_accept) or (p1 in secondary_planets):
                return True
    if type == AspectType.ANGLE_HOUSE_ANY_PLANET:
        #angle/houses to any planet
        if ((p1 in HOUSES) and (p2 in PLANETS)) or ((p1 in PLANETS) and (p2 in HOUSES)):
            return True
        if ((p1 in HOUSES) and (p2 == 'POF')) or ((p1 == 'POF') and (p2 in HOUSES)):
            return True
    if type == AspectType.MOON_PRIMARY:
        #moon to primary planet/house (p2 only cause p2 is always the directed factor and we don't care when Moon is radical)
        if ((p1 in angle_accept) or (p1 in house_accept)) and (p2 =='Moon'):
            return True
    if type == AspectType.MOON_SECONDARY:
        #moon to primary/secondary planet/house (p2 only cause p2 is always the directed factor and we don't care when Moon is radical)
        if ((p1 in angle_accept) or (p1 in house_accept)) and (p2 =='Moon'):
            return True
        if ((p1 in planet_accept) or (p1 in secondary_planets)) and (p2 == 'Moon'):
            return True
    if type == AspectType.MOON_ANGLE_HOUSE_PRIMARY:
        #moon to any planet or MOON to angle or angle to primary planet
        if ((p1 in planet_accept)) and (p2 =='Moon'):
            return True
        if (p1 in angle_accept) or (p1 in house_accept):
            if (p2 in planet_accept):
                return True
        if (p2 in angle_accept) or (p2 in house_accept):
            if (p1 in planet_accept):
                return True
    if type == AspectType.MOON_ANGLE_HOUSE_SECONDARY:
        #moon to any planet or MOON to angle or angle to primary/secondary planet
        if ((p1 in planet_accept) or (p1 in secondary_planets)) and (p2 =='Moon'):
            return True
        if (p1 in angle_accept) or (p1 in house_accept):
            if (p2 in planet_accept) or (p2 in secondary_planets):
                return True
        if (p2 in angle_accept) or (p2 in house_accept):
            if (p1 in planet_accept) or (p1 in secondary_planets):
                return True

def is_aspect_conj_opp(str_aspect):
    _, _, asp_orb = str_aspect.split(' ')
    aspect = asp_orb.split(',')[0][1:]

    if aspect in ['conjunction', 'opposition']:
        return True
    
    
def count_event_acceptable_aspects(event_id, str_all_aspects, count, type):
    "returns a (count, string) of only acceptable angular direction aspects"
    list_aspects = str_all_aspects.split('\n')
    str_acceptable_aspects = ""

    for i in range(0, len(list_aspects)):
        if (list_aspects[i] != ''):
            aspect = list_aspects[i]
            if is_acceptable_angular_aspect(event_id, aspect, type):
                str_acceptable_aspects += aspect + '\n'
                count += 1

    return count, str_acceptable_aspects.rstrip()

def count_pd_score_acceptable_aspects(event_id, str_all_aspects, score):
    "returns a (cumulative_score, string) of only acceptable primary direction aspects"
    list_aspects = str_all_aspects.split('\n')
    str_acceptable_aspects = ""

    for i in range(0, len(list_aspects)):
        if (list_aspects[i] != ''):
            aspect = list_aspects[i]
            asp_score = is_acceptable_pd_aspect(event_id, aspect)
            if asp_score > 0:
                str_acceptable_aspects += aspect + '\n'
                score += asp_score

    return score, str_acceptable_aspects.rstrip()

def is_acceptable_pd_aspect(event_id, str_aspect):
    """input the event id corresponding to dictionary and string with aspect as printed to textfile like this
    (Uranus,55.5 52,(r)) (H1,325.600,(d)) (square,3')"""
    
    if event_id == EventType.BLANK:
        return 0
    
    prim_rules = PRIMARY_RULES[event_id]
    second_rules = SECONDARY_RULES[event_id]
    if not prim_rules or not second_rules:
        return False  
    
    p1_d1_s1, p2_d2_s2, asp_orb = str_aspect.split(' ')
    p1, _, _ = p1_d1_s1.split(',')
    p1 = p1[1:]
    p2, _, _ = p2_d2_s2.split(',')
    p2 = p2[1:]
    aspect, _ = asp_orb.split(',')
    aspect = aspect[1:]

    prim_angle_house = prim_rules[0]
    angles = []
    prim_houses = []
    prim_planets = prim_rules[1]
    second_houses = second_rules[0]
    second_planets = second_rules[1]

    for angle_house in prim_angle_house:
        if angle_house in ['H1','H4','H7','H10']:
            angles.append(angle_house)
        else:
            prim_houses.append(angle_house)

    conj_opp = ['conjunction','opposition']
    sqr_tri_sext = ['trine','sextile','square']
    
    aspect_score = 0
    planet_score = 0
    angularity_score = 0

    if (aspect in conj_opp):
        aspect_score = 3
    elif (aspect in sqr_tri_sext):
        aspect_score = 2
    else:
        aspect_score = 1

    if ((p1 in angles) and (p2 in prim_planets)) or ((p2 in angles) and (p1 in prim_planets)):
        if aspect_score == 3:
            return 25
        if aspect_score == 2:
            return 20
        if aspect_score == 1:
            return 8
    elif ((p1 in angles) and (p2 in second_planets)) or ((p2 in angles) and (p1 in second_planets)):
        if aspect_score == 3:
            return 20
        if aspect_score == 2:
            return 16
        if aspect_score == 1:
            return 6
    elif ((p1 in angles) and (p2 in prim_houses)) or ((p2 in angles) and (p1 in prim_houses)):
        if aspect_score == 3:
            return 20
    elif ((p1 in angles) and (p2 in second_houses)) or ((p2 in angles) and (p1 in second_houses)):
        if aspect_score == 3:
            return 16
    elif ((p1 in prim_houses) and (p2 in prim_planets)) or ((p2 in prim_houses) and (p1 in prim_planets)):
        if aspect_score == 3:
            return 20
        if aspect_score == 2:
            return 16
        if aspect_score == 1:
            return 8
    elif ((p1 in prim_houses) and (p2 in second_planets)) or ((p2 in prim_houses) and (p1 in second_planets)):
        if aspect_score == 3:
            return 16
        if aspect_score == 2:
            return 10
        if aspect_score == 1:
            return 6
    elif ((p1 in second_houses) and (p2 in prim_planets)) or ((p2 in second_houses) and (p1 in prim_planets)):
        if aspect_score == 3:
            return 20
        if aspect_score == 2:
            return 12
        if aspect_score == 1:
            return 6
    elif ((p1 in second_houses) and (p2 in second_planets)) or ((p2 in second_houses) and (p1 in second_planets)):
        if aspect_score == 3:
            return 14
        if aspect_score == 2:
            return 10
        if aspect_score == 1:
            return 3

    return angularity_score * planet_score * aspect_score