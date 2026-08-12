"""
webapp/utils.py - NEW in Phase 8. Route-agnostic helper functions
relocated out of the former monolithic webapp/app.py, since neither
belongs to any one route/blueprint: sanitize_filename (used by both the
content and selections blueprints, to build saved_selections/*.txt
filenames) and get_aspect_str_orb (used by the content blueprint to sort
aspect strings by orb, and previously duplicated inline as a second,
near-identical regex within update_content() itself - see that route's
own Phase 8 note for where the inline duplicate went).

Both function bodies are copied verbatim from their pre-Phase-8 location
in app.py - this is pure code relocation, no logic changes.
"""
import re
import logging


def sanitize_filename(filename):
    """Turn a loaded-JSON basename + radix-candidate ISO datetime into a
    safe saved_selections/*.txt filename.

    Parameters:
        filename (str): the pre-sanitized base name, e.g.
            "ing_tea_2000-03-11T13:24:56".

    Returns:
        str: the sanitized filename with a ".txt" extension, e.g.
            "ing_tea_2000-03-11_13-24-56.txt".
    """
    sanitized = filename.replace(":", "-").replace(" ", "_").replace("T", "_")
    sanitized = re.sub(r'[<>:"/\\|?*]+', '', sanitized)
    return f"{sanitized}.txt"


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