import swisseph as swe
import julian
import pd_base as pd
import math
from aspects_base import calculate_obliquity, find_pd_swiss_aspects, format_house_list
from constants import PLANETS, HOUSES, calc_planets_pof_houses_labelled

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

#the values correspond to POLARIS event list
class EventType:
    BIRTH_BROTHER = 1
    BIRTH_SISTER = 2
    BIRTH_SON = 3
    BIRTH_DAUGHTER = 4
    BIRTH_GRANDSON = 5
    BIRTH_GRANDDAUGHTER = 6
    MARRIAGE_ENGAGEMENT_FOR_MALE = 7
    MARRIAGE_ENGAGEMENT_FOR_FEMALE = 8
    CHILDS_MARRIAGE = 9
    DIVORCE_SEPARATION = 10
    DEATH_FATHER_GRAND = 11
    DEATH_MOTHER_GRAND = 12
    DEATH_SON = 13
    DEATH_DAUGHTER = 14
    DEATH_WIFE_FRIEND = 15
    DEATH_HUSBAND_FRIEND = 16
    DEATH_BROTHER = 17
    DEATH_SISTER = 18
    DEATH = 19
    ASSASINATION_SUICIDE = 20
    SUCCESS_ELECTED = 21
    PROMOTION_JOB = 22
    FAILURE_DEFEATED = 23
    RESIGN_RETIRE = 24
    TRAVEL_OVERSEAS_POSITIVE = 25
    TRAVEL_POSITIVE = 26
    TRAVEL_NEGATIVE = 27
    MOBILIZATION = 28
    DEMOBILIZATION_RELEASE = 29
    ARREST = 30
    ACCIDENT = 31
    HOSPITALIZATION_ILLNESS = 32
    VIOLENCE = 33
    INTRIGUE = 34
    LOSSES = 35
    GAMBLING_LOSS = 36
    GAMBLING_GAIN = 37
    GRADUATION_PUBLICATION = 38
    MOVE_HOME = 39
    ARMY_PROMOTION = 40
    POSITIVE_AC_MC = 41
    NEGATIVE_AC_MC = 42
    POSITIVE_2_8 = 43
    NEGATIVE_2_8 = 44
    POSITIVE_3_9 = 45
    NEGATIVE_3_9 = 46
    POSITIVE_5_11 = 47
    NEGATIVE_5_11 = 48
    POSITIVE_6_12 = 49
    NEGATIVE_6_12 = 50
    BLANK = 51

    @classmethod
    def get_name(cls, value):
        """Returns the name of the event type for the given value."""
        for attr in dir(cls):
            if not attr.startswith("__") and getattr(cls, attr) == value:
                return attr
        return 'UNKNOWN_TYPE'

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
    APPROPRIATE_DIRECTED_CUSP_ONLY = 11
    APPROPRIATE_DIRECTED_CUSP_PLANET_TO_CUSP = 12
    APPROPRIATE_INCLUDING_PLANET_COMBOS = 13
    FAST_TO_SLOW_COMBO = 14
    
