import os
import nltk
from nltk.tokenize import TextTilingTokenizer
import re
import config

def download_nltk_resources():
    """Download necessary NLTK data safely"""
    required_packages = ['punkt', 'punkt_tab', 'stopwords']
    for package in required_packages:
        try:
            nltk.data.find(f'tokenizers/{package}')
        except LookupError:
            print(f"Downloading NLTK package: {package}...")
            nltk.download(package, quiet=True)

def clean_timestamps(text):
    """Removes [00.00s] timestamps so TextTiling can read the text"""
    # Regex to remove brackets and numbers inside them
    return re.sub(r'\[.*?\]', '', text)

def segment_transcript(filename):
    input_path = os.path.join(config.PROCESSED_FOLDER, filename)
    
    with open(input_path, "r", encoding="utf-8") as f:
        raw_content = f.read()

    # We need pure text for segmentation, but we want to keep structure
    clean_text = clean_timestamps(raw_content)

    print(f"\n--- Segmenting: {filename} ---")
    
    # Initialize TextTiling
    tt = TextTilingTokenizer(w=30, k=6)
    
    try:
        # Perform Segmentation
        segments = tt.tokenize(clean_text)
        print(f"✅ Found {len(segments)} segments.")
        
        base_name = filename.replace("transcript_", "segments_")
        output_path = os.path.join(config.PROCESSED_FOLDER, base_name)
        
        with open(output_path, "w", encoding="utf-8") as f:
            for i, segment in enumerate(segments):
                header = f"\n=== TOPIC {i+1} ===\n"
                f.write(header)
                f.write(segment.strip() + "\n")
                
        print(f"   Saved segmentation to: {base_name}")

    except ValueError:
        print("   ⚠️  Text too short/uniform to segment. Saving as single topic.")
        base_name = filename.replace("transcript_", "segments_")
        output_path = os.path.join(config.PROCESSED_FOLDER, base_name)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("=== TOPIC 1 ===\n" + clean_text)

def segment_all_transcripts():
    download_nltk_resources()
    files = [f for f in os.listdir(config.PROCESSED_FOLDER) if f.startswith("transcript_")]
    for f in files:
        segment_transcript(f)

if __name__ == "__main__":
    segment_all_transcripts()