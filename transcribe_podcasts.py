import os
import whisper
import warnings
import json
import torch
import time
import shutil
import sys
import soundfile as sf  # Added to calculate audio duration
from pathlib import Path
from tqdm import tqdm

# --- CONFIGURATION ---
# INPUT: The folder where 'preprocess_audio.py' saved the clean WAVs
INPUT_DIR = r"D:\farrakh important\internship_project infosys\podcast_data\processed_audio"

# OUTPUT: Where to save the transcripts
OUTPUT_DIR = r"D:\farrakh important\internship_project infosys\podcast_data\transcripts"

# SUMMARY OUTPUT: Where to save the summaries
SUMMARY_DIR = r"D:\farrakh important\internship_project infosys\podcast_data\short_summary"

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

def generate_summary(text):
    """
    Generates a smart abstractive summary using Hugging Face Transformers.
    Falls back to extractive summary if library is missing.
    """
    try:
        from transformers import pipeline
        import logging
        
        # Suppress HF warnings
        logging.getLogger("transformers").setLevel(logging.ERROR)
        
        print("   🧠 Generating smart summary (DistilBART)...")
        
        # Load the summarization pipeline
        # 'sshleifer/distilbart-cnn-12-6' is fast and effective for English
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        
        # Input text must be truncated to fit model context (approx 1024 tokens)
        # We take the first ~3500 characters to capture the Intro/Hook/Core Concept
        chunk = text[:3500]
        
        # Generate summary with parameters tuned for "Concise but Informative" (3-5 sentences style)
        summary_result = summarizer(chunk, max_length=200, min_length=60, do_sample=False)
        
        return summary_result[0]['summary_text']

    except ImportError:
        print("   ⚠️ Library 'transformers' not found. Using simple fallback summary.")
        print("   💡 Run 'pip install transformers' to enable AI summarization.")
        
        # Fallback: Extractive (First 25 sentences)
        all_sentences = [s.strip() for s in text.split('.') if s.strip()]
        selected_sentences = all_sentences[:25]
        return ". ".join(selected_sentences) + "."
        
    except Exception as e:
        print(f"   ⚠️ Smart summarization failed: {e}")
        return text[:1000] + "..."

def save_summary(summary, file_stem):
    """Saves the summary to the dedicated summary folder."""
    summary_path = Path(SUMMARY_DIR)
    summary_path.mkdir(parents=True, exist_ok=True)
    
    file_path = summary_path / f"{file_stem}_summary.txt"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(summary)
    
    print(f"   💾 Summary saved to: {file_path}")

def interactive_summary_mode(output_dir):
    """
    Allows the user to request summaries for specific files after processing.
    """
    print("\n--- 🧠 Interactive Summary Mode ---")
    print("You can now generate summaries for any processed file.")
    
    while True:
        choice = input("\n❓ Do you want to get a summary for a file? (y/n): ").lower().strip()
        
        if choice == 'n':
            print("Exiting Summary Mode.")
            break
        elif choice == 'y':
            file_name = input("   Enter the file name (e.g., '1001'): ").strip()
            
            # Clean up input to get the stem (remove extension if user typed it)
            file_stem = Path(file_name).stem
            json_path = output_dir / f"{file_stem}.json"
            
            if json_path.exists():
                try:
                    print(f"   📖 Loading '{file_stem}'...")
                    with open(json_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        text = data["text"]
                        
                        # Generate Smart Summary
                        summary = generate_summary(text)
                        
                        # Save Summary (No printing to terminal)
                        save_summary(summary, file_stem)
                        
                except Exception as e:
                    print(f"   ❌ Error reading file: {e}")
            else:
                print(f"   ❌ Transcript not found for '{file_stem}'. Please check the name.")
        else:
            print("   Please type 'y' for yes or 'n' for no.")

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
        
        # Calculate Total Audio Duration for Quality Check
        try:
            audio_info = sf.info(str(audio_file))
            total_duration_sec = audio_info.duration
        except Exception:
            total_duration_sec = 0

        try:
            # --- SKIP LOGIC: Load existing if available ---
            if json_file.exists():
                print(f"   ⏩ Found existing transcript. Skipping AI processing.")
                skipped_count += 1
                
                # Load existing data to check coverage
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "segments" in data and len(data["segments"]) > 0:
                        last_timestamp = data["segments"][-1]["end"]
                    else:
                        last_timestamp = 0
            else:
                # --- RUN AI ---
                print("   🎙️  Transcribing... (Please wait)")
                start_time = time.time()
                result = model.transcribe(str(audio_file), fp16=False)
                save_transcript(result, audio_file.stem, output_path)
                
                duration = time.time() - start_time
                print(f"   ✅ Done in {duration:.2f}s.")
                success_count += 1
                
                if "segments" in result and len(result["segments"]) > 0:
                    last_timestamp = result["segments"][-1]["end"]
                else:
                    last_timestamp = 0

            # --- QUALITY CHECK (PERCENTAGE) ---
            if total_duration_sec > 0:
                coverage_pct = (last_timestamp / total_duration_sec) * 100
                coverage_pct = min(coverage_pct, 100.0)
                
                print(f"   📊 Quality Check: {coverage_pct:.1f}% of audio covered.")
                
                if coverage_pct < 95:
                    print("      ⚠️ Warning: It seems some audio at the end was not transcribed.")
            else:
                print("   ⚠️ Could not calculate duration coverage.")

        except Exception as e:
            print(f"\n❌ Error handling {audio_file.name}: {e}")

    # --- 4. Summary ---
    print("\n🎉 All Finished!")
    print(f"✅ Processed New: {success_count}")
    print(f"⏩ Loaded Existing: {skipped_count}")
    print(f"📂 Results saved in: {OUTPUT_DIR}")

    # --- 5. Enter Interactive Summary Mode ---
    interactive_summary_mode(output_path)

if __name__ == "__main__":
    transcribe_all()