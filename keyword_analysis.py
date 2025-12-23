import os
import json
import warnings
from pathlib import Path
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer

INPUT_DIR = r"D:\farrakh important\internship_project infosys\podcast_data\transcripts"
OUTPUT_DIR = r"D:\farrakh important\internship_project infosys\podcast_data\keywords"

TOP_N_KEYWORDS = 10
NGRAM_RANGE = (1, 2)

def extract_keywords_tfidf(file_paths):
    """Computes TF-IDF across transcripts to find unique keywords per file."""
    print("Loading transcripts to build vocabulary...")
    documents = []
    filenames = []

    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                documents.append(data["text"])
                filenames.append(file_path.stem)
        except Exception as e:
            print(f"Skipping {file_path.name}: {e}")

    if not documents:
        print("No documents found.")
        return

    print("Analyzing word importance via TF-IDF...")
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=NGRAM_RANGE, max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(documents)
    feature_names = vectorizer.get_feature_names_out()

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for doc_idx, doc_vector in enumerate(tqdm(tfidf_matrix, desc="Extracting")):
        scores = doc_vector.toarray().flatten()
        top_indices = scores.argsort()[-TOP_N_KEYWORDS:][::-1]
        
        keywords = []
        for idx in top_indices:
            if scores[idx] > 0:
                keywords.append(f"{feature_names[idx]} ({scores[idx]:.2f})")

        output_file = Path(OUTPUT_DIR) / f"{filenames[doc_idx]}_keywords.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"=== KEYWORDS FOR: {filenames[doc_idx]} ===\n")
            f.write("\n".join(keywords))

def search_transcripts(query):
    """Filters transcripts containing a specific search term."""
    input_path = Path(INPUT_DIR)
    results = []
    
    print(f"Searching for '{query}'...")
    files = list(input_path.glob("*.json"))
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if query.lower() in data["text"].lower():
                results.append(file_path.stem)
    
    if results:
        print(f"Found '{query}' in {len(results)} files:")
        for res in results:
            print(f" - {res}")
    else:
        print(f"'{query}' not found.")

def main_menu():
    input_path = Path(INPUT_DIR)
    files = list(input_path.glob("*.json"))
    
    if not files:
        print(f"No transcripts found in {INPUT_DIR}")
        return

    extract_keywords_tfidf(files)
    
    while True:
        print("\n--- Keyword Filter Mode ---")
        query = input("Enter keyword to search (or 'q' to quit): ").strip()
        
        if query.lower() == 'q':
            break
        
        if query:
            search_transcripts(query)

if __name__ == "__main__":
    main_menu()