import swisseph as swe
import julian
import pd_base as pd
import math
from aspects_base import calculate_obliquity, find_pd_swiss_aspects, format_house_list
from constants import PLANETS, HOUSES, calc_planets_pof_houses_labelled

class EventType:
    BIRTH_BROTHER = 0
    BIRTH_SISTER = 1
    BIRTH_SON = 2
    BIRTH_DAUGHTER = 3
    DEATH_FATHER_GRAND = 4
    DEATH_MOTHER_GRAND = 5
    SUCCESS = 6
    FAILURE = 7
    TRAVEL_POSITIVE = 8
    TRAVEL_NEGATIVE = 9
    ARREST = 10
    LOSSES = 11
    GRADUATION = 12
    MOVE_HOME = 13
    BIRTH_GRANDSON = 14
    BIRTH_GRANDDAUGHTER = 15
    MARRIAGE_FOR_MALE = 16
    MARRIAGE_FOR_FEMALE = 17
    CHILDS_MARRIAGE = 18
    DIVORCE_SEPARATION = 19
    DEATH_SON = 20
    DEATH_DAUGHTER = 21
    DEATH_WIFE = 22
    DEATH_HUSBAND = 23
    DEATH_BROTHER = 24
    DEATH_SISTER = 25
    DEATH = 26
    ASSASINATION_SUICIDE = 27
    PROMOTION_JOB = 28
    RESIGN_RETIRE = 29
    TRAVEL_OVERSEAS_POSITIVE = 30
    MOBILIZATION = 31
    DEMOBILIZATION_RELEASE = 32
    ACCIDENT = 33
    HOSPITALIZATION_ILLNESS = 34
    VIOLENCE = 35
    INTRIGUE = 36
    GAMBLING_LOSS = 37
    GAMBLING_GAIN = 38
    ARMY_PROMOTION = 39
    POSITIVE_3_9 = 40
    POSITIVE_6_12 = 41
    POSITIVE_2_8 = 42
    POSITIVE_AC_MC = 43
    NEGATIVE_AC_MC = 44
    NEGATIVE_6_12 = 45
    BLANK = 46

    @classmethod
    def get_name(cls, value):
        """Returns the name of the event type for the given value."""
        for attr in dir(cls):
            if not attr.startswith("__") and getattr(cls, attr) == value:
                return attr
        return 'Unknown Event Type'

class AspectType:
    ANGLE_PRIMARY = 0
    ANGLE_HOUSE_PRIMARY = 1
    ANGLE_HOUSE_SECONDARY = 2
    PLANETS_PRIMARY = 3
    PLANETS_SECONDARY = 4
    ANGLE_HOUSE_ANY_PLANET = 5
    MOON_PRIMARY = 6
    MOON_ANGLE_HOUSE_PRIMARY = 7
    MOON_ANGLE_HOUSE_SECONDARY = 8
    MOON_SECONDARY = 9
    ANGLE_SECONDARY = 10

class Planet:
    SUN = 'Sun'
    MON = 'Moon'
    MER = 'Mercury'
    VEN = 'Venus'
    MAR = 'Mars'
    JUP = 'Jupiter'
    SAT = 'Saturn'
    URA = 'Uranus'
    NEP = 'Neptune'
    PLU = 'Pluto'
    NNO = 'Mean_Node'

