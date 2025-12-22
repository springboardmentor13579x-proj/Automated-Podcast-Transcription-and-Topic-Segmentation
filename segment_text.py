import os
import nltk
from nltk.tokenize import sent_tokenize

nltk.download("punkt")

INPUT_DIR = "../transcripts/predicted/"
OUTPUT_DIR = "../segmented/"

os.makedirs(OUTPUT_DIR, exist_ok=True)

for file in os.listdir(INPUT_DIR):
    if not file.endswith(".txt"):
        continue

    with open(os.path.join(INPUT_DIR, file), "r", encoding="utf-8") as f:
        text = f.read().strip()

    sentences = sent_tokenize(text)

    out_file = file.replace(".txt", "_segments.txt")
    with open(os.path.join(OUTPUT_DIR, out_file), "w", encoding="utf-8") as f:
        for i, sent in enumerate(sentences, 1):
            f.write(f"{i}. {sent}\n")

    print(f"Segmented: {file}")