import os

def get_project_root():
    """Returns the absolute path to the project root directory."""
    # Goes up 3 levels from this file: src/utils/file_utils.py -> src/utils -> src -> Project_Root
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_data_paths():
    """Returns a dictionary of critical data paths."""
    root = get_project_root()
    return {
        "root": root,  # <--- THIS WAS MISSING. I ADDED IT NOW.
        "raw_zip": os.path.join(root, "data", "raw", "full_dataset.zip"),
        "processed_dir": os.path.join(root, "data", "processed"),
        "transcripts_dir": os.path.join(root, "data", "transcripts"),
        "temp_dir": os.path.join(root, "data", "temp_processing") # For temporary extraction
    }

def ensure_dirs(paths):
    """Creates directories if they don't exist."""
    for p in paths:
        if not os.path.exists(p):
            os.makedirs(p)