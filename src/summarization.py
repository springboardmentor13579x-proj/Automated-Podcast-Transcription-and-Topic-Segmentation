# src/summarization.py
import os
import re
from nltk.tokenize import sent_tokenize

SEGMENTS_DIR = "segments"
FINAL_DIR = "transcripts/final"

os.makedirs(FINAL_DIR, exist_ok=True)

def clean_text(text):
    # Remove SEGMENT labels
    text = re.sub(r"\[?\s*segment\s*\d*\]?", "", text, flags=re.IGNORECASE)

    # Remove timestamps
    text = re.sub(r"\b\d{1,2}:\d{2}(:\d{2})?\b", "", text)

    # Remove excessive spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


def summarize_text(text, max_sentences=5):
    text = clean_text(text)
    sentences = sent_tokenize(text)
    return " ".join(sentences[:max_sentences])


def summarize_segments():
    files = [f for f in os.listdir(SEGMENTS_DIR) if f.endswith(".txt")]

    if not files:
        print("No segmented files found.")
        return

    for file in files:
        in_path = os.path.join(SEGMENTS_DIR, file)
        out_path = os.path.join(FINAL_DIR, file)

        with open(in_path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        summary = summarize_text(text)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(summary)

        print("Summarized:", file)


if __name__ == "__main__":
    summarize_segments()
