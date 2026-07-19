"""
app.py - the interactive Flask application ("Mode 1" per the Developer
Manual). Six routes: '/' (loads a birth-data JSON and builds the
candidate-time/event lists), '/update_content' (the main technique
calculation + display route), '/update_selection' and '/save_data' (the
selection-persistence workflow), plus '/custom_action', '/chart-data',
and '/generate_chart' (the charting subsystem - partially non-functional,
see the migration plan for the kerykeion-vs-astrochart.js disposition).

This module holds module-level global state (geo_pos_natal, dt_radix,
lunar_orb, restrict_orb, current_file, selections_data) that persists
across requests within a single running process - a known architectural
issue, not something this phase changes.

Recent change (de-duplication phase): this file no longer defines its own
local copies of parse_selection_file and get_technique_name - both are
now imported directly from constants.py, which already defined the
canonical versions. The only previously-forked functional differences
were: an extra debug print() statement, one extra (redundant, given
well-formed real data) whitespace guard on the aspect-line check, and one
missing log line for the file-not-found case - none of which affect the
parsed result for any real saved_selections file, confirmed directly by
diffing both implementations before removing this one.
"""
from flask import Flask, render_template, jsonify, request, send_from_directory
import pd_automate 
import pssr_swiss_auto
import secondary_automate
import transit_swiss_auto
import lunar_auto
import sra_auto
import harmonics_auto
import main_techniques
import julian
import process_techniques_files
from datetime import datetime
import swisseph as swe
from timezonefinder import TimezoneFinder
import os
import re
import shutil
import json
from constants import calc_planets_pof_houses_labelled, parse_selection_file, get_technique_name, SELECTIONS_DIR, DATA_INPUT_DIR, aTechniqueType
from aspects_base import calculate_obliquity
#from kerykeion import AstrologicalSubject, KerykeionChartSVG
import logging

logging.basicConfig(level=logging.INFO)

geo_pos_natal = []
dt_radix = None
lunar_orb = 9
restrict_orb = 3
current_file = "ing tea.json"

selections_data = {}

app = Flask(__name__)
app.secret_key = 'toposecret'

@app.route('/')
def home():
    global current_file
    files = [f for f in os.listdir(DATA_INPUT_DIR) if f.endswith('.json')]
    current_file = request.args.get('filename', current_file)
    if not files:
        return "Error: No JSON files found in data_input directory.", 500
    if current_file not in files:
        current_file = files[0]


    try:
        dt_actual_dob, _, dt_epoch, geopos_nat, list_of_events = main_techniques.get_json_birth_data(f"data_input/{current_file}")
    except Exception as e:
        return f"Error loading data file {current_file}. Please check the file format and content.", 500
    
    global geo_pos_natal, dt_radix
    geo_pos_natal = geopos_nat
    dt_radix = dt_actual_dob
    
    list_dt_events = [t[0].isoformat() for t in list_of_events]
    list_type_events = [pd_automate.EventType.get_name(t[1]) for t in list_of_events]
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
    
    temp = process_techniques_files.generate_hourly_datetimes(geo_pos_natal,dt_actual_dob)
    for t in temp:
        list_times.append(t)
    
    #left_items = [t.isoformat() for t in list_times]
    left_items = [dt.isoformat() for dt in list_times]
    right_items = [f"{dt}, {ty}, {i}, {loc}" for dt, ty, i, loc in zip(list_dt_events, list_type_events, list_event_index,list_event_locations)]
    logging.info(f"Serving homepage with file: {current_file}")
    
    
    return render_template('index.html', left_column_items=left_items, right_column_items=right_items, files=files, current_file=current_file)

def get_aspect_str_orb(line):
    """
    Extracts the orb value from an aspect string/*.
    Returns the orb as a float, or infinity if not found/error.
    """
    # Regex to find the orb value like '2.44' or '120'
    match = re.search(r'(\d+(\.\d+)?)\'', line)
    if match:
        try:
            # Group 1 captures the full number string (e.g., "2.44")
            return float(match.group(1))
        except (ValueError, IndexError):
            # Error converting to float or accessing group
            logging.warning(f"Could not convert orb to float in line: {line}")
            return float('inf') # Put problematic lines at the end
    else:
        # No orb match found in the expected format
        return float('inf') # Put lines without orbs at the end

