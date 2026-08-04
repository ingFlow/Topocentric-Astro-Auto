"""
significators/rules_data.py - the hand-curated significator research
tables that drive the entire rectification/scoring system: which
houses, planets, and specific planet-pairs are considered thematically
relevant to each life-event category.

Relocated here (Phase 5 of the migration plan) from
techniques/primary_directions/technique.py, where this data used to live
despite being reused by five of the seven techniques (Primary Directions,
Secondary, Transit, SRA, Harmonics), not specific to Primary Directions.
This move is a pure data relocation - every dict/class below is copied
verbatim, character-for-character, from its previous location. No values,
keys, or structure have been altered.

Contents:
    - Planet: three-letter planet-code constants used as dict keys
      throughout the tables below.
    - EventType: the ~50 life-event categories every rectification run is
      tested against. A comment above the class (preserved from the
      original) states these values "correspond to the POLARIS event
      list" - see the Developer Manual's Glossary entry on POLARIS for
      what little is known about that external reference.
    - AspectType: NOT an astrological aspect descriptor - a
      scoring-granularity enum controlling which acceptance/scoring rule
      applies (see significators/scoring.py).
    - GoodBadFlag: GOOD/BAD/NEUTRAL - whether an event's significators are
      read as favorable, unfavorable, or neutral when matching aspect
      polarity (conjunction/trine/sextile vs. square/opposition).
    - PRIMARY_RULES: EventType -> (relevant_houses, relevant_planets,
      GoodBadFlag) - the coarse "which houses/planets are thematically
      relevant at all" table.
    - SECONDARY_RULES: EventType -> (relevant_houses, relevant_planets) -
      the equivalent table used for the Secondary Progressions technique
      (no GoodBadFlag; less strict than PRIMARY_RULES by design).
    - PLANETARY_COMBO: EventType -> specific two-planet pairs considered
      meaningful for that event - a more granular table than
      PRIMARY_RULES/SECONDARY_RULES. Several entries alias or extend
      another EventType's list instead of repeating it (e.g.
      TRAVEL_OVERSEAS_POSITIVE = TRAVEL_POSITIVE's list + one extra pair;
      ARREST is a pure alias for FAILURE_DEFEATED's list) - this
      compression scheme is why significators/scoring.py's
      is_acceptable_planet_combo() has to branch on four different
      possible shapes of a PLANETARY_COMBO value.

This module has no dependency on significators/scoring.py or on any
technique module - it is pure, inert data, imported by scoring.py and
(for EventType/AspectType only) by batch/entrypoints.py.

Maintenance note: these tables are the hand-curated research core of the
project (see the Developer Manual's Section 8, "The Significator &
Scoring System") - they encode real, tested astrological methodology, not
disposable configuration. They should not be edited casually.
"""


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