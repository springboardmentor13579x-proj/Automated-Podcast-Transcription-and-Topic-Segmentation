import os
import json
import math
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DOCS_DIR = PROJECT_ROOT / "docs"
SEGMENTS_DIR = PROJECT_ROOT / "segments"

META_FILE = DOCS_DIR / "processing_metadata.json"

SEGMENTS_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)

MODEL_NAME = os.getenv(
    "SENTENCE_TRANSFORMER_MODEL",
    "all-MiniLM-L6-v2"  # fast + good for long text
)

SIMILARITY_THRESHOLD = float(os.getenv("SEGMENT_SIM_THRESHOLD", 0.75))
MIN_SENTENCES_PER_SEGMENT = int(os.getenv("MIN_SENTENCES_PER_SEGMENT", 4))
BATCH_SIZE = int(os.getenv("EMBEDDING_BATCH_SIZE", 32))

model = SentenceTransformer(MODEL_NAME)

def load_metadata():
    if not META_FILE.exists():
        return {}
    return json.loads(META_FILE.read_text())

def save_metadata(data):
    META_FILE.write_text(json.dumps(data, indent=4))

def batched_encode(texts, batch_size):
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        emb = model.encode(batch, show_progress_bar=False)
        embeddings.extend(emb)
    return embeddings


def segment_text(chunks):
    if len(chunks) < 2:
        return []

    texts = [c["text"] for c in chunks]

    embeddings = batched_encode(texts, BATCH_SIZE)

    boundaries = [0]
    last_boundary = 0

    for i in range(1, len(embeddings)):
        sim = cosine_similarity(
            [embeddings[i - 1]],
            [embeddings[i]]
        )[0][0]

        segment_length = i - last_boundary

        if (
            sim < SIMILARITY_THRESHOLD
            and segment_length >= MIN_SENTENCES_PER_SEGMENT
        ):
            boundaries.append(i)
            last_boundary = i

    boundaries.append(len(chunks))

    segments = []
    for i in range(len(boundaries) - 1):
        seg_chunks = chunks[boundaries[i]:boundaries[i + 1]]

        segments.append({
            "start": seg_chunks[0]["start"],
            "end": seg_chunks[-1]["end"],
            "text": " ".join(c["text"] for c in seg_chunks),
            "sentence_count": len(seg_chunks)
        })

    return segments

def run_segmentation():
    metadata = load_metadata()
    updated = False

    for file_key, data in metadata.items():
        if "transcription" not in data:
            continue

        if "segmentation" in data:
            continue

        chunks = data["transcription"].get("chunks", [])
        if not chunks:
            continue

        print(f"Segmenting: {file_key}")

        segments = segment_text(chunks)

        seg_file = SEGMENTS_DIR / f"{file_key}_segments.json"
        seg_file.write_text(json.dumps(segments, indent=4))

        data["segmentation"] = {
            "segment_file": str(seg_file),
            "total_segments": len(segments),
            "similarity_threshold": SIMILARITY_THRESHOLD,
            "min_sentences_per_segment": MIN_SENTENCES_PER_SEGMENT,
            "model": MODEL_NAME,
            "status": "done"
        }

        updated = True

    if updated:
        save_metadata(metadata)
        print("Segmentation completed")
    else:
        print("No new files to segment")

if __name__ == "__main__":
    run_segmentation()
