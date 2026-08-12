"""
webapp/routes/content.py - NEW in Phase 8. The 'content' blueprint:
'/update_content', the core interactive endpoint that computes and
returns aspects for a given (candidate time, event, technique) triple.
Relocated from the former monolithic app.py's update_content() route.

Phase 7 change: this route no longer uses
`global restrict_orb, selections_data, current_file` (nor implicitly
reads geo_pos_natal/lunar_orb without declaring them global, as the
original did). All six state values are now reached through
flask.current_app.state (an AppState instance - see webapp/state.py).
Every read of restrict_orb/selections_data/current_file/geo_pos_natal/
lunar_orb below was mechanically rewritten to state.restrict_orb/
state.selections_data/state.current_file/state.geo_pos_natal/
state.lunar_orb, preserving the EXACT same read/write pattern at each
call site (see the Phase 7 commit notes for content.py for the full
site-by-site mapping this was verified against before editing). No
technique-dispatch logic, no scoring/filtering logic, no orb-restriction
logic, no selections-lookup logic, and no static_message construction
logic changed in any other way - this is purely a state-access rewrite,
not a behavior change.

get_aspect_str_orb is now imported from webapp/utils.py (see that
module's own docstring) rather than defined inline in this file.
sanitize_filename is likewise imported from webapp/utils.py.

Phase 6 note (unchanged from that phase, reproduced here since this is
where the code that phase touched now lives): PRIMARY_DIRECT, SECONDARY_
DIRECT, PSSR, TRANSIT, and SRA are constructed via
techniques.base.construct_technique() instead of five near-duplicate
inline constructor calls. Harmonics, Lunar, and Natal are UNCHANGED -
they still branch explicitly, exactly as before Phase 6, since the
dispatcher deliberately does not handle them.
"""
import logging
import re
from datetime import datetime

import julian
import swisseph as swe
from flask import Blueprint, current_app, jsonify, request

from topo_astro.techniques.primary_directions import technique as pd_automate
from topo_astro.techniques import lunars as lunar_auto
from topo_astro.techniques import harmonics as harmonics_auto
from topo_astro.techniques import base as technique_dispatcher
from topo_astro.core.constants import calc_planets_pof_houses_labelled, SELECTIONS_DIR, aTechniqueType
from topo_astro.persistence.selections import parse_selection_file
from topo_astro.core.aspects import calculate_obliquity
from topo_astro.significators import scoring as significators_scoring
from topo_astro.webapp.utils import get_aspect_str_orb, sanitize_filename

import os

content_bp = Blueprint('content', __name__)


