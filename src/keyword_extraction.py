import os
import json
import pandas as pd
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# ---------------------------------------------------------
# 0. LOAD ENV VARIABLES
# ---------------------------------------------------------
load_dotenv()

# ---------------------------------------------------------
# 1. LOAD KEYBERT MODEL
# ---------------------------------------------------------
kw_model = KeyBERT(model=SentenceTransformer("all-MiniLM-L6-v2"))

# ---------------------------------------------------------
# 2. KEYWORD EXTRACTION
# ---------------------------------------------------------
def extract_keywords(text):
    keywords = kw_model.extract_keywords(text, top_n=8)
    return [k[0] for k in keywords]

# ---------------------------------------------------------
# 3. PROCESS SEGMENTS → SAVE JSON + COLLECT FOR EXCEL
# ---------------------------------------------------------
def process_keywords(json_folder, keyword_folder, excel_output):

    os.makedirs(keyword_folder, exist_ok=True)
    rows = []

    for file in os.listdir(json_folder):
        if not file.endswith(".json"):
            continue

        with open(os.path.join(json_folder, file), "r", encoding="utf-8") as f:
            data = json.load(f)

        keyword_data = {
            "source_file": file,
            "segments": []
        }

        for seg in data["segments"]:
            keywords = extract_keywords(seg["segment_text"])

            keyword_data["segments"].append({
                "segment_id": seg["segment_id"],
                "segment_label": seg["segment_label"],
                "keywords": keywords
            })

            rows.append({
                "File": file,
                "Segment ID": seg["segment_id"],
                "Segment Label": seg["segment_label"],
                "Segment Summary": seg["segment_summary"],
                "Keywords": ", ".join(keywords)
            })

        json_out = os.path.join(
            keyword_folder,
            file.replace(".json", "_keywords.json")
        )

        with open(json_out, "w", encoding="utf-8") as f:
            json.dump(keyword_data, f, indent=4)

        print(f"Saved keywords JSON: {json_out}")

    df = pd.DataFrame(rows)
    df.to_excel(excel_output, index=False)

    print("\nKeyword Excel saved:", excel_output)

# ---------------------------------------------------------
# 4. MAIN
# ---------------------------------------------------------
def main():

    segments_folder = os.getenv("SEGMENTS_DIR")
    keyword_folder = os.getenv("KEYWORDS_DIR")
    excel_output = os.getenv("KEYWORDS_EXCEL")

    process_keywords(segments_folder, keyword_folder, excel_output)

if __name__ == "__main__":
    main()
