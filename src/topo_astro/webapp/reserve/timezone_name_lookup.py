"""
webapp/reserve/timezone_name_lookup.py - a preserved, currently-unwired
web-layer utility.

get_timezone_name_from_pos returns an IANA timezone name (e.g.
"Europe/London") for a lat/long pair. It has no current caller - the one
place that used to call it, the /generate_chart route's kerykeion-based
SVG generation, currently has that call commented out (see
webapp/reserve/charting_kerykeion/ once Phase 8 relocates that code).
Kept because it's a complete, correct, working utility, not because it's
still wired into anything today.
"""
from timezonefinder import TimezoneFinder


def get_timezone_name_from_pos(geopos):
    tf = TimezoneFinder()
    geo_lat = geopos[0]
    geo_long = geopos[1]
    
    return tf.timezone_at(lat=geo_lat, lng=geo_long)
