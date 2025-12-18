import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define folder paths
DATA_FOLDER = os.path.join(BASE_DIR, "data")
RAW_AUDIO_FOLDER = os.path.join(DATA_FOLDER, "raw")
PROCESSED_FOLDER = os.path.join(DATA_FOLDER, "processed")

# Create directories
os.makedirs(RAW_AUDIO_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Settings
SAMPLE_RATE = 16000
CHUNK_DURATION = 60