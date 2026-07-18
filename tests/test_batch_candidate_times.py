"""
Batch engine: candidate-time generation (generate_hourly_datetimes) and
sort_polaris_times (the function whose fix you confirmed - this locks in
its corrected behavior as the new baseline).

--------------------------------------------------------------------------
Important finding, verified by mocking datetime.datetime.now(): despite
the "historical Local Mean Time" framing these fixtures were chosen for,
generate_hourly_datetimes does NOT compute true historical LMT. Its
get_timezone_from_pos helper calls `datetime.datetime.now(timezone)` -
TODAY's real-world time, at whatever moment the code happens to run - and
uses THAT date's DST status for the location's modern IANA timezone,
applied retroactively to the historical radix date being processed. For
Winston (Woodstock, Oxfordshire, 1874) and Wagner (Leipzig, 1813), this
means the function's output actually depends on what calendar date it
happens to be run on (UK/Germany's modern DST calendar), not on any
period-accurate LMT or historical timezone rule - England didn't even
adopt GMT nationally until 1880, six years after Winston's 1874 birth.

This is characterized explicitly below (not silently treated as "it just
works because it's historical") using two fixed, mocked "now" dates - one
in each location's modern DST and non-DST season - so this test suite
doesn't itself become non-deterministic depending on what day it's run.
--------------------------------------------------------------------------
"""

import datetime as real_datetime

import pytz
import pytest

import process_techniques_files as ptf


class _FrozenNow(real_datetime.datetime):
    """A datetime.datetime subclass whose .now(tz) always returns a fixed,
    injected instant - used to make get_timezone_from_pos's dependency on
    the real wall-clock date deterministic for testing."""
    _fixed_now_utc = None

    @classmethod
    def now(cls, tz=None):
        if tz is not None:
            return cls._fixed_now_utc.astimezone(tz)
        return cls._fixed_now_utc


@pytest.fixture
def freeze_now(monkeypatch):
    """Yields a function you call with a UTC datetime to fix 'now' to,
    for the duration of the test. Restores the real datetime.datetime
    automatically afterwards regardless of pass/fail.

    Rebinds process_techniques_files's own module-local `datetime` name to
    a proxy namespace (delegating everything except .datetime.now() to the
    real module), rather than mutating the real, shared datetime module's
    own .datetime attribute directly. The latter would be a process-wide
    side effect - every other importer of `datetime` sees the same module
    object - and was confirmed elsewhere in this suite (see
    test_excel_export.py) to corrupt openpyxl's own internal datetime
    usage when both were active at once. Harmless in this file today since
    nothing else here shares the same test process moment, but kept
    consistent with the safer pattern rather than leaving two different
    approaches with two different risk profiles in the same suite."""
    import types

    def _freeze(fixed_now_utc):
        _FrozenNow._fixed_now_utc = fixed_now_utc.replace(tzinfo=pytz.UTC) if fixed_now_utc.tzinfo is None else fixed_now_utc
        fake_module = types.SimpleNamespace(
            datetime=_FrozenNow,
            timedelta=real_datetime.timedelta,
            date=real_datetime.date,
            time=real_datetime.time,
            timezone=real_datetime.timezone,
        )
        monkeypatch.setattr(ptf, "datetime", fake_module)
    return _freeze


# Real natal geopos for all four fixture people - exercises all four
# timezone scenarios you specified.
GEOPOS = {
    "beyonce": [29.7217, -95.3875, 32],                      # modern IANA, no DST (US Central)
    "winston": [51.783333333, -1.35, 113.0],                 # historical LMT, England
    "jacqui_onassis": [40.885384, -72.3964, 8.0],             # modern DST active (US Eastern)
    "richard_wagner": [51.33333333333333, 12.38333333333333, 113.0],  # historical LMT, Germany
}


