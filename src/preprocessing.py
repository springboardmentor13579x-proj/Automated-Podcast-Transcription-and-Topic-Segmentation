import librosa
import numpy as np
import soundfile as sf

def preprocess_audio_array(y, sr, target_sr=16000, max_duration=15):
    if len(y) > max_duration * sr:
        y = y[:int(max_duration * sr)]
    if sr != target_sr:
        y = librosa.resample(y, orig_sr=sr, target_sr=target_sr)
        sr = target_sr
    y = librosa.util.normalize(y)
    y = librosa.effects.trim(y, top_db=20)[0]
    return y, sr

def save_temp_audio(y, sr, filename="temp.wav"):
    sf.write(filename, y, sr)
    return filename