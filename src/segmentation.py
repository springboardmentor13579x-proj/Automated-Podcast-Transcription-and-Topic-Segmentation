import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TopicSegmenter:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        logger.info(f"Loading Sentence Transformer model: {model_name}")
        self.model = SentenceTransformer(model_name)

    def segment_transcript(self, transcript_segments, window_size=3, threshold=0.5):
        """
        Segments the transcript based on semantic similarity gaps.
        
        Args:
            transcript_segments (list): List of dicts from Whisper [{'text': ..., 'start': ..., 'end': ...}]
            window_size (int): Number of sentences to group for comparison.
            threshold (float): Similarity threshold to define a break.
            
        Returns:
            list: List of chapters/topics [{'title': 'Topic 1', 'start': ..., 'end': ..., 'text': ...}]
        """
        logger.info("Segmenting transcript...")
        sentences = [seg['text'] for seg in transcript_segments]
        
        if not sentences:
            return []

        # Generate embeddings
        embeddings = self.model.encode(sentences)
        
        # Calculate cosine similarity between adjacent windows
        n = len(embeddings)
        similarities = []
        for i in range(n - 1):
            sim = cosine_similarity([embeddings[i]], [embeddings[i+1]])[0][0]
            similarities.append(sim)
            
        # Detect boundaries
        boundaries = [0]
        for i, sim in enumerate(similarities):
            if sim < threshold:
                boundaries.append(i + 1)
        boundaries.append(n)
        
        # Construct segments
        topics = []
        for i in range(len(boundaries) - 1):
            start_idx = boundaries[i]
            end_idx = boundaries[i+1]
            
            check_segments = transcript_segments[start_idx:end_idx]
            combined_text = " ".join([s['text'] for s in check_segments])
            start_time = check_segments[0]['start']
            end_time = check_segments[-1]['end']
            
            topics.append({
                'id': i,
                'start': start_time,
                'end': end_time,
                'text': combined_text.strip()
            })
            
        logger.info(f"Found {len(topics)} topics.")
        return topics
