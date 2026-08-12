"""
webapp/app_factory.py - NEW in Phase 8. The Flask application factory,
replacing the former module-level `app = Flask(__name__)` in the old
monolithic app.py.

create_app() builds the Flask app, attaches one AppState instance (see
state.py) as app.state, and registers the three surviving active-route
blueprints (main, content, selections - see webapp/routes/) at their
original, unprefixed paths, so every existing fetch() call in
templates/index.html continues to work unchanged.

The reserved kerykeion charting blueprint (webapp/reserve/
charting_kerykeion/routes.py) and the reserved /custom_action route
(webapp/reserve/custom_action_prototype.py) are DELIBERATELY NOT
registered here by default - per the migration plan's Phase 8 task 5,
they are "working-but-not-currently-mounted" blueprints, real and
importable, but not part of the app's default active surface. A future
caller who wants to reactivate either can import and register them
explicitly; see each reserved module's own docstring for how.

Routes deleted entirely in this phase (not relocated, not reserved -
gone, per the migration plan's explicit kerykeion-keep/astrochart.js-
remove decision): '/chart-data' (returned only hardcoded placeholder
data with no real caller) and the vendored static/js/astrochart.js file
it existed to feed. See webapp/routes/main.py's docstring and this
package's CHANGES notes for the full accounting of what was deleted vs.
relocated vs. kept.
"""
import logging
import os

from flask import Flask

from topo_astro.webapp.state import AppState
from topo_astro.webapp.routes.main import main_bp
from topo_astro.webapp.routes.content import content_bp
from topo_astro.webapp.routes.selections import selections_bp


def create_app():
    """Build and return a fully-configured Flask app instance.

    Returns:
        Flask: the app, with app.state set to a fresh AppState() and the
        main/content/selections blueprints registered at their original
        unprefixed paths ('/', '/update_content', '/update_selection',
        '/save_data').
    """
    logging.basicConfig(level=logging.INFO)

    app = Flask(__name__)
    app.secret_key = 'toposecret'

    # Phase 7: one explicit, process-lifetime state object replaces the
    # six former module-level globals (geo_pos_natal, dt_radix, lunar_orb,
    # restrict_orb, current_file, selections_data). See state.py's own
    # docstring for the full field-by-field mapping and rationale.
    app.state = AppState()

    app.register_blueprint(main_bp)
    app.register_blueprint(content_bp)
    app.register_blueprint(selections_bp)
    
    # WHEN WIRING KERYKEION
    # app.register_blueprint(custom_action_bp)
    # app.register_blueprint(kerykeion_chart_bp)

    return app


def _ensure_data_input_dir_exists():
    """Startup check, preserved from the original app.py's
    `if __name__ == '__main__':` block: verify data_input/ exists before
    serving, exiting with an error if not. Kept as its own function so
    the app-factory pattern doesn't force this check to run on every
    import (only when this module is actually run as the entry point -
    see the bottom of this file)."""
    from topo_astro.core.constants import DATA_INPUT_DIR
    if not os.path.isdir(DATA_INPUT_DIR):
        logging.error(f"Data input directory '{DATA_INPUT_DIR}' not found.")
        exit(1)


if __name__ == '__main__':
    _ensure_data_input_dir_exists()

    # Preserved from the original: static/charts/ is created on startup if
    # missing, even though nothing in the active route surface currently
    # writes into it (chart generation lives only in the reserved,
    # not-mounted-by-default kerykeion blueprint - see
    # webapp/reserve/charting_kerykeion/). Kept as dormant startup
    # behavior, matching the original exactly, rather than removed, since
    # removing it would be a behavior change beyond this phase's scope.
    charts_dir = 'static/charts'
    os.makedirs(charts_dir, exist_ok=True)

    logging.info("Starting Flask application...")
    app = create_app()
    app.run(debug=True, port=5000)