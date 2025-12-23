import os
import librosa
import soundfile as sf
import numpy as np
from pathlib import Path
from tqdm import tqdm
import random

# Configuration
INPUT_DIR = r"D:\farrakh important\internship_project infosys\podcast_data\audio"
OUTPUT_DIR = r"D:\farrakh important\internship_project infosys\podcast_data\processed_audio"
TARGET_SR = 16000

def verify_conversion(input_files, output_dir):
    """Picks one file and prints comparison stats"""
    if not input_files:
        return

    test_file = random.choice(input_files)
    processed_file = Path(output_dir) / (test_file.stem + ".wav")

    if not processed_file.exists():
        return

    print("\n--- VERIFICATION: Spot Check ---")
    
    # Load original stats
    y_orig, sr_orig = librosa.load(str(test_file), sr=None, mono=False)
    channels_orig = "Mono" if len(y_orig.shape) == 1 else "Stereo"
    size_orig = os.path.getsize(test_file) / 1024

    # Load processed stats
    y_proc, sr_proc = librosa.load(str(processed_file), sr=None, mono=False)
    channels_proc = "Mono" if len(y_proc.shape) == 1 else "Stereo"
    size_proc = os.path.getsize(processed_file) / 1024

    print(f"File: {test_file.name}")
    print(f"{'Property':<15} | {'Original (MP3)':<20} | {'Processed (WAV)':<20}")
    print("-" * 65)
    print(f"{'Sample Rate':<15} | {sr_orig} Hz | {sr_proc} Hz")
    print(f"{'Channels':<15} | {channels_orig:<20} | {channels_proc:<20}")
    print(f"{'File Size':<15} | {size_orig:.1f} KB | {size_proc:.1f} KB")
    print("-" * 65)

def preprocess_all():
    input_path = Path(INPUT_DIR)
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)

    # Gather audio files
    audio_files = list(input_path.glob("*.mp3")) + \
                list(input_path.glob("*.wav")) + \
                list(input_path.glob("*.flac"))
    
    if not audio_files:
        print(f"No audio files found in {INPUT_DIR}")
        return

    print(f"Found {len(audio_files)} files. Target: 16kHz, Mono, Normalized WAV")

    success_count = 0
    skipped_count = 0

    for audio_file in tqdm(audio_files):
        try:
            save_path = output_path / (audio_file.stem + ".wav")

            # Skip existing files
            if save_path.exists():
                skipped_count += 1
                continue

            # Load and resample
            y, sr = librosa.load(str(audio_file), sr=TARGET_SR, mono=True)

            # Normalize volume
            if np.max(np.abs(y)) > 0:
                y = y / np.max(np.abs(y))

            # Save file
            sf.write(save_path, y, sr)
            success_count += 1

        except Exception as e:
            print(f"\nError processing {audio_file.name}: {e}")

    print(f"\nPreprocessing Complete!")
    print(f"Skipped {skipped_count} files. Processed {success_count} new files.")
    
    if success_count > 0 or skipped_count > 0:
        verify_conversion(audio_files, OUTPUT_DIR)

if __name__ == "__main__":
    preprocess_all()