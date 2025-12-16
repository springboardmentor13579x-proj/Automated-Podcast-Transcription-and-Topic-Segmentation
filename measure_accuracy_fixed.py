import pandas as pd
import jiwer
import os
import warnings

warnings.filterwarnings("ignore")

def calculate_fixed_accuracy(ai_results_csv, ground_truth_csv):
    
    # 1. Load Data
    if not os.path.exists(ai_results_csv) or not os.path.exists(ground_truth_csv):
        print("❌ Error: Missing CSV files.")
        return

    df_ai = pd.read_csv(ai_results_csv)
    df_truth = pd.read_csv(ground_truth_csv)
    
    cleaner = jiwer.Compose([
        jiwer.ToLowerCase(),
        jiwer.RemovePunctuation(),
        jiwer.RemoveMultipleSpaces(),
        jiwer.Strip(),
        jiwer.ExpandCommonEnglishContractions()
    ])

    print(f"📊 Analyzing {len(df_ai)} files (Fixing Negative Scores)...")
    
    valid_scores = []
    
    for index, row in df_ai.iterrows():
        talk_id = row['talk_id']
        ai_text = str(row['ai_text'])
        
        # Find matching truth
        if 'talk__id' in df_truth.columns:
            match = df_truth[df_truth['talk__id'] == talk_id]
        else:
            match = df_truth[df_truth['talk_id'] == talk_id]
        
        if not match.empty:
            official_text = str(match.iloc[0]['transcript'])
            
            # MATH FIX:
            wer = jiwer.wer(cleaner(official_text), cleaner(ai_text))
            
            # If WER > 1.0 (Negative Accuracy), cap it at 0.0 (0% Accuracy)
            accuracy = max(0.0, 1.0 - wer)
            
            valid_scores.append(accuracy)
            
            # Print status
            if accuracy > 0.8:
                print(f"   ✅ ID {talk_id}: {accuracy:.2%}")
            elif accuracy == 0:
                print(f"   🚫 ID {talk_id}: 0.00% (Hallucination Detected)")
            else:
                print(f"   ⚠️ ID {talk_id}: {accuracy:.2%}")

    # Calculate True Average
    if valid_scores:
        true_average = sum(valid_scores) / len(valid_scores)
        print("\n" + "="*50)
        print(f"🏆 REAL AVERAGE ACCURACY: {true_average:.2%}")
        print("="*50)

if __name__ == "__main__":
    calculate_fixed_accuracy("clean_transcripts.csv", r"E:\speech_to_text\archive (2)\TED_Talk.csv")