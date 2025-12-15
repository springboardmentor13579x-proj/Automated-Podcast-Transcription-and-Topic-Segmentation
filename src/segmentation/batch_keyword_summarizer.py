import os
import json
from src.segmentation.keywords import keyword_extractor
from src.segmentation.summarizer import summarize_segment


def align_segments(segments, whisper_segments):
    aligned = []

    for seg_id, seg_text in enumerate(segments, start=1):
        seg_text = seg_text.strip()
        seg_start = None
        seg_end = None

        # Match start prefix
        for ws in whisper_segments:
            if ws["text"].strip().startswith(seg_text[:20]):
                seg_start = ws["start"]
                break

        # Match end suffix
        for ws in reversed(whisper_segments):
            if ws["text"].strip().endswith(seg_text[-20:]):
                seg_end = ws["end"]
                break

        aligned.append({
            "segment_id": seg_id,
            "text": seg_text,
            "start_time": seg_start,
            "end_time": seg_end
        })

    return aligned


SEGMENT_DIR = "data/segments"
WHISPER_DIR = "data/transcripts"
OUTPUT_DIR = "database"


def process_all_segments():

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    files = [f for f in os.listdir(SEGMENT_DIR) if f.endswith("_segments.json")]

    for file in files:
        print(f"📌 Processing: {file}")

        seg_path = os.path.join(SEGMENT_DIR, file)

        # Load segmentation file
        with open(seg_path, "r", encoding="utf-8") as f:
            seg_data = json.load(f)

        # Load whisper timestamps
        whisper_file = file.replace("_cleaned_segments.json", "_cleaned.json")
        whisper_path = os.path.join(WHISPER_DIR, whisper_file)

        with open(whisper_path, "r", encoding="utf-8") as f:
            whisper_data = json.load(f)

        whisper_segments = whisper_data.get("segments", [])

        # Choose segmentation algorithm
        text_segments = seg_data["bert_segments"]

        # Align timestamps
        aligned_segments = align_segments(text_segments, whisper_segments)

        # Output list for THIS file
        final_output = []

        for seg in aligned_segments:
            summary = summarize_segment(seg["text"])
            keywords = keyword_extractor(seg["text"])

            record = {
                "file": whisper_file,
                "segment_id": seg["segment_id"],
                "text": seg["text"],
                "summary": summary,
                "keywords": keywords,
                "start_time": seg["start_time"],
                "end_time": seg["end_time"]
            }

            final_output.append(record)

        # ----------- OUTPUT FILE NAME FIX ✔ ----------- #
        output_filename = file.replace("_cleaned_segments.json", "_segments.json")
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        # ------------------------------------------------ #

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(final_output, f, indent=4)

        print(f"✅ Saved: {output_path}")

    print("\n🎉 All keyword extraction, summarization & timestamp alignment completed!")


if __name__ == "__main__":
    process_all_segments()
