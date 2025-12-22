import os
import csv
from jiwer import wer, cer

TRANSCRIPTS_DIR = "../transcripts/predicted/"
GROUND_TRUTH_FILE = "../ground_truth/pg1661_clean.txt"
REPORT_FILE = "../evaluation_report.csv"

def clean_for_csv(text):
    return text.replace("\n", " ").replace("\r", " ").strip()

with open(GROUND_TRUTH_FILE, "r", encoding="utf-8") as f:
    ground_truth_text = clean_for_csv(f.read())

with open(REPORT_FILE, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(["file", "WER", "CER", "predicted", "ground_truth"])

    for file_name in os.listdir(TRANSCRIPTS_DIR):
        if not file_name.endswith(".txt"):
            continue

        with open(os.path.join(TRANSCRIPTS_DIR, file_name), "r", encoding="utf-8") as f:
            predicted_text = clean_for_csv(f.read())

        if not predicted_text:
            continue

        wer_score = wer(ground_truth_text, predicted_text)
        cer_score = cer(ground_truth_text, predicted_text)

        writer.writerow([
            file_name,
            round(wer_score, 3),
            round(cer_score, 3),
            predicted_text,
            ground_truth_text
        ])

print("✅ evaluation_report.csv created correctly")