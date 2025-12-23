import whisper
import librosa
import numpy as np
import soundfile as sf
import os

def preprocess_audio_array(y, sr, target_sr=16000, max_duration=15):
    if len(y) > max_duration * sr:
        y = y[:int(max_duration * sr)]
    if sr != target_sr:
        y = librosa.resample(y, orig_sr=sr, target_sr=target_sr)
        sr = target_sr
    y = librosa.util.normalize(y)
    y, _ = librosa.effects.trim(y, top_db=20)
    return y, sr

model = whisper.load_model("small")
print("Whisper model loaded: small")