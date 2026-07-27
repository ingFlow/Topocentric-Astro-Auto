"""
webapp/reserve/clear_directory.py - a preserved, currently-unwired
web-layer utility.

clear_directory deletes and recreates a directory (e.g. for resetting a
charts/ or temp/ output folder before a batch regeneration). Zero current
callers anywhere in the application - kept because it's a small, complete,
working utility that a future feature (e.g. the reserved kerykeion
charting work) could plausibly need.
"""
import os
import shutil


def clear_directory(directory_path):
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        shutil.rmtree(directory_path)
        os.makedirs(directory_path)  # Recreate the empty directory
    else:
        print("Directory does not exist or is not a directory.")
