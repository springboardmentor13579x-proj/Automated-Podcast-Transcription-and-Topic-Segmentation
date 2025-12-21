import os
import librosa
import soundfile as sf
import numpy as np

# -----------------------------
# Project Folder Paths (Batch)
# -----------------------------
INPUT_FOLDER = r"C:\Users\venka\OneDrive\Desktop\MedicalPodcastAI\Data\audio_raw"
OUTPUT_FOLDER = r"C:\Users\venka\OneDrive\Desktop\MedicalPodcastAI\Data\audio_processed"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -----------------------------
# Light Noise Handling
# -----------------------------
def reduce_noise(audio):
    """
    Very mild DC offset removal.
    Safe for speech / podcasts.
    """
    return audio - np.mean(audio)

# -----------------------------
# Audio Preprocessing (CORE)
# -----------------------------
def preprocess_audio(input_path, output_path):
    print(f"Processing: {input_path}")

    # Load audio → mono, 16kHz (Whisper requirement)
    audio, sr = librosa.load(input_path, sr=16000, mono=True)

    # Light noise cleanup
    cleaned = reduce_noise(audio)

    # Normalize volume
    normalized = librosa.util.normalize(cleaned)

    # Remove long silence (important for ASR accuracy)
    trimmed, _ = librosa.effects.trim(
        normalized,
        top_db=25,
        frame_length=2048,
        hop_length=512
    )

    # Prevent clipping
    trimmed = np.clip(trimmed, -1.0, 1.0)

    # Save as WAV
    sf.write(output_path, trimmed, sr)

    print(f"Saved: {output_path}")

# =========================================================
# Single Audio Preprocessing (FOR UI / FLASK BACKEND)
# =========================================================
def preprocess_single_audio(input_audio_path):
    """
    Used by Flask / UI.
    Takes one uploaded audio file,
    preprocesses it,
    returns path to processed WAV.
    """

    base = os.path.splitext(os.path.basename(input_audio_path))[0]
    output_path = os.path.join(OUTPUT_FOLDER, base + "_processed.wav")

    preprocess_audio(input_audio_path, output_path)

    return output_path

# -----------------------------
# Batch Mode Processing
# -----------------------------
def main():
    print("Starting audio preprocessing...")

    for file in os.listdir(INPUT_FOLDER):
        if file.lower().endswith((".mp3", ".wav", ".flac", ".ogg")):
            input_path = os.path.join(INPUT_FOLDER, file)

            output_name = os.path.splitext(file)[0] + ".wav"
            output_path = os.path.join(OUTPUT_FOLDER, output_name)

            preprocess_audio(input_path, output_path)

    print("Audio preprocessing completed successfully.")

# -----------------------------
# Run (Batch Mode)
# -----------------------------
if __name__ == "__main__":
    main()
