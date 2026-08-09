"""
techniques/base.py - NEW in Phase 6. The shared technique-construction
dispatcher: one function, construct_technique(), that knows how to
instantiate any of the seven technique classes given a radix/event pair,
replacing the two near-identical, independently-maintained branching
chains that used to live directly inside webapp/app.py's update_content
route and batch/grid_engine.py's append_grid_acceptable_angles.

WHAT THIS MODULE IS AND IS NOT
    This dispatcher's job is CONSTRUCTION ONLY - it does not impose a
    uniform accessor API on its result. The five techniques that
    genuinely share a shape (Primary Directions, Secondary, PSSR,
    Transit, SRA - see each of their own modules for the additive
    get_aspects()/get_info() wrappers added earlier in this phase) can be
    read uniformly by the caller once construct_technique() hands one
    back. Harmonics and Lunar cannot, and this dispatcher does not
    pretend otherwise: it returns their real objects unchanged, and the
    caller is expected to branch explicitly for them afterward - exactly
    as both original call sites already had to, just consolidated from
    two duplicated blocks into one.

WHY HARMONICS AND LUNAR ARE NOT PART OF THE UNIFORM FIVE
    (Reasoning below is a summary of what techniques/harmonics.py's and
    techniques/lunars.py's own module docstrings establish in full - see
    those files for the complete argument; this is not new reasoning
    invented for this module.)

    Harmonics_Auto.get_str_aspects() returns a SINGLE aspect string, not
    a (direct, converse) pair. This is not a gap - a harmonic chart is
    one derived chart (each radix planet's degree multiplied by years
    elapsed since birth), compared against the radix exactly once.
    Classical harmonic technique has no natural "converse" the way
    arc-based techniques (Primary Directions, Secondary Progressions) do.
    There is no second, inverse harmonic calculation anywhere in that
    class to unify with anything.

    Lunar_Auto.get_all_lunars()/get_info() are shaped the way they are
    because ONE Lunar_Auto instantiation computes THREE lunar sub-charts
    internally (LunarType.LUNAR, KINETIC, AS_LUNAR), each of which can
    itself expand into a direct/demi-direct/converse/demi-converse
    variant - a fundamentally different computation pattern from the
    other six techniques, which each compute exactly one calculation per
    instantiation. Lunar_Auto happens to already have a method literally
    named get_info() (a pre-existing naming coincidence, not evidence it
    belongs in the uniform five) but its return shape - a dict keyed by
    lunar-type, each value itself a sub-dict of 1-4 charts - is
    structurally incompatible with the other five techniques' flat,
    single-calculation info dict. Forcing Lunar or Harmonics into the
    uniform two-method shape would misrepresent what they actually
    return, which is exactly the mistake Phase 6 is careful not to make
    (see the migration plan's own framing of this, Phase 6 rationale).

CONSTRUCTOR-SHAPE DIFFERENCES THIS DISPATCHER ABSORBS
    Verified directly against both pre-Phase-6 call sites
    (webapp/app.py's update_content, batch/grid_engine.py's
    append_grid_acceptable_angles) before writing this dispatcher - the
    two call sites use IDENTICAL constructor argument shapes for all
    five uniform techniques; the only differences between them were
    local-variable naming (geo_pos_natal vs geopos_natal for the same
    natal geopos value; event_geopos vs geopos for the same per-event
    geopos value), not different argument shapes. This dispatcher takes
    the union of what both call sites needed as named parameters:

    - PD:        (jd_radix, jd_event, geopos_natal, rad_planets,
                   rad_planets_equatorial, rad_houses_info, e)
                 - takes a Julian Day radix, and rad_planets_equatorial/
                   rad_houses_info precomputed (both call sites already
                   compute these once per radix, ahead of the per-
                   technique branch, so they're passed in rather than
                   recomputed here).
    - Secondary: (jd_radix, jd_event, geopos_natal, e, ramc,
                   rad_planets)
                 - Secondary_Auto is the one technique that takes
                   geo_lat/geo_long as two separate floats rather than a
                   combined geopos - this dispatcher still accepts a
                   single geopos_natal list and unpacks it at the call
                   site inside construct_technique(), so callers don't
                   need to know about that quirk.
    - PSSR:      (dt_radix, dt_event, rad_planets)
                 - takes a Python datetime radix (not JD) - both original
                   call sites pass julian.from_jd(jd_radix) here, so this
                   dispatcher takes dt_radix directly and expects the
                   caller to already have it (both callers do, since they
                   parse an ISO radix string into a datetime before ever
                   computing jd_radix). No geopos parameter is threaded
                   through to PSSR_Auto's constructor, since both
                   original call sites always supply rad_planets and
                   never rely on PSSR_Auto's internal geopos fallback.
    - Transit:   (jd_radix, jd_event, geopos_event, rad_planets)
                 - the ONE uniform technique that uses the EVENT's
                   geopos, not the natal one. This is a real, load-
                   bearing distinction in the original code (app.py's
                   `event_geopos`, grid_engine.py's per-event `geopos`
                   from the event tuple) - this dispatcher keeps it as
                   its own explicit parameter (geopos_event) rather than
                   silently reusing geopos_natal, so a caller cannot
                   accidentally collapse the two.
    - SRA:       (dt_radix, dt_event, geopos_natal, rad_planets)
                 - like PSSR, takes a Python datetime radix, not JD.
                   Uses the natal geopos (both original call sites do).

    None of these per-technique argument shapes were changed by this
    dispatcher - they are reproduced exactly, just centralized. A caller
    who was passing the "wrong" geopos to Transit before this phase would
    still be doing so after it; this dispatcher does not silently fix or
    normalize any of the pre-existing per-technique quirks documented
    above (see Developer Manual Section 6, "the constructors are not
    uniform" table, and Section 13.8).
"""
from topo_astro.techniques.primary_directions.technique import PD_Automate
from topo_astro.techniques.secondary_progressions import Secondary_Auto
from topo_astro.techniques.pssr import PSSR_Auto
from topo_astro.techniques.transits import Transit_Auto
from topo_astro.techniques.sra import SRA_Auto
from topo_astro.core.constants import aTechniqueType

