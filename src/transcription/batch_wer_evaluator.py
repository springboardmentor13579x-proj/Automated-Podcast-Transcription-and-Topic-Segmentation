import os
import json
from src.transcription.accuracy_evaluator import calculate_wer

GROUND_TRUTH_DIR = "data/ground_truth"
TRANSCRIPT_DIR = "data/transcripts"

def load_transcript_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return " ".join([seg["text"] for seg in data["segments"]])


def find_matching_json(txt_filename):
    
    base_name = txt_filename.replace(".txt", "").lower()

    json_files = os.listdir(TRANSCRIPT_DIR)

    for jf in json_files:
        name_no_ext = jf.replace(".json", "").lower()

        
        if base_name in name_no_ext:
            return jf

    return None


def evaluate_all_wer():
    txt_files = os.listdir(GROUND_TRUTH_DIR)

    for txt_file in txt_files:
        if txt_file.endswith(".txt"):

            true_path = os.path.join(GROUND_TRUTH_DIR, txt_file)

            
            json_match = find_matching_json(txt_file)

            if json_match is None:
                print(f"❌ No matching JSON found for: {txt_file}")
                continue

            pred_path = os.path.join(TRANSCRIPT_DIR, json_match)

            # Load ground truth text
            with open(true_path, "r", encoding="utf-8") as f:
                true_text = f.read()

            # Load predicted text
            predicted_text = load_transcript_json(pred_path)

            # Calculate WER
            score = calculate_wer(true_text, predicted_text)

            print(f"WER for {txt_file.replace('.txt','')}: {score:.3f}")


if __name__ == "__main__":
    evaluate_all_wer()