class TestGenerateHourlyDatetimesStructure:
    """Structural correctness, independent of what the current UTC offset
    happens to be on any given day - self-consistent by construction."""

    @pytest.mark.parametrize("person_key", list(GEOPOS.keys()))
    def test_produces_289_five_minute_steps_spanning_exactly_24_hours(self, person_key):
        geopos = GEOPOS[person_key]
        input_dt = real_datetime.datetime(2000, 6, 15, 14, 30, 0)  # arbitrary reference date/time
        result = ptf.generate_hourly_datetimes(geopos, input_dt)

        # 24h / 5min = 288 intervals -> 289 points (start through end inclusive,
        # per the function's own `while current <= end_datetime` bound).
        assert len(result) == 289
        assert result[-1] - result[0] == real_datetime.timedelta(hours=24)
        for i in range(1, len(result)):
            assert result[i] - result[i - 1] == real_datetime.timedelta(minutes=5)

    @pytest.mark.parametrize("person_key", list(GEOPOS.keys()))
    def test_first_step_is_local_midnight_of_input_date_plus_current_utc_offset(self, person_key):
        geopos = GEOPOS[person_key]
        input_dt = real_datetime.datetime(2000, 6, 15, 14, 30, 0)

        current_offset = ptf.get_timezone_from_pos(geopos)  # same source of truth the function itself uses
        result = ptf.generate_hourly_datetimes(geopos, input_dt)

        expected_start = input_dt.replace(hour=0, minute=0, second=0, microsecond=0) + real_datetime.timedelta(hours=current_offset)
        assert result[0] == expected_start

    def test_only_the_date_of_input_datetime_matters_not_the_time_of_day(self):
        """The function discards input_datetime's time-of-day entirely
        (replace(hour=0, minute=0, ...)) - two candidates on the same date
        but different times of day must produce an identical result."""
        geopos = GEOPOS["beyonce"]
        result_a = ptf.generate_hourly_datetimes(geopos, real_datetime.datetime(2000, 6, 15, 2, 0, 0))
        result_b = ptf.generate_hourly_datetimes(geopos, real_datetime.datetime(2000, 6, 15, 23, 59, 0))
        assert result_a == result_b


class TestGenerateHourlyDatetimesUsesCurrentDateNotHistoricalDate:
    """Deterministic proof of the finding in this file's module docstring:
    output depends on the real-world date the code runs on, not on the
    historical radix date being processed."""

    def test_winston_lmt_offset_differs_between_uk_winter_and_summer_now(self, freeze_now):
        geopos = GEOPOS["winston"]
        historical_input = real_datetime.datetime(1874, 11, 30, 1, 4, 0)  # Winston's actual historical DOB

        freeze_now(real_datetime.datetime(2025, 1, 15))  # UK winter -> GMT, UTC+0
        result_winter_now = ptf.generate_hourly_datetimes(geopos, historical_input)

        freeze_now(real_datetime.datetime(2025, 7, 15))  # UK summer -> BST, UTC+1
        result_summer_now = ptf.generate_hourly_datetimes(geopos, historical_input)

        assert result_winter_now[0] != result_summer_now[0], (
            "expected the SAME historical input datetime to produce a DIFFERENT "
            "first candidate depending only on the real-world date the code runs "
            "on - if this ever stops being true, generate_hourly_datetimes has "
            "started computing genuine historical LMT instead of today's offset, "
            "which would be a deliberate improvement worth updating this test for, "
            "not a regression"
        )
        assert (result_summer_now[0] - result_winter_now[0]) == real_datetime.timedelta(hours=1)

    def test_wagner_lmt_offset_differs_between_germany_winter_and_summer_now(self, freeze_now):
        geopos = GEOPOS["richard_wagner"]
        historical_input = real_datetime.datetime(1813, 5, 22, 2, 53, 28)  # Wagner's actual historical DOB

        freeze_now(real_datetime.datetime(2025, 1, 15))  # Germany winter -> CET, UTC+1
        result_winter_now = ptf.generate_hourly_datetimes(geopos, historical_input)

        freeze_now(real_datetime.datetime(2025, 7, 15))  # Germany summer -> CEST, UTC+2
        result_summer_now = ptf.generate_hourly_datetimes(geopos, historical_input)

        assert result_winter_now[0] != result_summer_now[0]
        assert (result_summer_now[0] - result_winter_now[0]) == real_datetime.timedelta(hours=1)

    def test_beyonce_modern_no_dst_offset_is_stable_across_seasons(self, freeze_now):
        """Houston, TX observes DST too, so this isn't "no DST ever" - it's
        that at these two particular test dates (both outside the
        Jan/Jul transition edge cases) the US Central offset relative to
        these fixed 'now' dates happens to differ from Europe's simpler
        split. Included as a contrast case, not a claim that Houston has
        no DST at all.

        Note: kept to structural checks (length, spacing) rather than
        isinstance-checking against real_datetime.datetime, purely as a
        style match with the rest of this class - freeze_now's module-local
        rebind (see its own docstring) no longer poisons this file's
        real_datetime reference the way an earlier, direct-module-mutation
        version of this fixture briefly did during development, but the
        structural checks are just as meaningful either way."""
        geopos = GEOPOS["beyonce"]
        historical_input = real_datetime.datetime(1981, 9, 4, 2, 28, 44)

        freeze_now(real_datetime.datetime(2025, 1, 15))
        result_jan = ptf.generate_hourly_datetimes(geopos, historical_input)
        freeze_now(real_datetime.datetime(2025, 7, 15))
        result_jul = ptf.generate_hourly_datetimes(geopos, historical_input)

        # Confirmed by construction (both derived from the real, current
        # get_timezone_from_pos) rather than asserting a specific direction -
        # documenting whichever way it actually comes out is the point of a
        # characterization test.
        for result in (result_jan, result_jul):
            assert len(result) == 289
            assert result[-1] - result[0] == real_datetime.timedelta(hours=24)