class PD_Automate:
    def __init__(self,jd_rad : julian, jd : julian, geo_positions: list, rad_planets_labelled=None, rad_planets_equatorial=None, rad_houses_info=None, e=None):
        self.__dict_planets_extended_info = {}
        self.pd_for_time_event(jd_rad, jd, geo_positions, rad_planets_labelled, rad_planets_equatorial, rad_houses_info, e)

    def pd_for_time_event(self,jd_rad : julian, jd : julian, geo_positions: list, rad_planets_labelled=None, rad_planets_equatorial=None, rad_houses_info=None, e=None):
        if rad_planets_labelled == None: #ie there is only event info
            rad_houses_info = swe.houses(jd_rad, geo_positions[0], geo_positions[1], b'T')
            rad_planets_labelled = calc_planets_pof_houses_labelled(jd_rad)
            rad_planets_equatorial = calc_rad_planets_equatorial(jd_rad)
            e = calculate_obliquity(jd_rad)

        dir_houses, conv_houses = calc_directed_pd_houses(jd_rad,jd, geo_positions[0], rad_houses_info, e)
        dir_houses = format_house_list(dir_houses, '(d)')
        conv_houses = format_house_list(conv_houses, '(c)')
        dir_planets, conv_planets, dict_extended = calc_directed_pd_planets(jd_rad,jd, geo_positions[0], geo_positions[1], rad_houses_info, rad_planets_equatorial, e)

        #add POF  DATA
        dir_pof, conv_pof, dict_pof_info = calc_directed_POF(rad_planets_labelled, jd_rad, jd, geo_positions[0], rad_houses_info, e)
        dir_planets.append(('POF', dir_pof, "(d)"))
        conv_planets.append(('POF',conv_pof, "(c)"))
        #JOIN ARRAYS
        rad_positions = rad_planets_labelled
        dir_positions = [*dir_planets, *dir_houses]
        conv_positions = [*conv_planets, *conv_houses]

        self.__dict_planets_extended_info["base"] = {
            "dt_radix": julian.from_jd(jd_rad),
            "dt_event": julian.from_jd(jd),
            "geopos": geo_positions,
            "rad_positions": rad_positions,
            "rad_equatorial": rad_planets_equatorial,
            "directed_positions": dir_positions,
            "converse_positions": conv_positions
        }
        dict_extended.update(dict_pof_info)
        self.__dict_planets_extended_info["planets_extended"] = dict_extended
        self.__dict_planets_extended_info["MDOs"] = self.get_mdos_natal()
        self.__str_aspects_rad_dir = find_pd_swiss_aspects(rad_positions, dir_positions)
        self.__str_aspects_rad_conv = find_pd_swiss_aspects(rad_positions, conv_positions)
        

    def get_aspects_str(self):
        return self.__str_aspects_rad_dir, self.__str_aspects_rad_conv

    def get_extended_information(self):
        return self.__dict_planets_extended_info
    
    def get_mdos_natal(self):
        mdo_list = []
        extended_planets = self.__dict_planets_extended_info["planets_extended"]
        for key, value in extended_planets.items():
            mdo = value['MDO']
            mdo_list.append((key,mdo[0]))
        return mdo_list
    
