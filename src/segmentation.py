import os
import json
import re
from transformers import pipeline
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

# ---------------------------------------------------------
# 1. LOAD MODELS (SAFE & STABLE)
# ---------------------------------------------------------

# Summarization model
summarizer = pipeline(
    "summarization",
    model="facebook/bart-base",
    device=-1  # CPU safe
)

# Keyword extraction model
kw_model = KeyBERT(
    model=SentenceTransformer("all-MiniLM-L6-v2")
)

# ---------------------------------------------------------
# 2. TIMESTAMP PATTERN (WHISPER FORMAT)
# ---------------------------------------------------------
timestamp_pattern = re.compile(
    r"\[(\d{2}:\d{2}\.\d{2})\s*-\s*(\d{2}:\d{2}\.\d{2})\]\s*(.*)"
)

# ---------------------------------------------------------
# 3. PARSE TRANSCRIPT (WITH SAFE MERGING)
# ---------------------------------------------------------
def parse_transcript(text):
    parsed = []
    prev = None

    for line in text.splitlines():
        match = timestamp_pattern.match(line)
        if not match:
            continue

        start, end, sentence = match.groups()
        sentence = sentence.strip()

        # Merge broken continuation lines
        if prev and sentence and sentence[0].islower():
            prev["text"] += " " + sentence
            prev["end"] = end
        else:
            prev = {
                "start": start,
                "end": end,
                "text": sentence
            }
            parsed.append(prev)

    return parsed

# ---------------------------------------------------------
# 4. SENTENCE → SEGMENT LOGIC
# ---------------------------------------------------------
def segment_sentences(sentences, max_words=120):
    segments = []
    current_text = []
    start_time = None

    for s in sentences:
        if start_time is None:
            start_time = s["start"]

        combined = " ".join(current_text + [s["text"]])
        if len(combined.split()) <= max_words:
            current_text.append(s["text"])
            end_time = s["end"]
        else:
            segments.append({
                "start_time": start_time,
                "end_time": end_time,
                "text": " ".join(current_text)
            })
            current_text = [s["text"]]
            start_time = s["start"]
            end_time = s["end"]

    if current_text:
        segments.append({
            "start_time": start_time,
            "end_time": end_time,
            "text": " ".join(current_text)
        })

    return segments

# ---------------------------------------------------------
# 5. SAFE SUMMARIZATION
# ---------------------------------------------------------
def summarise(text):
    text = text[:800]  # hard safety limit
    result = summarizer(
        text,
        max_length=40,
        min_length=20,
        do_sample=False
    )
    return result[0]["summary_text"]

# ---------------------------------------------------------
# 6. CLEAN KEYWORDS
# ---------------------------------------------------------
def clean_keywords(keywords):
    cleaned = []
    for k in keywords:
        k = re.sub(r"[^a-zA-Z0-9\s]", "", k).strip().lower()
        if len(k) > 2:
            cleaned.append(k)
    return list(dict.fromkeys(cleaned))

# ---------------------------------------------------------
# 7. EXTRACT KEYWORDS
# ---------------------------------------------------------
def extract_keywords(text):
    if not text or not text.strip():
        return []

    raw = kw_model.extract_keywords(text, top_n=8)
    return clean_keywords([k[0] for k in raw])

# ---------------------------------------------------------
# 8. FULL SEGMENTATION + KEYWORDS PIPELINE
# ---------------------------------------------------------
def generate_segmentation(raw_text):

    parsed = parse_transcript(raw_text)
    segments = segment_sentences(parsed)

    output = {"segments": []}

    for idx, seg in enumerate(segments, start=1):
        summary = summarise(seg["text"])
        keywords = extract_keywords(seg["text"])

        output["segments"].append({
            "segment_id": idx,
            "segment_label": summary[:45],
            "segment_summary": summary,
            "start_time": seg["start_time"],
            "end_time": seg["end_time"],
            "segment_text": seg["text"],
            "keywords": keywords      #  INCLUDED HERE
        })

    return output

# ---------------------------------------------------------
# 9. WRAPPER FOR FLASK / UI
# ---------------------------------------------------------
def generate_segmentation_for_ui(transcript_text):
    return generate_segmentation(transcript_text)

# ---------------------------------------------------------
# 10. BATCH MODE (OPTIONAL)
# ---------------------------------------------------------
def main():

    transcripts_dir = r"C:\Users\venka\OneDrive\Desktop\MedicalPodcastAI\transcripts"
    output_dir = r"C:\Users\venka\OneDrive\Desktop\MedicalPodcastAI\segments"

    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(transcripts_dir):
        if not file.endswith(".txt"):
            continue

        with open(os.path.join(transcripts_dir, file), "r", encoding="utf-8") as f:
            raw_text = f.read()

        result = generate_segmentation(raw_text)

        out_path = os.path.join(
            output_dir, file.replace(".txt", ".json")
        )

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)

        print("Processed:", file)

    print("Segmentation + keywords completed!")

if __name__ == "__main__":
    main()