class GoodBadFlag:
    GOOD = 0
    BAD = 1
    NEUTRAL = 2

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
    EventType.BIRTH_BROTHER: (('H4', 'H7','H3'), (Planet.MER, Planet.JUP), GoodBadFlag.GOOD),
    EventType.BIRTH_SISTER: (('H4', 'H7', 'H3'), (Planet.MON, Planet.MER, Planet.VEN), GoodBadFlag.GOOD),
    EventType.BIRTH_SON: (('H4', 'H1','H5'), (Planet.MAR, Planet.SUN, Planet.JUP, Planet.NNO), GoodBadFlag.GOOD),
    EventType.BIRTH_DAUGHTER: (('H4', 'H1','H5'), (Planet.VEN, Planet.MON, Planet.JUP, Planet.NNO), GoodBadFlag.GOOD),
    EventType.DEATH_FATHER_GRAND: (('H10','H1', 'H8'), (Planet.SAT, Planet.SUN, Planet.NEP, Planet.PLU, Planet.MAR, Planet.NNO), GoodBadFlag.BAD),
    EventType.DEATH_MOTHER_GRAND: (('H4','H1', 'H8'), (Planet.MON, Planet.VEN, Planet.SAT, Planet.NEP, Planet.PLU, Planet.MAR, Planet.NNO), GoodBadFlag.BAD),
    EventType.SUCCESS_ELECTED: (('H10','H1','H3'), (Planet.SUN, Planet.JUP, Planet.MON, Planet.MER, Planet.URA, Planet.VEN), GoodBadFlag.GOOD),
    EventType.FAILURE_DEFEATED: (('H10','H1', 'H3'), (Planet.SAT, Planet.NEP, Planet.NNO, Planet.MAR, Planet.SUN), GoodBadFlag.BAD),
    EventType.TRAVEL_POSITIVE: (('H10','H1','H9'), (Planet.MON, Planet.MER, Planet.URA, Planet.JUP), GoodBadFlag.GOOD),
    EventType.TRAVEL_NEGATIVE: (('H10','H1','H9'), (Planet.SAT, Planet.MAR, Planet.NEP, Planet.PLU, Planet.MER, Planet.URA), GoodBadFlag.BAD),
    EventType.ARREST: (('H10','H1','H12'), (Planet.SAT, Planet.URA, Planet.NEP, Planet.MAR, Planet.PLU, Planet.NNO), GoodBadFlag.BAD),
    EventType.LOSSES: (('H10','H1','H2'), (Planet.NEP, Planet.URA, Planet.MER, Planet.MAR, Planet.SAT), GoodBadFlag.BAD),
    EventType.GRADUATION_PUBLICATION: (('H10','H1','H3'), (Planet.MER, Planet.MON, Planet.JUP, Planet.SUN, Planet.URA, Planet.VEN), GoodBadFlag.GOOD),
    EventType.MOVE_HOME: (('H4','H1','H3'), (Planet.MER, Planet.MON, Planet.NNO, Planet.JUP, Planet.SUN, Planet.VEN), GoodBadFlag.GOOD),
    EventType.BIRTH_GRANDSON:(('H4','H1','H5'),(Planet.MAR, Planet.SUN, Planet.JUP, Planet.NNO), GoodBadFlag.GOOD),
    EventType.BIRTH_GRANDDAUGHTER:(('H4','H1','H5'),(Planet.VEN,Planet.MON, Planet.JUP,Planet.NNO), GoodBadFlag.GOOD),
    EventType.MARRIAGE_ENGAGEMENT_FOR_MALE:(('H10','H7','H5'),(Planet.VEN,Planet.MON,Planet.NNO,Planet.JUP), GoodBadFlag.GOOD),
    EventType.MARRIAGE_ENGAGEMENT_FOR_FEMALE:(('H10','H7','H5'),(Planet.SUN,Planet.JUP,Planet.MAR,Planet.NNO), GoodBadFlag.GOOD),
    EventType.CHILDS_MARRIAGE:(('H10','H7','H5'),(Planet.MER,Planet.VEN,Planet.MON,Planet.NNO,Planet.JUP,Planet.SUN), GoodBadFlag.GOOD),
    EventType.DIVORCE_SEPARATION:(('H4','H7'),(Planet.MAR,Planet.SAT,Planet.NEP,Planet.NNO,Planet.PLU), GoodBadFlag.BAD),
    EventType.DEATH_SON:(('H4','H7','H8', 'H5'),(Planet.MAR,Planet.SAT,Planet.NEP,Planet.PLU,Planet.NNO), GoodBadFlag.BAD),
    EventType.DEATH_DAUGHTER:(('H4','H7','H8', 'H5'),(Planet.VEN,Planet.MON,Planet.NEP,Planet.PLU,Planet.NNO), GoodBadFlag.BAD),
    EventType.DEATH_WIFE_FRIEND:(('H4','H7','H8'),(Planet.MON,Planet.VEN,Planet.SAT,Planet.NEP,Planet.PLU,Planet.NNO,Planet.MAR), GoodBadFlag.BAD),
    EventType.DEATH_HUSBAND_FRIEND:(('H4','H7','H8'),(Planet.SAT,Planet.SUN,Planet.NEP,Planet.PLU,Planet.NNO,Planet.MAR), GoodBadFlag.BAD),
    EventType.DEATH_BROTHER:(('H4','H1','H8'),(Planet.MER,Planet.MAR,Planet.SAT,Planet.NEP,Planet.PLU,Planet.NNO), GoodBadFlag.BAD),
    EventType.DEATH_SISTER:(('H4','H1','H8'),(Planet.MON,Planet.MER,Planet.VEN,Planet.MAR,Planet.SAT,Planet.NEP,Planet.PLU,Planet.NNO), GoodBadFlag.BAD),
    EventType.DEATH:(('H10','H1','H8'),(Planet.SAT,Planet.PLU,Planet.NEP,Planet.NNO,Planet.SUN), GoodBadFlag.BAD),
    EventType.ASSASINATION_SUICIDE:(('H10','H1','H8'),(Planet.SAT,Planet.PLU,Planet.URA,Planet.NEP,Planet.NNO,Planet.MAR), GoodBadFlag.BAD),
    EventType.PROMOTION_JOB:(('H10','H1','H3','H2'),(Planet.SUN,Planet.JUP,Planet.MON,Planet.MER,Planet.URA,Planet.VEN), GoodBadFlag.GOOD),
    EventType.RESIGN_RETIRE:(('H10','H1','H3','H12'),(Planet.SAT,Planet.NEP,Planet.SUN,Planet.MAR,Planet.NNO), GoodBadFlag.BAD),
    EventType.TRAVEL_OVERSEAS_POSITIVE:(('H10','H1','H9'),(Planet.MON,Planet.MER,Planet.URA,Planet.JUP), GoodBadFlag.GOOD),
    EventType.MOBILIZATION:(('H10','H1','H12'),(Planet.MAR,Planet.SAT,Planet.PLU), GoodBadFlag.BAD),
    EventType.DEMOBILIZATION_RELEASE:(('H10','H1','H12'),(Planet.JUP,Planet.VEN,Planet.URA), GoodBadFlag.GOOD),
    EventType.ACCIDENT:(('H10','H1','H3','H12'),(Planet.MAR,Planet.URA,Planet.SAT,Planet.MER), GoodBadFlag.BAD),
    EventType.HOSPITALIZATION_ILLNESS:(('H10','H1','H12'),(Planet.SAT,Planet.NEP,Planet.MAR), GoodBadFlag.BAD),
    EventType.VIOLENCE:(('H10','H1','H12'),(Planet.MAR,Planet.PLU,Planet.SAT,Planet.URA), GoodBadFlag.BAD),
    EventType.INTRIGUE:(('H10','H1','H12'),(Planet.NEP,Planet.MER), GoodBadFlag.BAD),
    EventType.GAMBLING_LOSS:(('H10','H1','H2','H5'),(Planet.NEP,Planet.SAT,Planet.URA,Planet.MAR), GoodBadFlag.BAD),
    EventType.GAMBLING_GAIN:(('H10','H1','H2','H5'),(Planet.JUP,Planet.VEN,Planet.URA), GoodBadFlag.GOOD),
    EventType.ARMY_PROMOTION:(('H10','H1','H3'),(Planet.SUN,Planet.MAR,Planet.PLU,Planet.JUP,Planet.MON,Planet.MER,Planet.URA), GoodBadFlag.GOOD),
    EventType.POSITIVE_3_9:(('H10', 'H1', 'H3'),(Planet.JUP, Planet.MON, Planet.VEN), GoodBadFlag.GOOD),
    EventType.POSITIVE_6_12:(('H10', 'H1', 'H6'),(Planet.JUP, Planet.MON, Planet.VEN), GoodBadFlag.GOOD),
    EventType.POSITIVE_2_8:(('H10', 'H1', 'H2'),(Planet.JUP, Planet.MON, Planet.VEN), GoodBadFlag.GOOD),
    EventType.POSITIVE_AC_MC:(('H10', 'H1'),(Planet.JUP, Planet.MON, Planet.VEN), GoodBadFlag.GOOD),
    EventType.NEGATIVE_6_12:(('H10', 'H1', 'H6'),(Planet.SAT, Planet.NEP, Planet.NNO, Planet.MAR, Planet.PLU), GoodBadFlag.BAD),
    EventType.NEGATIVE_AC_MC:(('H10', 'H1'),(Planet.SAT, Planet.NEP, Planet.NNO, Planet.MAR, Planet.PLU), GoodBadFlag.NEUTRAL),
    EventType.BLANK:((''),())
}

