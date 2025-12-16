import torch
import whisper
import os
import pandas as pd
import json
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

def get_device():
    """
    Detects if NVIDIA GPU is available.
    """
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")

def transcribe_batch(input_folder, output_csv):
    """
    Iterates through audio files in the input folder, transcribes them using Whisper,
    and saves the results to a CSV file.
    """
    
    # 1. Validation
    if not os.path.exists(input_folder):
        print(f"[ERROR] Input folder '{input_folder}' does not exist.")
        return

    # 2. Setup Model
    device = get_device()
    print(f"[INFO] Using Hardware: {str(device).upper()}")
    print("[STATUS] Loading Whisper Model (Base)...")
    
    try:
        model = whisper.load_model("base", device=device)
    except Exception as e:
        print(f"[CRITICAL ERROR] Failed to load Whisper model: {e}")
        return

    # 3. Get Files
    audio_files = [f for f in os.listdir(input_folder) if f.endswith(".wav")]
    
    # Try to sort numerically (1.wav, 2.wav...)
    try:
        audio_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
    except:
        pass # Proceed with default sort if naming convention differs

    print(f"[INFO] Found {len(audio_files)} files to transcribe.")
    
    results = []
    
    # 4. Processing Loop
    for index, filename in enumerate(audio_files):
        file_path = os.path.join(input_folder, filename)
        
        # Extract Talk ID
        try:
            talk_id = int(filename.split('_')[1].split('.')[0])
        except:
            talk_id = 0

        print(f"[PROCESSING {index+1}/{len(audio_files)}] ID: {talk_id} | File: {filename}")
        
        try:
            # Inference
            transcription = model.transcribe(file_path)
            full_text = transcription['text'].strip()
            
            # Store Data
            results.append({
                "talk_id": talk_id,
                "filename": filename,
                "ai_text": full_text,  # Renamed to match accuracy script expectations
                "segments_json": json.dumps(transcription['segments']) 
            })
            
        except Exception as e:
            print(f"[ERROR] Failed to transcribe {filename}: {e}")

    # 5. Save Output
    if results:
        df = pd.DataFrame(results)
        df.to_csv(output_csv, index=False)
        print("\n" + "-"*50)
        print(f"[SUCCESS] Transcription complete.")
        print(f"[OUTPUT] Data saved to: {output_csv}")
        print("-"*50)
    else:
        print("[WARNING] No data was generated.")

def main():
    # Configuration
    INPUT_DIR = "cleaned_audio"       # Folder containing clean WAVs
    OUTPUT_FILE = "clean_transcripts.csv" # Output file
    
    transcribe_batch(INPUT_DIR, OUTPUT_FILE)

if __name__ == "__main__":
    main()