@app.route('/update_content')
def update_content():
    global restrict_orb, selections_data, current_file
    flag_show_accepted = request.args.get('show_accepted', default='false') == 'true'
    technique = int(request.args.get('right_radio', '0'))
    radix_date_str = request.args.get('left_item', '')
    right_item_str = request.args.get('right_item', '')  
    restrict_orb = int(request.args.get('orb_input',restrict_orb))
    flag_orb_restrict = True if (restrict_orb != -1) else False
    flag_show_data = request.args.get('show_data', default='false') == 'true'
    
    #swapping the aspects so that the direction part is always first
    aspect_pattern = re.compile(r"\(([^,]+),([0-9.]+),\(([^)]+)\)\)\s+\(([^,]+),([0-9.]+),\(([^)]+)\)\)\s+\(([^,]+),([0-9.]+)'\)")
    replacement_pattern = r"(\g<4>,\g<5>,(\g<6>)) (\g<1>,\g<2>,(\g<3>)) (\g<7>,\g<8>')"

    static_message = ''
    list_all_asp = []
    score = 0
    dt_event = None
    
    if not radix_date_str:
        return jsonify({
            'static_message': "Please select a radix date.",
            'aspects': [],
            'selections': {}
        }), 400

    try:
        radix_date = datetime.fromisoformat(radix_date_str)
        jd_radix = julian.to_jd(radix_date)
        
        event_info = []
        event_geopos = geo_pos_natal
        
        if right_item_str:
            event_info = right_item_str.split(', ')
            if len(event_info) >= 6:
                try:
                    dt_event = datetime.fromisoformat(event_info[0])
                    event_id = int(event_info[2])
                    event_locstr = [event_info[3][1:],event_info[4],event_info[5][:-1]]
                    event_geopos = [float(i) for i in event_locstr]
                except (ValueError, IndexError) as parse_error:
                    logging.warning(f"Could not parse event info (right_item_str): {right_item_str}: {parse_error}")
                    static_message = "Please select valid event"
                    event_id = None # Ensure event_id is None if parsing fails
                    dt_event = None
            else:
                logging.warning(f"Incomplete event info string: {right_item_str}")
                static_message = "Please select valid event"
        
        if right_item_str or technique == aTechniqueType.NATAL:
            rad_houses_info = swe.houses(jd_radix, geo_pos_natal[0], geo_pos_natal[1], b'T')
            rad_planets_equatorial = pd_automate.calc_rad_planets_equatorial(jd_radix)
            rad_planets_pof_houses_labelled = calc_planets_pof_houses_labelled(jd_radix, geo_pos_natal)
            str_all_directed_aspects = ""
            
            if dt_event:
                jd_event = julian.to_jd(dt_event)
                e = calculate_obliquity(jd_event)
                
                if technique == aTechniqueType.PRIMARY_DIRECT:
                    pd_auto_obj  = pd_automate.PD_Automate(jd_radix, jd_event, geo_pos_natal, rad_planets_pof_houses_labelled, rad_planets_equatorial, rad_houses_info, e)
                    str_rad_dir_aspects, str_rad_conv_aspects = pd_auto_obj.get_aspects_str()
                    pd_info = pd_auto_obj.get_extended_information()
                    str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects   
                    mdos_list = pd_auto_obj.get_mdos_natal()
                elif technique == aTechniqueType.SECONDARY_DIRECT:
                    secondary_obj = secondary_automate.Secondary_Auto(jd_radix, jd_event, geo_pos_natal[0], geo_pos_natal[1], e, rad_houses_info[1][2], rad_planets_pof_houses_labelled)
                    secondary_info = secondary_obj.get_dict_info()
                    str_rad_n_prog_aspects, str_rad_n_reg_aspects = secondary_obj.get_str_aspects()
                    str_all_directed_aspects = str_rad_n_prog_aspects + '\n' + str_rad_n_reg_aspects
                elif technique == aTechniqueType.PSSR:
                    pssr_obj = pssr_swiss_auto.PSSR_Auto(julian.from_jd(jd_radix), dt_event, rad_planets_pof_houses_labelled)
                    str_rad_dir_aspects, str_rad_conv_aspects = pssr_obj.get_str_aspects()
                    pssr_info = pssr_obj.get_dict_info()
                    str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects 
                elif technique == aTechniqueType.TRANSIT:
                    transit_obj = transit_swiss_auto.Transit_Auto(jd_radix, jd_event, event_geopos, rad_planets_pof_houses_labelled)
                    str_rad_dir_aspects, str_rad_conv_aspects = transit_obj.get_str_aspects()
                    transit_info = transit_obj.get_dict_info()
                    str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects 
                elif technique == aTechniqueType.SRA:
                    sra_auto_obj = sra_auto.SRA_Auto(julian.from_jd(jd_radix), dt_event, geo_pos_natal,rad_planets_pof_houses_labelled)
                    str_rad_dir_aspects, str_rad_conv_aspects = sra_auto_obj.get_str_aspects()
                    sra_info = sra_auto_obj.get_info()
                    str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects 
                    str_all_directed_aspects = str_all_directed_aspects.replace(")(", ")\n(")
                elif technique == aTechniqueType.NATAL:
                    for p in rad_planets_pof_houses_labelled:
                        str_all_directed_aspects+= f"{p}\n"
                elif technique == aTechniqueType.LUNAR:
                    lunar_obj = lunar_auto.Lunar_Auto(julian.from_jd(jd_radix),dt_event,event_geopos,geo_pos_natal,lunar_orb)
                    lunar_info = lunar_obj.get_info()
                    all_charts = lunar_obj.get_all_lunars()
                    str_all_directed_aspects = lunar_auto.get_str_labelled_aspects_from_array(all_charts)
                    counts = lunar_auto.count_each_planet_lunars(str_all_directed_aspects)
                    str_counts = lunar_auto.get_str_planet_counts(counts)
                    mal_count, ben_count = lunar_auto.count_mal_ben_from_str_aspects(str_all_directed_aspects)
                    static_message = f"{str_counts} #Malefics: {mal_count} vs Benefics: {ben_count}#"
                elif technique == aTechniqueType.HARMONICS:
                    harmonics_obj = harmonics_auto.Harmonics_Auto(jd_radix, jd_event, geo_pos_natal, rad_planets_pof_houses_labelled)
                    harmonics_info = harmonics_obj.get_dict_info()
                    str_all_directed_aspects = harmonics_obj.get_str_aspects()
                
                str_all_directed_aspects = re.sub(r"H10,","MC,", str_all_directed_aspects)
                str_all_directed_aspects = re.sub(r"H1,","AS,", str_all_directed_aspects)
                str_all_directed_aspects = re.sub(r"H7,","DS,", str_all_directed_aspects)
                str_all_directed_aspects = re.sub(r"H4,","IC,", str_all_directed_aspects)
                
                list_all_asp = str_all_directed_aspects.split('\n') 
                list_all_asp = [asp.strip() for asp in list_all_asp if asp.strip()] #Clean up

                if flag_show_accepted:
                    temp_filtered_list = []
                    str_accepted_aspects = ""
                    try:
                        if technique in [aTechniqueType.PRIMARY_DIRECT, aTechniqueType.SECONDARY_DIRECT, aTechniqueType.TRANSIT, aTechniqueType.SRA, aTechniqueType.HARMONICS]:
                            if event_id is not None:
                                score, str_accepted_aspects = pd_automate.count_pd_score_acceptable_aspects(event_id, str_all_directed_aspects, 0)
                                temp_filtered_list = [asp.strip() for asp in str_accepted_aspects.split('\n') if asp.strip()]
                                logging.info(f"Filtered aspects using pd_score for event {event_id}. Count: {len(temp_filtered_list)}")
                            else:
                                logging.warning(f"Show Accepted checked for technique {technique}, but no valid event_id found. Skipping filtering.")
                                temp_filtered_list = list_all_asp # Show unfiltered if event_id missing but flag checked      
                        elif technique == aTechniqueType.PSSR:
                            if event_id is not None:
                                score, str_accepted_aspects = pd_automate.count_event_acceptable_aspects(event_id,str_all_directed_aspects,0,pd_automate.AspectType.FAST_TO_SLOW_COMBO)
                                temp_filtered_list = [asp.strip() for asp in str_accepted_aspects.split('\n') if asp.strip()]
                                logging.info(f"Filtered aspects using event_acceptable for PSSR event {event_id}. Count: {len(temp_filtered_list)}")
                            else:
                                logging.warning(f"Show Accepted checked for PSSR, but no valid event_id found. Skipping filtering.")
                                temp_filtered_list = list_all_asp # Show unfiltered if event_id missing but flag checked
                        elif technique == aTechniqueType.LUNAR:
                            logging.info("Show Accepted checked for LUNAR - currently no specific filter applied.")
                            temp_filtered_list = list_all_asp
                        elif technique == aTechniqueType.NATAL:
                            logging.info("Show Accepted checked for NATAL - currently no specific filter applied.")
                            temp_filtered_list = list_all_asp
                            
                        list_all_asp = temp_filtered_list
                        
                    except Exception as filter_error:
                        logging.error(f"Error during filtering for technique {technique}, event {event_id}: {filter_error}")
                        list_all_asp = [asp.strip() for asp in str_all_directed_aspects.split('\n') if asp.strip()] # Revert to unfiltered
                        static_message = "Error filtering aspects. Please check the event ID and try again."
                            

                if flag_orb_restrict:
                    orb_restricted_list = []
                    for line in list_all_asp:
                        match = re.search(r'(\d+(\.\d+)?)\'', line)
                        if match:
                            try:
                                asp_orb_deg = float(match.group(1))
                                if asp_orb_deg <= restrict_orb:
                                    orb_restricted_list.append(line)
                            except ValueError:
                                orb_restricted_list.append(line)
                        else:
                            orb_restricted_list.append(line)
                    list_all_asp = orb_restricted_list

                final_list_to_send = []
                if not flag_show_data:
                    for line in list_all_asp:
                        swapped_line = aspect_pattern.sub(replacement_pattern, line)
                        final_list_to_send.append(swapped_line)
                    final_list_to_send.sort(key=get_aspect_str_orb)
                else:
                    technique_data = {}
                    if technique == aTechniqueType.PRIMARY_DIRECT:
                        technique_data = pd_info
                    elif technique == aTechniqueType.SECONDARY_DIRECT:
                        technique_data = secondary_info
                    elif technique == aTechniqueType.PSSR:
                        technique_data = pssr_info
                    elif technique == aTechniqueType.TRANSIT:
                        technique_data = transit_info
                    elif technique == aTechniqueType.LUNAR:
                        technique_data = lunar_info
                    elif technique == aTechniqueType.SRA:
                        technique_data = sra_info
                    elif technique == aTechniqueType.HARMONICS:
                        technique_data = harmonics_info
                    
                    if technique == aTechniqueType.PRIMARY_DIRECT or technique == aTechniqueType.LUNAR:
                        data_list = []
                        for main_key, sub_dict in technique_data.items():
                            data_list.append(f"{main_key}:") 
                            
                            if main_key == "MDOs":
                                data_list.append(sub_dict)
                            else:
                                for sub_key, value in sub_dict.items():
                                    data_list.append(f"  {sub_key}: {value}")
                    else:  
                        data_list = [f"{key}: {value}" for key, value in technique_data.items()]
                    
                    final_list_to_send = data_list

            selections_to_send = {} 
            
            if radix_date_str in selections_data:
                logging.info(f"Using existing in-memory selections_data for {radix_date_str}.")
                selections_to_send = selections_data[radix_date_str]
            else:
                current_file_base_name = os.path.splitext(current_file)[0]
                base_filename_part = f"{current_file_base_name}_{radix_date_str}"
                filename = sanitize_filename(base_filename_part)
                filepath = os.path.join(SELECTIONS_DIR, filename)
                
                logging.info(f"Attempting to parse file: {filepath}") # DEBUG LINE
                loaded_selections = parse_selection_file(filepath)
                
                if loaded_selections is not None:
                    logging.info(f"Using selections loaded from file: {filepath}")
                    selections_to_send = loaded_selections
                    print(loaded_selections)
                    selections_data[radix_date_str] = loaded_selections # Update in-memory data
                else:
                    #2. if file not found, or failed to parse, use in-memory data
                    logging.info(f"No valid saved file found for {radix_date_str}. Using in-memory selections (if any).")
                    selections_to_send = selections_data.get(radix_date_str, {})

            static_message_parts = []
            if radix_date:
                static_message_parts.append(f"Radix Date: {radix_date.isoformat()}")
            if geo_pos_natal:
                static_message_parts.append(f"GEO_LAT: {geo_pos_natal[0]} GEO_LONG: {geo_pos_natal[1]}")
            if dt_event and event_info:
                static_message_parts.append(f"Event Date: {dt_event.isoformat()}")
                static_message_parts.append(f"Event Type: {event_info[1]}: {event_id} Score: {score}")  
                static_message_parts.append(f"Score: {score}")
            if technique == aTechniqueType.LUNAR and 'str_counts' in locals():
                static_message_parts.append(f"Lunar Counts: {str_counts} Mal:{mal_count} Ben:{ben_count}")

            static_message = " | ".join(static_message_parts) # Use separator
            
            return jsonify({
                'static_message': static_message,
                'aspects': final_list_to_send, # Return the list of strings
                'selections': selections_to_send # Send back all known selections for this date
            })
        
    except ValueError as e:
        logging.error(f"Value error processing request: {e}")
        return jsonify({'static_message': f"Error: Invalid date format or value. {e}", 'aspects': [], 'selections': {}}), 400
        
    except Exception as e:
        logging.error(f"Error in /update_content")
        return jsonify({'static_message': f"An unexpected error occurred: {e}", 'aspects': [], 'selections': {}}), 500

    return jsonify({'static_message': "No data available for the selected options.", 'aspects': [], 'selections': {}}), 400
    
