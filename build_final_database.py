"""
Week 3: Precise Topic Segmentation (GPU Optimized)
--------------------------------------------------
Updates:
1. ENABLED GPU ACCELERATION for Summarization.
2. Fixes timestamp alignment using Whisper JSON.
3. Generates keywords safely.

Author: [Your Name]
Project: Smart Lecture Navigator
"""

import pandas as pd
import json
import nltk
import ssl
import os
import torch  # <--- NEW: Needed for GPU check
import warnings
from collections import Counter
from transformers import pipeline
from nltk.tokenize import TextTilingTokenizer

# Suppress warnings
warnings.filterwarnings("ignore")

# ==========================================
# 1. CONFIGURATION
# ==========================================
INPUT_FILE = "clean_transcripts.csv"
OUTPUT_FILE = "final_search_index_fixed.csv"
SUMMARIZATION_MODEL = "sshleifer/distilbart-cnn-12-6"

def setup_nlp_environment():
    """Download NLTK resources."""
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    print("[STATUS] Checking NLTK resources...")
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        nltk.download('punkt_tab', quiet=True)
    except Exception:
        pass

def load_models():
    print("[STATUS] Loading AI Models...")
    
    # --- GPU CHECK ---
    if torch.cuda.is_available():
        device_id = 0
        device_name = torch.cuda.get_device_name(0)
        print(f"🚀 SUCCESS: Found GPU: {device_name}")
    else:
        device_id = -1
        print("⚠️ WARNING: GPU not found. Running on CPU (this will be slow).")

    try:
        # We pass 'device=device_id' to use the GPU
        summarizer = pipeline("summarization", model=SUMMARIZATION_MODEL, device=device_id)
    except Exception as e:
        print(f"[WARNING] Summarizer failed to load: {e}")
        summarizer = None
        
    segmenter = TextTilingTokenizer(w=30, k=6)
    return summarizer, segmenter

def extract_keywords(text):
    """Simple keyword extractor (Backup safe)."""
    try:
        tokens = nltk.word_tokenize(text)
        tagged = nltk.pos_tag(tokens)
        stop_words = set(nltk.corpus.stopwords.words('english'))
        candidates = [
            w.lower() for w, t in tagged 
            if w.isalpha() and len(w) > 3 and w.lower() not in stop_words and t.startswith(('NN', 'JJ'))
        ]
        if not candidates: return "General Topic"
        return ", ".join([w for w, c in Counter(candidates).most_common(5)])
    except:
        return "Topic"

def create_word_timeline(segments_json):
    """
    Creates a map where every word has a specific timestamp.
    Unpacks the Whisper JSON into a list of (word, start_time, end_time).
    """
    try:
        raw_segments = json.loads(segments_json)
        word_timeline = []
        
        for seg in raw_segments:
            # We assume words are evenly distributed in the segment
            text_words = seg['text'].split()
            if not text_words: continue
            
            duration = seg['end'] - seg['start']
            time_per_word = duration / len(text_words)
            
            for i, word in enumerate(text_words):
                w_start = seg['start'] + (i * time_per_word)
                w_end = w_start + time_per_word
                word_timeline.append({
                    "word": word,
                    "start": w_start,
                    "end": w_end
                })
        return word_timeline
    except Exception as e:
        print(f"[ERROR] JSON Parse failed: {e}")
        return []

def process_database(input_csv, output_csv):
    if not os.path.exists(input_csv):
        print(f"[ERROR] {input_csv} not found.")
        return

    setup_nlp_environment()
    summarizer, segmenter = load_models()
    
    df = pd.read_csv(input_csv)
    print(f"\n[START] Processing {len(df)} transcripts (Precise Mode + GPU)...")
    
    database_rows = []

    for index, row in df.iterrows():
        talk_id = row['talk_id']
        filename = row['filename']
        
        # 1. Get Real Timeline from JSON
        if 'segments_json' not in row or pd.isna(row['segments_json']):
            print(f"[SKIP] ID {talk_id} missing JSON timestamps.")
            continue
            
        word_timeline = create_word_timeline(row['segments_json'])
        if not word_timeline:
            continue

        # 2. Reconstruct Text from Timeline (Ensures match)
        full_text = " ".join([w['word'] for w in word_timeline])
        
        print(f"[{index+1}/{len(df)}] ID {talk_id}: Aligning {len(word_timeline)} words...", end="\r")

        # 3. Segment Text
        try:
            # Add newlines for TextTiling to work
            formatted = full_text.replace(". ", ".\n\n")
            segments = segmenter.tokenize(formatted)
        except ValueError:
            segments = [full_text]

        # 4. Map Segments back to Timestamps
        current_word_idx = 0
        
        for i, segment_text in enumerate(segments):
            clean_segment = segment_text.replace("\n", " ").strip()
            segment_words = clean_segment.split()
            seg_len = len(segment_words)
            
            if seg_len == 0: continue
            
            # --- PRECISE ALIGNMENT LOGIC ---
            start_idx = current_word_idx
            end_idx = min(current_word_idx + seg_len - 1, len(word_timeline) - 1)
            
            if start_idx >= len(word_timeline): break
            
            real_start = word_timeline[start_idx]['start']
            real_end = word_timeline[end_idx]['end']
            
            start_str = f"{int(real_start // 60):02d}:{int(real_start % 60):02d}"
            end_str = f"{int(real_end // 60):02d}:{int(real_end % 60):02d}"

            # Summary (Uses GPU now)
            summary = "Summary unavailable"
            if summarizer and seg_len > 30:
                try:
                    res = summarizer(clean_segment[:1024], max_length=60, min_length=10, do_sample=False)
                    summary = res[0]['summary_text']
                except: pass
            
            keywords = extract_keywords(clean_segment)

            database_rows.append({
                "talk_id": talk_id,
                "filename": filename,
                "topic_id": i + 1,
                "start_time": start_str,
                "end_time": end_str,
                "start_seconds": int(real_start),
                "end_seconds": int(real_end),
                "summary": summary,
                "keywords": keywords,
                "full_text": clean_segment
            })
            
            current_word_idx += seg_len

    # Save
    if database_rows:
        final_df = pd.DataFrame(database_rows)
        final_df.to_csv(output_csv, index=False)
        print("\n" + "="*50)
        print("🎉 ALIGNMENT COMPLETE! (GPU Powered)")
        print(f"✅ Timestamps are synced to Whisper audio.")
        print(f"💾 Saved to: {output_csv}")
        print("="*50)

if __name__ == "__main__":
    process_database(INPUT_FILE, OUTPUT_FILE)