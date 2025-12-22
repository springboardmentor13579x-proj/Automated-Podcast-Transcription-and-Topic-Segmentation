import torch
from transformers import pipeline

class PodcastTranscriber:
    def __init__(self, model_name="openai/whisper-base"):
        """
        Initializes the Whisper model.
        Use 'tiny' for CPU/testing, 'medium' for GPU/accuracy.
        """
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading Model: {model_name} on {device}...")
        
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=model_name,
            chunk_length_s=30, # Critical for long podcasts
            device=device
        )

    def transcribe(self, audio_path):
        """
        Runs the model on an audio file.
        Returns the text and chunks (timestamps).
        """
        # return_timestamps=True is crucial for Milestone 2 (Topic Segmentation)
        result = self.pipe(audio_path, return_timestamps=True)
        return result["text"], result["chunks"]