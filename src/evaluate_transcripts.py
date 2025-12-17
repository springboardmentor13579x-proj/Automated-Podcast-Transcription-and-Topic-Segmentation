import os
import re
import pandas as pd
from jiwer import wer, cer
from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv

# -----------------------------
# 0. LOAD ENV VARIABLES
# -----------------------------
load_dotenv()

# -----------------------------
# 1. FILE PATHS (FROM .env)
# -----------------------------
REFERENCE_FOLDER = os.getenv("REFERENCE_DIR")
TRANSCRIPTS_FOLDER = os.getenv("TRANSCRIPTS_DIR")
OUTPUT_FILE = os.getenv("EVALUATION_OUTPUT_FILE")

# -----------------------------
# 2. LOAD MODEL
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# 3. TEXT NORMALIZATION
# -----------------------------
def normalize(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# -----------------------------
# 4. LOAD REFERENCE TEXT FILES
# -----------------------------
def load_reference_texts():
    references = {}
    for file in os.listdir(REFERENCE_FOLDER):
        if file.endswith(".txt"):
            file_id = file.replace(".txt", "")
            with open(
                os.path.join(REFERENCE_FOLDER, file),
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as f:
                references[file_id] = normalize(f.read())
    return references

# -----------------------------
# 5. EVALUATE TRANSCRIPTS
# -----------------------------
def evaluate_transcripts():
    reference_texts = load_reference_texts()
    results = []

    for file in os.listdir(TRANSCRIPTS_FOLDER):
        if file.endswith(".txt"):
            file_id = file.replace(".txt", "")

            if file_id not in reference_texts:
                continue

            ref = reference_texts[file_id]

            with open(
                os.path.join(TRANSCRIPTS_FOLDER, file),
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as f:
                hyp = normalize(f.read())

            # Error metrics
            word_error_rate = wer(ref, hyp)
            char_error_rate = cer(ref, hyp)

            # Semantic similarity
            emb1 = model.encode(ref, convert_to_tensor=True)
            emb2 = model.encode(hyp, convert_to_tensor=True)
            similarity = float(util.cos_sim(emb1, emb2))

            # Meaning-focused accuracy
            accuracy = round(
                (similarity * 0.85 + (1 - word_error_rate) * 0.15) * 100,
                2
            )

            results.append({
                "File": file,
                "WER (%)": round(word_error_rate * 100, 2),
                "CER (%)": round(char_error_rate * 100, 2),
                "Semantic Similarity": round(similarity, 3),
                "Final Accuracy Score (%)": accuracy
            })

    df = pd.DataFrame(results)
    df.to_excel(OUTPUT_FILE, index=False)

    print(
        f"\nTranscript evaluation completed.\n"
        f"Results saved to:\n{OUTPUT_FILE}\n"
    )

# -----------------------------
# 6. MAIN
# -----------------------------
if __name__ == "__main__":
    evaluate_transcripts()
