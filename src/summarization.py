from transformers import pipeline
import torch
import logging
import math

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Summarizer:
    def __init__(self, model_name="sshleifer/distilbart-cnn-12-6"):
        """
        Initializes the Summarization pipeline with GPU support.
        """
        self.device = 0 if torch.cuda.is_available() else -1
        description = "GPU" if self.device == 0 else "CPU"
        logger.info(f"Loading Summarization model: {model_name} on {description}")
        
        try:
            self.summarizer = pipeline("summarization", model=model_name, device=self.device)
            # Tokenizer is needed for chunking
            self.tokenizer = self.summarizer.tokenizer
        except Exception as e:
            logger.error(f"Failed to load summarizer: {e}")
            raise

    def summarize(self, text, max_length=150, min_length=40, extraction_type="paragraph"):
        """
        Summarizes text with safety handles for length and errors.
        Strategies:
        - 'paragraph': Standard summary.
        - 'tldr': Very short summary.
        - 'title': Extremely short summary.
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for summarization.")
            return ""

        # Adaptive length constraints based on input length
        # Approximate token count (1 word ~ 1.3 tokens usually, but let's be safe)
        input_len = len(text.split())
        
        # If input is shorter than min_length, just return it
        if input_len < min_length:
            return text

        # Adjust constraints
        if extraction_type == 'tldr':
            max_length = min(50, input_len // 2)
            min_length = 10
        elif extraction_type == 'title':
            max_length = 15
            min_length = 3
        
        try:
            # Handle long text via chunking
            # BART limit is usually 1024 tokens.
            # safe limit 900
            max_input_tokens = 900
            
            # Simple check: do we need chunking?
            # encoding efficiently
            tokens = self.tokenizer.encode(text, truncation=False)
            
            if len(tokens) <= max_input_tokens:
                return self._summarize_chunk(text, max_length, min_length)
            
            # Chunking strategy
            logger.info(f"Text too long ({len(tokens)} tokens), chunking...")
            chunk_size = 800 # overlap logic could be added, but simple chunking for now
            chunks = [tokens[i:i + chunk_size] for i in range(0, len(tokens), chunk_size)]
            
            summaries = []
            for chunk in chunks:
                chunk_text = self.tokenizer.decode(chunk, skip_special_tokens=True)
                # Summarize chunk with reduced length
                summ = self._summarize_chunk(chunk_text, max_length=max_length//len(chunks) + 20, min_length=10)
                summaries.append(summ)
                
            # Combine summaries
            combined_text = " ".join(summaries)
            # One final pass to smooth it out? 
            # If combined is still long, recurse. Else return.
            return combined_text
            
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            return text[:200] + "..." # Fallback

    def _summarize_chunk(self, text, max_len, min_len):
        """
        Summarizes a single chunk that fits in context.
        """
        try:
            # Ensure min_len < max_len
            if min_len >= max_len:
                min_len = max_len - 1 if max_len > 1 else 1
            
            output = self.summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)
            return output[0]['summary_text']
        except Exception as e:
            logger.warning(f"Chunk summarization failed: {e}")
            return text[:100]

    def summarize_topics(self, topics):
        """
        Enriches a list of topic segments with summaries and variants.
        Expected topic format: {'id':..., 'text':...}
        Adds: 'summary', 'tldr', 'title', 'bullets'
        """
        logger.info(f"Summarizing {len(topics)} topics...")
        
        for topic in topics:
            text = topic.get('text', '')
            
            # 1. Full Summary
            summary = self.summarize(text, max_length=130, min_length=30, extraction_type="paragraph")
            topic['summary'] = summary
            
            # 2. TL;DR
            topic['tldr'] = self.summarize(summary, extraction_type='tldr') # Summarize the summary for speed
            
            # 3. Title
            topic['title'] = self.summarize(summary, extraction_type='title')
            
            # 4. Bullets
            # Heuristic: Split summary into sentences.
            # Ideally use NLTK, but simple split on '. ' works for basic display
            bullets = [s.strip() for s in summary.split('. ') if s.strip()]
            topic['bullets'] = bullets
            
            logger.info(f"Summarized Topic {topic['id']}")
            
        return topics