PRIMARY_RULES = {
    EventType.BIRTH_BROTHER: (('H4', 'H7','H3'), (Planet.MER, Planet.JUP)),
    EventType.BIRTH_SISTER: (('H4', 'H7', 'H3'), (Planet.MON, Planet.MER, Planet.VEN)),
    EventType.BIRTH_SON: (('H4', 'H1','H5'), (Planet.MAR, Planet.SUN, Planet.JUP, Planet.NNO)),
    EventType.BIRTH_DAUGHTER: (('H4', 'H1','H5'), (Planet.VEN, Planet.MON, Planet.JUP, Planet.NNO)),
    EventType.DEATH_FATHER_GRAND: (('H10','H1', 'H8'), (Planet.SAT, Planet.SUN, Planet.NEP, Planet.PLU, Planet.MAR, Planet.NNO)),
    EventType.DEATH_MOTHER_GRAND: (('H4','H1', 'H8'), (Planet.MON, Planet.VEN, Planet.SAT, Planet.NEP, Planet.PLU, Planet.MAR, Planet.NNO)),
    EventType.SUCCESS: (('H10','H1','H3'), (Planet.SUN, Planet.JUP, Planet.MON, Planet.MER, Planet.URA, Planet.VEN)),
    EventType.FAILURE: (('H10','H1', 'H3'), (Planet.SAT, Planet.NEP, Planet.NNO, Planet.MAR, Planet.SUN)),
    EventType.TRAVEL_POSITIVE: (('H10','H1','H9'), (Planet.MON, Planet.MER, Planet.URA, Planet.JUP)),
    EventType.TRAVEL_NEGATIVE: (('H10','H1','H9'), (Planet.SAT, Planet.MAR, Planet.NEP, Planet.PLU, Planet.MER, Planet.URA)),
    EventType.ARREST: (('H10','H1','H12'), (Planet.SAT, Planet.URA, Planet.NEP, Planet.MAR, Planet.PLU, Planet.NNO)),
    EventType.LOSSES: (('H10','H1','H2'), (Planet.NEP, Planet.URA, Planet.MER, Planet.MAR, Planet.SAT)),
    EventType.GRADUATION: (('H10','H1','H3'), (Planet.MER, Planet.MON, Planet.JUP, Planet.SUN, Planet.URA, Planet.VEN)),
    EventType.MOVE_HOME: (('H4','H1','H3'), (Planet.MER, Planet.MON, Planet.NNO, Planet.JUP, Planet.SUN, Planet.VEN)),
    EventType.BIRTH_GRANDSON:(('H4','H1','H5'),(Planet.MAR, Planet.SUN, Planet.JUP, Planet.NNO)),
    EventType.BIRTH_GRANDDAUGHTER:(('H4','H1','H5'),(Planet.VEN,Planet.MON, Planet.JUP,Planet.NNO)),
    EventType.MARRIAGE_FOR_MALE:(('H10','H7','H5'),(Planet.VEN,Planet.MON,Planet.NNO,Planet.JUP)),
    EventType.MARRIAGE_FOR_FEMALE:(('H10','H7','H5'),(Planet.SUN,Planet.JUP,Planet.MAR,Planet.NNO)),
    EventType.CHILDS_MARRIAGE:(('H10','H7','H5'),(Planet.MER,Planet.VEN,Planet.MON,Planet.NNO,Planet.JUP,Planet.SUN)),
    EventType.DIVORCE_SEPARATION:(('H4','H7'),(Planet.MAR,Planet.SAT,Planet.NEP,Planet.NNO,Planet.PLU)),
    EventType.DEATH_SON:(('H4','H7','H8'),(Planet.MAR,Planet.SAT,Planet.NEP,Planet.PLU,Planet.NNO)),
    EventType.DEATH_DAUGHTER:(('H4','H7','H8'),(Planet.VEN,Planet.MON,Planet.NEP,Planet.PLU,Planet.NNO)),
    EventType.DEATH_WIFE:(('H4','H7','H8'),(Planet.MON,Planet.VEN,Planet.SAT,Planet.NEP,Planet.PLU,Planet.NNO,Planet.MAR)),
    EventType.DEATH_HUSBAND:(('H4','H7','H8'),(Planet.SAT,Planet.SUN,Planet.NEP,Planet.PLU,Planet.NNO,Planet.MAR)),
    EventType.DEATH_BROTHER:(('H4','H1','H8'),(Planet.MER,Planet.MAR,Planet.SAT,Planet.NEP,Planet.PLU,Planet.NNO)),
    EventType.DEATH_SISTER:(('H4','H1','H8'),(Planet.MON,Planet.MER,Planet.VEN,Planet.MAR,Planet.SAT,Planet.NEP,Planet.PLU,Planet.NNO)),
    EventType.DEATH:(('H10','H1','H8'),(Planet.SAT,Planet.PLU,Planet.NEP,Planet.NNO,Planet.SUN)),
    EventType.ASSASINATION_SUICIDE:(('H10','H1','H8'),(Planet.SAT,Planet.PLU,Planet.URA,Planet.NEP,Planet.NNO,Planet.MAR)),
    EventType.PROMOTION_JOB:(('H10','H1','H3'),(Planet.SUN,Planet.JUP,Planet.MON,Planet.MER,Planet.URA,Planet.VEN)),
    EventType.RESIGN_RETIRE:(('H10','H1','H3'),(Planet.SAT,Planet.NEP,Planet.SUN,Planet.MAR,Planet.NNO)),
    EventType.TRAVEL_OVERSEAS_POSITIVE:(('H10','H1'),(Planet.MON,Planet.MER,Planet.URA,Planet.JUP)),
    EventType.MOBILIZATION:(('H10','H1','H12'),(Planet.MAR,Planet.SAT,Planet.PLU)),
    EventType.DEMOBILIZATION_RELEASE:(('H10','H1','H12'),(Planet.JUP,Planet.VEN,Planet.URA)),
    EventType.ACCIDENT:(('H10','H1','H3'),(Planet.MAR,Planet.URA,Planet.SAT,Planet.MER)),
    EventType.HOSPITALIZATION_ILLNESS:(('H10','H1','H12'),(Planet.SAT,Planet.NEP,Planet.MAR)),
    EventType.VIOLENCE:(('H10','H1'),(Planet.MAR,Planet.PLU,Planet.SAT,Planet.URA)),
    EventType.INTRIGUE:(('H10','H1','H12'),(Planet.NEP,Planet.MER)),
    EventType.GAMBLING_LOSS:(('H10','H1','H2','H5'),(Planet.NEP,Planet.SAT,Planet.URA,Planet.MAR)),
    EventType.GAMBLING_GAIN:(('H10','H1','H2','H5'),(Planet.JUP,Planet.VEN,Planet.URA)),
    EventType.ARMY_PROMOTION:(('H10','H1','H3'),(Planet.SUN,Planet.MAR,Planet.PLU,Planet.JUP,Planet.MON,Planet.MER,Planet.URA)),
    EventType.POSITIVE_3_9:(('H10', 'H1', 'H3'),(Planet.JUP, Planet.MON, Planet.VEN)),
    EventType.POSITIVE_6_12:(('H10', 'H1', 'H6'),(Planet.JUP, Planet.MON, Planet.VEN)),
    EventType.POSITIVE_2_8:(('H10', 'H1', 'H2'),(Planet.JUP, Planet.MON, Planet.VEN)),
    EventType.POSITIVE_AC_MC:(('H10', 'H1'),(Planet.JUP, Planet.MON, Planet.VEN)),
    EventType.NEGATIVE_6_12:(('H10', 'H1', 'H6'),(Planet.SAT, Planet.NEP, Planet.NNO, Planet.MAR, Planet.PLU)),
    EventType.NEGATIVE_AC_MC:(('H10', 'H1'),(Planet.SAT, Planet.NEP, Planet.NNO, Planet.MAR, Planet.PLU)),
    EventType.BLANK:((''),())
}

