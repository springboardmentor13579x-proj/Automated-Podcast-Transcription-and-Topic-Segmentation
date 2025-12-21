import pandas as pd
import json
import os
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# ==========================================
# CONFIGURATION
# ==========================================
# Use the path defined in .env, or fallback to default
INPUT_CSV = os.getenv("OUTPUT_FILE", "data/final_search_index_fixed.csv")
OUTPUT_FOLDER = "segments_export"

def export_data():
    if not os.path.exists(INPUT_CSV):
        print(f"[ERROR] Could not find Input CSV at: {INPUT_CSV}")
        print("-> Make sure you ran the main pipeline first.")
        return

    # Create output folder in the main directory (not inside scripts)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    print(f"[STATUS] Exporting JSON segments to '{OUTPUT_FOLDER}/'...")

    df = pd.read_csv(INPUT_CSV)
    unique_files = df['filename'].unique()
    print(f"[INFO] Found {len(unique_files)} audio files.")

    for audio_filename in unique_files:
        # Filter and Sort
        file_data = df[df['filename'] == audio_filename].sort_values('topic_id')
        
        # Convert to JSON structure
        segments_list = file_data.to_dict(orient='records')
        
        # Save File
        base_name = os.path.splitext(audio_filename)[0]
        json_path = os.path.join(OUTPUT_FOLDER, f"{base_name}.json")
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(segments_list, f, indent=4)
        
        print(f"   -> Exported: {base_name}.json")

    print(f"\n[SUCCESS] All JSON files saved to: {os.path.abspath(OUTPUT_FOLDER)}")

if __name__ == "__main__":
    export_data()