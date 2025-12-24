import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TopicSegmenter:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initializes the SentenceTransformer model.
        """
        logger.info(f"Loading Sentence Transformer model: {model_name}")
        try:
            self.model = SentenceTransformer(model_name)
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise

    def segment_transcript(self, transcript_segments, window_size=3, step=1, min_topic_duration=30.0):
        """
        Segments transcript based on semantic similarity with dynamic thresholding.
        
        Args:
            transcript_segments (list): List of dicts [{'text': ..., 'start': ..., 'end': ...}]
            window_size (int): Sentences per window.
            step (int): Sliding step size.
            min_topic_duration (float): Minimum duration in seconds to accept a topic split.
            
        Returns:
            list: List of topics [{'id': ..., 'start': ..., 'end': ..., 'text': ...}]
        """
        if not transcript_segments:
            logger.warning("Empty transcript segments provided.")
            return []

        logger.info(f"Segmenting {len(transcript_segments)} segments...")

        sentences = [seg['text'] for seg in transcript_segments]
        
        # 1. Semantic Embedding
        embeddings = self.model.encode(sentences)
        
        # 2. Sliding Window & Cosine Similarity
        # We group sentences into windows and compare adjacent windows.
        n_sentences = len(sentences)
        similarities = []
        
        # Window indices
        # We look at valid start points for window i and window i+1
        # Window i: sentences[i : i + window_size]
        # Window i+1: sentences[i + step : i + step + window_size]
        # We want to detect the gap between index k and k+1.
        
        # Simpler approach: Calculate similarity between strictly adjacent windows of size k
        # or overlapping. Standard TextTiling uses block comparison.
        
        # Let's map similarity to the gap between sentence i and i+1.
        # We compute similarity of window ending at i vs window starting at i+1
        
        gap_scores = []
        
        for i in range(n_sentences - 2 * window_size + 1):
            # Window 1: left of gap
            w1_emb = np.mean(embeddings[i : i + window_size], axis=0).reshape(1, -1)
            # Window 2: right of gap
            w2_emb = np.mean(embeddings[i + window_size : i + 2 * window_size], axis=0).reshape(1, -1)
            
            sim = cosine_similarity(w1_emb, w2_emb)[0][0]
            gap_scores.append(sim)
            
        # If transcript is too short for windows, return single topic
        if not gap_scores:
            logger.info("Transcript too short for segmentation. Returning single topic.")
            return self._create_single_topic(transcript_segments)

        # 3. Dynamic Thresholding
        gap_scores = np.array(gap_scores)
        mean_sim = np.mean(gap_scores)
        std_sim = np.std(gap_scores)
        threshold = mean_sim - 0.5 * std_sim # Tune magnitude of std dev if needed
        
        logger.info(f"Similarity stats: Mean={mean_sim:.3f}, Std={std_sim:.3f}, Threshold={threshold:.3f}")
        
        # 4. Topic Construction
        # A boundary exists at index `i + window_size` if gap_scores[i] < threshold
        # But we need to map back to original segment indices.
        # gap_scores[0] corresponds to gap after sentence (0 + window_size - 1) -> Actually gap is between (window_size-1) and (window_size)
        
        boundaries = [0]
        last_boundary_time = transcript_segments[0]['start']
        
        # The i-th score in gap_scores corresponds to the gap at index (i + window_size)
        # sentences[i+window_size-1] is the last sent of left block
        # sentences[i+window_size] is the first sent of right block
        
        for i, score in enumerate(gap_scores):
            idx = i + window_size
            if score < threshold:
                # Potential boundary at index `idx` (start of new topic)
                seg_time = transcript_segments[idx]['start']
                
                # Check minimum duration constraint
                if (seg_time - last_boundary_time) >= min_topic_duration:
                    boundaries.append(idx)
                    last_boundary_time = seg_time
        
        boundaries.append(n_sentences)
        
        # 5. Construct Segments
        topics = []
        topic_id = 0
        
        for i in range(len(boundaries) - 1):
            start_idx = boundaries[i]
            end_idx = boundaries[i+1]
            
            if start_idx >= end_idx:
                continue
                
            chunk = transcript_segments[start_idx:end_idx]
            text = " ".join([s['text'] for s in chunk])
            start_t = chunk[0]['start']
            end_t = chunk[-1]['end']
            
            topics.append({
                "id": topic_id,
                "start": start_t,
                "end": end_t,
                "text": text
            })
            topic_id += 1
            
        logger.info(f"Found {len(topics)} topics.")
        return topics

    def _create_single_topic(self, segments):
        if not segments:
            return []
        text = " ".join([s['text'] for s in segments])
        return [{
            "id": 0,
            "start": segments[0]['start'],
            "end": segments[-1]['end'],
            "text": text
        }]
