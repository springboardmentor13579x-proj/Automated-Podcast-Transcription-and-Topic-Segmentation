import os

# The correct code for config.py
config_code = """import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define folder paths
DATA_FOLDER = os.path.join(BASE_DIR, "data")
RAW_AUDIO_FOLDER = os.path.join(DATA_FOLDER, "raw")
PROCESSED_FOLDER = os.path.join(DATA_FOLDER, "processed")

# Create directories if they don't exist
os.makedirs(RAW_AUDIO_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Configuration settings
SAMPLE_RATE = 16000
CHUNK_DURATION = 60
"""

# Overwrite config.py in the CURRENT folder
with open("config.py", "w", encoding="utf-8") as f:
    f.write(config_code)

print("✅ SUCCESS: config.py has been fixed in this folder.")
print(f"File location: {os.path.abspath('config.py')}")