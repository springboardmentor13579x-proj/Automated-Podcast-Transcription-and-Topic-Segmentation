import os
from pydub import AudioSegment
import noisereduce as nr
import librosa
import soundfile as sf

RAW_DIR = "../../data/raw_audio"
CLEAN_DIR = "../../data/clean_audio"


def preprocess_audio(file_name):
    print(f"\n Preprocessing: {file_name}")

    # 1. Load audio file path
    input_path = os.path.join(RAW_DIR, file_name)

    # 2. Convert to WAV using pydub
    sound = AudioSegment.from_file(input_path)
    wav_path = os.path.join(CLEAN_DIR, file_name.replace(".mp3", ".wav"))
    sound = sound.set_frame_rate(16000).set_channels(1)
    sound.export(wav_path, format="wav")

    # 3. Load WAV for noise reduction
    y, sr = librosa.load(wav_path, sr=16000)

    # 4. Apply noise reduction
    reduced_noise = nr.reduce_noise(y=y, sr=sr)

    # 5. Save cleaned file
    sf.write(wav_path, reduced_noise, sr)
    print(f" Cleaned audio saved: {wav_path}")


def run_preprocessing():
    for file in os.listdir(RAW_DIR):
        if file.endswith(".mp3") or file.endswith(".wav") or file.endswith(".m4a"):
            preprocess_audio(file)


if __name__ == "__main__":
    run_preprocessing()
