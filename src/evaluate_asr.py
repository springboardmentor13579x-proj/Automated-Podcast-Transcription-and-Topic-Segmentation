import os
import re
from jiwer import wer, cer

REFERENCE_DIR = "transcripts/raw_reference"
HYPOTHESIS_DIR = "transcripts/asr"
DOCS_DIR = "docs"

os.makedirs(DOCS_DIR, exist_ok=True)

def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def evaluate_asr():
    ref_files = [f for f in os.listdir(REFERENCE_DIR) if f.endswith(".txt")]

    if not ref_files:
        print("No reference transcripts found.")
        return

    csv_path = os.path.join(DOCS_DIR, "asr_evaluation.csv")
    table_path = os.path.join(DOCS_DIR, "asr_evaluation_table.txt")

    rows = []

    for ref_file in ref_files:
        ref_path = os.path.join(REFERENCE_DIR, ref_file)
        hyp_path = os.path.join(HYPOTHESIS_DIR, ref_file)

        if not os.path.exists(hyp_path):
            print("Missing ASR file:", ref_file)
            continue

        with open(ref_path, "r", encoding="utf-8") as f:
            ref_text = normalize_text(f.read())

        with open(hyp_path, "r", encoding="utf-8") as f:
            hyp_text = normalize_text(f.read())

        w = wer(ref_text, hyp_text)
        c = cer(ref_text, hyp_text)
        accuracy = (1 - w) * 100

        rows.append((ref_file, w, c, accuracy))

        print(f"{ref_file} | WER: {w:.4f} | Accuracy: {accuracy:.2f}%")

    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("file,wer,cer,accuracy_percent\n")
        for r in rows:
            f.write(f"{r[0]},{r[1]:.4f},{r[2]:.4f},{r[3]:.2f}\n")

    with open(table_path, "w", encoding="utf-8") as f:
        f.write(f"{'File':30} {'WER':10} {'CER':10} {'Accuracy (%)':15}\n")
        f.write("-" * 70 + "\n")
        for r in rows:
            f.write(f"{r[0]:30} {r[1]:<10.4f} {r[2]:<10.4f} {r[3]:<15.2f}\n")

    print("\nSaved:")
    print(csv_path)
    print(table_path)

if __name__ == "__main__":
    evaluate_asr()
