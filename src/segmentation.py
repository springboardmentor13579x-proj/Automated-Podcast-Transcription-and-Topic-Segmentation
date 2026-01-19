import os
from nltk.tokenize import sent_tokenize

def segment_text(text, max_sentences=5):
    sentences = sent_tokenize(text)
    segments = []
    for i in range(0, len(sentences), max_sentences):
        chunk = " ".join(sentences[i:i+max_sentences])
        segments.append(chunk)
    return segments


def segment_transcripts(input_dir, output_dir, max_sentences=5):
    os.makedirs(output_dir, exist_ok=True)

    files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]
    if not files:
        print("No transcript files found.")
        return

    for file in files:
        in_path = os.path.join(input_dir, file)
        out_path = os.path.join(output_dir, file)

        with open(in_path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        segments = segment_text(text, max_sentences=max_sentences)

        with open(out_path, "w", encoding="utf-8") as f:
            for idx, seg in enumerate(segments, 1):
                f.write(f"[SEGMENT {idx}]\n{seg}\n\n")

        print("Segmented:", file)
