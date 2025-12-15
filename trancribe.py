import os
import whisper
import warnings
import json
import torch
import time
import shutil
import sys
from pathlib import Path
from tqdm import tqdm

# --- CONFIGURATION ---
# INPUT: The folder where 'preprocess_audio.py' saved the clean WAVs
INPUT_DIR = r"D:\farrakh important\internship_project infosys\podcast_data\processed_audio"

# OUTPUT: Where to save the transcripts
OUTPUT_DIR = r"D:\farrakh important\internship_project infosys\podcast_data\transcripts"

# AI SETTINGS:
# Models: "tiny", "base", "small", "medium", "large"
MODEL_SIZE = "base"
# ---------------------

def check_ffmpeg():
    """Checks if FFmpeg is installed and accessible."""
    if not shutil.which("ffmpeg"):
        print("\n❌ CRITICAL ERROR: FFmpeg is not found in your system PATH.")
        print("Whisper requires FFmpeg to run.")
        print("\nPossible Fixes:")
        print("1. Did you just install it? RESTART VS CODE completely to update the PATH.")
        print("2. If that fails, download it manually from https://gyan.dev/ffmpeg/builds/")
        print("   and add the 'bin' folder to your Windows System PATH environment variable.")
        sys.exit(1)
    print("✅ FFmpeg detected.")

def save_transcript(result, file_stem, output_dir):
    """Saves both a readable text file and a structured JSON file."""
    
    # 1. Save Readable Text (.txt)
    txt_path = output_dir / f"{file_stem}.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(result["text"].strip())

    # 2. Save Data with Timestamps (.json) - Critical for next steps!
    json_path = output_dir / f"{file_stem}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

def generate_summary(text, num_sentences=3):
    """
    Generates a simple extractive summary by taking the first few sentences.
    (For a more advanced summary, we would need the 'transformers' library).
    """
    sentences = text.split('.')
    summary = ". ".join(sentences[:num_sentences]) + "."
    return summary

def transcribe_all():
    # Check dependencies first
    check_ffmpeg()

    input_path = Path(INPUT_DIR)
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)

    # --- 1. Setup AI Hardware ---
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🚀 Hardware detected: {device.upper()}")
    
    print(f"🧠 Loading Whisper model ('{MODEL_SIZE}')...")
    try:
        model = whisper.load_model(MODEL_SIZE, device=device)
        print("✅ Model loaded successfully.")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return

    # --- 2. Find Files ---
    audio_files = list(input_path.glob("*.wav"))
    if not audio_files:
        print(f"❌ No .wav files found in {INPUT_DIR}")
        print("Did you run 'preprocess_audio.py' first?")
        return

    print(f"📂 Found {len(audio_files)} files.")

    # --- 3. Process Loop ---
    success_count = 0
    skipped_count = 0

    for i, audio_file in enumerate(audio_files, 1):
        print(f"\n[{i}/{len(audio_files)}] Processing: {audio_file.name}")
        
        json_file = output_path / f"{audio_file.stem}.json"
        transcript_text = ""
        was_processed_now = False

        try:
            # --- SKIP LOGIC: Load existing if available ---
            if json_file.exists():
                print(f"   ⏩ Found existing transcript. Skipping AI processing.")
                skipped_count += 1
                # Load the text so we can still summarize it
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    transcript_text = data["text"]
            else:
                # --- RUN AI ---
                print("   🎙️  Transcribing... (Please wait)")
                start_time = time.time()
                result = model.transcribe(str(audio_file), fp16=False)
                save_transcript(result, audio_file.stem, output_path)
                transcript_text = result["text"]
                
                duration = time.time() - start_time
                print(f"   ✅ Done in {duration:.2f}s.")
                success_count += 1
                was_processed_now = True

            # --- QUALITY CHECK PREVIEW ---
            print("\n   --- 📝 Transcript Preview (Quality Check) ---")
            preview = transcript_text[:200].replace('\n', ' ')
            print(f"   \"{preview}...\"")
            print("   ---------------------------------------------")

            # --- INTERACTIVE SUMMARY ---
            while True:
                user_input = input(f"   ❓ Generate short summary for '{audio_file.name}'? (y/n/q=quit): ").lower().strip()
                
                if user_input == 'y':
                    summary = generate_summary(transcript_text)
                    print(f"\n   📖 SUMMARY:\n   {summary}\n")
                    break
                elif user_input == 'n':
                    print("   Okay, moving to next file.")
                    break
                elif user_input == 'q':
                    print("Exiting...")
                    return
                else:
                    print("   Please type 'y' for yes or 'n' for no.")

        except Exception as e:
            print(f"\n❌ Error handling {audio_file.name}: {e}")

    # --- 4. Summary ---
    print("\n🎉 All Finished!")
    print(f"✅ Processed New: {success_count}")
    print(f"⏩ Loaded Existing: {skipped_count}")
    print(f"📂 Results saved in: {OUTPUT_DIR}")

if __name__ == "__main__":
    transcribe_all()