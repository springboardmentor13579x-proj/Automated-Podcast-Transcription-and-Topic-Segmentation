import os
import librosa
import soundfile as sf
import numpy as np
import noisereduce as nr
from tqdm import tqdm

# ---------------------------------------------------------
# 1. PATHS (AUTO – project structure ke according)
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(BASE_DIR, "Raw _audio")
OUTPUT_DIR = os.path.join(BASE_DIR, "cleaned_audio")

SUPPORTED_EXT = ('.wav', '.mp3', '.flac', '.ogg', '.m4a')

# ---------------------------------------------------------
# 2. UTILITY FUNCTIONS
# ---------------------------------------------------------

def ensure_output_dir(path):
    os.makedirs(path, exist_ok=True)

def load_audio(file_path, target_sr=16000):
    audio, sr = librosa.load(file_path, sr=target_sr, mono=True)
    return audio, sr

def reduce_noise(audio, sr):
    return nr.reduce_noise(y=audio, sr=sr)

def normalize_audio(audio):
    return librosa.util.normalize(audio)

def trim_silence(audio, top_db=20):
    trimmed, _ = librosa.effects.trim(audio, top_db=top_db)
    return trimmed

def save_audio(audio, sr, output_path):
    sf.write(output_path, audio, sr)

# ---------------------------------------------------------
# 3. PIPELINE FUNCTION (single file)
# ---------------------------------------------------------

def preprocess_audio(input_path, output_path):
    audio, sr = load_audio(input_path)
    audio = reduce_noise(audio, sr)
    audio = np.nan_to_num(audio)
    audio = normalize_audio(audio)
    audio = trim_silence(audio)
    save_audio(audio, sr, output_path)

# ---------------------------------------------------------
# 4. MAIN FUNCTION (batch processing)
# ---------------------------------------------------------

def main():
    print("📂 Input folder:", INPUT_DIR)
    print("📂 Output folder:", OUTPUT_DIR)
    print("Exists:", os.path.exists(INPUT_DIR))

    ensure_output_dir(OUTPUT_DIR)

    for root, _, files in os.walk(INPUT_DIR):
        for file in tqdm(files):
            if file.lower().endswith(SUPPORTED_EXT):
                input_file = os.path.join(root, file)
                output_file = os.path.join(
                    OUTPUT_DIR, file.split(".")[0] + ".wav"
                )
                preprocess_audio(input_file, output_file)

    print("🎉 All audio files preprocessed & saved in audio_processed")

# ---------------------------------------------------------
# 5. ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":
    main()
