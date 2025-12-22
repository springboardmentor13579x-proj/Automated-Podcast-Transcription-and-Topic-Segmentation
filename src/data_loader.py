import os
import shutil
from pydub import AudioSegment, effects

def scan_and_process_audio(external_folder_path, temp_dir):
    """
    Scans an external folder for .mp3 AND .wav files.
    Converts them to normalized 16kHz WAV files for Whisper.
    """
    # 1. Verification
    if not os.path.exists(external_folder_path):
        print(f"❌ Error: The folder path does not exist:\n   {external_folder_path}")
        return

    print(f"📂 Scanning for audio files in: {external_folder_path}...")
    
    found_files = []
    # Walk through folder to find audio
    for root, dirs, files in os.walk(external_folder_path):
        for f in files:
            # 👇 CHANGE: Accept both .wav and .mp3
            if f.lower().endswith(('.wav', '.mp3')) and not f.startswith('.'):
                full_path = os.path.join(root, f)
                # Optional: Filter out tiny files (less than 50KB) to avoid errors
                if os.path.getsize(full_path) > 50 * 1024:
                    found_files.append(full_path)
    
    if not found_files:
        print("❌ No .mp3 or .wav files found!")
        print("   Please check the folder path in main.py again.")
        return

    print(f"✅ Found {len(found_files)} audio files. Starting processing...")

    # 2. Processing Loop
    for file_path in found_files:
        try:
            filename = os.path.basename(file_path)
            
            # Create temp output path (Always force .wav extension for Whisper)
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            
            # If original is "audio.mp3", temp becomes "audio.wav"
            base_name = os.path.splitext(filename)[0]
            temp_work_path = os.path.join(temp_dir, base_name + ".wav")

            # --- PREPROCESSING ---
            # PyDub handles mp3 automatically IF ffmpeg is installed
            raw_audio = AudioSegment.from_file(file_path)
            
            # Normalize volume
            normalized_audio = effects.normalize(raw_audio)
            
            # Set to 16kHz Mono (Ideal for Whisper)
            normalized_audio = normalized_audio.set_frame_rate(16000).set_channels(1)
            
            # Export as WAV to temp folder
            normalized_audio.export(temp_work_path, format="wav")
            
            # Yield the path to main.py
            # Note: We yield the NEW .wav filename, not the original .mp3 name
            yield temp_work_path, os.path.basename(temp_work_path)
            
            # Cleanup temp file
            if os.path.exists(temp_work_path):
                os.remove(temp_work_path)

        except FileNotFoundError:
             print("❌ ERROR: 'ffmpeg' not found. You cannot process MP3s without it.")
             print("   👉 Install ffmpeg or download a WAV dataset instead.")
             break
        except Exception as e:
            print(f"⚠️ Error processing {filename}: {e}")