@app.route('/update_selection', methods=['POST'])
def update_selection():
    global selections_data
    data = request.get_json()

    primary_date_str = data.get('primary_date')
    event_str = data.get('event')
    technique_idx = data.get('technique_idx') # Send index from frontend
    aspect = data.get('aspect')
    is_selected = data.get('selected')

    # Basic validation
    if not all([primary_date_str, event_str, technique_idx is not None, aspect is not None, is_selected is not None]):
        logging.warning(f"Missing data in /update_selection: {data}")
        return jsonify({"status": "error", "message": "Missing data"}), 400

    try:
        technique_name = get_technique_name(int(technique_idx)) # Get the string name

        # Ensure nested dictionaries/lists exist
        selections_data.setdefault(primary_date_str, {})
        selections_data[primary_date_str].setdefault(event_str, {})
        selections_data[primary_date_str][event_str].setdefault(technique_name, [])

        # Add or remove the aspect
        aspect_list = selections_data[primary_date_str][event_str][technique_name]
        if is_selected:
            if aspect not in aspect_list:
                aspect_list.append(aspect)
                logging.info(f"Added selection: {primary_date_str} > {event_str} > {technique_name} > {aspect}")
        else:
            if aspect in aspect_list:
                aspect_list.remove(aspect)
                logging.info(f"Removed selection: {primary_date_str} > {event_str} > {technique_name} > {aspect}")

        # Clean up empty structures (optional but good practice)
        if not selections_data[primary_date_str][event_str][technique_name]:
            del selections_data[primary_date_str][event_str][technique_name]
        if not selections_data[primary_date_str][event_str]:
            del selections_data[primary_date_str][event_str]
        if not selections_data[primary_date_str]:
            del selections_data[primary_date_str]

        # logging.debug(f"Current selections_data: {json.dumps(selections_data, indent=2)}")
        return jsonify({"status": "success", "message": "Selection updated"})

    except Exception as e:
        logging.exception("Error in /update_selection")
        return jsonify({"status": "error", "message": f"Server error: {e}"}), 500

