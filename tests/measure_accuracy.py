import pandas as pd
import jiwer
import os
import warnings
from dotenv import load_dotenv

# Suppress warnings
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()

# Configuration (Loaded from .env)
AI_RESULTS_FILE = os.getenv("TRANSCRIPT_FILE", "clean_transcripts.csv")
GROUND_TRUTH_FILE = os.getenv("MERGE_CSV_SOURCE")

def calculate_accuracy(ai_csv, truth_csv):
    """
    Calculates the Word Error Rate (WER) and Accuracy between AI transcripts
    and the official Ground Truth.
    """
    # 1. Validation
    if not ai_csv or not os.path.exists(ai_csv):
        print(f"[ERROR] AI transcript file not found: {ai_csv}")
        return
    
    if not truth_csv or not os.path.exists(truth_csv):
        print(f"[ERROR] Ground truth file not found: {truth_csv}")
        return

    print(f"[STATUS] Loading data from {ai_csv} and {truth_csv}...")
    df_ai = pd.read_csv(ai_csv)
    df_truth = pd.read_csv(truth_csv)
    
    # 2. Define Text Cleaner (Standardizes text for fair comparison)
    cleaner = jiwer.Compose([
        jiwer.ToLowerCase(),
        jiwer.RemovePunctuation(),
        jiwer.RemoveMultipleSpaces(),
        jiwer.Strip(),
        jiwer.ExpandCommonEnglishContractions()
    ])

    print(f"[STATUS] Analyzing {len(df_ai)} files...")
    
    valid_scores = []
    
    for index, row in df_ai.iterrows():
        talk_id = row['talk_id']
        ai_text = str(row['ai_text'])
        
        # Find matching ground truth entry
        # Checks for 'talk__id' (common in TED datasets) or 'talk_id'
        if 'talk__id' in df_truth.columns:
            match = df_truth[df_truth['talk__id'] == talk_id]
        else:
            match = df_truth[df_truth['talk_id'] == talk_id]
        
        if not match.empty:
            official_text = str(match.iloc[0]['transcript'])
            
            # Calculate Word Error Rate (WER)
            wer = jiwer.wer(cleaner(official_text), cleaner(ai_text))
            
            # Convert WER to Accuracy
            # Logic: If WER is > 100% (mostly errors), accuracy is 0.
            accuracy = max(0.0, 1.0 - wer)
            valid_scores.append(accuracy)
            
            # Print individual result
            if accuracy > 0.8:
                status = "High Accuracy"
            elif accuracy == 0:
                status = "Potential Hallucination"
            else:
                status = "Low Accuracy"

            print(f"ID {talk_id}: {accuracy:.2%} [{status}]")

    # 3. Final Report
    if valid_scores:
        average_accuracy = sum(valid_scores) / len(valid_scores)
        print("-" * 50)
        print(f"FINAL RESULT: Average Accuracy = {average_accuracy:.2%}")
        print("-" * 50)
    else:
        print("[WARNING] No matching Talk IDs found between the two files.")

if __name__ == "__main__":
    calculate_accuracy(AI_RESULTS_FILE, GROUND_TRUTH_FILE)