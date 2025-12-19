import os
import json
import nltk
import textwrap
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from datetime import timedelta
from keybert import KeyBERT
from faster_whisper import WhisperModel

# ================= PATHS =================
TRANSCRIPT_DIR = r"C:/Users/Dell/Desktop/meeting_workspace/transcripts"
AUDIO_DIR = r"C:/Users/Dell/Desktop/meeting_workspace/clean_wav"
OUTPUT_DIR = r"C:/Users/Dell/Desktop/meeting_workspace/summaries"

# ================= SETUP =================
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

stop_words = set(stopwords.words("english"))

kw_model = KeyBERT("all-MiniLM-L6-v2")

whisper = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)

# ================= HELPERS =================
def format_time(sec):
    return str(timedelta(seconds=int(sec)))

def clean_text(text):
    return " ".join(
        line.strip()
        for line in text.splitlines()
        if line.strip() and line.strip() not in [".", "..", "..."]
    )

def normalize_base(filename):
    return (
        filename.replace("_safe_transcription.txt", "")
                .replace("_transcription.txt", "")
                .replace(".txt", "")
    )

# ================= KEYWORDS =================
def extract_keywords(text, top_n=5):
    if not text.strip():
        return []
    try:
        return [k[0] for k in kw_model.extract_keywords(text, top_n=top_n)]
    except:
        return []

# ================= NLP SUMMARY =================
def generate_summary(sentences, max_sentences=5):
    words = []
    for s in sentences:
        words += [
            w.lower() for w in word_tokenize(s)
            if w.isalnum() and w.lower() not in stop_words
        ]

    if not words:
        return ""

    freq = Counter(words)
    scores = {}

    for sent in sentences:
        score = sum(freq.get(w.lower(), 0) for w in word_tokenize(sent))
        scores[sent] = score

    ranked = sorted(scores, key=scores.get, reverse=True)
    top = ranked[:max_sentences]

    summary_sents = [s for s in sentences if s in top]
    paragraph = " ".join(summary_sents)

    return textwrap.fill(paragraph, width=90)

# ================= AUDIO TIMESTAMPS =================
def get_audio_segments(audio_path):
    print(f"🎧 Aligning audio: {os.path.basename(audio_path)}")
    segments, _ = whisper.transcribe(
        audio_path,
        vad_filter=True,
        beam_size=1
    )
    return list(segments)

# ================= PROCESS FILE =================
def process_file(txt_path):
    filename = os.path.basename(txt_path)
    base = normalize_base(filename)
    audio_path = os.path.join(AUDIO_DIR, base + ".wav")

    if not os.path.exists(audio_path):
        print(f"Audio missing: {filename}")
        return

    with open(txt_path, "r", encoding="utf-8") as f:
        text = clean_text(f.read())

    sentences = sent_tokenize(text)
    audio_segments = get_audio_segments(audio_path)

    segments_out = []
    last_time = 0

    for i, sent in enumerate(sentences):
        if i < len(audio_segments):
            last_time = int(audio_segments[i].start)
        else:
            last_time += 1  # fallback

        segment_keywords = extract_keywords(sent)

        segments_out.append({
            "timestamp": format_time(last_time),
            "text": textwrap.fill(sent, width=90),
            "keywords": segment_keywords
        })

    summary = generate_summary(sentences)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, base + ".json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "filename": filename,
            "segments": segments_out,
            "summary": summary
        }, f, indent=4, ensure_ascii=False)

    print(f"✔ Saved: {out_path}")

# ================= MAIN =================
def main():
    print("Processing with REAL audio alignment...")
    for f in os.listdir(TRANSCRIPT_DIR):
        if f.endswith(".txt"):
            process_file(os.path.join(TRANSCRIPT_DIR, f))
    print("Done.")

if __name__ == "__main__":
    main()
