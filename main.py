import os
import json
from src.utils.file_utils import get_data_paths, ensure_dirs
from src.preprocessing.data_loader import scan_and_process_audio
from src.models.transcriber import PodcastTranscriber
from dotenv import load_dotenv # <--- Add this

# Load environment variables
load_dotenv()

EXTERNAL_AUDIO_FOLDER = os.getenv('AUDIO_DIR')
if not EXTERNAL_AUDIO_FOLDER:
    print("Error: AUDIO_DIR not found in .env file")
    exit()

def main():
    # 1. Setup Internal Paths (For Output)
    paths = get_data_paths()
    ensure_dirs([paths["transcripts_dir"], paths["temp_dir"]])
    
    # 2. Initialize Model
    print("Loading Whisper Model...")
    ai_transcriber = PodcastTranscriber(model_name="openai/whisper-tiny")

    print(f"\n--- Starting Processing from: {EXTERNAL_AUDIO_FOLDER} ---\n")

    # 3. Run the Scan Loop
    # We pass your external folder path to the loader
    for audio_path, filename in scan_and_process_audio(EXTERNAL_AUDIO_FOLDER, paths["temp_dir"]):
        
        print(f"🎤 Transcribing: {filename}...")
        
        txt_filename = os.path.splitext(filename)[0] + ".txt"
        json_filename = os.path.splitext(filename)[0] + ".json"
        
        # Output paths (inside your project folder)
        txt_out = os.path.join(paths["transcripts_dir"], txt_filename)
        json_out = os.path.join(paths["transcripts_dir"], json_filename)
        
        # Skip if already done
        if os.path.exists(txt_out):
            print(f"   -> Skipping (Already exists)")
            continue

        # Transcribe
        full_text, chunks = ai_transcriber.transcribe(audio_path)
        
        # Save Results
        with open(txt_out, "w", encoding="utf-8") as f:
            f.write(full_text)
            
        with open(json_out, "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=4)
            
        print(f"Saved: {txt_filename}")

    print("\n DONE! All transcripts are in 'data/transcripts'")

if __name__ == "__main__":
    main()


