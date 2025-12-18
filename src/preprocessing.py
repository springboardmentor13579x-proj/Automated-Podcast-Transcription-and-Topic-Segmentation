import os
import json
import time
import librosa
import soundfile as sf
from pydub import AudioSegment, effects
from dotenv import load_dotenv

load_dotenv()

AUDIO_RAW = os.getenv("AUDIO_RAW_DIR")
AUDIO_PROCESSED = os.getenv("AUDIO_PROCESSED_DIR")
META_FILE = "./docs/processing_metadata.json"

os.makedirs(AUDIO_PROCESSED, exist_ok=True)
os.makedirs("./docs", exist_ok=True)

def load_metadata():
    if not os.path.exists(META_FILE):
        return {}
    with open(META_FILE, "r") as f:
        return json.load(f)

def save_metadata(data):
    with open(META_FILE, "w") as f:
        json.dump(data, f, indent=4)

def preprocess_audio(file_path):
    start_time = time.time()
    filename = os.path.basename(file_path)
    name, _ = os.path.splitext(filename)

    output_path = os.path.join(AUDIO_PROCESSED, f"{name}_denoised.wav")


    if os.path.exists(output_path):
        return output_path, 0.0


    audio = AudioSegment.from_file(file_path)


    audio = audio.set_channels(1)
    audio = effects.normalize(audio)


    audio.export(output_path, format="wav")

    elapsed = round(time.time() - start_time, 2)
    return output_path, elapsed

def process_all_audio():
    metadata = load_metadata()

    for file in os.listdir(AUDIO_RAW):
        if not file.lower().endswith((".wav", ".mp3", ".m4a")):
            continue

        raw_path = os.path.join(AUDIO_RAW, file)
        processed_path, time_taken = preprocess_audio(raw_path)

        key = os.path.basename(file)

        metadata[key] = metadata.get(key, {})
        metadata[key]["preprocessing"] = {
            "processed_audio": processed_path,
            "time_taken_sec": time_taken,
            "status": "done"
        }

        save_metadata(metadata)
        print(f"Preprocessed: {file}")

if __name__ == "__main__":
    process_all_audio()
