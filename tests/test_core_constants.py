"""
Core layer: constants.py's radix-position and altitude-cache helpers.

--------------------------------------------------------------------------
CORRECTION TO THE PHASE 2 PLAN, found while writing these tests (documented
here rather than silently fixed, per the same "flag discrepancies rather
than assume" standard the migration plan itself was built on):

1. The Phase 2 plan describes testing "Part of Fortune day-formula and
   night-formula branches each tested once." There is no such branch
   anywhere in this codebase. calc_planets_pof_houses_labelled always
   computes Part of Fortune as `degnorm(ascendant + moon - sun)` - the
   conventional "day" formula - regardless of whether the birth was
   during the day or night. There is no sect-aware alternate formula to
   test, so this file tests the one formula that actually exists instead
   of two branches that don't.

2. The Phase 2 plan lists calc_planets_near_angles under the core/
   constants.py layer. It doesn't live there - it's defined in
   lunar_auto.py and is Lunar-technique-specific (used internally by the
   demi-return angularity check). Its test lives in
   test_technique_lunar_specifics.py instead, next to the rest of
   Lunar's own special-case behavior, not here.
--------------------------------------------------------------------------
"""

import json
import os

import constants


class TestCalcPlanetsPofHousesLabelled:
    """Beyoncé's natal chart (Houston, TX) as a fixed, hand-checkable
    fixture: 11 planets + Part of Fortune + 11 house cusps (H1-H11, per
    the function's own `range(0, 11)` - H12 is never appended; this is
    the function's real, current behavior, verified directly rather than
    assumed, and is exactly the kind of detail a byte-for-byte
    characterization test exists to catch if it ever silently changes)."""

    JD_RADIX = 2444851.6032870371  # Beyoncé, 1981-09-04T02:28:44 (see golden/beyonce_techniques.json)
    GEOPOS = [29.7217, -95.3875, 32]

    def test_returns_11_planets_plus_pof_plus_11_house_cusps(self):
        result = constants.calc_planets_pof_houses_labelled(self.JD_RADIX, self.GEOPOS)
        names = [r[0] for r in result]
        assert names[:11] == constants.PLANETS
        assert names[11] == "POF"
        assert names[12:] == [f"H{i}" for i in range(1, 12)]
        assert len(result) == 23  # 11 planets + POF + 11 houses (not 12 - see class docstring)

    def test_every_entry_is_labelled_r_for_radix(self):
        result = constants.calc_planets_pof_houses_labelled(self.JD_RADIX, self.GEOPOS)
        assert all(label == "(r)" for _name, _degree, label in result)

    def test_part_of_fortune_matches_the_one_formula_that_exists(self):
        """POF = degnorm(ascendant + moon - sun). Recomputed independently
        here (not just re-calling the function on itself) so this test
        would actually catch a change to the formula, not just a change
        to whether the function runs at all."""
        import swisseph as swe
        result = constants.calc_planets_pof_houses_labelled(self.JD_RADIX, self.GEOPOS)
        by_name = {name: degree for name, degree, _label in result}

        houses = swe.houses(self.JD_RADIX, self.GEOPOS[0], self.GEOPOS[1], b'T')
        ac = houses[0][0]
        expected_pof = swe.degnorm(ac + by_name["Moon"] - by_name["Sun"])

        assert round(by_name["POF"], 6) == round(expected_pof, 6)


class TestCalcPlanetsLabelled:
    def test_returns_one_entry_per_planet_with_requested_label(self):
        result = constants.calc_planets_labelled(2444851.6032870371, "(test)")
        assert len(result) == len(constants.PLANETS)
        assert [r[0] for r in result] == constants.PLANETS
        assert all(label == "(test)" for _name, _degree, label in result)
        assert all(0.0 <= degree < 360.0 for _name, degree, _label in result)


class TestGetAltitudeCache:
    """get_altitude(lat, lon) reads/writes a relative "altitudes.json" in
    the current working directory, and falls back to a live network call
    to api.open-elevation.com on a cache miss. Cache-hit is tested against
    the real, shipped altitudes.json; cache-miss is tested with the
    network call mocked out, both so this test suite never depends on a
    third-party API being reachable, and because CI/sandboxed environments
    commonly can't reach arbitrary external hosts at all."""

    REAL_ALTITUDES_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "fixtures", "reference_data", "altitudes.json"
    )

    def test_cache_hit_returns_stored_value_without_network_call(self, tmp_path, monkeypatch):
        # Work in an isolated directory seeded with a copy of the real
        # altitudes.json, so this test can never accidentally write into
        # (or depend on) the real source tree's copy.
        with open(self.REAL_ALTITUDES_PATH) as f:
            real_data = json.load(f)
        (tmp_path / "altitudes.json").write_text(json.dumps(real_data))
        monkeypatch.chdir(tmp_path)

        def _fail_if_called(*a, **k):
            raise AssertionError("get_altitude made a network call on a cache HIT - cache lookup is broken")
        monkeypatch.setattr("requests.get", _fail_if_called)

        # -26.183333,28.066667 -> 1784.0 in the real, shipped altitudes.json
        result = constants.get_altitude(-26.183333, 28.066667)
        assert result == 1784.0

    def test_cache_miss_calls_network_and_persists_result(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)  # empty directory - guaranteed cache miss

        class _FakeResponse:
            status_code = 200
            def json(self):
                return {"results": [{"elevation": 42.0}]}

        calls = []
        def _fake_get(url):
            calls.append(url)
            return _FakeResponse()
        monkeypatch.setattr("requests.get", _fake_get)

        result = constants.get_altitude(12.345678, 98.765432)

        assert result == 42.0
        assert len(calls) == 1
        assert "12.345678,98.765432" in calls[0]

        # and it must have been persisted to the (now-created) cache file
        with open(tmp_path / "altitudes.json") as f:
            written = json.load(f)
        assert written["12.345678,98.765432"] == 42.0

    def test_none_lat_or_lon_returns_none_without_touching_cache_or_network(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)

        def _fail_if_called(*a, **k):
            raise AssertionError("get_altitude made a network call for None input")
        monkeypatch.setattr("requests.get", _fail_if_called)

        assert constants.get_altitude(None, 28.0) is None
        assert constants.get_altitude(-26.0, None) is None
        assert not (tmp_path / "altitudes.json").exists()