SECONDARY_RULES = {
    EventType.BIRTH_BROTHER: ((''),(Planet.SUN, Planet.MON, Planet.VEN, Planet.NNO, Planet.URA, Planet.PLU)),
    EventType.BIRTH_SISTER: ((''), (Planet.SUN, Planet.JUP, Planet.NNO, Planet.URA, Planet.PLU)),
    EventType.BIRTH_SON: ((''), (Planet.PLU, Planet.URA, Planet.MON, Planet.VEN, Planet.MER)),
    EventType.BIRTH_DAUGHTER: ((''), (Planet.MAR, Planet.URA, Planet.PLU, Planet.SUN, Planet.MER)),
    EventType.DEATH_FATHER_GRAND: (('H12'), (Planet.URA, Planet.MON)),
    EventType.DEATH_MOTHER_GRAND: (('H12'), (Planet.SUN, Planet.URA)),
    EventType.SUCCESS: ((''), (Planet.NNO)),
    EventType.FAILURE: (('H12'), (Planet.URA, Planet.MON, Planet.MER, Planet.PLU)),
    EventType.TRAVEL_POSITIVE: ((''), (Planet.VEN, Planet.SUN, Planet.NNO)),
    EventType.TRAVEL_NEGATIVE: (('H12'), ()),
    EventType.ARREST: (('H3'), (Planet.SUN,Planet.MER)),
    EventType.LOSSES: ((''), (Planet.PLU, Planet.NNO)),
    EventType.GRADUATION: ((''), (Planet.NNO)),
    EventType.MOVE_HOME: ((''), (Planet.URA)),
    EventType.BIRTH_GRANDSON:(('H9'), (Planet.PLU, Planet.URA,Planet.MON,Planet.VEN,Planet.MER)),
    EventType.BIRTH_GRANDDAUGHTER:(('H9'), (Planet.MAR,Planet.URA,Planet.PLU,Planet.SUN,Planet.MER)),
    EventType.MARRIAGE_FOR_MALE:((''), (Planet.MER,Planet.URA,Planet.MAR,Planet.SUN)),
    EventType.MARRIAGE_FOR_FEMALE:((''), (Planet.MER,Planet.URA,Planet.VEN,Planet.MON,Planet.PLU)),
    EventType.CHILDS_MARRIAGE:((''), (Planet.URA,Planet.MAR,Planet.PLU)),
    EventType.DIVORCE_SEPARATION:(('H12'), (Planet.MER,Planet.URA,Planet.VEN,Planet.MON,Planet.PLU)),
    EventType.DEATH_SON:(('H5','H12'), (Planet.SUN,Planet.MER,Planet.URA)),
    EventType.DEATH_DAUGHTER:(('H5','H12'), (Planet.MAR, Planet.URA,Planet.MER)),
    EventType.DEATH_WIFE:(('H5','H12'), (Planet.URA)),
    EventType.DEATH_HUSBAND:(('H5','H12'), (Planet.URA)),
    EventType.DEATH_BROTHER:(('H3','H12'), (Planet.MON,Planet.SUN)),
    EventType.DEATH_SISTER:(('H3','H12'), ()),
    EventType.DEATH:(('H12'), (Planet.URA,Planet.MAR,Planet.MON)),
    EventType.ASSASINATION_SUICIDE:(('H12'), (Planet.MON)),
    EventType.PROMOTION_JOB:(('H2','H11'), (Planet.PLU,Planet.NNO)),
    EventType.RESIGN_RETIRE:(('H12'), (Planet.URA,Planet.MON,Planet.MER,Planet.PLU)),
    EventType.TRAVEL_OVERSEAS_POSITIVE:(('H9'), (Planet.VEN,Planet.NEP,Planet.SUN,Planet.NNO)),
    EventType.MOBILIZATION:(('H3'), (Planet.MON,Planet.MER)),
    EventType.DEMOBILIZATION_RELEASE:(('H3'), (Planet.MON,Planet.MER,Planet.NNO)),
    EventType.ACCIDENT:(('H12'), (Planet.NEP,Planet.NNO,Planet.PLU,Planet.MON)),
    EventType.HOSPITALIZATION_ILLNESS:((''), (Planet.PLU,Planet.MON)),
    EventType.VIOLENCE:(('H12'), (Planet.MER)),
    EventType.INTRIGUE:((''), (Planet.PLU,Planet.MAR)),
    EventType.GAMBLING_LOSS:((''), (Planet.PLU,Planet.NNO)),
    EventType.GAMBLING_GAIN:((''), (Planet.PLU)),
    EventType.ARMY_PROMOTION:(('H2','H11'), (Planet.VEN,Planet.NNO)),
    EventType.POSITIVE_3_9:((''),(Planet.SUN, Planet.URA, Planet.MER)),
    EventType.POSITIVE_6_12:((''),(Planet.SUN, Planet.MER, Planet.URA)),
    EventType.POSITIVE_2_8:((''),(Planet.SUN, Planet.MER, Planet.URA)),
    EventType.POSITIVE_AC_MC:((''),(Planet.SUN, Planet.MER, Planet.URA)),
    EventType.NEGATIVE_6_12:((''),(Planet.SUN, Planet.MER)),
    EventType.NEGATIVE_AC_MC:((''),(Planet.SUN, Planet.MER)),
    EventType.BLANK:((''),())
}

