import os
import json
import nltk
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download("punkt")

# -----------------------------
# PATHS
# -----------------------------
SEGMENT_DIR = r"C:\Users\hp\Desktop\Automated transcription project\project\segments"
OUTPUT_DIR = r"C:\Users\hp\Desktop\Automated transcription project\project\Summarization"

# -----------------------------
def summarize_text(text, num_sentences=2):
    sentences = sent_tokenize(text)

    if len(sentences) <= num_sentences:
        return text

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform(sentences)
    scores = tfidf.sum(axis=1)

    ranked = sorted(
        [(float(scores[i]), i) for i in range(len(sentences))],
        reverse=True
    )

    top_ids = sorted([idx for _, idx in ranked[:num_sentences]])
    return " ".join([sentences[i] for i in top_ids])

# -----------------------------
def process_file(file_path, output_path):
    with open(file_path, "r", encoding="utf-8") as f:
        segments = json.load(f)

    for seg in segments:
        seg["summary"] = summarize_text(seg["text"])

    with open(output_path, "w", encoding="utf-8") as jf:
        json.dump(segments, jf, indent=4, ensure_ascii=False)

    print(f"✅ Summary saved → {output_path}")

# -----------------------------
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for file in os.listdir(SEGMENT_DIR):
        if file.endswith("_segments.json"):
            input_path = os.path.join(SEGMENT_DIR, file)
            output_path = os.path.join(
                OUTPUT_DIR,
                file.replace("_segments.json", "_summary.json")
            )
            process_file(input_path, output_path)

if __name__ == "__main__":
    main()
