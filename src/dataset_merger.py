import pandas as pd
import os
from dotenv import load_dotenv

# Load variables
load_dotenv()

# Configuration (From .env)
AUDIO_FOLDER_PATH = os.getenv("MERGE_AUDIO_SOURCE")
CSV_FILE_PATH = os.getenv("MERGE_CSV_SOURCE")
OUTPUT_FILENAME = os.getenv("MERGED_DATASET", "final_project_dataset.csv")

def merge_dataset():
    """
    Links audio files to transcripts.
    """
    if not AUDIO_FOLDER_PATH or not CSV_FILE_PATH:
        print("Error: Missing paths in .env file.")
        return

    if not os.path.exists(CSV_FILE_PATH):
        print(f"Error: CSV file not found at {CSV_FILE_PATH}")
        return

    print(f"Loading CSV: {CSV_FILE_PATH}")
    df = pd.read_csv(CSV_FILE_PATH)

    # Identify ID column
    id_col = 'talk__id' if 'talk__id' in df.columns else 'talk_id'
    if id_col not in df.columns:
        print("Error: Could not find ID column.")
        return

    valid_pairs = []
    missing_count = 0

    print("Linking audio files...")
    for index, row in df.iterrows():
        talk_id = row[id_col]
        # Assuming filenames are 1001.mp3, etc.
        audio_filename = f"{talk_id}.mp3"
        full_audio_path = os.path.join(AUDIO_FOLDER_PATH, audio_filename)
        
        if os.path.exists(full_audio_path):
            valid_pairs.append({
                'talk_id': talk_id,
                'title': row.get('title', 'Unknown'),
                'transcript': row.get('transcript', ''),
                'audio_path': full_audio_path
            })
        else:
            missing_count += 1

    if valid_pairs:
        pd.DataFrame(valid_pairs).to_csv(OUTPUT_FILENAME, index=False)
        print(f"Success! Saved {len(valid_pairs)} pairs to {OUTPUT_FILENAME}")
    else:
        print("Failure. No matching audio files found.")

if __name__ == "__main__":
    merge_dataset()