@app.route('/save_data', methods=['POST'])
def save_data():
    global selections_data, current_file
    data = request.get_json()
    date_to_save_str = data.get('date_to_save') # Expecting ISO string format

    if not date_to_save_str:
        return jsonify({"status": "error", "message": "Missing date_to_save"}), 400

    if date_to_save_str not in selections_data:
        logging.info(f"No selections found for date {date_to_save_str}, nothing to save.")
        return jsonify({"status": "success", "message": "No selections to save"})

    # Prepare filename
    json_base_name = os.path.splitext(current_file)[0]
    base_name_filename = f"{json_base_name}_{date_to_save_str}"
    filename = sanitize_filename(base_name_filename) # Use existing sanitize function
    filepath = os.path.join(SELECTIONS_DIR, filename)

    # Ensure the save directory exists
    os.makedirs(SELECTIONS_DIR, exist_ok=True)

    logging.info(f"Attempting to save data for {date_to_save_str} to {filepath}")

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            date_data = selections_data[date_to_save_str]
            sorted_events = sorted(date_data.keys()) # Sort events for consistent output

            for event_str in sorted_events:
                if not date_data[event_str]: continue # Skip empty events
                f.write(f"Event: {event_str}\n")
                technique_data = date_data[event_str]
                sorted_techniques = sorted(technique_data.keys()) # Sort techniques

                for technique_name in sorted_techniques:
                    if not technique_data[technique_name]: continue # Skip empty techniques
                    f.write(f"  Technique: {technique_name}\n")
                    aspect_list = technique_data[technique_name]
                    sorted_aspects = sorted(aspect_list) # Sort aspects
                    for aspect in sorted_aspects:
                        f.write(f"    - {aspect}\n")
                f.write("\n") # Add a blank line between events

        logging.info(f"Successfully saved data to {filepath}")

        # Optional: Clear data from memory after successful save if desired
        # del selections_data[date_to_save_str]

        return jsonify({"status": "success", "message": f"Data saved to {filename}"})

    except Exception as e:
        logging.exception(f"Error writing file {filepath}")
        return jsonify({"status": "error", "message": f"Failed to save file: {e}"}), 500


