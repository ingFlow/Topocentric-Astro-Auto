# Phase 2 Characterization Test Suite

153 tests, all run against the real, unmodified (pre-Phase-3) source and
verified passing before delivery. Every golden value and every assertion
below was produced by actually executing the application's own code
against real fixture data - nothing here is a hand-typed or assumed
expected value. Every item originally listed as "not yet covered" now has
a real, executed test behind it, including `csv_analysis.py`, which had
zero callers anywhere in the application - every one of its tests
constructs a genuine call into it via the real, current production
pipeline, rather than a synthetic invocation.

## Running it

```bash
$env:TOPO_ASTRO_SOURCE_ROOT="C:\path\to\the\flat\source\tree"   # defaults to /home/claude/repo_extracted
pip install pytest pyswisseph julian timezonefinder pytz pandas openpyxl requests #if needed
python3 -m pytest tests/ -v
```

## /!\ Please read before trusting the golden values as final

The source calls `swe.set_ephe_path('/usr/share/swisseph/ephe')`, which
doesn't exist in the environment these golden files were generated in, so
`pyswisseph` silently falls back to its built-in **Moshier** analytical
ephemeris. Moshier is accurate to a small fraction of an arcsecond for the
Sun and a few arcseconds for the outer planets - finer than the orbs this
system checks aspects against - but is not guaranteed bit-identical to a
full file-based Swiss Ephemeris run. Re-run
`python3 fixtures/generate_golden_files.py` in an environment that has the
real ephemeris files, and let it overwrite the golden files here. Every
golden JSON records which mode was used in its `ephemeris_mode` field.

## The winston.json fix, still worth double-checking

`winston.json` as originally uploaded was two JSON objects concatenated
together, differing in `geopos_natal`'s longitude sign, with the first
object's own events even inconsistent with its own natal value. Resolved
to `-1.35` throughout (geographically and Swiss-Ephemeris-convention
correct for Blenheim Palace, Woodstock - confirmed against how this
codebase actually calls `swe.houses()`, and cross-checked against Wagner's
own unambiguous, correctly-signed fixture). This was a judgment call on
ambiguous input - please confirm it matches your intent.

## Major findings from this session, in rough order of significance

1. **A real, confirmed crash bug in `/update_content`.** Driving the route
   with a `flask.testing` client rather than just reading the source
   surfaced an `UnboundLocalError`: whenever `right_item` is non-empty but
   `dt_event` ends up `None` for *any* reason (too few comma-separated
   parts, or the right shape but an inner field that fails to parse), the
   route correctly skips the `if dt_event:` block - but `final_list_to_send`
   is *only ever assigned inside that same block*, and the route
   unconditionally references it in the closing `jsonify()` call
   regardless. The result is a 500 with the exception's own message as
   `static_message`, caught by the route's own broad `except Exception`.
   Confirmed with `PROPAGATE_EXCEPTIONS` enabled to get the real traceback
   before writing the assertion - my first instinct (that this degrades
   gracefully) was wrong, and a second, supposedly-contrasting case I
   expected to succeed hit the identical crash. See
   `test_flask_routes.py::TestUpdateContentRoute`.

2. **`csv_analysis.py`'s `Secondary_Direct` handling silently produces
   zero rows - a 100% data loss, not a crash.** `extract_data_from_file`
   sets `flag_pssr=True` for `TechniqueType.Secondary_Direct`, expecting
   the moon-aware 7-field COUNT format. But the real production pipeline
   (`main_techniques.other_techniques_from_times`) calls
   `count_aspect_groups_txt(filename, flag_pssr_count_moon)` with
   `flag_pssr_count_moon=False` for `SECONDARY_DIRECT` (only `PSSR` gets
   `True`), which writes the simpler 5-field format instead. Fed through
   `extract_data_from_file` exactly as `csv_analysis.py`'s own code
   implies it should be, every real `Secondary_Direct` COUNT.txt file
   parses to an empty DataFrame - and since `load_and_concatenate_files`
   inner-joins on `Time`, merging that empty frame with any other real
   file collapses the *entire* final result to zero rows too. Verified by
   actually running the real grid -> `count_aspect_groups_txt` ->
   `csv_analysis` pipeline for all four real techniques and comparing row
   counts directly - PSSR, Transit, and Primary_Direct all parse
   correctly; only Secondary_Direct silently fails. This is a real bug
   worth a deliberate fix (either `other_techniques_from_times` should
   pass `flag_pssr_count_moon=True` for Secondary too, or `csv_analysis`'s
   Secondary_Direct branch should expect the simpler format) - which side
   is correct is a judgment call, not something picked here. See
   `test_csv_analysis.py::TestExtractDataFromFileAgainstRealPipelineOutput`.