import julian


# The five techniques this dispatcher can construct via the uniform path.
# Harmonics and Lunar are deliberately NOT in this set - see module
# docstring. A caller asking construct_technique() for Harmonics or Lunar
# gets a clear error rather than a silently wrong result; those two
# techniques must still be constructed directly by the caller, exactly as
# both original call sites already did.
UNIFORM_TECHNIQUES = frozenset({
    aTechniqueType.PRIMARY_DIRECT,
    aTechniqueType.SECONDARY_DIRECT,
    aTechniqueType.PSSR,
    aTechniqueType.TRANSIT,
    aTechniqueType.SRA,
})


def construct_technique(
    technique,
    jd_radix,
    jd_event,
    dt_radix,
    dt_event,
    geopos_natal,
    geopos_event,
    rad_planets,
    rad_planets_equatorial=None,
    rad_houses_info=None,
    e=None,
    ramc=None,
):
    """Construct and return one of the five uniform technique objects
    (PD_Automate, Secondary_Auto, PSSR_Auto, Transit_Auto, SRA_Auto) for
    a given radix/event pair, replacing the near-identical per-technique
    branching that used to be duplicated in webapp/app.py's
    update_content and batch/grid_engine.py's append_grid_acceptable_angles.

    Does NOT handle Harmonics or Lunar (see module docstring for why) -
    raises ValueError if asked to. Callers must continue to construct
    Harmonics_Auto/Lunar_Auto directly, exactly as before this phase.

    Parameters:
        technique (int): one of the aTechniqueType values. Must be one
            of PRIMARY_DIRECT, SECONDARY_DIRECT, PSSR, TRANSIT, SRA - see
            UNIFORM_TECHNIQUES.
        jd_radix (float): the radix Julian Day. Required by PD, Secondary.
        jd_event (float): the event Julian Day. Required by PD, Secondary.
        dt_radix (datetime): the radix as a Python datetime. Required by
            PSSR, SRA (both take a datetime radix, not a JD - see module
            docstring).
        dt_event (datetime): the event as a Python datetime. Required by
            PSSR, SRA.
        geopos_natal (list): [lat, lon, alt] of the birth location.
            Required by PD, Secondary, SRA.
        geopos_event (list): [lat, lon, alt] of the EVENT's location (not
            necessarily the same as geopos_natal). Required by Transit
            only - see module docstring for why this is its own
            parameter rather than reusing geopos_natal.
        rad_planets (list): precomputed radix planet/house/POF positions
            (calc_planets_pof_houses_labelled's output). Required by all
            five.
        rad_planets_equatorial (list, optional): precomputed equatorial
            radix planet positions. Required by PD only.
        rad_houses_info (tuple, optional): precomputed swe.houses() radix
            output. Required by PD, Secondary (Secondary reads RAMC out
            of this via rad_houses_info[1][2] if ramc isn't given
            directly).
        e (float, optional): obliquity at the event date. Required by PD,
            Secondary.
        ramc (float, optional): radix RAMC. Required by Secondary. If not
            given, Secondary_Auto derives it internally from
            rad_houses_info[1][2] the same way the original call sites
            did (see Secondary_Auto's own constructor).

    Returns:
        One of PD_Automate, Secondary_Auto, PSSR_Auto, Transit_Auto,
        SRA_Auto - already fully constructed for this radix/event pair.
        Call .get_aspects()/.get_info() (or the original
        get_aspects_str()/get_str_aspects()/get_extended_information()/
        get_dict_info()/get_info() names - both remain available, see
        each technique module's own Phase 6 note) on the result.
    """
    if technique not in UNIFORM_TECHNIQUES:
        raise ValueError(
            f"construct_technique() does not handle technique={technique!r} "
            f"(Harmonics and Lunar are deliberately excluded - construct "
            f"Harmonics_Auto/Lunar_Auto directly; see this module's docstring)."
        )

    if technique == aTechniqueType.PRIMARY_DIRECT:
        return PD_Automate(
            jd_radix,
            jd_event,
            geopos_natal,
            rad_planets,
            rad_planets_equatorial,
            rad_houses_info,
            e,
        )

    if technique == aTechniqueType.SECONDARY_DIRECT:
        derived_ramc = ramc if ramc is not None else rad_houses_info[1][2]
        return Secondary_Auto(
            jd_radix,
            jd_event,
            geopos_natal[0],
            geopos_natal[1],
            e,
            derived_ramc,
            rad_planets,
        )

    if technique == aTechniqueType.PSSR:
        return PSSR_Auto(
            dt_radix,
            dt_event,
            rad_planets,
        )

    if technique == aTechniqueType.TRANSIT:
        return Transit_Auto(
            jd_radix,
            jd_event,
            geopos_event,
            rad_planets,
        )

    if technique == aTechniqueType.SRA:
        return SRA_Auto(
            dt_radix,
            dt_event,
            geopos_natal,
            rad_planets,
        )