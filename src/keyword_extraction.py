# src/keyword_extraction.py
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer

FINAL_DIR = "transcripts/final"
DOCS_DIR = "docs"

os.makedirs(DOCS_DIR, exist_ok=True)

def clean_text(text):
    # Remove segment labels
    text = re.sub(r"\[?\s*segment\s*\d*\]?", "", text, flags=re.IGNORECASE)

    # Remove timestamps (00:01:23 or 01:23)
    text = re.sub(r"\b\d{1,2}:\d{2}(:\d{2})?\b", "", text)

    # Remove punctuation
    text = re.sub(r"[^\w\s]", "", text)

    # Normalize spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text.lower()

def filter_duplicates(keywords):
    """
    Remove overlapping keywords.
    If 'hr interview' exists, remove 'interview' or 'hr'.
    """
    final_keywords = []

    for kw in keywords:
        skip = False
        for chosen in final_keywords:
            if kw in chosen or chosen in kw:
                skip = True
                break
        if not skip:
            final_keywords.append(kw)

    return final_keywords

def extract_keywords(text, top_k=8):
    text = clean_text(text)

    if len(text.split()) < 5:
        return []

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=200,
        min_df=1        # IMPORTANT FIX: must be 1 for single-document TF-IDF
    )

    try:
        tfidf = vectorizer.fit_transform([text])
    except ValueError:
        return []

    scores = tfidf.toarray()[0]
    terms = vectorizer.get_feature_names_out()

    ranked = sorted(zip(terms, scores), key=lambda x: x[1], reverse=True)
    raw_keywords = [term for term, _ in ranked]

    filtered_keywords = filter_duplicates(raw_keywords)

    return filtered_keywords[:top_k]

def run_keyword_extraction():
    files = [f for f in os.listdir(FINAL_DIR) if f.endswith(".txt")]

    if not files:
        print("No final transcripts found.")
        return

    out_path = os.path.join(DOCS_DIR, "keywords.txt")

    with open(out_path, "w", encoding="utf-8") as out:
        for file in files:
            path = os.path.join(FINAL_DIR, file)

            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            keywords = extract_keywords(text)

            out.write(file + "\n")
            out.write(", ".join(keywords) + "\n\n")

            print("Keywords extracted:", file)

if __name__ == "__main__":
    run_keyword_extraction()
