from jiwer import wer

def calculate_wer(true_text, predicted_text):
    return wer(true_text, predicted_text)