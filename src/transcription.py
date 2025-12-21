import torch
import whisper
import os
import pandas as pd
import json
import warnings

warnings.filterwarnings("ignore")

def get_device():
    """Returns 'cuda' if NVIDIA GPU is available, else 'cpu'."""
    return torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

def load_whisper_model(size="base"):
    """Loads the Whisper model into memory."""
    device = get_device()
    print(f"[INFO] Loading Whisper ('{size}') on {str(device).upper()}...")
    try:
        return whisper.load_model(size, device=device)
    except Exception as e:
        print(f"[ERROR] Failed to load model: {e}")
        return None

def transcribe_audio(model, audio_path):
    """Transcribes a single audio file and returns text + segments."""
    if not os.path.exists(audio_path):
        return None, None

    try:
        result = model.transcribe(audio_path)
        return result['text'].strip(), json.dumps(result['segments'])
    except Exception as e:
        print(f"[ERROR] Transcription failed for {os.path.basename(audio_path)}: {e}")
        return None, None

def transcribe_batch(input_folder, output_csv):
    """Batch processes all .wav files in a directory."""
    if not os.path.exists(input_folder):
        print(f"[ERROR] Input folder not found: {input_folder}")
        return

    model = load_whisper_model("base")
    if not model: return

    # Get and sort .wav files
    audio_files = [f for f in os.listdir(input_folder) if f.endswith(".wav")]
    try:
        audio_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
    except:
        pass 

    print(f"[INFO] Found {len(audio_files)} files. Starting transcription...")
    results = []

    for filename in audio_files:
        file_path = os.path.join(input_folder, filename)
        
        # Extract ID if present (e.g., cleaned_1001.wav -> 1001)
        try:
            talk_id = int(filename.split('_')[1].split('.')[0])
        except:
            talk_id = 0

        print(f" -> Processing: {filename}", end="\r")
        
        text, segments = transcribe_audio(model, file_path)
        
        if text:
            results.append({
                "talk_id": talk_id,
                "filename": filename,
                "ai_text": text,
                "segments_json": segments
            })

    if results:
        pd.DataFrame(results).to_csv(output_csv, index=False)
        print(f"\n[SUCCESS] Saved {len(results)} transcripts to: {output_csv}")
    else:
        print("\n[WARNING] No transcripts generated.")