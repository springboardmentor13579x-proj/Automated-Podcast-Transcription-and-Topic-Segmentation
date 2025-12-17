import os
import json
import re
from nltk.tokenize import sent_tokenize
from transformers import pipeline
from dotenv import load_dotenv

# ---------------------------------------------------------
# LOAD ENV VARIABLES
# ---------------------------------------------------------
load_dotenv()

# ---------------------------------------------------------
# 1. LOAD VALID & STABLE SUMMARIZATION MODEL
# ---------------------------------------------------------
summarizer = pipeline(
    "summarization",
    model="facebook/bart-base",
    device=-1
)

# ---------------------------------------------------------
# 2. EXTRACT TIMESTAMPS FROM WHISPER TRANSCRIPTS
# ---------------------------------------------------------
timestamp_pattern = re.compile(
    r"\[(\d{2}:\d{2}\.\d{2})\s*-\s*(\d{2}:\d{2}\.\d{2})\]\s*(.*)"
)

def parse_transcript(text):
    parsed = []
    for line in text.splitlines():
        match = timestamp_pattern.match(line)
        if match:
            start, end, sentence = match.groups()
            parsed.append({
                "start": start,
                "end": end,
                "text": sentence.strip()
            })
    return parsed

# ---------------------------------------------------------
# 3. SENTENCE-BASED SEGMENTATION
# ---------------------------------------------------------
def segment_sentences(sentences, max_words=120):
    segments = []
    current_text = []
    start_time = None

    for s in sentences:
        if start_time is None:
            start_time = s["start"]

        words = " ".join(current_text + [s["text"]]).split()

        if len(words) <= max_words:
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
# 4. SAFE SUMMARIZATION
# ---------------------------------------------------------
def summarise(text):
    text = text[:800]
    result = summarizer(
        text,
        max_length=40,
        min_length=20,
        do_sample=False
    )
    return result[0]["summary_text"]

# ---------------------------------------------------------
# 5. FULL SEGMENTATION PIPELINE
# ---------------------------------------------------------
def generate_segmentation(raw_text):
    parsed_sentences = parse_transcript(raw_text)
    segments = segment_sentences(parsed_sentences)

    output = {"segments": []}

    for idx, seg in enumerate(segments, start=1):
        summary = summarise(seg["text"])

        output["segments"].append({
            "segment_id": idx,
            "segment_label": summary[:45],
            "segment_summary": summary,
            "start_time": seg["start_time"],
            "end_time": seg["end_time"],
            "segment_text": seg["text"]
        })

    return output

# ---------------------------------------------------------
# 6. PROCESS ALL TRANSCRIPTS
# ---------------------------------------------------------
def main():

    transcripts_dir = os.getenv("TRANSCRIPTS_DIR")
    output_dir = os.getenv("SEGMENTS_DIR")

    os.makedirs(output_dir, exist_ok=True)

    print("Starting topic segmentation with timestamps...")

    for file in os.listdir(transcripts_dir):
        if file.endswith(".txt"):
            input_path = os.path.join(transcripts_dir, file)
            output_path = os.path.join(output_dir, file.replace(".txt", ".json"))

            with open(input_path, "r", encoding="utf-8") as f:
                raw_text = f.read()

            result = generate_segmentation(raw_text)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4)

            print("Processed:", file)

    print("Segmentation completed successfully!")

# ---------------------------------------------------------
# RUN
# ---------------------------------------------------------
if __name__ == "__main__":
    main()
