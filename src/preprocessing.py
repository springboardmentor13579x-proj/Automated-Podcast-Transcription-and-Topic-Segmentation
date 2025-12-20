import os
import librosa
import soundfile as sf
import numpy as np
import noisereduce as nr

# ---------------------------------------------------------
# 1. PATHS
# ---------------------------------------------------------
INPUT_DIR = r"C:\Users\USER\OneDrive\Desktop\Project\audio_raw"
OUTPUT_DIR = r"C:\Users\USER\OneDrive\Desktop\Project\audio_processed"

# ---------------------------------------------------------
# 2. UTILITY FUNCTIONS
# ---------------------------------------------------------
def ensure_output_dir(path):
    """Create output directory if it does not exist."""
    os.makedirs(path, exist_ok=True)


def load_audio(file_path, target_sr=16000):
    """Load audio as mono with target sampling rate."""
    audio, sr = librosa.load(file_path, sr=target_sr, mono=True)
    return audio, sr


def reduce_noise(audio, sr):
    """Apply noise reduction."""
    return nr.reduce_noise(y=audio, sr=sr)


def normalize_audio(audio):
    """Normalize audio amplitude."""
    return librosa.util.normalize(audio)


def trim_silence(audio, top_db=20):
    """Trim leading and trailing silence."""
    trimmed, _ = librosa.effects.trim(audio, top_db=top_db)
    return trimmed


def save_audio(audio, sr, output_path):
    """Save processed audio to disk."""
    sf.write(output_path, audio, sr)


# ---------------------------------------------------------
# 3. PIPELINE FUNCTION (single file)
# ---------------------------------------------------------
def preprocess_audio(input_path, output_path):
    print(f"Processing: {input_path}")

    audio, sr = load_audio(input_path)
    audio = reduce_noise(audio, sr)
    audio = normalize_audio(audio)
    audio = trim_silence(audio)

    save_audio(audio, sr, output_path)

    print(f"Saved cleaned file → {output_path}\n")


# ---------------------------------------------------------
# 4. MAIN FUNCTION (batch processing)
# ---------------------------------------------------------
def main():
    ensure_output_dir(OUTPUT_DIR)

    audio_extensions = ('.wav', '.mp3', '.flac', '.ogg', '.m4a')

    for file_name in os.listdir(INPUT_DIR):
        if file_name.lower().endswith(audio_extensions):
            input_file = os.path.join(INPUT_DIR, file_name)
            output_file = os.path.join(OUTPUT_DIR, file_name)

            preprocess_audio(input_file, output_file)

    print("🎉 All audio files have been preprocessed successfully!")


# ---------------------------------------------------------
# 5. ENTRY POINT
# ---------------------------------------------------------
if __name__ == "__main__":
    main()
