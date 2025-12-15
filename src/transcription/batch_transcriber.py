import os
from src.transcription.whisper_transcriber import transcribe_audio

PROCESSED_DIR = "data/processed"
TRANSCRIPT_DIR = "data/transcripts"

def transcribe_all_audios():
    
    files = os.listdir(PROCESSED_DIR)
    
    for f in files:
        
        if f.endswith((".wav", ".mp3")):
            input_path = os.path.join(PROCESSED_DIR, f)
            
            base_name = os.path.splitext(f)[0]
            output_path = os.path.join(TRANSCRIPT_DIR, base_name + ".json")
            
            print(f"Transcribing: {f}")
            transcribe_audio(input_path, output_path)
            
    print("\nAll transcripts generated successfully!")
    
    
if __name__ == "__main__":
    transcribe_all_audios()