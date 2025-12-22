from keybert import KeyBERT
import yake
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KeywordExtractor:
    def __init__(self, method='keybert'):
        self.method = method
        if method == 'keybert':
            logger.info("Loading KeyBERT model...")
            self.kw_model = KeyBERT()
        # YAKE doesn't need model loading at init generally, but config
        
    def extract(self, text, top_n=5):
        if not text:
            return []
            
        if self.method == 'keybert':
            keywords = self.kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=top_n)
            return [k[0] for k in keywords]
        
        elif self.method == 'yake':
            kw_extractor = yake.KeywordExtractor(lan="en", n=2, dedupLim=0.9, top=top_n, features=None)
            keywords = kw_extractor.extract_keywords(text)
            return [k[0] for k in keywords]
        
        else:
            return []