def get_accept_lists(event_id):
    """input the event id corresponding to dictionary and string with aspect as printed to textfile like this
    (Uranus,55.5 52,(r)) (Hmd1,325.600,(d)) (square,3')"""
    
    aspect_rules = PRIMARY_RULES[event_id]
    house_aspect_rules = SECONDARY_RULES[event_id]
    if not aspect_rules:
        #if event_id doesn't exist
        return False  
    
    angle_house_accept = aspect_rules[0]
    angle_accept = []
    house_accept = []
    planet_accept = aspect_rules[1]
    pre_house_accept = house_aspect_rules[0]
    secondary_planets = house_aspect_rules[1]
    
    if isinstance(pre_house_accept, str):
        house_accept = [pre_house_accept]
    elif isinstance(pre_house_accept, tuple):
        for h in pre_house_accept:
            house_accept.append(h)

    for angle_house in angle_house_accept:
        if angle_house in ['H1','H4','H7','H10']:
            angle_accept.append(angle_house)
        else:
            house_accept.append(angle_house)

    return angle_accept, house_accept, planet_accept, secondary_planets

def is_acceptable_angular_aspect(event_id, str_aspect, type):
    angle_accept, house_accept, planet_accept, secondary_planets = get_accept_lists(event_id)
    
    p1_d1_s1, p2_d2_s2, _ = str_aspect.split(' ')
    p1, _, _ = p1_d1_s1.split(',')
    p1 = p1[1:]
    p2, _, _ = p2_d2_s2.split(',')
    p2 = p2[1:]

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
    
