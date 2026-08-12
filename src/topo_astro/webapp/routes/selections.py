"""
webapp/routes/selections.py - NEW in Phase 8. The 'selections'
blueprint: '/update_selection' (POST, toggles one aspect's accepted state
in the in-memory cache) and '/save_data' (POST, persists the current
in-memory selections for one radix date to saved_selections/*.txt).
Relocated from the former monolithic app.py's update_selection() and
save_data() routes.

Phase 7 change: neither route uses `global selections_data`/
`global selections_data, current_file` any more - both read/mutate
state.selections_data and state.current_file through
flask.current_app.state (see webapp/state.py). Every dict
setdefault/append/remove/del operation on selections_data below is
otherwise byte-for-byte identical to the pre-Phase-7 version; only the
name each operation is performed through (state.selections_data instead
of the bare module-global name) has changed. get_technique_name is
imported from core.constants (unchanged from before this phase);
sanitize_filename now comes from webapp/utils.py (see that module's own
docstring for why it moved there rather than staying inline).
"""
import logging
import os

from flask import Blueprint, current_app, jsonify, request

from topo_astro.core.constants import get_technique_name, SELECTIONS_DIR
from topo_astro.webapp.utils import sanitize_filename

selections_bp = Blueprint('selections', __name__)


@selections_bp.route('/update_selection', methods=['POST'])
def update_selection():
    state = current_app.state
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
        state.selections_data.setdefault(primary_date_str, {})
        state.selections_data[primary_date_str].setdefault(event_str, {})
        state.selections_data[primary_date_str][event_str].setdefault(technique_name, [])

        # Add or remove the aspect
        aspect_list = state.selections_data[primary_date_str][event_str][technique_name]
        if is_selected:
            if aspect not in aspect_list:
                aspect_list.append(aspect)
                logging.info(f"Added selection: {primary_date_str} > {event_str} > {technique_name} > {aspect}")
        else:
            if aspect in aspect_list:
                aspect_list.remove(aspect)
                logging.info(f"Removed selection: {primary_date_str} > {event_str} > {technique_name} > {aspect}")

        # Clean up empty structures (optional but good practice)
        if not state.selections_data[primary_date_str][event_str][technique_name]:
            del state.selections_data[primary_date_str][event_str][technique_name]
        if not state.selections_data[primary_date_str][event_str]:
            del state.selections_data[primary_date_str][event_str]
        if not state.selections_data[primary_date_str]:
            del state.selections_data[primary_date_str]

        # logging.debug(f"Current selections_data: {json.dumps(selections_data, indent=2)}")
        return jsonify({"status": "success", "message": "Selection updated"})

    except Exception as e:
        logging.exception("Error in /update_selection")
        return jsonify({"status": "error", "message": f"Server error: {e}"}), 500


@selections_bp.route('/save_data', methods=['POST'])
def save_data():
    state = current_app.state
    data = request.get_json()
    date_to_save_str = data.get('date_to_save') # Expecting ISO string format

    if not date_to_save_str:
        return jsonify({"status": "error", "message": "Missing date_to_save"}), 400

    if date_to_save_str not in state.selections_data:
        logging.info(f"No selections found for date {date_to_save_str}, nothing to save.")
        return jsonify({"status": "success", "message": "No selections to save"})

    # Prepare filename
    json_base_name = os.path.splitext(state.current_file)[0]
    base_name_filename = f"{json_base_name}_{date_to_save_str}"
    filename = sanitize_filename(base_name_filename) # Use existing sanitize function
    filepath = os.path.join(SELECTIONS_DIR, filename)

    # Ensure the save directory exists
    os.makedirs(SELECTIONS_DIR, exist_ok=True)

    logging.info(f"Attempting to save data for {date_to_save_str} to {filepath}")

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            date_data = state.selections_data[date_to_save_str]
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