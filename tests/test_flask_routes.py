"""
Flask route contracts, using flask.testing's real test client - not just
reading the route source. Every test below drives an actual HTTP-style
request through the real app, against a real, isolated data_input/ +
saved_selections/ directory pair (seeded with Beyoncé's real fixture).

--------------------------------------------------------------------------
Updated for Phase 8 (migration plan): webapp/app.py's monolithic module-
level `app = Flask(__name__)` and its six bare globals (geo_pos_natal,
dt_radix, lunar_orb, restrict_orb, current_file, selections_data) no
longer exist. The app is now built via webapp/app_factory.py's
create_app(), which returns a fresh Flask instance with a fresh,
explicit AppState (webapp/state.py) attached as app.state on every call -
no module-level app object to import, and no module-level globals to
reset before/after each test.

This means _reset_app_globals() - which previously reached into
flask_app_module's six bare attributes and reset them by hand before and
after every test, the same kind of pre/post-test hygiene this repo's
batch-side tests needed for grid_engine.py's now-removed globals - is no
longer needed. Each call to create_app() inside the `client` fixture below
already produces a brand-new AppState() with fresh defaults; test
isolation between test functions is now structural (a new app + a new
state object every time), not convention-based via a manual reset
function a future test author could forget to call. _reset_app_globals()
has been removed rather than kept as a no-op stub.

Every assertion that used to read `flask_app_module.X` (e.g.
`flask_app_module.current_file`, `flask_app_module.geo_pos_natal`) now
reads `client.application.state.X` - Flask's test client exposes the
Flask app instance it's driving via `.application`, and that app's state
is attached at `.state` (see app_factory.create_app()). This is the exact
same object route code reaches via `flask.current_app.state` inside a
request - reading it from the test via `client.application.state` after
the request completes confirms the SAME state object routes mutated
during the request, not a copy or a different instance.

Route paths are unchanged from before Phase 8 ('/', '/update_content',
'/update_selection', '/save_data') - app_factory.create_app() registers
all three blueprints at their original, unprefixed paths specifically so
that no caller (including this test file) needs to know blueprints exist
at all.
--------------------------------------------------------------------------
"""

import json
import os
import shutil

import pytest

from webapp.app_factory import create_app

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
BIRTH_DATA_DIR = os.path.join(FIXTURES_DIR, "birth_data")


@pytest.fixture
def client(tmp_path, monkeypatch):
    """A real Flask test client, running against an isolated working
    directory seeded with Beyoncé's real fixture data - data_input/ and
    saved_selections/ are relative paths in the real app (DATA_INPUT_DIR =
    'data_input', SELECTIONS_DIR = 'saved_selections'), resolved against
    the current working directory at request time, not against app.py's
    own location - confirmed directly before relying on it here.

    Phase 8 update: builds a fresh app via create_app() on every call to
    this fixture (i.e. once per test), rather than reusing one shared
    module-level app object. This gives every test its own isolated
    AppState by construction - see this file's module docstring."""
    (tmp_path / "data_input").mkdir()
    (tmp_path / "saved_selections").mkdir()
    shutil.copy(
        os.path.join(BIRTH_DATA_DIR, "beyonce.json"),
        tmp_path / "data_input" / "beyonce.json",
    )
    monkeypatch.chdir(tmp_path)

    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


