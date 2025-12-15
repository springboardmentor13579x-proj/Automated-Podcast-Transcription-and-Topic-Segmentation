import os
import librosa
import soundfile as sf
import numpy as np
from pathlib import Path
from tqdm import tqdm
import random

# --- CONFIGURATION ---
# 1. Input: Where your raw downloaded MP3s are
INPUT_DIR = r"D:\farrakh important\internship_project infosys\podcast_data\audio"

# 2. Output: Where to save the clean, processed WAV files
OUTPUT_DIR = r"D:\farrakh important\internship_project infosys\podcast_data\processed_audio"

# 3. Settings for Whisper AI
TARGET_SR = 16000  # Whisper expects 16kHz audio
# ---------------------

def verify_conversion(input_files, output_dir):
    """Picks one file and prints the Before vs After stats"""
    if not input_files:
        return

    # Pick a random file to test
    test_file = random.choice(input_files)
    processed_file = Path(output_dir) / (test_file.stem + ".wav")

    if not processed_file.exists():
        return

    print("\n🔎 --- VERIFICATION: Spot Check ---")
    
    # Load Original
    y_orig, sr_orig = librosa.load(str(test_file), sr=None, mono=False)
    channels_orig = "Mono" if len(y_orig.shape) == 1 else "Stereo"
    size_orig = os.path.getsize(test_file) / 1024

    # Load Processed
    y_proc, sr_proc = librosa.load(str(processed_file), sr=None, mono=False)
    channels_proc = "Mono" if len(y_proc.shape) == 1 else "Stereo"
    size_proc = os.path.getsize(processed_file) / 1024

    print(f"File: {test_file.name}")
    print(f"{'Property':<15} | {'Original (MP3)':<20} | {'Processed (WAV)':<20}")
    print("-" * 65)
    print(f"{'Sample Rate':<15} | {sr_orig} Hz {'(Too High)' if sr_orig > 16000 else '':<10} | {sr_proc} Hz (Perfect for AI)")
    print(f"{'Channels':<15} | {channels_orig:<20} | {channels_proc:<20}")
    print(f"{'File Size':<15} | {size_orig:.1f} KB {'(Compressed)':<12} | {size_proc:.1f} KB (Uncompressed)")
    print("-" * 65)
    print("✅ The AI will now process this file much faster.")

def preprocess_all():
    input_path = Path(INPUT_DIR)
    output_path = Path(OUTPUT_DIR)
    
    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)

    # Find all audio files (MP3, WAV, FLAC)
    audio_files = list(input_path.glob("*.mp3")) + \
                list(input_path.glob("*.wav")) + \
                list(input_path.glob("*.flac"))
    
    if not audio_files:
        print(f"❌ No audio files found in {INPUT_DIR}")
        return

    print(f"🔍 Found {len(audio_files)} files. Checking for new files...")
    print(f"🎯 Target: 16kHz, Mono, Normalized WAV")

    success_count = 0
    skipped_count = 0

    for audio_file in tqdm(audio_files):
        try:
            # Construct the expected output path first
            output_filename = audio_file.stem + ".wav"
            save_path = output_path / output_filename

            # --- CHECK: If file exists, skip it ---
            if save_path.exists():
                skipped_count += 1
                continue
            # --------------------------------------

            # 1. Load Audio
            # librosa.load automatically resamples (sr=TARGET_SR) and mixes to mono (mono=True)
            y, sr = librosa.load(str(audio_file), sr=TARGET_SR, mono=True)

            # 2. Normalize Volume (Optional but recommended)
            if np.max(np.abs(y)) > 0:
                y = y / np.max(np.abs(y))

            # 3. Save as WAV
            sf.write(save_path, y, sr)
            success_count += 1

        except Exception as e:
            print(f"\n❌ Error processing {audio_file.name}: {e}")

    print(f"\n🎉 Preprocessing Complete!")
    
    if success_count == 0 and skipped_count > 0:
        print("✅ All data is already processed. No new files to convert.")
    else:
        print(f"⏩ Skipped {skipped_count} already processed files.")
        print(f"✅ Successfully processed {success_count} new files.")
        print(f"📂 Clean data saved to: {OUTPUT_DIR}")
        # Only run verification if we actually processed something or want to check
        verify_conversion(audio_files, OUTPUT_DIR)

if __name__ == "__main__":
    preprocess_all()