3. **`count_aspect_groups_txt` has no header-row-skipping guard**, unlike
   its newer sibling `count_extended_aspect_groups_txt` (which has an
   explicit `flag_1st_row`). Every COUNT.txt it writes has a garbage first
   line from mis-parsing the grid file's header row (`time` becomes the
   literal string `"Time"`, `count` becomes the literal string `"Count"`).
   Confirmed harmless in practice: `csv_analysis`'s own regex requires
   `count` to be `\d+`, which `"Count"` never matches, so the line is
   silently and correctly excluded downstream. Real, but not
   data-damaging. See `test_csv_analysis.py::TestCountAspectGroupsTxtHeaderRowHandling`.

4. **`load_and_concatenate_files` infers technique from the full path
   string, not just the filename.** If a COUNT file's *directory* happens
   to contain `'pssr'`, `'prim'`, `'sec'`, or `'tran'`, it gets
   misclassified regardless of its own actual filename or content -
   demonstrated directly with a real Transit file placed in a
   `pssr`-containing directory, which then gets labeled with PSSR's `-sr`
   column suffix instead of Transit's own `-tr`. (This was originally
   discovered by accident - pytest's own `tmp_path` fixture names its
   directory after the test function, and a test named
   `..._pssr_and_transit_...` collided with this exact behavior - since
   turned into a deliberate test rather than left as a flaky one.) See
   `test_csv_analysis.py::TestLoadAndConcatenateFiles`.

5. **`create_analysis_workbook`'s dated-sheet naming has 1-second
   granularity.** Two runs within the same wall-clock second produce the
   same sheet name, and the function explicitly removes any existing sheet
   with that name before writing a fresh one - so fast successive runs
   silently *replace* rather than *add* a sheet. Confirmed deterministically
   by mocking `datetime.now()` to the same instant for both calls, with a
   contrast test showing a genuine 1-second gap correctly produces two
   distinct sheets. See `test_excel_export.py::TestCreateAnalysisWorkbookEndToEnd`.

6. **`generate_hourly_datetimes` doesn't compute real historical LMT** -
   it uses `datetime.now()`'s date for the location's *modern* timezone
   DST status, applied to the historical radix date. Proven
   deterministically by mocking "now" to a UK winter date vs. a summer
   date and showing Winston's *same* 1874 birth time produces a
   *different* candidate list depending only on which day the code
   happens to run.

7. **A real, naturally-occurring trigger for the MD > SA quadrant
   correction** ("Bug #1" territory per the Developer Manual), found by
   instrumenting `PD_Base` against all 2,706 real planet-direction checks
   across the four people's full event lists: Wagner's `dt_radix_start`
   candidate puts Pluto in house 12 in exactly the configuration that
   fires it.

8. **`is_acceptable_angular_aspect` can return `None`, not just
   `True`/`False`** - harmless today since its only caller uses a plain
   truthy check, but worth knowing before a future cleanup "fixes" the
   implicit `None`s into explicit `False`.

## A testing-practice lesson worth flagging to whoever maintains this suite

Both `test_batch_candidate_times.py` and (initially) `test_excel_export.py`
needed to mock "now" for `process_techniques_files`. The first working
version of that mock did `monkeypatch.setattr(ptf.datetime, "datetime", FakeClass)`
- this mutates the **shared** `datetime` module object every importer of
`datetime` anywhere in the process sees, not just `process_techniques_files`'s
own view of it. It happened to work in the first file, but in
`test_excel_export.py` it corrupted `openpyxl`'s own internal use of
`datetime` during `workbook.save()`, producing an unreadable `.xlsx` file.
Fixed everywhere by rebinding `ptf.datetime` itself (a module-local name)
to a small proxy object, rather than mutating the real module's
attributes - see `_frozen_datetime_module()` in `test_excel_export.py` and
the matching `freeze_now` fixture in `test_batch_candidate_times.py`.

