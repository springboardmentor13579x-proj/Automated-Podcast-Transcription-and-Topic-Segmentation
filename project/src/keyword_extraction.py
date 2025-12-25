import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer

# -----------------------------
# PATHS
# -----------------------------
SEGMENTS_DIR = r"C:\Users\hp\Desktop\Automated transcription project\project\segments"
OUTPUT_DIR = r"C:\Users\hp\Desktop\Automated transcription project\project\keyword"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# Keyword Extraction Function
# -----------------------------
def extract_keywords(text, top_k=5):
    if not text.strip():
        return []

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=50
    )

    tfidf = vectorizer.fit_transform([text])
    scores = tfidf.toarray()[0]
    words = vectorizer.get_feature_names_out()

    top_indices = scores.argsort()[-top_k:][::-1]
    return [words[i] for i in top_indices]

# -----------------------------
# Process One File
# -----------------------------
def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        segments = json.load(f)

    for seg in segments:
        seg["keywords"] = extract_keywords(seg.get("text", ""))

    file_name = os.path.basename(file_path)
    out_path = os.path.join(OUTPUT_DIR, file_name)

    with open(out_path, "w", encoding="utf-8") as jf:
        json.dump(segments, jf, indent=4, ensure_ascii=False)

    print(f"✅ Keywords saved → {out_path}")

# -----------------------------
# MAIN
# -----------------------------
def main():
    for file in os.listdir(SEGMENTS_DIR):
        if file.endswith("_segments.json"):
            process_file(os.path.join(SEGMENTS_DIR, file))

if __name__ == "__main__":
    main()
