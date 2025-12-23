import os
import json
import numpy as np
import nltk
import warnings
from pathlib import Path
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline

# Configuration
INPUT_DIR = r"D:\farrakh important\internship_project infosys\podcast_data\transcripts"
OUTPUT_DIR = r"D:\farrakh important\internship_project infosys\podcast_data\semantic_segments"

# Segmentation and Model Settings
WINDOW_SIZE = 3
SIMILARITY_THRESHOLD = 0.65 
SUMMARY_MODEL = "sshleifer/distilbart-cnn-12-6"

def setup_nltk():
    """Initializes NLTK resources."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab', quiet=True)

def get_sentences(text):
    return nltk.sent_tokenize(text)

def segment_text(sentences):
    """Segments text using TF-IDF and Cosine Similarity."""
    if len(sentences) < WINDOW_SIZE * 2:
        return [sentences]

    # Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(sentences)
    
    # Calculate Similarity across windows
    similarities = []
    for i in range(len(sentences) - WINDOW_SIZE):
        vec1 = tfidf_matrix[i : i + WINDOW_SIZE].mean(axis=0)
        vec2 = tfidf_matrix[i + 1 : i + 1 + WINDOW_SIZE].mean(axis=0)
        sim = cosine_similarity(np.asarray(vec1), np.asarray(vec2))[0][0]
        similarities.append(sim)

    # Detect segment cut points
    segments = []
    current_segment = []
    
    for i, sim in enumerate(similarities):
        current_segment.append(sentences[i])
        
        if sim < SIMILARITY_THRESHOLD:
            is_dip = True
            if i > 0 and similarities[i-1] < sim: is_dip = False
            if i < len(similarities)-1 and similarities[i+1] < sim: is_dip = False
            
            if is_dip:
                segments.append(" ".join(current_segment))
                current_segment = []
    
    remaining = sentences[len(similarities):]
    current_segment.extend(remaining)
    segments.append(" ".join(current_segment))
    
    return segments

def generate_segment_summary(text, summarizer):
    """Generates summary for text segments."""
    try:
        clean_text = text[:3500]
        if len(clean_text) < 150:
            return text 

        result = summarizer(clean_text, max_length=130, min_length=40, do_sample=False)
        return result[0]['summary_text']
    except Exception as e:
        return f"Summary failed: {str(e)}"

def process_semantic_segmentation():
    setup_nltk()
    
    input_path = Path(INPUT_DIR)
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)

    try:
        summarizer = pipeline("summarization", model=SUMMARY_MODEL)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    files = list(input_path.glob("*.json"))
    files.sort()

    for file_path in tqdm(files, desc="Segmenting Topics"):
        output_file = output_path / f"{file_path.stem}_topics.txt"
        
        if output_file.exists():
             os.remove(output_file) 

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                full_text = data["text"]

            sentences = get_sentences(full_text)
            text_segments = segment_text(sentences)

            final_report = []
            final_report.append(f"=== TOPIC ANALYSIS FOR: {file_path.stem} ===\n")
            final_report.append(f"Total Sentences: {len(sentences)} | Detected Topics: {len(text_segments)}\n")
            
            for i, segment_content in enumerate(text_segments):
                topic_summary = generate_segment_summary(segment_content, summarizer)
                final_report.append(f"\nTOPIC {i+1}: {topic_summary}")
                final_report.append(f"   (Starts with: \"{segment_content[:200]}...\")\n")

            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(final_report))

        except Exception as e:
            print(f"\nError processing {file_path.name}: {e}")

    print(f"\nSegmentation Complete. Output in: {OUTPUT_DIR}")

if __name__ == "__main__":
    process_semantic_segmentation()