@app.route('/custom_action', methods=['POST'])
def custom_action():
    data = request.get_json()
    selected_text = data.get('selected_text')
    left_item = data.get('left_item')
    right_item = data.get('right_item')
    right_radio = data.get('right_radio')

    # Process received data as needed
    message = f"Received text: {selected_text}, Left Item: {left_item}, Right Item: {right_item}, Radio Value: {right_radio}"
    return jsonify({"message": message})

def clear_directory(directory_path):
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        shutil.rmtree(directory_path)
        os.makedirs(directory_path)  # Recreate the empty directory
    else:
        print("Directory does not exist or is not a directory.")

def get_timezone_name_from_pos(geopos):
    tf = TimezoneFinder()
    geo_lat = geopos[0]
    geo_long = geopos[1]
    
    return tf.timezone_at(lat=geo_lat, lng=geo_long)

def reset_globals():
    global geo_pos_natal, dt_radix
    geo_pos_natal = []
    dt_radix = None
    
@app.route('/chart-data')
def chart_data():
    data_radix = {
        "planets": {
            "Moon": [45.930008627285154],
            "Venus": [263.2584780960899],
            "Jupiter": [173.07043720306802],
            "NNode": [174.6895307834239],
            "Mars": [217.97167231451178],
            "Lilith": [196.19480722950317],
            "Saturn": [252.92341772675047],
            "Chiron": [348.1157239728284],
            "Uranus": [16.7900184974611],
            "Sun": [297.68062428797253],
            "Mercury": [289.10132025725494],
            "Neptune": [338.01899718442604],
            "Pluto": [285.6473452237151, -0.123]
        },
        "cusps": [
            348.20510089894015,
            38.108507808919654,
            65.20783751818992,
            84.96083001338991,
            103.77897207128007,
            127.1084408347092,
            168.20510089894015,
            218.10850780891965,
            245.20783751818993,
            264.9608300133899,
            283.77897207128007,
            307.1084408347092
        ]
    }

    data_transit = {
        "planets": {
            "Moon": [60.739220451080115],
            "Venus": [305.6996431634707],
            "Jupiter": [198.6565699576221],
            "NNode": [157.25592636170012],
            "Mars": [324.84013049518734],
            "Lilith": [232.88904207991555],
            "Saturn": [259.1015412368795, -0.2],
            "Chiron": [350.7285587924208],
            "Uranus": [20.678747795787075],
            "Sun": [260.94912160755536],
            "Mercury": [281.5699804920016],
            "Neptune": [339.3848859932604],
            "Pluto": [286.29683069280685]
        },
        "cusps": [296, 350, 30, 56, 75, 94, 116, 170, 210, 236, 255, 274]
    }

    return jsonify({"radix": data_radix, "transit": data_transit})

    
