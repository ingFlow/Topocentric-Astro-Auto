"""
webapp/reserve/charting_kerykeion/routes.py - NEW in Phase 8. The working
kerykeion-based server-side chart-rendering route ('/generate_chart'),
relocated here per the migration plan's Phase 8 task 5 and the Phase 11
"keep kerykeion, remove astrochart.js" decision (see Phase 11's decision
table).

WHAT CHANGED VS. THE ORIGINAL app.py
    The original app.py's '/generate_chart' route had its actual SVG-
    generation call - the AstrologicalSubject(...) construction and the
    KerykeionChartSVG(...).makeSVG() call - sitting inside a triple-quoted
    string, i.e. present in the file but never executed (Developer Manual
    Section 7.1: "the actual AstrologicalSubject / KerykeionChartSVG
    generation call is entirely commented out - the route currently does
    not produce a chart"). Per Phase 8 task 5, that block has been
    UNCOMMENTED here - turned from an inert string into real, executing
    code - along with its corresponding
    `from kerykeion import AstrologicalSubject, KerykeionChartSVG` import
    (previously also commented out at the top of app.py). Every other
    line of this route - the chart_datetime/chart_pos/technique/event_info
    parsing, the SRA/LUNAR/TRANSIT event-geopos-substitution branch, the
    svg_full_path/svg_path filename construction - is copied verbatim
    from the original, unchanged.

    get_timezone_name_from_pos is still commented out at its one call
    site (`#timezone_name = get_timezone_name_from_pos(chart_pos)`) below,
    exactly as in the original - that computed value was never actually
    used by anything even in the original file (the variable was
    assigned and never read again), so uncommenting the assignment alone,
    without a real consumer for its result, would not be a meaningful
    restoration of function; it is left commented, matching the original
    behavior exactly. If a future caller wants to actually use the
    timezone name (e.g. to pass tz_str= something other than the
    hardcoded "UTC" below), webapp/reserve/timezone_name_lookup.py's
    get_timezone_name_from_pos is already a complete, working utility -
    see that module's own docstring.

WHY THIS BLUEPRINT IS NOT REGISTERED BY DEFAULT
    Per the migration plan (Phase 8 task 5): this is "a working-but-not-
    currently-mounted Flask blueprint (i.e., real, callable code, just
    not registered on the app factory by default)". webapp/app_factory.py's
    create_app() does NOT import or register kerykeion_chart_bp - a
    caller who wants to reactivate server-side chart rendering must do so
    explicitly:

        from topo_astro.webapp.app_factory import create_app
        from topo_astro.webapp.reserve.charting_kerykeion.routes import kerykeion_chart_bp
        app = create_app()
        app.register_blueprint(kerykeion_chart_bp)

    This mirrors exactly what the migration plan's own Phase 8 validation
    checklist asks for: "webapp/reserve/charting_kerykeion/routes.py
    imports cleanly and, run directly (not through the main app),
    successfully generates an SVG for a test input - confirming the 'it
    worked' claim is still true after relocation, before this code goes
    dormant again."

WHY THIS STILL ISN'T THE FULL PICTURE (see README.md in this same folder)
    Per the Developer Manual's Section 12.3, this kerykeion-based approach
    "technically worked but didn't produce the visual result you wanted" -
    it is real, callable, working code (confirmed importable and callable
    here), but reactivating it is a deliberate future decision, not
    something this migration silently re-enables by default.

A NOTE ON WHAT COULD NOT BE VERIFIED IN THIS PASS
    kerykeion is not installed in this migration's sandbox (nor is it
    listed in requirements.txt/setup.sh, per Phase 1's dependency
    manifest, since the original app never depended on it at runtime -
    only this now-reactivated reserved code does). This file has been
    checked for syntactic correctness and the exact preservation of every
    line from the original inert block, but an actual live
    AstrologicalSubject/KerykeionChartSVG round-trip could not be executed
    in this environment. If you plan to actually mount and use this
    blueprint, add `kerykeion` to your own environment's dependencies
    first (it is intentionally NOT added to the shared requirements.txt,
    since this blueprint is reserved/opt-in, not part of the app's
    default active surface) and confirm the import at the top of this
    file resolves before registering the blueprint.
"""
import os
from datetime import datetime

from flask import Blueprint, current_app, request, send_from_directory
from kerykeion import AstrologicalSubject, KerykeionChartSVG

from topo_astro.core.constants import aTechniqueType

kerykeion_chart_bp = Blueprint('kerykeion_chart', __name__)


@kerykeion_chart_bp.route('/generate_chart')
def generate_chart():
    state = current_app.state

    chart_datetime = request.args.get('chart_datetime', default=state.dt_radix)
    chart_pos = request.args.get('chart_pos', default=state.geo_pos_natal)
    technique = int(request.args.get('right_radio', ''))
    event_info = request.args.get('right_item', '').split(', ')

    try:
        event_locstr = [event_info[3][1:],event_info[4],event_info[5][:-1]]
        event_pos = [float(i) for i in event_locstr]
    except:
        event_pos = chart_pos
    
    if chart_datetime != state.dt_radix:
        try:
            chart_datetime = datetime.fromisoformat(chart_datetime)
        except ValueError:
            try:
                chart_datetime = datetime.strptime(chart_datetime, "%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                try:
                    chart_datetime = datetime.strptime(chart_datetime, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    return None # 

    if technique in [aTechniqueType.SRA, aTechniqueType.LUNAR, aTechniqueType.TRANSIT] and chart_pos == state.geo_pos_natal:
        chart_pos = [event_pos[0],event_pos[1]]
    
    #timezone_name = get_timezone_name_from_pos(chart_pos)
    filename = f'{chart_datetime.strftime("%Y-%m-%d %H_%M_%S")}'    
    svg_full_path = f"static/charts/{filename} - Natal Chart.svg"
    svg_path = f"{filename} - Natal Chart.svg" 
    
    chart_subject = AstrologicalSubject(
        filename,
        chart_datetime.year,
        chart_datetime.month,
        chart_datetime.day,
        chart_datetime.hour,
        chart_datetime.minute,
        chart_datetime.second,  
        lng=chart_pos[1],
        lat=chart_pos[0],
        tz_str="UTC",
        houses_system_identifier="T"
    )
    
    date_natal_chart = KerykeionChartSVG(chart_subject, theme="dark-high-contrast", new_output_directory="static/charts")
    date_natal_chart.makeSVG()

    if os.path.exists(svg_full_path):
        return send_from_directory('static/charts', svg_path) 
    else:
        return "File not found", 404