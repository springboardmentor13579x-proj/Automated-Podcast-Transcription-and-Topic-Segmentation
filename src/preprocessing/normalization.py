import librosa
import numpy as np
import soundfile as sf

def normalize_audio(input_path, output_path):
    audio, sr = librosa.load(input_path, sr=None)
    normalized_audio = audio / np.max(np.abs(audio))
    sf.write(output_path,normalized_audio, sr)