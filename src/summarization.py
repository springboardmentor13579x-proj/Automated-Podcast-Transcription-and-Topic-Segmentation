import torch
from transformers import pipeline
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

SUMMARIZATION_MODEL = "sshleifer/distilbart-cnn-12-6"

def load_summarizer():
    """Loads the summarization model on GPU if available."""
    print("[STATUS] Loading AI Models...")
    
    # --- GPU CHECK ---
    if torch.cuda.is_available():
        device_id = 0
        device_name = torch.cuda.get_device_name(0)
        print(f"SUCCESS: Found GPU: {device_name}")
    else:
        device_id = -1
        print("WARNING: GPU not found. Running on CPU.")

    try:
        return pipeline("summarization", model=SUMMARIZATION_MODEL, device=device_id)
    except Exception as e:
        print(f"[WARNING] Summarizer failed to load: {e}")
        return None

def generate_summary(summarizer, text):
    """Generates a summary for a given text segment."""
    if not summarizer:
        return "Summary unavailable"
    
    try:
        # Truncate text to avoid model size limits (simple safety check)
        # We limit to roughly 3000 chars to stay safe within token limits
        safe_text = text[:3000] 
        
        res = summarizer(safe_text, max_length=60, min_length=10, do_sample=False)
        return res[0]['summary_text']
    except Exception:
        return "Summary unavailable"

# Only runs if you execute this file directly
if __name__ == "__main__":
    print("--- TESTING SUMMARIZATION ---")
    
    model = load_summarizer()
    
    sample_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by animals including humans.
    AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals.
    The term "artificial intelligence" had previously been used to describe machines that mimic and display "human" cognitive skills that are associated with the human mind, such as "learning" and "problem-solving".
    """
    
    print(f"\nOriginal Text Length: {len(sample_text)} characters")
    summary = generate_summary(model, sample_text)
    print(f"\nSummary: {summary}")