def calc_directed_pd_houses(jd_radix, jd_event, geo_latitude, rad_houses, e):
    """returns 2 tuples with house cusps 1 to 12 dir, conv
    removed functionality for Hmd1 and Hmd2 (H1/H2)"""
    arc = pd.calc_arc(jd_radix, jd_event)
    ramc = rad_houses[1][2]

    directed = swe.houses_armc(swe.degnorm(ramc+arc), geo_latitude, e, b'T')[0]
    converse = swe.houses_armc(swe.degnorm(ramc-arc), geo_latitude, e, b'T')[0]
    #print(f"dirHouse ----- {directed} \nconvHouse------- {converse}")
    return directed, converse

def calc_directed_pd_planets(jd_radix, jd_event, geo_latitude, geo_longitude, houses_info, rad_planets_equatorial, e):
    """returns tuple (dir_planets, conv_planets, extended_planet_info)"""
    dir_planets = []
    conv_planets = []
    dict_extended_info = {}

    for planet in range(0, len(PLANETS)):
        long, ra, decl = rad_planets_equatorial[planet]
        cusps = houses_info[0]
        p_house = pd.get_housepos_manual(long, cusps)
        ac, mc, ramc = calc_radix_ac_mc_ramc(houses_info)

        direct_pd_obj = pd.PD_Base(jd_radix, jd_event, geo_latitude, decl, ra, ramc, mc, True, p_house, ac, long, e)
        long_directed = direct_pd_obj.get_long_directed()
        dir_planets.append((PLANETS[planet], long_directed, "(d)"))
        
        converse_pd_obj = pd.PD_Base(jd_radix, jd_event, geo_latitude, decl, ra, ramc, mc, False, p_house, ac, long, e)
        long_conv = converse_pd_obj.get_long_directed()
        conv_planets.append((PLANETS[planet], long_conv, "(c)"))

        #append planets md,sa,adp etc to dict information
        dict_extended_info[PLANETS[planet]] = direct_pd_obj.get_extended_planet_info()

    return dir_planets, conv_planets, dict_extended_info

def calc_rad_planets_equatorial(jd_radix):
    """returns array with (long, ra, decl) for each of PLANETS(list) following PLANETS INDEXING"""
    planet_info = [] 
    for planet in range(0, len(PLANETS)):
        xx, _ = swe.calc_ut(jd_radix, planet)
        xx1, _ = swe.calc_ut(jd_radix, planet, swe.FLG_EQUATORIAL)
        long = xx[0]
        ra = xx1[0]
        decl = xx1[1]
        planet_info.append((long, ra, decl))

    return planet_info

