import pandas as pd
import re
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration (From .env)
INPUT_CSV = os.getenv("MERGED_DATASET", "final_project_dataset.csv")
OUTPUT_CSV = os.getenv("CLEAN_DATASET", "clean_project_dataset.csv")

def clean_text_logic(text):
    """
    Removes non-speech metadata.
    """
    if not isinstance(text, str):
        return ""
    
    # Remove (Applause), [Music], etc.
    text = re.sub(r'\s*\(.*?\)\s*', ' ', text)
    text = re.sub(r'\s*\[.*?\]\s*', ' ', text)
    return " ".join(text.split())

def clean_ground_truth():
    if not os.path.exists(INPUT_CSV):
        print(f"Error: {INPUT_CSV} not found.")
        return

    print(f"Cleaning transcripts in {INPUT_CSV}...")
    df = pd.read_csv(INPUT_CSV)
    
    if 'transcript' in df.columns:
        df['clean_transcript'] = df['transcript'].apply(clean_text_logic)
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"Success! Cleaned data saved to {OUTPUT_CSV}")
    else:
        print("Error: 'transcript' column not found.")

if __name__ == "__main__":
    clean_ground_truth()