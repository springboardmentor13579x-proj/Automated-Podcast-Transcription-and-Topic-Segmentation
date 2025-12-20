# src/preprocessing.py

import os
import librosa
import soundfile as sf
import numpy as np
import noisereduce as nr
from config import AUDIO_RAW, AUDIO_PROCESSED

def preprocess_audio(original_path=AUDIO_RAW, cleaned_path=AUDIO_PROCESSED):
    """Reduce noise, normalize, and boost audio files"""
    os.makedirs(cleaned_path, exist_ok=True)
    audio_files = [f for f in os.listdir(original_path) if f.endswith(".wav")]
    
    if not audio_files:
        print("⚠️ No audio files found in", original_path)
        return

    print("Audio files found:", audio_files)

    for file in audio_files:
        path = os.path.join(original_path, file)

        # Load audio
        audio, sr = librosa.load(path, sr=16000)

        # Noise reduction
        audio_reduced = nr.reduce_noise(y=audio, sr=sr)

        # Normalize
        audio_normalized = librosa.util.normalize(audio_reduced)

        # Boost volume slightly
        audio_boosted = np.clip(audio_normalized * 1.4, -1.0, 1.0)

        # Save cleaned audio
        out_path = os.path.join(cleaned_path, file)
        sf.write(out_path, audio_boosted, sr)
        print("Processed & saved:", out_path)

if __name__ == "__main__":
    preprocess_audio()
