import os
import json
from src.utils.file_utils import get_data_paths
from src.segmentation.semantic_segmenter import SemanticSegmenter

def load_transcript_data(json_path):
    """Loads text and timestamps from the Whisper JSON output."""
    with open(json_path, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    
    sentences = []
    timestamps = []
    full_text = ""
    
    for chunk in chunks:
        text = chunk['text'].strip()
        if text:
            sentences.append(text)
            timestamps.append(chunk['timestamp'])
            full_text += text + " "
            
    return full_text, sentences, timestamps

def main():
    paths = get_data_paths()
    transcripts_dir = paths["transcripts_dir"]
    output_dir = os.path.join(paths["root"], "data", "segmented_topics")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Initialize Segmenters
    # tiling_model = TilingSegmenter()  # Good for pure text structure
    bert_model = SemanticSegmenter()    # Better for meaning/context
    
    # Process all JSON transcripts
    files = [f for f in os.listdir(transcripts_dir) if f.endswith('.json')]
    
    if not files:
        print("❌ No JSON transcripts found! Run main.py (Milestone 1) first.")
        return

    print(f"Found {len(files)} transcripts to segment.")

    for filename in files:
        print(f"\n🧠 Segmenting: {filename}...")
        file_path = os.path.join(transcripts_dir, filename)
        
        # 1. Load Data
        full_text, sentences, timestamps = load_transcript_data(file_path)
        
        # 2. Run Semantic Segmentation (Preferred for podcasts)
        # Threshold: Lower (e.g. 0.4) = fewer topics, Higher (e.g. 0.7) = more topics
        segments = bert_model.segment(sentences, timestamps, threshold=0.5)
        
        # 3. Save Results
        out_name = filename.replace(".json", "_segmented.json")
        out_path = os.path.join(output_dir, out_name)
        
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(segments, f, indent=4)
            
        print(f"   ✅ Identified {len(segments)} topics.")
        
        # 4. Print Preview
        for seg in segments[:3]: # Show first 3 topics
            print(f"      Topic {seg['topic_id']} ({seg['start_time']}s - {seg['end_time']}s): {seg['text'][:50]}...")

if __name__ == "__main__":
    main()