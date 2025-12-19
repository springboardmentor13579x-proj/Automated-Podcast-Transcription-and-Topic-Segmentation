import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from pydub import AudioSegment
import soundfile as sf
# Folders and settings
INPUT_DIR = "asr_denver_sample"        # Folder with MP3 files
OUTPUT_DIR = "clean_audio"             # Output folder for WAV
METADATA_FILE = "metadata.csv"
TARGET_SR = 16000                      # Target sample rate for ASR
# Function to clean audio
def clean_audio(input_path, output_path):
    try:
        # Load MP3 using pydub
        audio = AudioSegment.from_file(input_path)

        # Convert stereo → mono
        audio = audio.set_channels(1)

        # Resample to TARGET_SR
        audio = audio.set_frame_rate(TARGET_SR)

        # Convert to numpy array
        samples = np.array(audio.get_array_of_samples(), dtype=np.float32)

        # Normalize audio
        max_val = np.max(np.abs(samples))
        if max_val > 0:
            samples /= max_val

        # Save as WAV using soundfile
        sf.write(output_path, samples, TARGET_SR)

        # Return duration in seconds
        return len(samples) / TARGET_SR

    except Exception as e:
        print(f" ERROR processing {input_path}: {e}")
        return None
# Main processing
def main():
    if not os.path.exists(INPUT_DIR):
        print(f" Input folder does not exist: {INPUT_DIR}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    mp3_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".mp3")]
    print(f"\nFound {len(mp3_files)} MP3 files.\n")

    metadata_rows = []

    for file_name in tqdm(mp3_files, desc="Cleaning audio"):
        in_path = os.path.join(INPUT_DIR, file_name)
        out_path = os.path.join(OUTPUT_DIR, file_name.replace(".mp3", ".wav"))

        duration = clean_audio(in_path, out_path)

        if duration is not None:
            metadata_rows.append({
                "original_file": file_name,
                "clean_wav": out_path,
                "duration_seconds": round(duration, 2),
                "sampling_rate": TARGET_SR
            })

    # Save metadata CSV
    df = pd.DataFrame(metadata_rows)
    df.to_csv(METADATA_FILE, index=False)
    print("\n Cleaning Completed")
    print(" Clean WAV files saved in:", OUTPUT_DIR)
    print("Metadata created:", METADATA_FILE)
if __name__ == "__main__":
    main()




