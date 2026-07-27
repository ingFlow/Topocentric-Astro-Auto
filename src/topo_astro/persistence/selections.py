"""
persistence/selections.py - the single canonical reader for
saved_selections/*.txt files.

parse_selection_file is used by both the interactive Flask app (to reload
a person's previously-saved aspect selections) and the batch Excel-export
path (create_analysis_workbook). There must be only one implementation of
this - app.py used to define its own, near-identical shadowing copy; that
was removed during the de-duplication phase (see the migration plan) in
favor of always importing this one.
"""
import os
import logging


def parse_selection_file(filepath):
    """Reads a saved selection file and parses it into a dictionary."""
    if not os.path.exists(filepath):
        logging.info(f"Selection file not found: {filepath}")
        return None

    loaded_selections = {}
    current_event = None
    current_technique = None
    line_number = 0

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_content in f:
                line_number += 1
                processed_line = line_content.rstrip()

                if not processed_line.startswith(' ') and processed_line.startswith("Event: "):
                    current_event = processed_line[len("Event: "):].strip()
                    if not current_event: # Handle empty event string if it occurs
                        logging.warning(f"Empty event string found at line {line_number} in {filepath}")
                        current_event = f"UNKNOWN_EVENT_{line_number}" # Placeholder
                    loaded_selections[current_event] = {}
                    current_technique = None
                elif processed_line.startswith("  ") and not processed_line.startswith("   ") and "Technique: " in processed_line:
                    if current_event:
                        try:
                            technique_part = processed_line.split("Technique: ", 1)[1]
                            current_technique = technique_part.strip()
                            if not current_technique: # Handle empty technique string
                                logging.warning(f"Empty technique string for event '{current_event}' at line {line_number} in {filepath}")
                                current_technique = f"UNKNOWN_TECHNIQUE_{line_number}" # Placeholder
                            loaded_selections[current_event][current_technique] = []
                        except IndexError:
                            logging.warning(f"Malformed Technique line for event '{current_event}' at line {line_number} in {filepath}: {processed_line}")
                            current_technique = None
                    else:
                        logging.warning(f"Found Technique line without preceding Event at line {line_number} in {filepath}: {processed_line}")
                        current_technique = None
                elif processed_line.startswith("    - "): # No need for 'not startswith("     ")' if structure is consistent
                    if current_event and current_technique:
                        # Ensure the technique key and list exist
                        if current_technique not in loaded_selections[current_event]:
                            logging.warning(f"Aspect found for event '{current_event}' but technique '{current_technique}' not initialized at line {line_number} in {filepath}. Initializing.")
                            loaded_selections[current_event][current_technique] = []

                        if isinstance(loaded_selections[current_event].get(current_technique), list):
                            aspect = processed_line[len("    - "):].strip()
                            if aspect: # Only add non-empty aspects
                                loaded_selections[current_event][current_technique].append(aspect)
                        else: # Should not happen if initialized correctly
                            logging.error(f"Critical parsing error: Technique list for '{current_event}' -> '{current_technique}' is not a list at line {line_number} in {filepath}.")
                    # else: Ignore aspect lines found out of proper context

        logging.info(f"Successfully parsed selections from {filepath}")
        # print("Parsed Dictionary:", loaded_selections) # Keep for debugging if needed
        return loaded_selections

    except Exception as e:
        logging.error(f"Error parsing selection file {filepath} at line ~{line_number}: {e}")
        return None
