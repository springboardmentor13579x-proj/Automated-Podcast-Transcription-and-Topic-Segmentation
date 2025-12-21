import json
import warnings
import pandas as pd
import os
import sys
from nltk.tokenize import TextTilingTokenizer

warnings.filterwarnings("ignore")

# ==========================================
# CORE FUNCTIONS
# ==========================================
def create_word_timeline(segments_json):
    """Parses Whisper JSON to create a word-level timeline."""
    try:
        raw_segments = json.loads(segments_json)
        word_timeline = []
        
        for seg in raw_segments:
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
    except Exception:
        return []

def load_segmenter():
    """Returns the TextTiling tokenizer."""
    return TextTilingTokenizer(w=30, k=6)

def segment_text(segmenter, full_text):
    """Splits full text into topic segments."""
    try:
        formatted = full_text.replace(". ", ".\n\n")
        return segmenter.tokenize(formatted)
    except ValueError:
        return [full_text]

# ==========================================
# MAIN EXECUTION BLOCK (Runs Step 3)
# ==========================================
if __name__ == "__main__":
    # 1. Setup paths to allow importing sibling modules
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    sys.path.append(project_root)
    
    # 2. Import Summarization and Keywords (These must exist in src/)
    try:
        from src.summarization import load_summarizer, generate_summary
        from src.keyword_extraction import extract_keywords
    except ImportError:
        print("Error: Could not import summarization or keyword_extraction modules.")
        sys.exit()

    # 3. Define File Paths
    input_csv = os.path.join(project_root, "transcripts", "clean_transcripts.csv")
    output_csv = os.path.join(project_root, "segments", "final_search_index.csv")

    if not os.path.exists(input_csv):
        print(f"Error: Transcript file not found at {input_csv}")
        print("Please run 'python src/transcription.py' first.")
        sys.exit()

    print(f"Loading Intelligence Models...")
    segmenter = load_segmenter()
    summarizer = load_summarizer()
    
    print(f"Reading transcripts from: {input_csv}")
    df = pd.read_csv(input_csv)
    
    final_rows = []

    # 4. Process Each Transcript
    for index, row in df.iterrows():
        filename = row['filename']
        print(f"Processing: {filename}...", end="\r")
        
        # A. Create Timeline
        if 'segments_json' not in row or pd.isna(row['segments_json']): continue
        timeline = create_word_timeline(row['segments_json'])
        if not timeline: continue

        # B. Segment Text
        full_text = row['ai_text']
        segments = segment_text(segmenter, full_text)
        
        current_idx = 0
        
        for i, seg_text in enumerate(segments):
            clean_text = seg_text.replace("\n", " ").strip()
            words = clean_text.split()
            if not words: continue
            
            # C. Align Time
            # We estimate time based on word counts matching the timeline
            seg_len = len(words)
            start_time = timeline[current_idx]['start'] if current_idx < len(timeline) else 0
            
            end_idx = min(current_idx + seg_len, len(timeline) - 1)
            end_time = timeline[end_idx]['end'] if timeline else 0
            
            # D. Summarize & Extract Keywords
            summary = generate_summary(summarizer, clean_text)
            keywords = extract_keywords(clean_text)
            
            # E. Format Time String (MM:SS)
            start_str = f"{int(start_time//60):02d}:{int(start_time%60):02d}"
            end_str = f"{int(end_time//60):02d}:{int(end_time%60):02d}"

            final_rows.append({
                "filename": filename,
                "topic_id": i + 1,
                "start_time": start_str,
                "end_time": end_str,
                "start_seconds": int(start_time),
                "end_seconds": int(end_time),
                "summary": summary,
                "keywords": keywords,
                "full_text": clean_text
            })
            
            current_idx += seg_len

    # 5. Save Final Database
    if final_rows:
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        pd.DataFrame(final_rows).to_csv(output_csv, index=False)
        print(f"\nSuccess! Final database saved to: {output_csv}")
    else:
        print("\nWarning: No segments generated.")