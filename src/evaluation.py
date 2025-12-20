import os
import re
from jiwer import wer, cer

def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    fillers = ['um','uh','mm-hmm','ah','oh','yeah','okay']
    for f in fillers:
        text = re.sub(r'\b'+f+r'\b', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def evaluate_asr(manual_path, asr_path, sessions):
    results = {}
    for session in sessions:
        manual_file = os.path.join(manual_path, f"{session}_manual.txt")
        asr_file = os.path.join(asr_path, f"{session}.txt")
        if not os.path.exists(manual_file) or not os.path.exists(asr_file):
            results[session] = None
            continue
        with open(manual_file, "r", encoding="utf-8") as f:
            manual_text = normalize_text(f.read())
        with open(asr_file, "r", encoding="utf-8") as f:
            asr_text = normalize_text(f.read())
        error = wer(manual_text, asr_text)
        results[session] = 1 - error
        print(f"{session} Accuracy: {(1-error)*100:.2f}% | WER: {error*100:.2f}%")
    return results
