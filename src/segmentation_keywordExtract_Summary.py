import os
import json
from pydub import AudioSegment
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk

# Download tokenizer
nltk.download("punkt")

# -----------------------------
# Get audio duration (seconds)
# -----------------------------
def get_audio_duration(audio_path):
    try:
        audio = AudioSegment.from_file(audio_path)
        return len(audio) / 1000
    except:
        return None

# -----------------------------
# Segment transcript text
# -----------------------------
def segment_text(text, sentences_per_segment=5):
    sentences = sent_tokenize(text)
    return [
        " ".join(sentences[i:i + sentences_per_segment])
        for i in range(0, len(sentences), sentences_per_segment)
    ]

# -----------------------------
# Match audio file
# -----------------------------
def find_audio_file(audio_dir, transcript_file):
    base_name = transcript_file.replace(".txt", "").lower()
    for file in os.listdir(audio_dir):
        if file.lower().endswith(".mp3") and base_name in file.lower():
            return os.path.join(audio_dir, file)
    return None

# -----------------------------
# Keyword extraction
# -----------------------------
def extract_keywords(text, top_k=5):
    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf = vectorizer.fit_transform([text])
        scores = tfidf.toarray()[0]
        words = vectorizer.get_feature_names_out()
        top_idx = scores.argsort()[-top_k:][::-1]
        return [words[i] for i in top_idx]
    except:
        return []

# -----------------------------
# Text summarization
# -----------------------------
def summarize_text(text, num_sentences=2):
    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text
    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf = vectorizer.fit_transform(sentences)
        scores = tfidf.sum(axis=1)
        ranked = sorted(
            [(float(scores[i]), i) for i in range(len(sentences))],
            reverse=True
        )
        top_ids = sorted([idx for _, idx in ranked[:num_sentences]])
        return " ".join([sentences[i] for i in top_ids])
    except:
        return "Summary not available."

# -----------------------------
# Process single transcript
# -----------------------------
def process_single_file(transcript_path, audio_dir, output_dir):
    transcript_name = os.path.basename(transcript_path)
    audio_path = find_audio_file(audio_dir, transcript_name)

    if audio_path is None:
        print(f"Audio not found for {transcript_name}")
        return

    with open(transcript_path, "r", encoding="utf-8") as f:
        text = f.read()

    segments = segment_text(text)
    audio_duration = get_audio_duration(audio_path)
    sec_per_segment = audio_duration / len(segments) if audio_duration else None

    json_segments = []

    for idx, seg in enumerate(segments, start=1):
        if sec_per_segment:
            start = (idx - 1) * sec_per_segment
            end = start + sec_per_segment
        else:
            start = end = None

        json_segments.append({
            "segment_id": idx,
            "start_time": round(start, 2) if start is not None else None,
            "end_time": round(end, 2) if end is not None else None,
            "text": seg,
            "keywords": extract_keywords(seg),
            "summary": summarize_text(seg)
        })

    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(
        output_dir, transcript_name.replace(".txt", "_segments.json")
    )

    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(json_segments, jf, indent=4, ensure_ascii=False)

    print(f"Saved JSON → {json_path}")

# -----------------------------
# Process all transcripts
# -----------------------------
def process_all_transcripts(transcript_dir, audio_dir, output_dir):
    for file in os.listdir(transcript_dir):
        if file.endswith(".txt"):
            process_single_file(
                os.path.join(transcript_dir, file),
                audio_dir,
                output_dir
            )

# -----------------------------
# MAIN
# -----------------------------
def main():
    TRANSCRIPT_DIR = r"C:\Users\USER\OneDrive\Desktop\Project\transcripts"
    AUDIO_DIR = r"C:\Users\USER\OneDrive\Desktop\Project\audio_processed"
    OUTPUT_DIR = r"C:\Users\USER\OneDrive\Desktop\Project\segments_keywordExtract_summary"

    process_all_transcripts(TRANSCRIPT_DIR, AUDIO_DIR, OUTPUT_DIR)

if __name__ == "__main__":
    main()