## Complete file list

| File | Covers |
|---|---|
| `test_core_aspects.py` | `calculate_aspect` orb boundaries (all 9 `ALL_ASPECTS` entries + conjunction wraparound), `MAJOR_ASPECTS`/`ALL_ASPECTS` consistency, `flag_major` filtering, the reserved `find_trans_aspects` |
| `test_core_constants.py` | `calc_planets_pof_houses_labelled`, `calc_planets_labelled`, `get_altitude` cache hit/miss (network mocked) |
| `test_techniques_golden.py` | **The centerpiece** - all 7 techniques + Natal, byte-for-byte against golden files, across all 4 people, every candidate, every chosen event |
| `test_pd_md_sa_correction.py` | The MD > SA edge case, using the real Wagner/`radix_start`/Pluto trigger |
| `test_significators_scoring.py` | `is_acceptable_pd_aspect`, `count_pd_score_acceptable_aspects`, `is_acceptable_angular_aspect`, `count_event_acceptable_aspects`, `is_acceptable_planet_combo` |
| `test_batch_candidate_times.py` | `generate_hourly_datetimes` across all 4 timezone scenarios, `sort_polaris_times` post-fix |
| `test_batch_grid_engine.py` | `generate_grid_times_manual` → `append_grid_acceptable_angles` end-to-end, the `grid_aspects`/`resetvars()` global-state leak Phase 7 removes |
| `test_technique_lunar_specifics.py` | `calc_planets_near_angles`, the `get_str_only_aspects_from_data` fix |
| `test_persistence_selections.py` | `parse_selection_file` against both real, shipped `saved_selections/*.txt` files |
| `test_convergence.py` | `categorize_aspect` (every branch), `count_extended_aspect_groups_txt` end-to-end, `sum_sec_prim`/`read_file`/`sum_all_m`/`write_result` |
| `test_csv_analysis.py` | **NEW** - `csv_analysis.py`'s entire real surface, run via a genuinely constructed end-to-end call through the real grid → count → csv pipeline; documents finding 2 above precisely |
| `test_excel_export.py` | **NEW** - `sanitize_sheet_name`, `abbreviate_aspect_string`, and a full, mocked-`input()` end-to-end `create_analysis_workbook()` run against the two real saved_selections files; documents finding 5 above |
| `test_flask_routes.py` | **NEW** - all 6 routes via a real `flask.testing` client against real fixture data; documents finding 1 above |

## Directory layout

```
tests/
├── README.md                          (this file)
├── conftest.py
├── fixtures/
│   ├── fixture_manifest.py            (single source of truth: which people/candidates/events)
│   ├── generate_golden_files.py       (re-runnable - see the ephemeris caveat above)
│   ├── birth_data/                    (the 4 cleaned fixture JSON files)
│   ├── golden/                        (captured golden JSON, one per person)
│   ├── saved_selections/              (2 real, shipped sample files)
│   └── reference_data/altitudes.json  (real, shipped altitude cache)
├── test_core_aspects.py
├── test_core_constants.py
├── test_techniques_golden.py
├── test_pd_md_sa_correction.py
├── test_significators_scoring.py
├── test_batch_candidate_times.py
├── test_batch_grid_engine.py
├── test_technique_lunar_specifics.py
├── test_persistence_selections.py
├── test_convergence.py
├── test_csv_analysis.py
├── test_excel_export.py
└── test_flask_routes.py
```

## What's still not covered

Nothing from the original Phase 2 exhaustive list or the earlier
follow-up list remains outstanding. If anything new comes up as the
migration phases proceed (for instance, once Phase 6 introduces the
shared dispatcher, or Phase 9 introduces the `Aspect` structure), the
right move is the same one used throughout this suite: find the real call
site, run it for real, and let the actual output - bugs included - be
what gets characterized.