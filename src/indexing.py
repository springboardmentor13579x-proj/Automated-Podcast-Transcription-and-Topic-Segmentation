import logging
from sentence_transformers import SentenceTransformer, util
import numpy as np
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TopicIndexer:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initializes the Semantic Indexer/Navigation Agent.
        
        Args:
            model_name (str): SentenceTransformer model name.
        """
        self.model_name = model_name
        self.model = None
        self.topics = []
        self.embeddings = None
        self._is_loaded = False
        
    def _load_model(self):
        if not self._is_loaded:
            logger.info(f"Loading Indexing Model: {self.model_name}...")
            try:
                self.model = SentenceTransformer(self.model_name)
                self._is_loaded = True
            except Exception as e:
                logger.error(f"Failed to load indexing model: {e}")
                
    def index_topics(self, topics):
        """
        Builds a semantic index for the provided topics.
        
        Args:
            topics (list): List of topic dictionaries (id, text, summary, keywords, etc.)
        """
        if not topics:
            logger.warning("No topics provided for indexing.")
            return

        self.topics = topics
        self._load_model()
        
        if not self.model:
            logger.error("Model not loaded, skipping indexing.")
            return

        logger.info(f"Indexing {len(topics)} topics...")
        
        # Construct semantic representation for each topic
        # We combine Title, Summary, and Keywords for a rich representation
        corpus = []
        for t in topics:
            title = t.get('title', '')
            summary = t.get('summary', '')
            keywords = ", ".join(t.get('keywords', []))
            
            # Representation: "Title. Summary. Keywords"
            text_rep = f"{title}. {summary}. {keywords}".strip()
            # If summary/keywords missing, use text snippet (longer, but better than nothing)
            if len(text_rep) < 10:
                text_rep = t.get('text', '')[:1000] 
                
            corpus.append(text_rep)
            
        try:
            self.embeddings = self.model.encode(corpus, convert_to_tensor=True)
            logger.info("Topic indexing complete.")
        except Exception as e:
            logger.error(f"Indexing failed: {e}")
            self.embeddings = None

    def search(self, query, top_n=3):
        """
        Performs semantic search on the indexed topics.
        
        Args:
            query (str): User search query.
            top_n (int): Number of results to return.
            
        Returns:
            list: List of result dicts: { 'id', 'score', 'start', 'title', 'summary' }
        """
        if not query or not query.strip():
            return []
            
        if self.embeddings is None or len(self.topics) == 0:
            logger.warning("Index is empty. Call index_topics() first.")
            return []
            
        self._load_model()
        
        try:
            # Embed Query
            query_embedding = self.model.encode(query, convert_to_tensor=True)
            
            # Compute Similarity
            cos_scores = util.cos_sim(query_embedding, self.embeddings)[0]
            
            # Rank Results
            # torch.topk is efficient
            top_results = list(zip(cos_scores, range(len(cos_scores))))
            top_results.sort(key=lambda x: x[0], reverse=True)
            top_results = top_results[:top_n]
            
            results = []
            for score, idx in top_results:
                topic = self.topics[idx]
                results.append({
                    'id': topic.get('id'),
                    'score': float(score),
                    'start': topic.get('start'),
                    'end': topic.get('end'),
                    'title': topic.get('title', f"Topic {topic.get('id')}"),
                    'summary': topic.get('summary', '')[:200] + "..." 
                })
                
            return results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            logger.debug(traceback.format_exc())
            return []

    def get_topic_by_id(self, topic_id):
        """
        Helper to get full topic data by ID.
        """
        for t in self.topics:
            if t.get('id') == topic_id:
                return t
        return None
