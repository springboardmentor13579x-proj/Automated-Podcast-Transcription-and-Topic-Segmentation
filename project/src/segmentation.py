import os
import json
import nltk
from nltk.tokenize import sent_tokenize
from pydub import AudioSegment

# -----------------------------
# DOWNLOAD NLTK TOKENIZER
# -----------------------------
nltk.download("punkt")

# -----------------------------
# ABSOLUTE BASE PATH
# -----------------------------
BASE_DIR = r"C:\Users\hp\Desktop\Automated transcription project\project"

TRANSCRIPT_DIR = os.path.join(BASE_DIR, "transcripts")
AUDIO_DIR = os.path.join(BASE_DIR, "cleaned_audio")  # change if needed
OUTPUT_DIR = os.path.join(BASE_DIR, "segments")

# -----------------------------
# GET AUDIO DURATION
# -----------------------------
def get_audio_duration(audio_path):
    try:
        audio = AudioSegment.from_file(audio_path)
        return len(audio) / 1000  # seconds
    except Exception as e:
        print(f"Audio read error: {audio_path}")
        return None

# -----------------------------
# TEXT SEGMENTATION
# -----------------------------
def segment_text(text, sentences_per_segment=5):
    sentences = sent_tokenize(text)

    if len(sentences) == 0:
        return []

    return [
        " ".join(sentences[i:i + sentences_per_segment])
        for i in range(0, len(sentences), sentences_per_segment)
    ]

# -----------------------------
# FIND MATCHING AUDIO FILE
# -----------------------------
def find_audio_file(base_name):
    for file in os.listdir(AUDIO_DIR):
        if file.lower().startswith(base_name.lower()):
            return os.path.join(AUDIO_DIR, file)
    return None

# -----------------------------
# PROCESS ONE TRANSCRIPT
# -----------------------------
def process_file(transcript_file):
    base_name = transcript_file.replace(".txt", "")
    audio_path = find_audio_file(base_name)

    if not audio_path:
        print(f"Audio not found for {base_name}")
        return

    transcript_path = os.path.join(TRANSCRIPT_DIR, transcript_file)

    with open(transcript_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print(f"Empty transcript: {transcript_file}")
        return

    segments = segment_text(text)

    if len(segments) == 0:
        print(f"No segments created for {transcript_file}")
        return

    duration = get_audio_duration(audio_path)

    if not duration:
        print(f"Could not get duration for {audio_path}")
        return

    sec_per_segment = duration / len(segments)

    output = []
    for i, seg in enumerate(segments):
        start = i * sec_per_segment
        end = start + sec_per_segment

        output.append({
            "segment_id": i + 1,
            "start_time": round(start, 2),
            "end_time": round(end, 2),
            "text": seg
        })

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, base_name + "_segments.json")

    with open(out_path, "w", encoding="utf-8") as jf:
        json.dump(output, jf, indent=4, ensure_ascii=False)

    print(f"✅ Segments saved → {out_path}")

# -----------------------------
# MAIN
# -----------------------------
def main():
    for file in os.listdir(TRANSCRIPT_DIR):
        if file.endswith(".txt"):
            process_file(file)

if __name__ == "__main__":
    main()
