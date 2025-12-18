import os
import json
from datetime import datetime
import config

# Importing your existing modules
from audio_cleaner import clean_all_audio
from audio_transcriber import transcribe_all_audio
from text_segmenter import segment_all_transcripts
from summarizer import process_summaries

def run_full_pipeline():
    print("\n" + "="*50)
    print("🚀 STARTING PODCAST PROCESSING PIPELINE")
    print("="*50)

    # Step 1: Clean the Audio
    print("\n[Step 1/4] 🧹 Cleaning Audio...")
    clean_all_audio()

    # Step 2: Transcribe
    print("\n[Step 2/4] 🎙️ Transcribing Audio...")
    transcribe_all_audio()

    # Step 3: Segment into Topics
    print("\n[Step 3/4] ✂️ Segmenting Topics...")
    segment_all_transcripts()

    # Step 4: Summarize and SAVE
    print("\n[Step 4/4] 📝 Generating Summaries...")
    # This calls your summarizer and returns the list of topics
    final_data = process_summaries() 

    # --- THE MISSING PART: SAVE TO JSON ---
    if final_data:
        # Create a unique filename based on time
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"summary_{timestamp}.json"
        output_path = os.path.join(config.PROCESSED_FOLDER, output_filename)

        # Save the file to data/processed/
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({"topics": final_data}, f, indent=4)
        
        print(f"\n✅ SUCCESS: Pipeline complete!")
        print(f"📄 Result saved to: {output_path}")
    else:
        print("\n❌ FAILED: Summarizer returned no data.")

if __name__ == "__main__":
    run_full_pipeline()