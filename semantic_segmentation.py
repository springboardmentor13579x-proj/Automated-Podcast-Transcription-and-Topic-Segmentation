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

# --- CONFIGURATION ---
INPUT_DIR = r"D:\farrakh important\internship_project infosys\podcast_data\transcripts"
OUTPUT_DIR = r"D:\farrakh important\internship_project infosys\podcast_data\semantic_segments"

# Segmentation Settings
# WINDOW_SIZE: How many sentences to look at (3 is usually good)
WINDOW_SIZE = 3
# SIMILARITY_THRESHOLD: The "Sensitivity" of the cutter.
# 0.3 = Very strict (Only cuts big changes) -> Few topics
# 0.7 = Very sensitive (Cuts small changes) -> Many topics
SIMILARITY_THRESHOLD = 0.65 

# Summary Settings
SUMMARY_MODEL = "sshleifer/distilbart-cnn-12-6"
# ---------------------

def setup_nltk():
    """Downloads necessary NLTK data."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("⬇️ Downloading NLTK data (punkt)...")
        nltk.download('punkt', quiet=True)
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        print("⬇️ Downloading NLTK data (punkt_tab)...")
        nltk.download('punkt_tab', quiet=True)

def get_sentences(text):
    """Uses NLTK to split text into clean sentences."""
    return nltk.sent_tokenize(text)

def segment_text(sentences):
    """
    The Core Logic: TF-IDF + Cosine Similarity.
    """
    if len(sentences) < WINDOW_SIZE * 2:
        return [sentences]

    # 1. Create Vectors (TF-IDF)
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(sentences)
    
    # 2. Calculate Similarity
    similarities = []
    for i in range(len(sentences) - WINDOW_SIZE):
        vec1 = tfidf_matrix[i : i + WINDOW_SIZE].mean(axis=0)
        vec2 = tfidf_matrix[i + 1 : i + 1 + WINDOW_SIZE].mean(axis=0)
        sim = cosine_similarity(np.asarray(vec1), np.asarray(vec2))[0][0]
        similarities.append(sim)

    # 3. Find Cut Points
    segments = []
    current_segment = []
    
    for i, sim in enumerate(similarities):
        current_segment.append(sentences[i])
        
        # Cut if similarity drops below threshold
        if sim < SIMILARITY_THRESHOLD:
            # Simple local minima detection
            is_dip = True
            if i > 0 and similarities[i-1] < sim: is_dip = False
            if i < len(similarities)-1 and similarities[i+1] < sim: is_dip = False
            
            if is_dip:
                segments.append(" ".join(current_segment))
                current_segment = []
    
    # Add remaining
    remaining = sentences[len(similarities):]
    current_segment.extend(remaining)
    segments.append(" ".join(current_segment))
    
    return segments

def generate_segment_summary(text, summarizer):
    """Uses BART to summarize a specific segment."""
    try:
        # We take a slightly larger chunk to ensure context
        clean_text = text[:3500]
        
        if len(clean_text) < 150:
            return text  # Too short, just return the text itself

        # Increased max_length to prevent cutting off sentences
        result = summarizer(clean_text, max_length=130, min_length=40, do_sample=False)
        return result[0]['summary_text']
    except Exception as e:
        return f"Summary failed: {str(e)}"

def process_semantic_segmentation():
    setup_nltk()
    
    input_path = Path(INPUT_DIR)
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"🧠 Loading Summarization Model ({SUMMARY_MODEL})...")
    try:
        summarizer = pipeline("summarization", model=SUMMARY_MODEL)
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return

    files = list(input_path.glob("*.json"))
    print(f"📂 Found {len(files)} transcripts to analyze.")

    # Sort files to process them in order
    files.sort()

    for file_path in tqdm(files, desc="Segmenting Topics"):
        output_file = output_path / f"{file_path.stem}_topics.txt"
        
        # --- Remove this block if you want to overwrite old results with new tuning ---
        if output_file.exists():
             # Delete old file so we can regenerate with better settings
             os.remove(output_file) 
        # ---------------------------------------------------------------------------

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
                
                final_report.append(f"\n🔹 TOPIC {i+1}: {topic_summary}")
                # Save first 200 chars as snippet to verify boundary
                final_report.append(f"   (Starts with: \"{segment_content[:200]}...\")\n")

            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(final_report))

        except Exception as e:
            print(f"\n❌ Error processing {file_path.name}: {e}")

    print(f"\n🎉 Semantic Segmentation Complete!")
    print(f"📂 Check folder: {OUTPUT_DIR}")

if __name__ == "__main__":
    process_semantic_segmentation()