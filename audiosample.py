import os
import zipfile
import random
import soundfile as sf
import numpy as np
from scipy.signal import resample
from tqdm import tqdm
import pandas as pd
ZIP_URL = "https://huggingface.co/datasets/huuuyeah/MeetingBank_Audio/resolve/main/Denver/mp3/Denver-1.zip"
ZIP_PATH = "Denver-1.zip"
EXTRACT_DIR = "extracted_samples"
CLEAN_DIR = "clean_wav"
METADATA_FILE = "metadata.csv"
def download_zip():
    if os.path.exists(ZIP_PATH):
        print("Zip already downloaded.")
        return

    import requests
    print("⬇ Downloading Denver-1.zip ...")

    with requests.get(ZIP_URL, stream=True) as r:
        r.raise_for_status()
        total = int(r.headers.get("Content-Length", 0))
        with open(ZIP_PATH, "wb") as f, tqdm(total=total, unit="B", unit_scale=True) as pbar:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)
                pbar.update(len(chunk))

    print("Download done.")
# Extract 8 random MP3 files
def extract_random_8():
    os.makedirs(EXTRACT_DIR, exist_ok=True)

    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        mp3_files = [f for f in z.namelist() if f.endswith(".mp3")]
        print("Total MP3 in ZIP:", len(mp3_files))

        selected = random.sample(mp3_files, 8)
        print("Selected:", selected)

        for f in selected:
            print("→ Extracting:", f)
            z.extract(f, EXTRACT_DIR)

    return selected
# Convert MP3 → WAV (fast)
def convert_to_wav(mp3_path, wav_path, target_sr=16000):
    try:
        data, sr = sf.read(mp3_path)

        if sr != target_sr:
            # fast resampling
            num_samples = int(len(data) * target_sr / sr)
            data = resample(data, num_samples)

        sf.write(wav_path, data, target_sr)
        return len(data) / target_sr

    except Exception as e:
        print(" Error:", mp3_path, e)
        return None
# Main pipeline
def main():
    download_zip()
    selected_files = extract_random_8()

    rows = []
    os.makedirs(CLEAN_DIR, exist_ok=True)

    for f in selected_files:
        mp3_path = os.path.join(EXTRACT_DIR, f)
        wav_path = os.path.join(CLEAN_DIR, f.replace(".mp3", ".wav"))

        duration = convert_to_wav(mp3_path, wav_path)

        if duration:
            rows.append({
                "file": f,
                "wav_path": wav_path,
                "duration_sec": round(duration, 2),
                "sampling_rate": 16000
            })

    # save metadata
    df = pd.DataFrame(rows)
    df.to_csv(METADATA_FILE, index=False)
    print("✔ Metadata saved:", METADATA_FILE)
if __name__ == "__main__":
    main()
