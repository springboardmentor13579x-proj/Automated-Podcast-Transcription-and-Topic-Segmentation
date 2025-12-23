from transformers import pipeline
from keybert import KeyBERT
from textblob import TextBlob  # <--- NEW IMPORT

class ContentProcessor:
    def __init__(self):
        print("⏳ Loading Summarization & Keyword models...")
        # Summarizer (DistilBART)
        self.summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        # Keyword Extractor
        self.kw_model = KeyBERT()

    def generate_summary(self, text, max_len=60):
        """
        Generates a concise summary and polishes the formatting.
        """
        # 1. Safety Check
        if len(text.split()) < 30:
            return text
            
        try:
            # 2. Generate Raw Summary
            summary_result = self.summarizer(text, max_length=max_len, min_length=15, do_sample=False)
            raw_summary = summary_result[0]['summary_text']
            
            # 3. 🛀 POLISH THE TEXT (New Step)
            # Remove extra spaces (e.g., " . " -> ". ")
            polished = raw_summary.replace(" .", ".").replace(" ,", ",")
            # Ensure it starts with Capital
            polished = polished[0].upper() + polished[1:]
            # Ensure it ends with a period
            if not polished.endswith("."):
                polished += "."
                
            return polished
            
        except Exception as e:
            print(f"   ⚠️ Summarization error: {e}")
            return text[:100] + "..."

    def extract_keywords(self, text, top_n=5):
        try:
            keywords = self.kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words='english', top_n=top_n)
            return [kw[0] for kw in keywords]
        except:
            return []

    # 👇 NEW FUNCTION: SENTIMENT ANALYSIS
    def analyze_sentiment(self, text):
        """
        Returns a score from -1.0 (Negative) to 1.0 (Positive).
        """
        try:
            blob = TextBlob(text)
            return blob.sentiment.polarity
        except:
            return 0.0