def calc_directed_POF(rad_planets, jd_radix, jd_event, geo_latitude, houses_info, e):
    """returns tuple (pof_rad, pof_directed, pof_converse)"""
    ac, mc, ramc = calc_radix_ac_mc_ramc(houses_info)
    cusps = houses_info[0]
    pof_long = rad_planets[11][1]
    p_house = pd.get_housepos_manual(pof_long, cusps)
    
    ra, decl, _ = swe.cotrans((pof_long, 0.0, 1), e)
    decl = -decl
    
    direct_pof_obj = pd.PD_Base(jd_radix, jd_event, geo_latitude, decl, ra, ramc, mc, True, p_house, ac, pof_long, e)
    long_directed = direct_pof_obj.get_long_directed()

    converse_pof_obj = pd.PD_Base(jd_radix, jd_event, geo_latitude, decl, ra, ramc, mc, False, p_house, ac, pof_long, e)
    long_conv = converse_pof_obj.get_long_directed()

    dict_info = {}
    dict_info["POF"] = direct_pof_obj.get_extended_planet_info()
    
    return long_directed, long_conv, dict_info

def calc_planet_house_pos(ramc, geo_lat, e, long, lat):
    hpos = swe.house_pos(ramc, geo_lat, e, (long,lat), b'T')
    
    return int(hpos)

def calc_radix_ac_mc_ramc(houses_info):
    """returns tuple of radix (ac, mc, ramc)"""
    ac = houses_info[0][0]
    mc = houses_info[1][1]
    ramc = houses_info[1][2]
    
    return (ac, mc, ramc)

def add_suffix_to_tuples(tuples_list, suffix):
    return tuple(list(t) + [suffix] for t in tuples_list)

def calc_alt(lst_hours, ra_deg, decl_deg, latitude_deg):
    """
    Calculate the altitude of an astronomical object given LST, RA, Dec, and Latitude.

    Parameters:
    lst_str (str): Local Sidereal Time in HH:MM:SS format.
    ra_deg (float): Right Ascension in degrees.
    dec_deg (float): Declination in degrees.
    latitude_deg (float): Latitude of the observer in degrees.

    Returns:
    float: Altitude in degrees.
    """    
    lst_deg = lst_hours * 15.0
    h = lst_deg - ra_deg
    h = swe.degnorm(h)    #normalize degree

    lat_rad = math.radians(latitude_deg)
    decl_rad = math.radians(decl_deg)
    h_rad = math.radians(h)

    alt_rad = math.asin(math.sin(decl_rad) * math.sin(lat_rad) + 
                        math.cos(decl_rad) * math.cos(lat_rad) * math.cos(h_rad))

    alt_deg = math.degrees(alt_rad)

    return alt_deg

def calc_lst(jd, longitude):
    """
    Calculate the Local Sidereal Time (LST) and Greenwich Mean Sidereal Time (GMST)
    from Julian Date (JD) and longitude.

    Parameters:
    jd (float): Julian Date.
    longitude (float): Longitude of the location in degrees.

    Prints:
    - Julian Date
    - Greenwich Mean Sidereal Time
    - Local Sidereal Time
    """

    # Convert longitude to degrees, minutes, seconds format for display
    hemisphere = 'E' if longitude > 0 else 'W'
    longitude_deg = int(abs(longitude))
    longitude_min = int((abs(longitude) - longitude_deg) * 60)
    longitude_sec = int(((abs(longitude) - longitude_deg) * 60 - longitude_min) * 60)

    # Calculate Greenwich Mean Sidereal Time (GMST)
    gmst = 18.697374558 + 24.06570982441908 * (jd - 2451545)
    gmst = gmst % 24  # Convert to 24-hour format

    # Convert longitude to sidereal hours
    longitude_hours = longitude / 15.0

    # Calculate Local Sidereal Time (LST)
    lst = gmst + longitude_hours
    if lst < 0:
        lst += 24
    elif lst >= 24:
        lst -= 24
    
    return lst
