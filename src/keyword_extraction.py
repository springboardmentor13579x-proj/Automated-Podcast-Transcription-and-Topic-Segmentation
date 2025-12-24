import logging
import yake
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer, util
import numpy as np
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KeywordExtractor:
    def __init__(self, method='keybert', model_name='all-MiniLM-L6-v2'):
        """
        Initializes the Semantic Keyword Extraction Agent.
        
        Args:
            method (str): 'keybert' (default) or 'yake'.
            model_name (str): SentenceTransformer model name for semantic embedding.
        """
        self.method = method
        self.model_name = model_name
        self.kw_model = None
        self.embedding_model = None
        
        # Lazy loading flags
        self._keybert_loaded = False
        self._embedder_loaded = False
        
    def _load_keybert(self):
        if not self._keybert_loaded:
            logger.info("Loading KeyBERT model...")
            try:
                # KeyBERT can implicitly load a model, but we control it to share resources if needed
                # We'll let KeyBERT load its own default or pass our embedder if strictly needed,
                # but typically KeyBERT(model=...) works best.
                self.kw_model = KeyBERT(model=self.model_name)
                self._keybert_loaded = True
            except Exception as e:
                logger.error(f"Failed to load KeyBERT: {e}")
                self.method = 'yake' # Fallback
                
    def _load_embedder(self):
        if not self._embedder_loaded:
            logger.info(f"Loading SentenceTransformer: {self.model_name}...")
            try:
                self.embedding_model = SentenceTransformer(self.model_name)
                self._embedder_loaded = True
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}")
                
    def extract(self, text, top_n=5):
        """
        Extracts context-aware keywords from the text using semantic similarity.
        
        Args:
            text (str): Input text chunk.
            top_n (int): Number of keywords to return.
            
        Returns:
            list: List of top_n semantic keyword phrases.
        """
        if not text or len(text.strip()) < 10:
            logger.warning("Input text too short for keyword extraction.")
            return []
            
        try:
            candidates = []
            
            # --- Method 1: KeyBERT (Preferred) ---
            if self.method == 'keybert':
                self._load_keybert()
                if self.kw_model:
                    # extract_keywords returns list of (keyword, score)
                    # use_mmr=True adds diversity to avoid repetitive keywords
                    keywords_scores = self.kw_model.extract_keywords(
                        text, 
                        keyphrase_ngram_range=(1, 3), 
                        stop_words='english', 
                        use_mmr=True, 
                        diversity=0.3, # 0.7 is diverse, 0.2 is precise
                        top_n=top_n
                    )
                    return [kw for kw, _ in keywords_scores]
            
            # --- Method 2: YAKE + Semantic Re-ranking (Fallback) ---
            # If KeyBERT failed or method is explicitly 'yake'
            
            # 1. Generate Candidates with YAKE
            yake_extractor = yake.KeywordExtractor(lan="en", n=3, dedupLim=0.9, top=top_n*3, features=None)
            yake_keywords = yake_extractor.extract_keywords(text)
            candidate_phrases = [kw for kw, score in yake_keywords] # YAKE score: lower is better, but we just want candidates
            
            if not candidate_phrases:
                return []
                
            # 2. Semantic Re-ranking
            self._load_embedder()
            if self.embedding_model:
                # Embed full text
                doc_embedding = self.embedding_model.encode(text, convert_to_tensor=True)
                
                # Embed candidates
                candidate_embeddings = self.embedding_model.encode(candidate_phrases, convert_to_tensor=True)
                
                # Compute Cosine Similarity
                cos_scores = util.cos_sim(doc_embedding, candidate_embeddings)[0]
                
                # Create (phrase, score) pairs and sort descending
                scored_candidates = []
                for i, phrase in enumerate(candidate_phrases):
                    scored_candidates.append((phrase, cos_scores[i].item()))
                
                # Sort by similarity (high to low)
                scored_candidates.sort(key=lambda x: x[1], reverse=True)
                
                # Deduplicate roughly (optional, but YAKE handles some) and pick Top N
                final_keywords = [cand[0] for cand in scored_candidates[:top_n]]
                return final_keywords
            
            else:
                # If embedder failed, just return YAKE results sorted by YAKE score (which was original order)
                return candidate_phrases[:top_n]

        except Exception as e:
            logger.error(f"Error in keyword extraction: {e}")
            logger.debug(traceback.format_exc())
            return []

    def extract_topics(self, topics, top_n=5):
        """
        Enriches a list of topic segments with keywords.
        Preserves original metadata.
        
        Args:
            topics (list): List of dicts (id, start, end, text, ...).
            top_n (int): Keywords per topic.
            
        Returns:
            list: Updated topics list with 'keywords' field.
        """
        if not topics:
            return []
            
        logger.info(f"Extracting keywords for {len(topics)} topics...")
        
        for topic in topics:
            text = topic.get('text', '')
            if text:
                keywords = self.extract(text, top_n=top_n)
                topic['keywords'] = keywords
                # logger.info(f"Topic {topic.get('id', '?')}: {keywords}")
            else:
                topic['keywords'] = []
                
        return topics
