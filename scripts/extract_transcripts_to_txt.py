import pandas as pd
import os
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# ==========================================
# CONFIGURATION
# ==========================================
INPUT_CSV = os.getenv("TRANSCRIPT_FILE", "data/clean_transcripts.csv")
OUTPUT_FOLDER = "transcripts_export"

def extract_transcripts():
    if not os.path.exists(INPUT_CSV):
        print(f"[ERROR] Could not find Input CSV at: {INPUT_CSV}")
        return

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    print(f"[STATUS] Extracting text files to '{OUTPUT_FOLDER}/'...")

    try:
        df = pd.read_csv(INPUT_CSV)
    except Exception as e:
        print(f"[ERROR] Failed to read CSV: {e}")
        return

    if 'filename' not in df.columns or 'ai_text' not in df.columns:
        print("[ERROR] CSV is missing required columns ('filename', 'ai_text').")
        return

    for index, row in df.iterrows():
        audio_filename = str(row['filename'])
        transcript_text = str(row['ai_text'])

        base_name = os.path.splitext(audio_filename)[0]
        txt_path = os.path.join(OUTPUT_FOLDER, f"{base_name}.txt")

        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(transcript_text)

        print(f"   -> Saved: {base_name}.txt")

    print(f"\n[SUCCESS] All text files saved to: {os.path.abspath(OUTPUT_FOLDER)}")

if __name__ == "__main__":
    extract_transcripts()