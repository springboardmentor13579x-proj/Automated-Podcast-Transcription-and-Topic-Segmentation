import os
from src.preprocessing.audio_preprocessor import preprocess_audio

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

def preprocess_all_audio():
    files = os.listdir(RAW_DIR)
    
    for f in files:
        if f.endswith((".mp3", ".wav", ".m4a",)):
            input_path = os.path.join(RAW_DIR, f)
            output_filename = os.path.splitext(f)[0] + "_cleaned.wav"
            output_path = os.path.join(PROCESSED_DIR, output_filename)
            
            preprocess_audio(input_path, output_path)
            
    print("All audio files processed successfully!")
    
if __name__ == "__main__":
    preprocess_all_audio()
