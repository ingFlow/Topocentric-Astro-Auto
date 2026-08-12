"""
webapp/reserve/custom_action_prototype.py - NEW in Phase 8. The
'/custom_action' route, relocated here from the former monolithic
app.py, per the migration plan's Phase 8 task 9.

WHAT THIS IS
    Accepts arbitrary JSON via POST and echoes it back in a message
    string. Per the Developer Manual (Section 7.1), this route is
    confirmed "Dead": no frontend code anywhere in templates/ or static/
    calls it (confirmed by search - zero references). Its most plausible
    counterpart is templates/inf.html's `customAction()` JavaScript
    function - a standalone prototype of a custom right-click context
    menu that is itself never rendered by any route (`render_template()`
    is called exactly once anywhere in the codebase, always with
    'index.html') - but that connection is circumstantial, not confirmed.
    The intended wiring between the two was, per the Developer Manual's
    own account, simply never completed.

WHY THIS IS PRESERVED, NOT DELETED
    Per the migration plan's own rule (Section 2.1): a function/route is
    only a deletion candidate if it is (a) genuine duplication of
    something else already active, or (b) pure mechanism tied to an
    architectural pattern itself being removed. '/custom_action' is
    neither - it's a small, complete, self-contained, real Flask route
    that happens to have zero current callers. That makes it exactly the
    kind of thing this migration preserves and relocates to an honestly-
    labeled home, not deletes.

WHY THIS IS NOT MOUNTED BY DEFAULT
    Since it has no known current use and no confirmed intended
    caller, webapp/app_factory.py's create_app() does NOT register this
    blueprint by default - matching the same "working-but-not-currently-
    mounted" treatment given to the reserved kerykeion charting blueprint
    (see webapp/reserve/charting_kerykeion/). A future caller who
    determines a real use for this endpoint (e.g. finishing the
    inf.html context-menu prototype it may have been intended to serve)
    can register it explicitly:

        from topo_astro.webapp.app_factory import create_app
        from topo_astro.webapp.reserve.custom_action_prototype import custom_action_bp
        app = create_app()
        app.register_blueprint(custom_action_bp)

Function body copied verbatim from the original app.py - no logic
changed, only its location and how it's exposed (a Blueprint instead of
a direct @app.route decorator on the monolithic app object).
"""
from flask import Blueprint, jsonify, request

custom_action_bp = Blueprint('custom_action', __name__)


@custom_action_bp.route('/custom_action', methods=['POST'])
def custom_action():
    data = request.get_json()
    selected_text = data.get('selected_text')
    left_item = data.get('left_item')
    right_item = data.get('right_item')
    right_radio = data.get('right_radio')

    # Process received data as needed
    message = f"Received text: {selected_text}, Left Item: {left_item}, Right Item: {right_item}, Radio Value: {right_radio}"
    return jsonify({"message": message})