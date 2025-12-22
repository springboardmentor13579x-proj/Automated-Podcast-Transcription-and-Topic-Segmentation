from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Summarizer:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        logger.info(f"Loading Summarization model: {model_name}")
        self.summarizer = pipeline("summarization", model=model_name)

    def summarize(self, text, max_length=130, min_length=30):
        if not text:
            return ""
        
        # Handle long text by chunking if necessary, but for now simple truncated call
        # BART has a limit usually 1024 tokens.
        try:
            # Simple truncation for safety
            input_text = text[:4000] 
            summary = self.summarizer(input_text, max_length=max_length, min_length=min_length, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            return text[:200] + "..." # Fallback