@content_bp.route('/update_content')
def update_content():
    state = current_app.state

    flag_show_accepted = request.args.get('show_accepted', default='false') == 'true'
    technique = int(request.args.get('right_radio', '0'))
    radix_date_str = request.args.get('left_item', '')
    right_item_str = request.args.get('right_item', '')
    state.restrict_orb = int(request.args.get('orb_input', state.restrict_orb))
    flag_orb_restrict = True if (state.restrict_orb != -1) else False
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
        event_geopos = state.geo_pos_natal
        
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
            rad_houses_info = swe.houses(jd_radix, state.geo_pos_natal[0], state.geo_pos_natal[1], b'T')
            rad_planets_equatorial = pd_automate.calc_rad_planets_equatorial(jd_radix)
            rad_planets_pof_houses_labelled = calc_planets_pof_houses_labelled(jd_radix, state.geo_pos_natal)
            str_all_directed_aspects = ""
            
            if dt_event:
                jd_event = julian.to_jd(dt_event)
                e = calculate_obliquity(jd_event)
                
                if technique in (aTechniqueType.PRIMARY_DIRECT, aTechniqueType.SECONDARY_DIRECT, aTechniqueType.PSSR, aTechniqueType.TRANSIT, aTechniqueType.SRA):
                    # Phase 6: construct via the shared dispatcher instead of a
                    # per-technique inline constructor call. See
                    # techniques/base.py's module docstring for the exact
                    # per-technique argument-shape mapping this replaces -
                    # verified argument-for-argument identical to the original
                    # 5 inline constructor calls before this edit was made.
                    technique_obj = technique_dispatcher.construct_technique(
                        technique=technique,
                        jd_radix=jd_radix,
                        jd_event=jd_event,
                        dt_radix=julian.from_jd(jd_radix),
                        dt_event=dt_event,
                        geopos_natal=state.geo_pos_natal,
                        geopos_event=event_geopos,
                        rad_planets=rad_planets_pof_houses_labelled,
                        rad_planets_equatorial=rad_planets_equatorial,
                        rad_houses_info=rad_houses_info,
                        e=e,
                        ramc=rad_houses_info[1][2],
                    )

                    if technique == aTechniqueType.PRIMARY_DIRECT:
                        str_rad_dir_aspects, str_rad_conv_aspects = technique_obj.get_aspects_str()
                        pd_info = technique_obj.get_extended_information()
                        str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects
                        mdos_list = technique_obj.get_mdos_natal()
                    elif technique == aTechniqueType.SECONDARY_DIRECT:
                        secondary_info = technique_obj.get_dict_info()
                        str_rad_n_prog_aspects, str_rad_n_reg_aspects = technique_obj.get_str_aspects()
                        str_all_directed_aspects = str_rad_n_prog_aspects + '\n' + str_rad_n_reg_aspects
                    elif technique == aTechniqueType.PSSR:
                        str_rad_dir_aspects, str_rad_conv_aspects = technique_obj.get_str_aspects()
                        pssr_info = technique_obj.get_dict_info()
                        str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects
                    elif technique == aTechniqueType.TRANSIT:
                        str_rad_dir_aspects, str_rad_conv_aspects = technique_obj.get_str_aspects()
                        transit_info = technique_obj.get_dict_info()
                        str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects
                    elif technique == aTechniqueType.SRA:
                        str_rad_dir_aspects, str_rad_conv_aspects = technique_obj.get_str_aspects()
                        sra_info = technique_obj.get_info()
                        str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects
                        str_all_directed_aspects = str_all_directed_aspects.replace(")(", ")\n(")
                elif technique == aTechniqueType.NATAL:
                    for p in rad_planets_pof_houses_labelled:
                        str_all_directed_aspects+= f"{p}\n"
                elif technique == aTechniqueType.LUNAR:
                    lunar_obj = lunar_auto.Lunar_Auto(julian.from_jd(jd_radix),dt_event,event_geopos,state.geo_pos_natal,state.lunar_orb)
                    lunar_info = lunar_obj.get_info()
                    all_charts = lunar_obj.get_all_lunars()
                    str_all_directed_aspects = lunar_auto.get_str_labelled_aspects_from_array(all_charts)
                    counts = lunar_auto.count_each_planet_lunars(str_all_directed_aspects)
                    str_counts = lunar_auto.get_str_planet_counts(counts)
                    mal_count, ben_count = lunar_auto.count_mal_ben_from_str_aspects(str_all_directed_aspects)
                    static_message = f"{str_counts} #Malefics: {mal_count} vs Benefics: {ben_count}#"
                elif technique == aTechniqueType.HARMONICS:
                    harmonics_obj = harmonics_auto.Harmonics_Auto(jd_radix, jd_event, state.geo_pos_natal, rad_planets_pof_houses_labelled)
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
                                score, str_accepted_aspects = significators_scoring.count_pd_score_acceptable_aspects(event_id, str_all_directed_aspects, 0)
                                temp_filtered_list = [asp.strip() for asp in str_accepted_aspects.split('\n') if asp.strip()]
                                logging.info(f"Filtered aspects using pd_score for event {event_id}. Count: {len(temp_filtered_list)}")
                            else:
                                logging.warning(f"Show Accepted checked for technique {technique}, but no valid event_id found. Skipping filtering.")
                                temp_filtered_list = list_all_asp # Show unfiltered if event_id missing but flag checked      
                        elif technique == aTechniqueType.PSSR:
                            if event_id is not None:
                                score, str_accepted_aspects = significators_scoring.count_event_acceptable_aspects(event_id,str_all_directed_aspects,0,pd_automate.AspectType.FAST_TO_SLOW_COMBO)
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
                                if asp_orb_deg <= state.restrict_orb:
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
            
            if radix_date_str in state.selections_data:
                logging.info(f"Using existing in-memory selections_data for {radix_date_str}.")
                selections_to_send = state.selections_data[radix_date_str]
            else:
                current_file_base_name = os.path.splitext(state.current_file)[0]
                base_filename_part = f"{current_file_base_name}_{radix_date_str}"
                filename = sanitize_filename(base_filename_part)
                filepath = os.path.join(SELECTIONS_DIR, filename)
                
                logging.info(f"Attempting to parse file: {filepath}") # DEBUG LINE
                loaded_selections = parse_selection_file(filepath)
                
                if loaded_selections is not None:
                    logging.info(f"Using selections loaded from file: {filepath}")
                    selections_to_send = loaded_selections
                    print(loaded_selections)
                    state.selections_data[radix_date_str] = loaded_selections # Update in-memory data
                else:
                    #2. if file not found, or failed to parse, use in-memory data
                    logging.info(f"No valid saved file found for {radix_date_str}. Using in-memory selections (if any).")
                    selections_to_send = state.selections_data.get(radix_date_str, {})

            static_message_parts = []
            if radix_date:
                static_message_parts.append(f"Radix Date: {radix_date.isoformat()}")
            if state.geo_pos_natal:
                static_message_parts.append(f"GEO_LAT: {state.geo_pos_natal[0]} GEO_LONG: {state.geo_pos_natal[1]}")
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