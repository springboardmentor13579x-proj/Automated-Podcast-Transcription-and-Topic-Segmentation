from faster_whisper import WhisperModel
import logging
import torch
import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Transcriber:
    def __init__(self, model_size="base", device=None, compute_type="int8"):
        """
        Initializes the Faster-Whisper model efficiently.
        """
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        logger.info(f"Loading Faster-Whisper model: {model_size} on {self.device} with {compute_type}")
        
        try:
            self.model = WhisperModel(model_size, device=self.device, compute_type=compute_type)
        except Exception as e:
            logger.warning(f"Failed to load with {compute_type}, falling back to float32. Error: {e}")
            try:
                 self.model = WhisperModel(model_size, device=self.device, compute_type="float32")
            except Exception as e2:
                 logger.error(f"Critical error loading model: {e2}")
                 raise

    def transcribe(self, audio_path):
        """
        Transcribes audio file and returns result dict with text, segments, and info.
        Uses beam search and VAD (silence filtering).
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
        logger.info(f"Transcribing {audio_path}...")
        try:
            # vad_filter=True enables silence filtering
            segments_generator, info = self.model.transcribe(
                audio_path, 
                beam_size=5, 
                vad_filter=True
            )
            
            segments = []
            full_text = ""
            
            for segment in segments_generator:
                segments.append({
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text.strip()
                })
                full_text += segment.text + " "
                
            logger.info(f"Transcription complete. Detected language: {info.language} (probability: {info.language_probability:.2f})")
            
            return {
                "text": full_text.strip(),
                "segments": segments,
                "language": info.language
            }
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise

    def save_outputs(self, result, audio_filename, transcript_dir="transcripts", segments_dir="segments"):
        """
        Saves full transcription text to transcripts/ and segments to segments/.
        """
        try:
            # Ensure directories exist
            os.makedirs(transcript_dir, exist_ok=True)
            os.makedirs(segments_dir, exist_ok=True)
            
            base_name = os.path.splitext(audio_filename)[0]
            
            # Save Text (.txt)
            txt_path = os.path.join(transcript_dir, f"{base_name}.txt")
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(result['text'])
            logger.info(f"Saved transcript to {txt_path}")
            
            # Save Segments (.json)
            # Also saving language info in the same file for completeness? 
            # Request asked for "Detailed segment data". I'll save the segments list wrapped in a dict or just the list.
            # Usually strict JSON structure is preferred.
            json_path = os.path.join(segments_dir, f"{base_name}.json")
            output_data = {
                "language": result['language'],
                "segments": result['segments']
            }
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved segments to {json_path}")
            
            return txt_path, json_path
            
        except Exception as e:
            logger.error(f"Failed to save outputs: {e}")
            raise

    def process_file(self, audio_path, transcript_dir, segments_dir):
        """
        Orchestrates transcription and saving.
        """
        result = self.transcribe(audio_path)
        filename = os.path.basename(audio_path)
        self.save_outputs(result, filename, transcript_dir, segments_dir)
        return result
