import os
import json
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from pathlib import Path
from tqdm import tqdm

# --- CONFIGURATION ---
INPUT_DIR = r"D:\farrakh important\internship_project infosys\podcast_data\transcripts"
OUTPUT_DIR = r"D:\farrakh important\internship_project infosys\podcast_data\sentiment_data"
# ---------------------

def setup_nltk():
    """Downloads necessary NLTK sentiment data."""
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        print("⬇️ Downloading NLTK VADER lexicon...")
        nltk.download('vader_lexicon', quiet=True)

def analyze_sentiment_for_file(file_path, sia, output_path):
    """
    Reads a transcript JSON, calculates sentiment for each segment,
    and saves the detailed timeline data.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check if the JSON has segment-level data (timestamps)
        # Whisper output usually includes a "segments" list
        if "segments" not in data:
            print(f"⚠️ Warning: No timestamped segments found in {file_path.name}. Skipping timeline generation.")
            return

        sentiment_timeline = []
        
        # Analyze each small segment (sentence/phrase)
        for segment in data["segments"]:
            text = segment["text"].strip()
            start = segment["start"]
            end = segment["end"]
            
            # Get Sentiment Scores
            # compound: -1 (Most Negative) to +1 (Most Positive)
            scores = sia.polarity_scores(text)
            compound_score = scores['compound']
            
            # Determine Label
            if compound_score >= 0.05:
                label = "Positive"
            elif compound_score <= -0.05:
                label = "Negative"
            else:
                label = "Neutral"

            sentiment_timeline.append({
                "start": start,
                "end": end,
                "text": text,
                "score": compound_score,
                "label": label
            })

        # Save the analyzed data
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(sentiment_timeline, f, indent=4)

    except Exception as e:
        print(f"❌ Error analyzing {file_path.name}: {e}")

def process_sentiment_analysis():
    setup_nltk()
    
    input_path = Path(INPUT_DIR)
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)

    print("🧠 Initializing VADER Sentiment Analyzer...")
    sia = SentimentIntensityAnalyzer()

    # Find Transcript Files
    files = list(input_path.glob("*.json"))
    print(f"📂 Found {len(files)} transcripts to analyze.")

    success_count = 0
    
    for file_path in tqdm(files, desc="Analyzing Sentiment"):
        output_file = output_path / f"{file_path.stem}_sentiment.json"
        
        # Skip if already done
        if output_file.exists():
            continue

        analyze_sentiment_for_file(file_path, sia, output_file)
        success_count += 1

    print(f"\n🎉 Sentiment Analysis Complete!")
    print(f"✅ Processed {success_count} new files.")
    print(f"📂 Data ready for visualization in: {OUTPUT_DIR}")

if __name__ == "__main__":
    process_sentiment_analysis()