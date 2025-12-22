import whisper
import logging
import torch
import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Transcriber:
    def __init__(self, model_size="base", device=None):
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        logger.info(f"Loading Whisper model: {model_size} on {self.device}")
        self.model = whisper.load_model(model_size, device=self.device)

    def transcribe(self, audio_path):
        """
        Transcribes audio file and returns result dict with text and segments.
        """
        logger.info(f"Transcribing {audio_path}...")
        try:
            result = self.model.transcribe(audio_path, verbose=False)
            logger.info("Transcription complete.")
            return result
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise

    def save_transcript(self, result, output_path):
        """
        Saves transcript to JSON file.
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        logger.info(f"Transcript saved to {output_path}")

    def save_text(self, result, output_path):
        """
        Saves text only to txt file.
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result['text'])
        logger.info(f"Text saved to {output_path}")
