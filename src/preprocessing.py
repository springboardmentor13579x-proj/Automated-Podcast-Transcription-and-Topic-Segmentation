import os
import librosa
import soundfile as sf
import numpy as np
from dotenv import load_dotenv

# -----------------------------
# LOAD ENV VARIABLES
# -----------------------------
load_dotenv()

# -----------------------------
# Project Folder Paths (FROM .env)
# -----------------------------
INPUT_FOLDER = os.getenv("RAW_DATA_DIR")
OUTPUT_FOLDER = os.getenv("AUDIO_PROCESSED_DIR")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -----------------------------
# Light Noise Handling (Safe for podcasts)
# -----------------------------
def reduce_noise(audio):
    # very mild DC offset removal
    return audio - np.mean(audio)

# -----------------------------
# Audio Preprocessing
# -----------------------------
def preprocess_audio(input_path, output_path):
    print(f"Processing: {input_path}")

    # Load MP3/WAV → mono, 16kHz
    audio, sr = librosa.load(input_path, sr=16000, mono=True)

    # Light cleaning
    cleaned = reduce_noise(audio)

    # Normalize volume
    normalized = librosa.util.normalize(cleaned)

    # Save as WAV (Whisper compatible)
    sf.write(output_path, normalized, sr)

    print(f"Saved: {output_path}")

# -----------------------------
# Main Pipeline
# -----------------------------
def main():
    print("Starting audio preprocessing...")

    for file in os.listdir(INPUT_FOLDER):
        if file.lower().endswith((".mp3", ".wav")):
            input_path = os.path.join(INPUT_FOLDER, file)

            # Always convert to WAV
            output_name = os.path.splitext(file)[0] + ".wav"
            output_path = os.path.join(OUTPUT_FOLDER, output_name)

            preprocess_audio(input_path, output_path)

    print("Audio preprocessing completed.")

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    main()
