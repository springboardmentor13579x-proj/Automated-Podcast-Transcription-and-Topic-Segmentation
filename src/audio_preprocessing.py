import torch
import librosa
import soundfile as sf
import os
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# ==========================================
# CONFIGURATION
# ==========================================
INPUT_FOLDER = r"E:\speech_to_text\archive\AUDIO"
OUTPUT_FOLDER = "cleaned_audio"
TEMP_FILE = "temp_vad_processing.wav"
FILE_LIMIT = 250  # Process first 500 files

def get_device():
    """
    Detects if NVIDIA GPU is available for acceleration.
    """
    if torch.cuda.is_available():
        device_name = torch.cuda.get_device_name(0)
        print(f"[INFO] Hardware Acceleration: Enabled ({device_name})")
        return torch.device("cuda")
    else:
        print("[INFO] Hardware Acceleration: Disabled (Using CPU)")
        return torch.device("cpu")

def get_sorted_files(folder_path):
    """
    Retrieves a list of MP3 files sorted numerically (1, 2, 3...) instead of alphabetically.
    """
    try:
        files = [f for f in os.listdir(folder_path) if f.endswith('.mp3')]
        # Sort by the integer value of the filename (e.g., '10.mp3' -> 10)
        files.sort(key=lambda x: int(x.split('.')[0]))
        return files
    except Exception as e:
        print(f"[ERROR] Could not list files: {e}")
        return []

def preprocess_audio_batch(input_dir, output_dir, limit):
    """
    Main preprocessing pipeline:
    1. VAD (Voice Activity Detection) -> Removes intro music and silence.
    2. LibROSA -> Normalizes volume and enhances signal clarity.
    """
    
    # Create output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"[STATUS] Created output directory: {output_dir}")

    # Setup AI Model
    device = get_device()
    print("[STATUS] Loading Silero VAD Model...")
    
    try:
        model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                      model='silero_vad',
                                      force_reload=False,
                                      trust_repo=True)
        (get_speech_timestamps, save_audio, read_audio, _, collect_chunks) = utils
        model.to(device)
    except Exception as e:
        print(f"[CRITICAL ERROR] Failed to load VAD model: {e}")
        return

    # Get file list
    all_files = get_sorted_files(input_dir)
    batch_files = all_files[:limit]
    
    print(f"\n[STATUS] Starting Preprocessing on {len(batch_files)} files...")
    print("-" * 60)

    success_count = 0
    skip_count = 0

    for index, filename in enumerate(batch_files):
        input_path = os.path.join(input_dir, filename)
        final_output_path = os.path.join(output_dir, f"cleaned_{filename.replace('.mp3', '.wav')}")
        
        # Display progress
        print(f"[PROCESSING {index+1}/{len(batch_files)}] File: {filename}", end="\r")
        
        try:
            # --- STEP 1: INTELLIGENT SEGMENTATION (Silero VAD) ---
            # Reads audio and moves it to GPU
            wav = read_audio(input_path, sampling_rate=16000)
            wav = wav.to(device)
            
            # Detect human speech segments
            speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=16000)
            
            if len(speech_timestamps) > 0:
                # Save the "Speech Only" audio to a temporary file
                save_audio(TEMP_FILE, collect_chunks(speech_timestamps, wav), sampling_rate=16000)
                
                # --- STEP 2: SIGNAL ENHANCEMENT (LibROSA) ---
                # Load the VAD-cleaned file using SoundFile (Faster than LibROSA load)
                y, sr = sf.read(TEMP_FILE)
                
                # A. Amplitude Normalization (Standardize Volume)
                y_norm = librosa.util.normalize(y)
                
                # B. Pre-Emphasis Filter (Enhance high frequencies for clarity)
                y_final = librosa.effects.preemphasis(y_norm, coef=0.97)
                
                # Save Final Processed File
                sf.write(final_output_path, y_final, sr)
                success_count += 1
                
            else:
                skip_count += 1
                # print(f"\n[SKIPPED] No speech detected in {filename}")

        except Exception as e:
            print(f"\n[ERROR] Failed on {filename}: {e}")

    # Cleanup
    if os.path.exists(TEMP_FILE):
        os.remove(TEMP_FILE)

    print("\n" + "-" * 60)
    print("[COMPLETED] Audio Preprocessing Finished.")
    print(f"[RESULT] Successfully Processed: {success_count}")
    print(f"[RESULT] Skipped (Empty/No Speech): {skip_count}")
    print(f"[LOCATION] Output saved to: '{output_dir}/'")
    print("-" * 60)

def main():
    # Execute the pipeline
    preprocess_audio_batch(INPUT_FOLDER, OUTPUT_FOLDER, FILE_LIMIT)

if __name__ == "__main__":
    main()