@app.route('/generate_chart')
def generate_chart():
    global geo_pos_natal

    chart_datetime = request.args.get('chart_datetime', default=dt_radix) 
    chart_pos = request.args.get('chart_pos', default=geo_pos_natal)
    technique = int(request.args.get('right_radio', ''))
    event_info = request.args.get('right_item', '').split(', ')

    try:
        event_locstr = [event_info[3][1:],event_info[4],event_info[5][:-1]]
        event_pos = [float(i) for i in event_locstr]
    except:
        event_pos = chart_pos
    
    if chart_datetime != dt_radix:
        try:
            chart_datetime = datetime.fromisoformat(chart_datetime)
        except ValueError:
            try:
                chart_datetime = datetime.strptime(chart_datetime, "%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                try:
                    chart_datetime = datetime.strptime(chart_datetime, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    return None # 

    if technique in [aTechniqueType.SRA, aTechniqueType.LUNAR, aTechniqueType.TRANSIT] and chart_pos == geo_pos_natal:
        chart_pos = [event_pos[0],event_pos[1]]
    
    #timezone_name = get_timezone_name_from_pos(chart_pos)
    filename = f'{chart_datetime.strftime("%Y-%m-%d %H_%M_%S")}'    
    svg_full_path = f"static/charts/{filename} - Natal Chart.svg"
    svg_path = f"{filename} - Natal Chart.svg" 
    
    '''chart_subject = AstrologicalSubject(
        filename,
        chart_datetime.year,
        chart_datetime.month,
        chart_datetime.day,
        chart_datetime.hour,
        chart_datetime.minute,
        chart_datetime.second,  
        lng=chart_pos[1],
        lat=chart_pos[0],
        tz_str="UTC",
        houses_system_identifier="T"
    )
    
    date_natal_chart = KerykeionChartSVG(chart_subject, theme="dark-high-contrast", new_output_directory="static/charts")
    date_natal_chart.makeSVG()

    if os.path.exists(svg_full_path):
        return send_from_directory('static/charts', svg_path) 
    else:
        return "File not found", 404
'''
def sanitize_filename(filename):
    sanitized = filename.replace(":", "-").replace(" ", "_").replace("T", "_")
    sanitized = re.sub(r'[<>:"/\\|?*]+', '', sanitized)
    return f"{sanitized}.txt"

if __name__ == '__main__':
    #THIS DOES NOT WORK  main_converge.pd_rect_grid_score_create('data_input/ing tea prim.json','ingtea_rect_ver4_',8)
    #main_techniques.rect_ver_data_create('data_times/winston narrow.csv', main_techniques.timesFileType.DATE_N_TIME, 'data_input/winston.json', 'data_rect/02_12_24_Winston_v1/02_12_24_')
    #DONT USE UNLESS NEEDED
    #aspects_implementation.count_aspect_groups_txt('ingtea_rect_ver4_2000-03-12_primaries.txt',False)
    #analysis.create_csv_count_txt(['txt/26_10_24_Jacqui/26_10_24_1929-07-28_primdirCOUNT.txt','txt/26_10_24_Jacqui/26_10_24_1929-07-28_secondCOUNT.txt','txt/26_10_24_Jacqui/26_10_24_1929-07-28_pssrCOUNT.txt','txt/26_10_24_Jacqui/26_10_24_1929-07-28_transCOUNT.txt'],'txt/26_10_24_Jacqui/26_10_24_Jacqui_data_tally.csv')
    #analysis.create_csv_count_txt(['txt/26_10_24_Jacqui/26_10_24_1929-07-28_primdirCOUNT.txt'],'txt/26_10_24_Jacqui/26_10_24_Jacqui_data_tally.csv')
    # Ensure the data directory exists
    if not os.path.isdir(DATA_INPUT_DIR):
        logging.error(f"Data input directory '{DATA_INPUT_DIR}' not found.")
        exit(1) # Or handle appropriately

    # Optional: Clear charts directory on start if desired
    charts_dir = 'static/charts'
    if os.path.exists(charts_dir):
        # shutil.rmtree(charts_dir) # Uncomment carefully - deletes existing charts!
        pass
    os.makedirs(charts_dir, exist_ok=True)

    logging.info("Starting Flask application...")
    app.run(debug=True, port=5000) # Use specific port, debug=True for developmen