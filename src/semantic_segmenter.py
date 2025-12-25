from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SemanticSegmenter:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        print(f"Loading BERT model: {model_name}...")
        self.model = SentenceTransformer(model_name)

    def segment(self, sentences, timestamps, threshold=0.6):
        """
        Splits based on semantic similarity drops.
        
        Args:
            sentences: List of strings (sentences/chunks).
            timestamps: List of (start, end) tuples matching sentences.
            threshold: Similarity score below which a new topic starts (0.0-1.0).
        """
        if not sentences:
            return []

        # 1. Encode all sentences to vectors
        embeddings = self.model.encode(sentences)
        
        segments = []
        current_segment_text = [sentences[0]]
        current_start = timestamps[0][0]
        
        # 2. Compare each sentence with the previous one
        for i in range(1, len(sentences)):
            # Calculate similarity between current sentence and previous
            sim = cosine_similarity(
                [embeddings[i-1]], 
                [embeddings[i]]
            )[0][0]
            
            # If similarity drops below threshold, it's a new topic
            if sim < threshold:
                # Save old segment
                segments.append({
                    "start_time": current_start,
                    "end_time": timestamps[i-1][1],
                    "text": " ".join(current_segment_text),
                    "topic_id": len(segments) + 1
                })
                # Start new segment
                current_segment_text = []
                current_start = timestamps[i][0]
            
            current_segment_text.append(sentences[i])

        # Add the last segment
        segments.append({
            "start_time": current_start,
            "end_time": timestamps[-1][1],
            "text": " ".join(current_segment_text),
            "topic_id": len(segments) + 1
        })
        

        return segments