SECONDARY_RULES = {
    EventType.BIRTH_BROTHER: ((''),(Planet.SUN, Planet.MON, Planet.VEN, Planet.NNO, Planet.URA, Planet.PLU, Planet.MAR)),
    EventType.BIRTH_SISTER: ((''), (Planet.SUN, Planet.JUP, Planet.NNO, Planet.URA, Planet.PLU)),
    EventType.BIRTH_SON: ((''), (Planet.PLU, Planet.URA, Planet.MON, Planet.VEN, Planet.MER)),
    EventType.BIRTH_DAUGHTER: ((''), (Planet.MAR, Planet.URA, Planet.PLU, Planet.SUN, Planet.MER)),
    EventType.DEATH_FATHER_GRAND: (('H12'), (Planet.URA, Planet.MON)),
    EventType.DEATH_MOTHER_GRAND: (('H12'), (Planet.SUN, Planet.URA)),
    EventType.SUCCESS_ELECTED: ((''), (Planet.NNO)),
    EventType.FAILURE_DEFEATED: (('H12'), (Planet.URA, Planet.MON, Planet.MER, Planet.PLU)),
    EventType.TRAVEL_POSITIVE: ((''), (Planet.VEN, Planet.SUN, Planet.NNO)),
    EventType.TRAVEL_NEGATIVE: (('H12'), ()),
    EventType.ARREST: (('H3'), (Planet.SUN,Planet.MER)),
    EventType.LOSSES: ((''), (Planet.PLU, Planet.NNO)),
    EventType.GRADUATION_PUBLICATION: ((''), (Planet.NNO)),
    EventType.MOVE_HOME: ((''), (Planet.URA)),
    EventType.BIRTH_GRANDSON:(('H9'), (Planet.PLU, Planet.URA,Planet.MON,Planet.VEN,Planet.MER)),
    EventType.BIRTH_GRANDDAUGHTER:(('H9'), (Planet.MAR,Planet.URA,Planet.PLU,Planet.SUN,Planet.MER)),
    EventType.MARRIAGE_ENGAGEMENT_FOR_MALE:((''), (Planet.MER,Planet.URA,Planet.MAR,Planet.SUN)),
    EventType.MARRIAGE_ENGAGEMENT_FOR_FEMALE:((''), (Planet.MER,Planet.URA,Planet.VEN,Planet.MON)),
    EventType.CHILDS_MARRIAGE:((''), (Planet.URA,Planet.MAR,Planet.PLU)),
    EventType.DIVORCE_SEPARATION:(('H12'), (Planet.MER,Planet.URA,Planet.VEN,Planet.MON,Planet.PLU)),
    EventType.DEATH_SON:(('H12'), (Planet.SUN,Planet.MER,Planet.URA)),
    EventType.DEATH_DAUGHTER:(('H12'), (Planet.MAR, Planet.URA,Planet.MER)),
    EventType.DEATH_WIFE_FRIEND:(('H5','H12'), (Planet.URA)),
    EventType.DEATH_HUSBAND_FRIEND:(('H5','H12'), (Planet.URA)),
    EventType.DEATH_BROTHER:(('H3','H12'), (Planet.MON,Planet.SUN)),
    EventType.DEATH_SISTER:(('H3','H12'), ()),
    EventType.DEATH:(('H12'), (Planet.URA,Planet.MAR,Planet.MON)),
    EventType.ASSASINATION_SUICIDE:(('H12'), (Planet.MON)),
    EventType.PROMOTION_JOB:(('H11'), (Planet.PLU,Planet.NNO)),
    EventType.RESIGN_RETIRE:((''), (Planet.URA,Planet.MON,Planet.MER,Planet.PLU)),
    EventType.TRAVEL_OVERSEAS_POSITIVE:((''), (Planet.VEN,Planet.NEP,Planet.SUN,Planet.NNO)),
    EventType.MOBILIZATION:(('H3'), (Planet.MON,Planet.MER)),
    EventType.DEMOBILIZATION_RELEASE:(('H3'), (Planet.MON,Planet.MER,Planet.NNO)),
    EventType.ACCIDENT:((''), (Planet.NEP,Planet.NNO,Planet.PLU,Planet.MON)),
    EventType.HOSPITALIZATION_ILLNESS:((''), (Planet.PLU,Planet.MON)),
    EventType.VIOLENCE:((''), (Planet.MER)),
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

PLANETARY_COMBO = {
    EventType.BIRTH_BROTHER: ((Planet.SUN,Planet.MON),(Planet.SUN,Planet.MER),(Planet.SUN,Planet.VEN),(Planet.SUN,Planet.MAR),(Planet.SUN,Planet.JUP),(Planet.SUN,Planet.URA),(Planet.SUN,Planet.NNO),(Planet.MON,Planet.MER),(Planet.MER,Planet.VEN),(Planet.MER,Planet.JUP),(Planet.MER,Planet.URA),(Planet.MER,Planet.PLU),(Planet.MER,Planet.NNO),(Planet.VEN,Planet.JUP),(Planet.MAR,Planet.JUP),(Planet.MAR,Planet.PLU),(Planet.MAR,Planet.NNO),(Planet.JUP,Planet.PLU),(Planet.JUP,Planet.NNO),(Planet.PLU,Planet.NNO)),
    EventType.BIRTH_SISTER: ((Planet.SUN,Planet.VEN),(Planet.MON,Planet.MER),(Planet.MON,Planet.VEN),(Planet.MON,Planet.JUP),(Planet.MON,Planet.URA),(Planet.MON,Planet.PLU),(Planet.MON,Planet.NNO),(Planet.MER,Planet.VEN),(Planet.MER,Planet.JUP),(Planet.MER,Planet.URA),(Planet.MER,Planet.PLU),(Planet.MER,Planet.NNO),(Planet.VEN,Planet.JUP),(Planet.VEN,Planet.URA),(Planet.VEN,Planet.PLU),(Planet.VEN,Planet.NNO),(Planet.JUP,Planet.PLU),(Planet.JUP,Planet.NNO),(Planet.PLU,Planet.NNO)),
    EventType.BIRTH_SON: ((Planet.SUN,Planet.MON),(Planet.SUN,Planet.MER),(Planet.SUN,Planet.VEN),(Planet.SUN,Planet.MAR),(Planet.SUN,Planet.JUP),(Planet.SUN,Planet.URA),(Planet.SUN,Planet.PLU),(Planet.SUN,Planet.NNO),(Planet.MON,Planet.MER),(Planet.MER,Planet.VEN),(Planet.MER,Planet.MAR),(Planet.MER,Planet.JUP),(Planet.MER,Planet.URA),(Planet.MER,Planet.PLU),(Planet.MER,Planet.NNO),(Planet.VEN,Planet.MAR),(Planet.VEN,Planet.JUP),(Planet.MAR,Planet.JUP),(Planet.MAR,Planet.PLU),(Planet.MAR,Planet.NNO),(Planet.JUP,Planet.URA),(Planet.JUP,Planet.PLU),(Planet.JUP,Planet.NNO),(Planet.URA,Planet.NNO),(Planet.PLU,Planet.NNO)),
    EventType.BIRTH_DAUGHTER: ((Planet.SUN,Planet.VEN),(Planet.MON,Planet.MER),(Planet.MON,Planet.VEN),(Planet.MON,Planet.JUP),(Planet.MON,Planet.URA),(Planet.MON,Planet.PLU),(Planet.MON,Planet.NNO),(Planet.MER,Planet.VEN),(Planet.MER,Planet.JUP),(Planet.MER,Planet.URA),(Planet.MER,Planet.PLU),(Planet.MER,Planet.NNO),(Planet.VEN,Planet.JUP),(Planet.VEN,Planet.URA),(Planet.VEN,Planet.PLU),(Planet.VEN,Planet.NNO),(Planet.JUP,Planet.URA),(Planet.JUP,Planet.PLU),(Planet.JUP,Planet.NNO),(Planet.URA,Planet.NNO),(Planet.PLU,Planet.NNO)),
    EventType.DEATH_FATHER_GRAND: ((Planet.SUN,Planet.MAR),(Planet.SUN,Planet.SAT),(Planet.SUN,Planet.URA),(Planet.SUN,Planet.NEP),(Planet.SUN,Planet.PLU),(Planet.MER,Planet.MAR),(Planet.MER,Planet.SAT),(Planet.MER,Planet.URA),(Planet.MER,Planet.PLU),(Planet.MER,Planet.NNO),(Planet.MAR,Planet.SAT),(Planet.MAR,Planet.URA),(Planet.MAR,Planet.NEP),(Planet.MAR,Planet.PLU),(Planet.MAR,Planet.NNO),(Planet.JUP,Planet.SAT),(Planet.JUP,Planet.NEP),(Planet.JUP,Planet.PLU),(Planet.JUP,Planet.NNO),(Planet.SAT,Planet.URA),(Planet.SAT,Planet.NEP),(Planet.SAT,Planet.PLU),(Planet.SAT,Planet.NNO),(Planet.URA,Planet.NEP),(Planet.URA,Planet.PLU),(Planet.URA,Planet.NNO),(Planet.NEP,Planet.PLU),(Planet.NEP,Planet.NNO),(Planet.PLU,Planet.NNO)),
    EventType.DEATH_MOTHER_GRAND: ((Planet.MON,Planet.MAR),(Planet.MON,Planet.SAT),(Planet.MON,Planet.URA),(Planet.MON,Planet.NEP),(Planet.MON,Planet.PLU),(Planet.MON,Planet.NNO),(Planet.MER,Planet.MAR),(Planet.MER,Planet.SAT),(Planet.MER,Planet.URA),(Planet.MER,Planet.PLU),(Planet.MER,Planet.NNO),(Planet.VEN,Planet.SAT),(Planet.VEN,Planet.URA),(Planet.VEN,Planet.NEP),(Planet.VEN,Planet.PLU),(Planet.VEN,Planet.NNO),(Planet.MAR,Planet.SAT),(Planet.MAR,Planet.URA),(Planet.MAR,Planet.NEP),(Planet.MAR,Planet.PLU),(Planet.MAR,Planet.NNO),(Planet.JUP,Planet.SAT),(Planet.JUP,Planet.NEP),(Planet.JUP,Planet.PLU),(Planet.JUP,Planet.NNO),(Planet.SAT,Planet.URA),(Planet.SAT,Planet.NEP),(Planet.SAT,Planet.PLU),(Planet.SAT,Planet.NNO),(Planet.URA,Planet.NEP),(Planet.URA,Planet.PLU),(Planet.URA,Planet.NNO),(Planet.NEP,Planet.PLU),(Planet.NEP,Planet.NNO),(Planet.PLU,Planet.NNO)),
    EventType.SUCCESS_ELECTED: ((Planet.SUN,Planet.MON),(Planet.SUN,Planet.MER),(Planet.SUN,Planet.VEN),(Planet.SUN,Planet.JUP),(Planet.SUN,Planet.URA),(Planet.SUN,Planet.NNO),(Planet.MON,Planet.MER),(Planet.MON,Planet.VEN),(Planet.MON,Planet.JUP),(Planet.MON,Planet.URA),(Planet.MON,Planet.NNO),(Planet.MER,Planet.VEN),(Planet.MER,Planet.JUP),(Planet.MER,Planet.URA),(Planet.MER,Planet.PLU),(Planet.MER,Planet.NNO),(Planet.VEN,Planet.MAR),(Planet.VEN,Planet.JUP),(Planet.VEN,Planet.URA),(Planet.VEN,Planet.PLU),(Planet.VEN,Planet.NNO),(Planet.MAR,Planet.JUP),(Planet.JUP,Planet.URA),(Planet.JUP,Planet.PLU),(Planet.JUP,Planet.NNO),(Planet.URA,Planet.NNO),(Planet.PLU,Planet.NNO)),
    EventType.FAILURE_DEFEATED: ((Planet.SUN,Planet.MAR),(Planet.SUN,Planet.SAT),(Planet.SUN,Planet.URA),(Planet.SUN,Planet.NEP),(Planet.SUN,Planet.PLU),(Planet.MON,Planet.MAR),(Planet.MON,Planet.SAT),(Planet.MON,Planet.URA),(Planet.MON,Planet.NEP),(Planet.MON,Planet.PLU),(Planet.MON,Planet.NNO),(Planet.MER,Planet.MAR),(Planet.MER,Planet.SAT),(Planet.MER,Planet.URA),(Planet.MER,Planet.NEP),(Planet.MER,Planet.PLU),(Planet.MER,Planet.NNO),(Planet.VEN,Planet.MAR),(Planet.VEN,Planet.MAR),(Planet.VEN,Planet.SAT),(Planet.VEN,Planet.NEP),(Planet.VEN,Planet.NNO),(Planet.MAR,Planet.JUP),(Planet.MAR,Planet.SAT),(Planet.MAR,Planet.URA),(Planet.MAR,Planet.NEP),(Planet.MAR,Planet.PLU),(Planet.MAR,Planet.NNO),(Planet.JUP,Planet.SAT),(Planet.JUP,Planet.NEP),(Planet.JUP,Planet.PLU),(Planet.SAT,Planet.URA),(Planet.SAT,Planet.NEP),(Planet.SAT,Planet.PLU),(Planet.SAT,Planet.NNO),(Planet.URA,Planet.NEP),(Planet.URA,Planet.PLU),(Planet.URA,Planet.NNO),(Planet.NEP,Planet.PLU),(Planet.NEP,Planet.NNO),(Planet.PLU,Planet.NNO)),
    EventType.TRAVEL_POSITIVE: ((Planet.SUN,Planet.MER),(Planet.SUN,Planet.VEN),(Planet.SUN,Planet.JUP),(Planet.SUN,Planet.NNO),(Planet.MON,Planet.MER),(Planet.MON,Planet.VEN),(Planet.MON,Planet.JUP),(Planet.MON,Planet.URA),(Planet.MON,Planet.NNO),(Planet.MER,Planet.VEN),(Planet.MER,Planet.JUP),(Planet.MER,Planet.URA),(Planet.MER,Planet.NEP),(Planet.MER,Planet.PLU),(Planet.MER,Planet.NNO),(Planet.VEN,Planet.JUP),(Planet.VEN,Planet.URA),(Planet.VEN,Planet.NNO),(Planet.MAR,Planet.JUP),(Planet.JUP,Planet.SAT),(Planet.JUP,Planet.URA),(Planet.JUP,Planet.NEP),(Planet.JUP,Planet.PLU),(Planet.JUP,Planet.NNO),(Planet.URA,Planet.NNO),(Planet.PLU,Planet.NNO)),
    EventType.TRAVEL_NEGATIVE: ((Planet.SUN,Planet.NNO),(Planet.MON,Planet.MER),(Planet.MON,Planet.URA),(Planet.MON,Planet.NNO),(Planet.MER,Planet.URA),(Planet.MER,Planet.NEP),(Planet.MER,Planet.PLU),(Planet.MER,Planet.NNO),(Planet.MAR,Planet.JUP),(Planet.JUP,Planet.SAT),(Planet.JUP,Planet.URA),(Planet.JUP,Planet.NEP),(Planet.JUP,Planet.PLU),(Planet.JUP,Planet.NNO),(Planet.URA,Planet.NNO),(Planet.PLU,Planet.NNO)),
    EventType.TRAVEL_OVERSEAS_POSITIVE: (EventType.TRAVEL_POSITIVE,(Planet.URA,Planet.PLU)),
    EventType.ARREST: (EventType.FAILURE_DEFEATED),
    EventType.LOSSES: ((Planet.VEN,Planet.PLU),(Planet.VEN,Planet.URA),(Planet.VEN,Planet.SAT),(Planet.VEN,Planet.NNO)),
    EventType.GRADUATION_PUBLICATION: (EventType.SUCCESS_ELECTED,(Planet.JUP,Planet.PLU)),
    EventType.MOVE_HOME: ((Planet.SUN,Planet.MER),(Planet.MON,Planet.MER),(Planet.MON,Planet.VEN),(Planet.MON,Planet.JUP),(Planet.MON,Planet.URA),(Planet.MER,Planet.VEN),(Planet.MER,Planet.JUP),(Planet.MER,Planet.NEP),(Planet.MER,Planet.PLU),(Planet.JUP,Planet.NNO),(Planet.URA,Planet.NNO),(Planet.NEP,Planet.NNO)),
    EventType.BIRTH_GRANDSON: ((Planet.SUN,Planet.MON),(Planet.SUN,Planet.MER),(Planet.SUN,Planet.VEN),(Planet.SUN,Planet.MAR),(Planet.SUN,Planet.JUP),(Planet.SUN,Planet.URA),(Planet.SUN,Planet.PLU),(Planet.SUN,Planet.NNO),(Planet.MON,Planet.MER),(Planet.MER,Planet.VEN),(Planet.MER,Planet.MAR),(Planet.MER,Planet.JUP),(Planet.MER,Planet.URA),(Planet.MER,Planet.PLU),(Planet.MER,Planet.NNO),(Planet.VEN,Planet.JUP),(Planet.MAR,Planet.JUP),(Planet.MAR,Planet.PLU),(Planet.MAR,Planet.NNO),(Planet.JUP,Planet.PLU),(Planet.JUP,Planet.NNO),(Planet.URA,Planet.NNO),(Planet.PLU,Planet.NNO)),
    EventType.BIRTH_GRANDDAUGHTER: ((Planet.SUN,Planet.VEN),(Planet.MON,Planet.MER),(Planet.MON,Planet.VEN),(Planet.MON,Planet.JUP),(Planet.MON,Planet.URA),(Planet.MON,Planet.PLU),(Planet.MON,Planet.NNO),(Planet.MER,Planet.VEN),(Planet.MER,Planet.JUP),(Planet.MER,Planet.URA),(Planet.MER,Planet.PLU),(Planet.MER,Planet.NNO),(Planet.VEN,Planet.JUP),(Planet.VEN,Planet.URA),(Planet.VEN,Planet.PLU),(Planet.VEN,Planet.NNO),(Planet.JUP,Planet.PLU),(Planet.JUP,Planet.NNO),(Planet.URA,Planet.NNO),(Planet.PLU,Planet.NNO)),
    EventType.MARRIAGE_ENGAGEMENT_FOR_MALE: ((Planet.MON,Planet.MER),(Planet.MON,Planet.VEN),(Planet.MON,Planet.JUP),(Planet.MON,Planet.URA),(Planet.MON,Planet.NNO),(Planet.MER,Planet.VEN),(Planet.MER,Planet.JUP),(Planet.VEN,Planet.MAR),(Planet.VEN,Planet.JUP),(Planet.VEN,Planet.URA),(Planet.VEN,Planet.PLU),(Planet.VEN,Planet.NNO),(Planet.JUP,Planet.URA),(Planet.JUP,Planet.PLU),(Planet.JUP,Planet.NNO),(Planet.URA,Planet.NNO)),
    EventType.MARRIAGE_ENGAGEMENT_FOR_FEMALE: ((Planet.SUN,Planet.MON),(Planet.SUN,Planet.MER),(Planet.SUN,Planet.VEN),(Planet.SUN,Planet.JUP),(Planet.SUN,Planet.URA),(Planet.SUN,Planet.NNO),(Planet.MER,Planet.VEN),(Planet.MER,Planet.JUP),(Planet.MAR,Planet.JUP),(Planet.MAR,Planet.NNO),(Planet.JUP,Planet.URA),(Planet.JUP,Planet.PLU),(Planet.JUP,Planet.NNO),(Planet.URA,Planet.NNO)),
    EventType.CHILDS_MARRIAGE: ((Planet.SUN,Planet.MON),(Planet.SUN,Planet.MER),(Planet.SUN,Planet.VEN),(Planet.SUN,Planet.JUP),(Planet.MON,Planet.MER),(Planet.MON,Planet.VEN),(Planet.MON,Planet.JUP),(Planet.MON,Planet.URA),(Planet.MON,Planet.NNO),(Planet.VEN,Planet.MAR),(Planet.VEN,Planet.JUP),(Planet.VEN,Planet.URA),(Planet.VEN,Planet.PLU),(Planet.VEN,Planet.NNO),(Planet.MAR,Planet.NNO),(Planet.JUP,Planet.URA),(Planet.JUP,Planet.PLU),(Planet.JUP,Planet.NNO)),
    EventType.DIVORCE_SEPARATION: ((Planet.SUN,Planet.SAT),(Planet.MON,Planet.SAT),(Planet.MON,Planet.NEP),(Planet.MER,Planet.SAT),(Planet.VEN,Planet.URA),(Planet.VEN,Planet.NEP),(Planet.VEN,Planet.PLU),(Planet.VEN,Planet.PLU),(Planet.MAR,Planet.JUP),(Planet.MAR,Planet.SAT),(Planet.SAT,Planet.URA),(Planet.SAT,Planet.NNO),(Planet.URA,Planet.PLU),(Planet.NEP,Planet.NNO),(Planet.PLU,Planet.NNO)),
    EventType.DEATH_SON: ((Planet.SUN,Planet.MAR),(Planet.SUN,Planet.SAT),(Planet.SUN,Planet.URA),(Planet.SUN,Planet.NEP),(Planet.SUN,Planet.PLU),(Planet.MER,Planet.MAR),(Planet.MER,Planet.SAT),(Planet.MER,Planet.URA),(Planet.MER,Planet.PLU),(Planet.MER,Planet.NNO),(Planet.MAR,Planet.SAT),(Planet.MAR,Planet.URA),(Planet.MAR,Planet.NEP),(Planet.MAR,Planet.PLU),(Planet.MAR,Planet.NNO),(Planet.JUP,Planet.SAT),(Planet.JUP,Planet.NEP),(Planet.JUP,Planet.PLU),(Planet.JUP,Planet.NNO),(Planet.SAT,Planet.URA),(Planet.SAT,Planet.NEP),(Planet.SAT,Planet.PLU),(Planet.SAT,Planet.NNO),(Planet.URA,Planet.NEP),(Planet.URA,Planet.PLU),(Planet.URA,Planet.NNO),(Planet.NEP,Planet.PLU),(Planet.NEP,Planet.NNO),(Planet.PLU,Planet.NNO)),
    EventType.DEATH_DAUGHTER: ((Planet.MON,Planet.MAR),(Planet.MON,Planet.SAT),(Planet.MON,Planet.URA),(Planet.MON,Planet.NEP),(Planet.MON,Planet.PLU),(Planet.MON,Planet.NNO),(Planet.MER,Planet.MAR),(Planet.MER,Planet.SAT),(Planet.MER,Planet.URA),(Planet.MER,Planet.PLU),(Planet.MER,Planet.NNO),(Planet.VEN,Planet.SAT),(Planet.VEN,Planet.URA),(Planet.VEN,Planet.NEP),(Planet.VEN,Planet.PLU),(Planet.VEN,Planet.NNO),(Planet.MAR,Planet.SAT),(Planet.MAR,Planet.URA),(Planet.MAR,Planet.NEP),(Planet.MAR,Planet.PLU),(Planet.MAR,Planet.NNO),(Planet.JUP,Planet.SAT),(Planet.JUP,Planet.NEP),(Planet.JUP,Planet.PLU),(Planet.JUP,Planet.NNO),(Planet.SAT,Planet.URA),(Planet.SAT,Planet.NEP),(Planet.SAT,Planet.PLU),(Planet.SAT,Planet.NNO),(Planet.URA,Planet.NEP),(Planet.URA,Planet.PLU),(Planet.URA,Planet.NNO),(Planet.NEP,Planet.PLU),(Planet.NEP,Planet.NNO),(Planet.PLU,Planet.NNO)),
    EventType.DEATH_HUSBAND_FRIEND: ((Planet.SUN,Planet.MAR),(Planet.SUN,Planet.SAT),(Planet.SUN,Planet.URA),(Planet.SUN,Planet.NEP),(Planet.SUN,Planet.PLU),(Planet.MER,Planet.MAR),(Planet.MER,Planet.SAT),(Planet.MER,Planet.URA),(Planet.MER,Planet.PLU),(Planet.MER,Planet.NNO),(Planet.MAR,Planet.SAT),(Planet.MAR,Planet.URA),(Planet.MAR,Planet.NEP),(Planet.MAR,Planet.PLU),(Planet.MAR,Planet.NNO),(Planet.JUP,Planet.SAT),(Planet.JUP,Planet.NEP),(Planet.JUP,Planet.PLU),(Planet.JUP,Planet.NNO),(Planet.SAT,Planet.URA),(Planet.SAT,Planet.NEP),(Planet.SAT,Planet.PLU),(Planet.SAT,Planet.NNO),(Planet.URA,Planet.NEP),(Planet.URA,Planet.PLU),(Planet.URA,Planet.NNO),(Planet.NEP,Planet.PLU),(Planet.NEP,Planet.NNO),(Planet.PLU,Planet.NNO)),
    EventType.DEATH_WIFE_FRIEND: ((Planet.MON,Planet.MAR),(Planet.MON,Planet.SAT),(Planet.MON,Planet.URA),(Planet.MON,Planet.NEP),(Planet.MON,Planet.PLU),(Planet.MON,Planet.NNO),(Planet.MER,Planet.MAR),(Planet.MER,Planet.SAT),(Planet.MER,Planet.URA),(Planet.MER,Planet.PLU),(Planet.MER,Planet.NNO),(Planet.VEN,Planet.SAT),(Planet.VEN,Planet.URA),(Planet.VEN,Planet.NEP),(Planet.VEN,Planet.PLU),(Planet.VEN,Planet.NNO),(Planet.MAR,Planet.SAT),(Planet.MAR,Planet.URA),(Planet.MAR,Planet.NEP),(Planet.MAR,Planet.PLU),(Planet.MAR,Planet.NNO),(Planet.JUP,Planet.SAT),(Planet.JUP,Planet.NEP),(Planet.JUP,Planet.PLU),(Planet.JUP,Planet.NNO),(Planet.SAT,Planet.URA),(Planet.SAT,Planet.NEP),(Planet.SAT,Planet.PLU),(Planet.SAT,Planet.NNO),(Planet.URA,Planet.NEP),(Planet.URA,Planet.PLU),(Planet.URA,Planet.NNO),(Planet.NEP,Planet.PLU),(Planet.NEP,Planet.NNO),(Planet.PLU,Planet.NNO)),
    EventType.DEATH_BROTHER: ((Planet.SUN,Planet.MAR),(Planet.SUN,Planet.SAT),(Planet.SUN,Planet.URA),(Planet.SUN,Planet.NEP),(Planet.SUN,Planet.PLU),(Planet.MER,Planet.MAR),(Planet.MER,Planet.SAT),(Planet.MER,Planet.URA),(Planet.MER,Planet.PLU),(Planet.MER,Planet.NNO),(Planet.MAR,Planet.SAT),(Planet.MAR,Planet.URA),(Planet.MAR,Planet.NEP),(Planet.MAR,Planet.PLU),(Planet.MAR,Planet.NNO),(Planet.JUP,Planet.SAT),(Planet.JUP,Planet.NEP),(Planet.JUP,Planet.PLU),(Planet.JUP,Planet.NNO),(Planet.SAT,Planet.URA),(Planet.SAT,Planet.NEP),(Planet.SAT,Planet.PLU),(Planet.SAT,Planet.NNO),(Planet.URA,Planet.NEP),(Planet.URA,Planet.PLU),(Planet.URA,Planet.NNO),(Planet.NEP,Planet.PLU),(Planet.NEP,Planet.NNO),(Planet.PLU,Planet.NNO)),
    EventType.DEATH_SISTER: ((Planet.MON,Planet.MAR),(Planet.MON,Planet.SAT),(Planet.MON,Planet.URA),(Planet.MON,Planet.NEP),(Planet.MON,Planet.PLU),(Planet.MON,Planet.NNO),(Planet.MER,Planet.MAR),(Planet.MER,Planet.SAT),(Planet.MER,Planet.URA),(Planet.MER,Planet.PLU),(Planet.MER,Planet.NNO),(Planet.VEN,Planet.SAT),(Planet.VEN,Planet.URA),(Planet.VEN,Planet.NEP),(Planet.VEN,Planet.PLU),(Planet.VEN,Planet.NNO),(Planet.MAR,Planet.SAT),(Planet.MAR,Planet.URA),(Planet.MAR,Planet.NEP),(Planet.MAR,Planet.PLU),(Planet.MAR,Planet.NNO),(Planet.JUP,Planet.SAT),(Planet.JUP,Planet.NEP),(Planet.JUP,Planet.PLU),(Planet.JUP,Planet.NNO),(Planet.SAT,Planet.URA),(Planet.SAT,Planet.NEP),(Planet.SAT,Planet.PLU),(Planet.SAT,Planet.NNO),(Planet.URA,Planet.NEP),(Planet.URA,Planet.PLU),(Planet.URA,Planet.NNO),(Planet.NEP,Planet.PLU),(Planet.NEP,Planet.NNO),(Planet.PLU,Planet.NNO)),
    EventType.DEATH: ((Planet.SUN,Planet.MAR),(Planet.SUN,Planet.SAT),(Planet.SUN,Planet.URA),(Planet.SUN,Planet.NEP),(Planet.SUN,Planet.PLU),(Planet.MON,Planet.MAR),(Planet.MON,Planet.SAT),(Planet.MON,Planet.NEP),(Planet.MON,Planet.PLU),(Planet.MER,Planet.MAR),(Planet.MAR,Planet.SAT),(Planet.MAR,Planet.PLU),(Planet.MAR,Planet.NNO),(Planet.SAT,Planet.URA),(Planet.SAT,Planet.NEP),(Planet.SAT,Planet.PLU),(Planet.URA,Planet.NEP),(Planet.NEP,Planet.PLU),(Planet.NEP,Planet.NNO),(Planet.PLU,Planet.NNO)),
    EventType.ASSASINATION_SUICIDE: ((Planet.SUN,Planet.MAR),(Planet.SUN,Planet.SAT),(Planet.SUN,Planet.URA),(Planet.SUN,Planet.NEP),(Planet.SUN,Planet.PLU),(Planet.MON,Planet.MAR),(Planet.MON,Planet.SAT),(Planet.MON,Planet.NEP),(Planet.MON,Planet.PLU),(Planet.MER,Planet.MAR),(Planet.MAR,Planet.SAT),(Planet.MAR,Planet.PLU),(Planet.MAR,Planet.NNO),(Planet.SAT,Planet.URA),(Planet.SAT,Planet.NEP),(Planet.SAT,Planet.PLU),(Planet.URA,Planet.NEP),(Planet.NEP,Planet.PLU),(Planet.NEP,Planet.NNO),(Planet.PLU,Planet.NNO)),
    EventType.PROMOTION_JOB: ((Planet.SUN,Planet.MON),(Planet.SUN,Planet.MER),(Planet.SUN,Planet.VEN),(Planet.SUN,Planet.JUP),(Planet.SUN,Planet.URA),(Planet.MON,Planet.MER),(Planet.MON,Planet.VEN),(Planet.MON,Planet.JUP),(Planet.MON,Planet.URA),(Planet.MER,Planet.VEN),(Planet.MER,Planet.JUP),(Planet.MER,Planet.URA),(Planet.MER,Planet.PLU),(Planet.VEN,Planet.URA),(Planet.VEN,Planet.PLU),(Planet.VEN,Planet.NNO),(Planet.MAR,Planet.JUP),(Planet.JUP,Planet.SAT),(Planet.JUP,Planet.URA),(Planet.JUP,Planet.PLU),(Planet.JUP,Planet.NNO)),
    EventType.RESIGN_RETIRE: ((Planet.MON,Planet.SAT),(Planet.MON,Planet.PLU),(Planet.MON,Planet.NNO),(Planet.MER,Planet.SAT),(Planet.VEN,Planet.NEP),(Planet.MAR,Planet.JUP),(Planet.MAR,Planet.URA),(Planet.JUP,Planet.NEP),(Planet.SAT,Planet.NEP),(Planet.SAT,Planet.PLU),(Planet.URA,Planet.NEP),(Planet.URA,Planet.PLU),(Planet.NEP,Planet.PLU)),
    EventType.MOBILIZATION: (EventType.FAILURE_DEFEATED),
    EventType.DEMOBILIZATION_RELEASE: (EventType.SUCCESS_ELECTED),
    EventType.ACCIDENT: ((Planet.SUN,Planet.MAR),(Planet.SUN,Planet.SAT),(Planet.SUN,Planet.NEP),(Planet.SUN,Planet.PLU),(Planet.MON,Planet.MAR),(Planet.MON,Planet.SAT),(Planet.MON,Planet.NEP),(Planet.MON,Planet.PLU),(Planet.MON,Planet.NNO),(Planet.MER,Planet.MAR),(Planet.MER,Planet.SAT),(Planet.MER,Planet.URA),(Planet.MER,Planet.NEP),(Planet.VEN,Planet.NEP),(Planet.MAR,Planet.SAT),(Planet.MAR,Planet.NEP),(Planet.MAR,Planet.PLU),(Planet.MAR,Planet.NNO),(Planet.SAT,Planet.NEP),(Planet.SAT,Planet.PLU),(Planet.SAT,Planet.NNO),(Planet.URA,Planet.NNO)),
    EventType.HOSPITALIZATION_ILLNESS: ((Planet.SUN,Planet.MON),(Planet.SUN,Planet.MER),(Planet.SUN,Planet.MAR),(Planet.SUN,Planet.SAT),(Planet.SUN,Planet.URA),(Planet.SUN,Planet.NEP),(Planet.SUN,Planet.PLU),(Planet.SUN,Planet.NNO),(Planet.MON,Planet.MER),(Planet.MON,Planet.MAR),(Planet.MON,Planet.SAT),(Planet.MON,Planet.NEP),(Planet.MON,Planet.PLU),(Planet.MER,Planet.MAR),(Planet.MER,Planet.SAT),(Planet.MER,Planet.NEP),(Planet.VEN,Planet.MAR),(Planet.VEN,Planet.SAT),(Planet.VEN,Planet.NEP),(Planet.MAR,Planet.SAT),(Planet.MAR,Planet.NEP),(Planet.MAR,Planet.PLU),(Planet.MAR,Planet.NNO),(Planet.JUP,Planet.NEP),(Planet.SAT,Planet.NEP),(Planet.SAT,Planet.PLU),(Planet.SAT,Planet.NNO),(Planet.URA,Planet.NEP),(Planet.URA,Planet.PLU),(Planet.NEP,Planet.PLU)),
    EventType.VIOLENCE: (EventType.ACCIDENT),
    EventType.INTRIGUE: (EventType.FAILURE_DEFEATED),
    EventType.GAMBLING_LOSS: (EventType.LOSSES),
    EventType.GAMBLING_GAIN: ((Planet.SUN,Planet.JUP),(Planet.VEN,Planet.JUP),(Planet.JUP,Planet.URA)),
    EventType.ARMY_PROMOTION: ((Planet.MER,Planet.MAR),(Planet.SUN,Planet.MAR),(Planet.MON,Planet.MAR))
}

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
