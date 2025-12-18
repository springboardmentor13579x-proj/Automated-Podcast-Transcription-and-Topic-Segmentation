import os
import librosa
import soundfile as sf
from pydub import AudioSegment
import config

def clean_all_audio():
    print("\n--- STARTING: Audio Cleaning Module ---")
    
    # Get list of all raw files (supports mp3, flac, wav)
    files = [f for f in os.listdir(config.RAW_FOLDER) if f.endswith(('.flac', '.wav', '.mp3'))]
    
    if not files:
        print("❌ No files found! Please put an audio file in 'data/raw'.")
        return

    for filename in files:
        print(f"Processing: {filename}...")
        
        input_path = os.path.join(config.RAW_FOLDER, filename)
        file_base_name = os.path.splitext(filename)[0]
        output_wav = os.path.join(config.PROCESSED_FOLDER, f"clean_{file_base_name}.wav")
        temp_wav = os.path.join(config.PROCESSED_FOLDER, "temp.wav")

        try:
            # 1. Resample to 16kHz (Standard for AI)
            # Note: librosa loads any format (mp3/flac) and converts to array
            y, sr = librosa.load(input_path, sr=16000)
            sf.write(temp_wav, y, sr)

            # 2. Normalize Volume (Make it consistent)
            audio = AudioSegment.from_wav(temp_wav)
            normalized_audio = audio.normalize()
            
            # 3. Save Final Clean File
            normalized_audio.export(output_wav, format="wav")
            print(f"   Cleaned: {output_wav}")

        except Exception as e:
            print(f"    Error: {e}")
            
    # Cleanup temp file
    if os.path.exists(temp_wav):
        os.remove(temp_wav)

if __name__ == "__main__":
    clean_all_audio()