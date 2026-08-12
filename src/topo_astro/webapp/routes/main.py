"""
webapp/routes/main.py - NEW in Phase 8. The 'main' blueprint: the '/'
home route, relocated verbatim (logic-wise) from the former monolithic
app.py.

Phase 7 change: home() no longer uses `global current_file`/
`global geo_pos_natal, dt_radix` - it reads and writes those three values
through flask.current_app.state (an AppState instance - see
webapp/state.py) instead. Every other line of this route's logic -
the file-listing, the default-file fallback, get_json_birth_data() call,
the hardcoded/commented-out candidate-time-list experiments, the
str_date/list_times construction, and the final render_template() call -
is unchanged from the pre-Phase-7/8 version.

Route path preserved exactly: '/' (GET), matching the original so
templates/index.html's own requests need no changes.
"""
import logging
import os
from datetime import datetime

from flask import Blueprint, render_template, request, current_app

from topo_astro.batch import entrypoints as main_techniques
from topo_astro.batch import grid_engine as process_techniques_files
from topo_astro.core.constants import DATA_INPUT_DIR
from topo_astro.significators import rules_data as significators_rules

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    state = current_app.state

    files = [f for f in os.listdir(DATA_INPUT_DIR) if f.endswith('.json')]
    state.current_file = request.args.get('filename', state.current_file)
    if not files:
        return "Error: No JSON files found in data_input directory.", 500
    if state.current_file not in files:
        state.current_file = files[0]

    try:
        dt_actual_dob, _, dt_epoch, geopos_nat, list_of_events = main_techniques.get_json_birth_data(f"data_input/{state.current_file}")
    except Exception as e:
        return f"Error loading data file {state.current_file}. Please check the file format and content.", 500

    state.geo_pos_natal = geopos_nat
    state.dt_radix = dt_actual_dob

    list_dt_events = [t[0].isoformat() for t in list_of_events]
    list_type_events = [significators_rules.EventType.get_name(t[1]) for t in list_of_events]
    list_event_locations = [t[2] for t in list_of_events]
    list_event_index = [t[1] for t in list_of_events]
    #CHANGE HERE FOR LEFT COL TIMES
    list_times = []
    list_times = [
        datetime(2000,3,11,13,24,56),
        datetime(1997,11,16,12,57,4)
        #07:49:20
        #15:49:36
        
    ]

    time_strings = [
        "1:51:36", "7:46:40", "13:49:20", "10:38:48", "13:41:12", "15:26:56",
        "12:58:24", "11:27:52", "10:15:36", "12:29:28", "15:24:56",
        "11:39:44", "15:29:20", "7:49:12", "9:23:28", "14:26:56",
        "5:37:36", "13:08:40", "13:46:32", "6:06:56", "9:21:28",
        "8:28:16", "15:44:56", "12:09:04", "9:44:00", "14:09:12"
    ]

    #list_times = [datetime.strptime(f"1874-11-30 {time}", "%Y-%m-%d %H:%M:%S") for time in time_strings]
    
    str_date = dt_actual_dob.strftime('%d %B %Y')
    list_times.append(dt_actual_dob)
    #list_times = aspects_implementation.process_manual_rect_csv('ingtea_ver3_sorted_data.csv',str_date,100,+2)
    #list_times.append(process_techniques_files.process_polaris_times(r'data_times\25_01_05_ingtea react.txt', 150))
    #list_times = process_techniques_files.process_datetime_count_csv('data_times/winston narrow.csv')
    #452801u7\'^":iclist_times = [dt_actual_dob, dt_epoch]
    
    temp = process_techniques_files.generate_hourly_datetimes(state.geo_pos_natal, dt_actual_dob)
    for t in temp:
        list_times.append(t)
    
    #left_items = [t.isoformat() for t in list_times]
    left_items = [dt.isoformat() for dt in list_times]
    right_items = [f"{dt}, {ty}, {i}, {loc}" for dt, ty, i, loc in zip(list_dt_events, list_type_events, list_event_index, list_event_locations)]
    logging.info(f"Serving homepage with file: {state.current_file}")
    
    
    return render_template('index.html', left_column_items=left_items, right_column_items=right_items, files=files, current_file=state.current_file)