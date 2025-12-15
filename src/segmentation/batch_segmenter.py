import os
import json

from src.segmentation.text_tiling import text_tiling_segments
from src.segmentation.bert_segmentation import bert_topic_segments

TRANSCRIPT_DIR = "data/transcripts"
SEGMENT_OUTPUT_DIR = "data/segments"

os.makedirs(SEGMENT_OUTPUT_DIR, exist_ok=True)


def load_transcript(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return " ".join([seg["text"] for seg in data["segments"]])


def segment_all_files():
    files = os.listdir(TRANSCRIPT_DIR)

    for file in files:
        if file.endswith(".json"):
            input_path = os.path.join(TRANSCRIPT_DIR, file)

            print(f"\n📌 Segmenting: {file}")

            text = load_transcript(input_path)

            # Run both algorithms
            tt = text_tiling_segments(text)
            bert = bert_topic_segments(text)

            # Save results
            output = {
                "file": file,
                "texttiling_segments": tt,
                "bert_segments": bert,
                "num_texttiling": len(tt),
                "num_bert": len(bert),
            }

            output_filename = file.replace(".json", "_segments.json")
            output_path = os.path.join(SEGMENT_OUTPUT_DIR, output_filename)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=4)

            print(f"✔ Saved segments → {output_path}")


if __name__ == "__main__":
    segment_all_files()
