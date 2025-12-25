import os
import json
from src.utils.file_utils import get_data_paths, ensure_dirs
from src.summarization.content_processor import ContentProcessor

def main():
    # 1. Setup Paths
    paths = get_data_paths()
    # Input comes from segmentation step
    input_dir = os.path.join(paths["root"], "data", "segmented_topics")
    # Output goes to final folder
    output_dir = os.path.join(paths["root"], "data", "final_output")
    
    ensure_dirs([output_dir])

    # 2. Initialize AI Processor
    processor = ContentProcessor()

    # 3. Find Segmented Files
    if not os.path.exists(input_dir):
        print(f" Error: Input directory '{input_dir}' not found.")
        print("   Did you run run_segmentation.py?")
        return

    files = [f for f in os.listdir(input_dir) if f.endswith('.json')]
    
    if not files:
        print(" No segmented files found.")
        return

    print(f"\n Processing {len(files)} episodes for Summaries & Keywords...\n")

    for filename in files:
        print(f" Processing: {filename}...")
        input_path = os.path.join(input_dir, filename)
        
        # Load the segmented data
        with open(input_path, 'r', encoding='utf-8') as f:
            segments = json.load(f)
        
        # Process each topic segment
        for i, segment in enumerate(segments):
            text = segment['text']
            
            # A. Summary
            print(f"   -> Summarizing Topic {i+1}...")
            segment['summary'] = processor.generate_summary(text)
            
            # B. Keywords
            segment['keywords'] = processor.extract_keywords(text)
            
            # C.  NEW: Sentiment Analysis
            segment['sentiment'] = processor.analyze_sentiment(text)

        # Save Final Result
        output_filename = filename.replace("_segmented.json", "_final.json")
        output_path = os.path.join(output_dir, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(segments, f, indent=4)
            
        print(f" Finished! Saved to: data/final_output/{output_filename}\n")

if __name__ == "__main__":

    main()
