import librosa
import noisereduce as nr
import soundfile as sf

def reduce_noise(input_path, output_path):
    audio, sr = librosa.load(input_path, sr=None)
    reduced_noise = nr.reduce_noise(y=audio, sr=sr)
    sf.write(output_path, reduced_noise, sr)