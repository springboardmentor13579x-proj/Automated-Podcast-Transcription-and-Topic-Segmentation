import os
import re
import pandas as pd
from jiwer import wer, cer
from sentence_transformers import SentenceTransformer, util

# -----------------------------
# 1. FILE PATHS
# -----------------------------
REFERENCE_FOLDER = r"C:\Users\venka\OneDrive\Desktop\MedicalPodcastAI\Clean_Transcripts"
TRANSCRIPTS_FOLDER = r"C:\Users\venka\OneDrive\Desktop\MedicalPodcastAI\transcripts"
OUTPUT_FILE = r"C:\Users\venka\OneDrive\Desktop\MedicalPodcastAI\final_evaluation.xlsx"

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
# 5. CHECK IF EVALUATION EXISTS
# -----------------------------
def evaluation_data_exists():
    return os.path.exists(OUTPUT_FILE)

# -----------------------------
# 6. LOAD SUMMARY ONLY (NO RE-COMPUTE)
# -----------------------------
def load_evaluation_summary():
    df = pd.read_excel(OUTPUT_FILE)

    return {
        "avg_accuracy": round(df["Final Accuracy Score (%)"].mean(), 2),
        "avg_wer": round(df["WER (%)"].mean(), 2),
        "avg_cer": round(df["CER (%)"].mean(), 2),
        "avg_similarity": round(df["Semantic Similarity"].mean() * 100, 2)
    }

# -----------------------------
# 7. EVALUATE TRANSCRIPTS
# -----------------------------
def evaluate_transcripts(load_only=False):
    """
    load_only=True  → only load stored Excel
    load_only=False → compute evaluation once
    """

    # UI / QUALITY TAB CALL
    if load_only:
        return load_evaluation_summary()

    #  PREVENT RE-COMPUTATION
    if evaluation_data_exists():
        return load_evaluation_summary()

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

            word_error_rate = wer(ref, hyp)
            char_error_rate = cer(ref, hyp)

            emb1 = model.encode(ref, convert_to_tensor=True)
            emb2 = model.encode(hyp, convert_to_tensor=True)
            similarity = float(util.cos_sim(emb1, emb2))

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

    print(f"\nTranscript evaluation completed.\nSaved to:\n{OUTPUT_FILE}\n")

    return load_evaluation_summary()

# -----------------------------
# 8. MAIN (BATCH MODE ONLY)
# -----------------------------
if __name__ == "__main__":
    evaluate_transcripts()