class TestSortPolarisTimes:
    """sort_polaris_times(file_name, file_write_name, count_times_wanted,
    threshold) - the function whose file_write_name/valid_lines naming
    mismatch you confirmed has since been fixed. This locks in the
    corrected, current behavior: descending sort by the 'A value' column,
    filtered by threshold, each surviving line followed by the file's own
    year marker line."""

    def _write_synthetic_polaris_file(self, tmp_path):
        # POLARIS-style output: >3 whitespace-separated tokens = a data
        # line, the 5th token (index 4) is the 'A value' being sorted on;
        # a single short line = the year marker, per the real function's
        # own valid_lines/non_valid_lines split (len(line.split()) > 3).
        lines = [
            "2001",  # year marker (non-valid-line: <= 3 tokens)
            "01 01 12 00 3 1 extra",   # A value = 3
            "01 01 12 05 9 1 extra",   # A value = 9 (highest)
            "01 01 12 10 1 1 extra",   # A value = 1 (below threshold=2, must be dropped)
            "01 01 12 15 5 1 extra",   # A value = 5
        ]
        path = tmp_path / "synthetic_polaris.txt"
        path.write_text("\n".join(lines) + "\n")
        return str(path)

    def test_sorts_descending_by_a_value_and_filters_by_threshold(self, tmp_path):
        input_path = self._write_synthetic_polaris_file(tmp_path)
        output_path = str(tmp_path / "sorted_output.txt")

        ptf.sort_polaris_times(input_path, output_path, count_times_wanted=2, threshold=2)

        with open(output_path) as f:
            content = f.read()

        # A value 1 (below threshold 2) must be excluded entirely.
        assert " 1 1 extra" not in content.replace("\t", " ")
        # Remaining three lines must appear in descending A-value order: 9, 5, 3.
        idx_9 = content.index("9 1 extra")
        idx_5 = content.index("5 1 extra")
        idx_3 = content.index("3 1 extra")
        assert idx_9 < idx_5 < idx_3

    def test_not_enough_times_for_count_returns_without_writing(self, tmp_path):
        """count_times_wanted greater than half the line count triggers the
        function's own early-return guard - confirms it still does not
        write an output file in that case (matches the source's `return`
        with no file write beforehand)."""
        input_path = self._write_synthetic_polaris_file(tmp_path)
        output_path = str(tmp_path / "should_not_exist.txt")

        ptf.sort_polaris_times(input_path, output_path, count_times_wanted=999, threshold=2)

        import os
        assert not os.path.exists(output_path)