class TestHomeRoute:
    def test_loads_the_only_available_json_file_by_default(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert client.application.state.current_file == "beyonce.json"
        # confirms home() actually loaded Beyoncé's real geopos into the
        # state object update_content() depends on
        assert client.application.state.geo_pos_natal == [29.7217, -95.3875, 32]

    def test_explicit_filename_query_param_is_honored(self, client):
        response = client.get("/?filename=beyonce.json")
        assert response.status_code == 200
        assert client.application.state.current_file == "beyonce.json"

    def test_returns_500_with_no_json_files_present(self, client, tmp_path):
        os.remove(tmp_path / "data_input" / "beyonce.json")
        response = client.get("/")
        assert response.status_code == 500
        assert b"No JSON files found" in response.data

    def test_response_includes_the_real_natal_event_list(self, client):
        """The rendered page must include Beyoncé's real events - confirms
        list_dt_events actually made it into the template context, not
        just that the page loaded without error."""
        response = client.get("/")
        assert b"BIRTH_SISTER" in response.data
        assert b"DIVORCE_SEPARATION" in response.data


class TestUpdateContentRoute:
    def test_missing_left_item_returns_400_with_prompt_message(self, client):
        client.get("/")  # establishes geo_pos_natal/current_file via home() first
        response = client.get("/update_content?right_radio=0")
        assert response.status_code == 400
        data = response.get_json()
        assert data["static_message"] == "Please select a radix date."

    def test_real_pd_request_for_birth_daughter_returns_real_aspects(self, client):
        client.get("/")
        right_item = "2012-01-07T12:00:00, BIRTH_DAUGHTER, 4, [29.7217, -95.3875, 32]"
        response = client.get(
            "/update_content",
            query_string={
                "right_radio": "0",  # PD
                "left_item": "1981-09-04T02:28:44",
                "right_item": right_item,
            },
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "aspects" in data
        assert len(data["aspects"]) > 0
        # house-label substitution (H10->MC etc.) must already be applied
        joined = " ".join(data["aspects"])
        assert "H10," not in joined  # substituted to MC
        assert "H1," not in joined  # substituted to AS

    def test_incomplete_right_item_currently_crashes_with_500_confirmed_bug(self, client):
        """Real, confirmed bug, not an assumption: a right_item string with
        fewer than 6 comma-separated parts hits the route's own
        `else: logging.warning("Incomplete event info string...")` branch
        (webapp/routes/content.py, relocated verbatim from the pre-Phase-8
        app.py's update_content route), which does NOT set dt_event (it
        stays at its initial None). The route then correctly skips the
        `if dt_event:` block - but final_list_to_send is ONLY ever
        assigned inside that same block (as either [] or data_list), and
        the route unconditionally references it in the final jsonify()
        call regardless of whether dt_event was set. Result: an
        UnboundLocalError, caught by the route's own broad
        `except Exception`, surfaced as a 500 with the exception's own
        message as static_message.

        Confirmed still present, byte-for-byte, after the Phase 7/8
        relocation into webapp/routes/content.py - this is a pre-existing
        bug (see docs/phase2_README.md Finding #1) that Phase 7/8 was a
        zero-logic-change refactor and correctly did not touch. If this
        test ever starts passing with a 200, the bug has been fixed
        (good news, but out of scope for the Phase 7/8 pass that produced
        the current content.py), and this test needs deliberately
        updating to match the fix rather than being left looking like a
        working graceful-degradation test it never actually was."""
        client.get("/")
        response = client.get(
            "/update_content",
            query_string={"right_radio": "0", "left_item": "1981-09-04T02:28:44", "right_item": "not, valid, enough"},
        )
        assert response.status_code == 500
        data = response.get_json()
        assert "final_list_to_send" in data["static_message"]

    def test_the_same_crash_also_fires_for_a_well_formed_but_unparseable_right_item(self, client):
        """Confirms the bug's real scope is broader than "too few parts":
        a right_item with the correct 6-part shape, but where an inner
        field fails to parse (here, a non-integer event_id), is caught by
        the route's OWN inner try/except - which explicitly resets
        dt_event back to None before continuing. This was initially
        assumed (wrongly) to be a working contrast case showing graceful
        degradation; empirically, it hits the exact same UnboundLocalError
        as the too-few-parts case above, since both paths leave dt_event
        at None and final_list_to_send unassigned either way. The bug
        fires whenever right_item_str is truthy AND dt_event ends up None
        for ANY reason - not specifically tied to one parsing branch."""
        client.get("/")
        malformed_but_right_length = "2012-01-07T12:00:00, BIRTH_DAUGHTER, NOT_AN_INT, [29.7217, -95.3875, 32]"
        response = client.get(
            "/update_content",
            query_string={"right_radio": "0", "left_item": "1981-09-04T02:28:44", "right_item": malformed_but_right_length},
        )
        assert response.status_code == 500
        data = response.get_json()
        assert "final_list_to_send" in data["static_message"]


class TestUpdateSelectionAndSaveDataRoutes:
    def test_add_then_remove_a_selection_round_trips_correctly(self, client):
        add_response = client.post(
            "/update_selection",
            json={
                "primary_date": "1981-09-04T02:28:44",
                "event": "2012-01-07T12:00:00, BIRTH_DAUGHTER, 4, [29.7217, -95.3875, 32]",
                "technique_idx": 0,
                "aspect": "(Jupiter,192.284,(r)) (IC,132.368,(d)) (sextile,5.00')",
                "selected": True,
            },
        )
        assert add_response.status_code == 200
        assert add_response.get_json()["status"] == "success"
        assert client.application.state.selections_data  # real, non-empty state now

        remove_response = client.post(
            "/update_selection",
            json={
                "primary_date": "1981-09-04T02:28:44",
                "event": "2012-01-07T12:00:00, BIRTH_DAUGHTER, 4, [29.7217, -95.3875, 32]",
                "technique_idx": 0,
                "aspect": "(Jupiter,192.284,(r)) (IC,132.368,(d)) (sextile,5.00')",
                "selected": False,
            },
        )
        assert remove_response.status_code == 200
        # the cleanup logic must have removed the now-empty nested structure entirely
        assert client.application.state.selections_data == {}

    def test_missing_required_field_returns_400(self, client):
        response = client.post("/update_selection", json={"primary_date": "1981-09-04T02:28:44"})
        assert response.status_code == 400

    def test_save_data_writes_a_real_file_matching_the_persistence_format(self, client, tmp_path):
        client.get("/")  # sets current_file = beyonce.json
        client.post(
            "/update_selection",
            json={
                "primary_date": "1981-09-04T02:28:44",
                "event": "2012-01-07T12:00:00, BIRTH_DAUGHTER, 4, [29.7217, -95.3875, 32]",
                "technique_idx": 0,
                "aspect": "(Jupiter,192.284,(r)) (IC,132.368,(d)) (sextile,5.00')",
                "selected": True,
            },
        )

        save_response = client.post("/save_data", json={"date_to_save": "1981-09-04T02:28:44"})
        assert save_response.status_code == 200
        assert save_response.get_json()["status"] == "success"

        saved_files = os.listdir(tmp_path / "saved_selections")
        assert len(saved_files) == 1
        assert saved_files[0].startswith("beyonce_")

        # Confirms the saved file round-trips through the real parse_selection_file
        from persistence import selections as constants
        parsed = constants.parse_selection_file(str(tmp_path / "saved_selections" / saved_files[0]))
        key = "2012-01-07T12:00:00, BIRTH_DAUGHTER, 4, [29.7217, -95.3875, 32]"
        assert parsed[key]["PD"] == ["(Jupiter,192.284,(r)) (IC,132.368,(d)) (sextile,5.00')"]

    def test_save_data_with_nothing_selected_reports_success_without_writing_a_file(self, client, tmp_path):
        client.get("/")
        response = client.post("/save_data", json={"date_to_save": "1999-01-01T00:00:00"})
        assert response.status_code == 200
        assert response.get_json()["message"] == "No selections to save"
        assert os.listdir(tmp_path / "saved_selections") == []