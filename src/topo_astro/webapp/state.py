"""
webapp/state.py - NEW in Phase 7. The explicit state container replacing
webapp/app.py's former module-level globals (geo_pos_natal, dt_radix,
lunar_orb, restrict_orb, current_file, selections_data).

WHY THIS EXISTS AND WHAT IT DOES NOT CHANGE
    The pre-Phase-7 app.py held six bare module globals, mutated by routes
    via the `global` keyword. Per the Developer Manual (Section 6.15) this
    was "an intentional-enough simplification given this is a single-user,
    single-process tool" - and the migration plan's Phase 7 rationale is
    explicit that removing the globals is about making the code
    independently testable and eliminating "forgot to reset between runs"
    failure modes BY CONSTRUCTION, not about changing the app's actual
    concurrency model. This module does NOT introduce per-request or
    per-session scoping, Flask sessions, or any kind of multi-user
    isolation - AppState is instantiated exactly ONCE by the app factory
    (see app_factory.py) and lives for the lifetime of the running process,
    exactly as the six module globals did before this phase. The only
    thing that has changed is HOW routes reach these values: explicitly,
    through one object (retrieved via flask.current_app), instead of
    implicitly, through `global` statements scattered across the module.

WHAT EACH FIELD IS AND WHERE IT CAME FROM
    - geo_pos_natal (list): [lat, lon, alt] of the currently-loaded
      person's birth location. Set once per '/' request (main blueprint's
      home()); read by the content blueprint's update_content() and by
      the reserved kerykeion charting code.
    - dt_radix (datetime | None): the currently-loaded person's
      "best-known" birth datetime (dt_actual_dob). Set once per '/'
      request; read as a query-parameter default by the reserved
      kerykeion charting code's generate_chart() route.
    - lunar_orb (int): the Lunar technique's orb setting, default 9.
      Never reassigned anywhere in the original code (there is no route
      or form control that changes it) - kept here rather than as a bare
      module constant only so every value update_content() reads lives in
      one consistent place; its value truly is fixed for the process
      lifetime, same as before.
    - restrict_orb (int): the orb-restriction value, default 3,
      REASSIGNED on every '/update_content' request from the
      'orb_input' query parameter (see content.py). This is the one field
      that behaves like a live, frequently-mutated setting rather than a
      one-time-per-file value - preserved exactly as such.
    - current_file (str): the basename of the currently-loaded
      data_input/*.json file, default "ing tea.json". Set from the
      '?filename=' query parameter on '/' requests; read by
      update_content() and save_data() to build saved_selections/*.txt
      paths.
    - selections_data (dict): the in-memory cache of parsed/edited
      selection data, keyed by radix-date ISO string. THIS is the one
      value Phase 7's own task list calls out by name as needing to
      "outlive a single request" - kept here as a single, explicitly-
      documented cache with a clear, explicit lifetime (the AppState
      instance's lifetime, i.e. the running process), exactly matching
      the original global's actual behavior. Populated lazily: on
      cache-miss, update_content() falls back to
      persistence.selections.parse_selection_file() to read an
      on-disk saved_selections/*.txt file, then writes the result back
      into this cache (see content.py).

reset_globals(), formerly defined in app.py, is NOT reproduced here.
Per the migration plan (Phase 7 rationale, and MIGRATION_MANUAL_V2.md
Section 2.1(b)): reset_globals() was pure mechanism tied directly to the
module-global pattern this phase removes - "once the values it resets are
no longer module globals, there is nothing left to reset." It was also
already confirmed dead code (Developer Manual Section 12.1: "Defined to
reset the module's global state variables; never called by any route.")
before this phase, so its removal loses no reachable behavior. If a
future caller genuinely needs to reset an AppState instance, a fresh
AppState() can simply be constructed - there is no special reset
procedure to write, since ordinary Python object construction already
does exactly that.
"""


class AppState:
    """Single, explicit, process-lifetime state container for the
    interactive Flask app. Instantiated exactly once by
    app_factory.create_app() and attached to the Flask app object; routes
    reach it via flask.current_app.state (see any of the route blueprints
    for the exact access pattern)."""

    def __init__(self):
        self.geo_pos_natal = []
        self.dt_radix = None
        self.lunar_orb = 9
        self.restrict_orb = 3
        self.current_file = "ing tea.json"
        self.selections_data = {}