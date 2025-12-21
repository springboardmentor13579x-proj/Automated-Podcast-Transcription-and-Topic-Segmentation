import re
from jiwer import wer, cer
from sentence_transformers import SentenceTransformer, util

# Load once
model = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------------------------------------
# NORMALIZATION
# -------------------------------------------------
def normalize_text(text):
    if not text or not text.strip():
        return ""

    text = text.lower()
    text = re.sub(r"\[[^\]]+\]", "", text)      # timestamps
    text = re.sub(r"\b(d|p):", "", text)        # speaker labels
    text = re.sub(r"[^\w\s]", "", text)         # punctuation
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# -------------------------------------------------
# FINAL QUALITY EVALUATION (SAFE)
# -------------------------------------------------
def get_evaluation_summary_for_ui(predicted_text, reference_text):

    # --------- HARD GUARD ----------
    if not reference_text or not reference_text.strip():
        return {
            "avg_accuracy": 0.0,
            "avg_wer": 100.0,
            "avg_cer": 100.0,
            "avg_similarity": 0.0
        }

    pred_clean = normalize_text(predicted_text)
    ref_clean = normalize_text(reference_text)

    # --------- EMPTY CHECK ----------
    if not pred_clean or not ref_clean:
        return {
            "avg_accuracy": 0.0,
            "avg_wer": 100.0,
            "avg_cer": 100.0,
            "avg_similarity": 0.0
        }

    # --------- WER ----------
    wer_score = wer(ref_clean, pred_clean)
    wer_pct = wer_score * 100
    wer_accuracy = max(0.0, (1 - wer_score) * 100)

    # --------- CER ----------
    cer_score = cer(ref_clean, pred_clean)
    cer_pct = cer_score * 100

    # --------- SEMANTIC ----------
    emb_ref = model.encode(ref_clean, convert_to_tensor=True)
    emb_pred = model.encode(pred_clean, convert_to_tensor=True)
    similarity = util.cos_sim(emb_ref, emb_pred).item() * 100

    # --------- FINAL ACCURACY ----------
    final_accuracy = (0.5 * wer_accuracy) + (0.5 * similarity)

    return {
        "avg_accuracy": round(final_accuracy, 2),
        "avg_wer": round(wer_pct, 2),
        "avg_cer": round(cer_pct, 2),
        "avg_similarity": round(similarity, 2)
    }
