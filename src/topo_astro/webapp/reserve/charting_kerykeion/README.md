# webapp/reserve/charting_kerykeion/

This is the **working** half of the abandoned charting subsystem
described in the Developer Manual (Section 12.3) and the migration plan
(Section 2, "What Gets Preserved vs. Removed, and Why"; Phase 8; Phase
11's decision table, item 1: "Keep kerykeion, remove `astrochart.js`").

## What this is

`routes.py` contains `/generate_chart`, a Flask route that renders a
natal-chart SVG using the third-party `kerykeion` library
(`AstrologicalSubject` + `KerykeionChartSVG`). In the original,
pre-migration `app.py`, this route's SVG-generation call existed but sat
inside a triple-quoted Python string - present in the file, syntactically
valid, but never executed. Everything **around** that call (parsing
`chart_datetime`/`chart_pos`/`technique`/`right_item`, the SRA/LUNAR/
TRANSIT event-geopos substitution, the output filename construction) was
already live, working code.

As part of Phase 8, that inert block was turned into real, executing code
- the triple-quote markers were removed and nothing inside them was
changed - and the whole route was relocated here, alongside its
corresponding `from kerykeion import AstrologicalSubject,
KerykeionChartSVG` import (also previously commented-out, at the top of
the original `app.py`).

## Why it's real but not "on" by default

This blueprint is **not** registered by `webapp/app_factory.py`'s
`create_app()`. It is real, importable, callable code - not a draft, not
a sketch - but it is intentionally kept off the app's default active
route surface. To mount it:

```python
from topo_astro.webapp.app_factory import create_app
from topo_astro.webapp.reserve.charting_kerykeion.routes import kerykeion_chart_bp

app = create_app()
app.register_blueprint(kerykeion_chart_bp)
```

You will also need `kerykeion` installed in your own environment - it is
deliberately **not** added to the project's shared `requirements.txt`,
since (per the migration plan's Phase 1) that manifest only lists real
runtime dependencies of the app's default active surface, and this
blueprint sits outside that surface by design.

## Why it "worked" but isn't the end of the story

Per the Developer Manual (Section 12.3) and the git history it
reconstructs (`"Deleted kery and astroseek"`, Dec 18 2024; `"not really
working astrocharts"`, Jan 26 2025): this kerykeion-based approach
technically produced SVG output, but did not produce the visual result
the original developer wanted, and was abandoned in favor of a
never-finished client-side approach (`static/js/astrochart.js` - now
**removed entirely**, per this same Phase 8 pass; see below). Reactivating
this route restores a working chart-generation code path, not
necessarily a chart-generation code path that looks the way you want -
that's a deliberate follow-up decision for whoever picks this back up,
not something this migration silently resolves for you.

## What was deleted instead of kept

Per the Phase 8/Phase 11 decision to keep kerykeion and remove
`astrochart.js` entirely:

- `static/js/astrochart.js` (the vendored client-side charting library)
  - **deleted**, not relocated.
- The `/chart-data` route (returned only hardcoded, fake sample
  positions, feeding nothing real) - **deleted**.
- The empty `generateChart()`/`loadChart()` JavaScript stubs in
  `templates/index.html`, and the "Hi" button that triggered
  `generateChart()` - **deleted**.

See `webapp/routes/main.py` and `templates/index.html`'s own Phase 8
notes for exactly what changed there.

## `examples/` - retrieved from the `old-push` branch (ACTION NEEDED)

Per the migration plan's Phase 1 (task 2) and Phase 8 (task 6), this
folder is meant to hold a **safety copy** of the two rendered chart SVGs
and the kerykeion-specific `index_k.html` template variant that exist
only on the stale `old-push` git branch - retrieved *before* Phase 11
cleans that branch up, so nothing is lost to an accidental branch
deletion.

**This migration pass did not have access to your `old-push` branch, its
git history, or your Phase 1 safety-copy folder
(`_archive/old-push-kerykeion/`)** - only the current, post-Phase-6 repo
snapshot and the two manuals were available. Rather than fabricate SVG or
HTML content that was never actually seen, `examples/` currently contains
only a placeholder (see `examples/PLACEHOLDER.md`) explaining exactly
what belongs here.

**To finish this specific sub-task**, please:

1. Confirm your Phase 1 safety copy (`_archive/old-push-kerykeion/` or
   wherever you placed it) still contains the two SVGs and the
   `index_k.html` template variant.
2. Copy those three files into this `examples/` directory, replacing
   `PLACEHOLDER.md`.
3. Only then proceed with Phase 11's branch cleanup (deleting `old-push`)
   - per Phase 11's own validation checklist: *"`webapp/reserve/
   charting_kerykeion/` is confirmed complete (routes + both SVGs +
   template variant) before `old-push` is deleted."*

Everything else in this Phase 8 pass (the route relocation, the
astrochart.js/chart-data/dead-JS removal, the blueprint structure) is
complete and does not depend on this step.