import torch
import librosa
import soundfile as sf
import os
import warnings

warnings.filterwarnings("ignore")

def get_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    else:
        return torch.device("cpu")

def get_sorted_files(folder_path):
    try:
        files = [f for f in os.listdir(folder_path) if f.endswith('.mp3')]
        try:
            files.sort(key=lambda x: int(x.split('.')[0]))
        except ValueError:
            files.sort()
        return files
    except Exception:
        return []

# ==========================================
# THIS IS THE MISSING FUNCTION
# ==========================================
def preprocess_audio(input_path, output_path):
    """
    Process a single audio file: VAD -> Normalize -> Save as WAV
    """
    temp_file = "temp_vad_processing.wav"
    device = get_device()
    
    try:
        # Load VAD Model
        model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                      model='silero_vad',
                                      force_reload=False,
                                      trust_repo=True)
        (get_speech_timestamps, save_audio, read_audio, _, collect_chunks) = utils
        model.to(device)
        
        # Read Audio
        wav = read_audio(input_path, sampling_rate=16000)
        wav = wav.to(device)
        
        # Detect Speech
        speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=16000)
        
        if len(speech_timestamps) > 0:
            # Save Speech Chunk
            save_audio(temp_file, collect_chunks(speech_timestamps, wav), sampling_rate=16000)
            
            # Enhance (Librosa)
            y, sr = sf.read(temp_file)
            y_norm = librosa.util.normalize(y)
            y_final = librosa.effects.preemphasis(y_norm, coef=0.97)
            
            # Save Final
            sf.write(output_path, y_final, sr)
            
            # Cleanup
            if os.path.exists(temp_file): os.remove(temp_file)
            return True
        else:
            return False # No speech detected

    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        if os.path.exists(temp_file): os.remove(temp_file)
        return False

# ==========================================
# BATCH FUNCTION (Kept for compatibility)
# ==========================================
def preprocess_audio_batch(input_dir, output_dir, limit=None):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    all_files = get_sorted_files(input_dir)
    if limit: all_files = all_files[:limit]
    
    print(f"Processing {len(all_files)} files...")

    for filename in all_files:
        input_path = os.path.join(input_dir, filename)
        new_filename = f"cleaned_{os.path.splitext(filename)[0]}.wav"
        output_path = os.path.join(output_dir, new_filename)
        
        print(f"Processing: {filename}", end="\r")
        preprocess_audio(input_path, output_path)

    print("\nPreprocessing Complete.")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    default_input = os.path.join(base_dir, "audio_raw")
    default_output = os.path.join(base_dir, "audio_processed")
    preprocess_audio_batch(default_input, default_output, limit=5)