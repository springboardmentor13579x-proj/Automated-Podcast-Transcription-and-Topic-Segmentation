import os
import librosa
import soundfile as sf
import noisereduce as nr
import numpy as np

def preprocess_audio(input_dir, output_dir, sr=16000):
    print("=== AUDIO PREPROCESSING ===")
    print("Input directory:", os.path.abspath(input_dir))
    print("Output directory:", os.path.abspath(output_dir))

    if not os.path.exists(input_dir):
        print("ERROR: Input directory does not exist.")
        return

    os.makedirs(output_dir, exist_ok=True)

    files = os.listdir(input_dir)
    print("Files found:", files)

    if len(files) == 0:
        print("ERROR: No files in input directory.")
        return

    for filename in files:
        if not filename.lower().endswith(".wav"):
            print("Skipping (not wav):", filename)
            continue

        input_path = os.path.join(input_dir, filename)
        print("Loading:", input_path)

        try:
            audio, _ = librosa.load(input_path, sr=sr)
        except Exception as e:
            print("ERROR loading file:", filename)
            print(e)
            continue

        try:
            audio_reduced = nr.reduce_noise(y=audio, sr=sr)
            audio_normalized = librosa.util.normalize(audio_reduced)
            audio_boosted = np.clip(audio_normalized * 1.4, -1.0, 1.0)

            output_path = os.path.join(output_dir, filename)
            sf.write(output_path, audio_boosted, sr)
            print("Saved:", output_path)

        except Exception as e:
            print("ERROR processing file:", filename)
            print(e)
