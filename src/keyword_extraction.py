import json
import yake
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
META_FILE = PROJECT_ROOT / "docs" / "processing_metadata.json"

kw_extractor = yake.KeywordExtractor(n=2, top=10)

def extract_keywords(text):
    return [kw for kw, _ in kw_extractor.extract_keywords(text)]

def run_keywords():
    if not META_FILE.exists():
        raise RuntimeError("processing_metadata.json not found")

    metadata = json.loads(META_FILE.read_text())

    for key, data in metadata.items():

        if "segmentation" not in data:
            continue

        seg_file = Path(data["segmentation"]["segment_file"])
        if not seg_file.exists():
            continue

        segments = json.loads(seg_file.read_text())
        if not segments:
            continue

        for seg in segments:
            if "text" not in seg or not seg["text"].strip():
                seg["keywords"] = []
            else:
                seg["keywords"] = extract_keywords(seg["text"])

        seg_file.write_text(json.dumps(segments, indent=4))

        data["keywords"] = {
            "engine": "yake",
            "total_segments": len(segments),
            "status": "done"
        }

    META_FILE.write_text(json.dumps(metadata, indent=4))

if __name__ == "__main__":
    run_keywords()
