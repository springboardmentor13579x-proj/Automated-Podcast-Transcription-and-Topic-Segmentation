import os
import whisper
import config

def transcribe_all_audio():
    print("\n--- STARTING: Transcription Module ---")
    print("Loading Whisper AI Model (This may take a moment)...")
    model = whisper.load_model("base")

    files = [f for f in os.listdir(config.PROCESSED_FOLDER) if f.startswith("clean_") and f.endswith(".wav")]
    
    if not files:
        print("❌ No clean audio found. Run cleaning first.")
        return

    for filename in files:
        print(f"Transcribing: {filename}...")
        input_path = os.path.join(config.PROCESSED_FOLDER, filename)
        
        # Output filename: clean_audio.wav -> transcript_audio.txt
        base_name = filename.replace("clean_", "transcript_").replace(".wav", ".txt")
        output_path = os.path.join(config.PROCESSED_FOLDER, base_name)

        try:
            # Transcribe
            result = model.transcribe(input_path)
            
            # Save nicely formatted text (Time + Text)
            with open(output_path, "w", encoding="utf-8") as f:
                for segment in result["segments"]:
                    start = segment['start']
                    end = segment['end']
                    text = segment['text'].strip()
                    # Format: [00:12.00 -> 00:15.00] Hello world.
                    f.write(f"[{start:.2f}s -> {end:.2f}s] {text}\n")
            
            print(f"   ✅ Saved Transcript: {base_name}")

        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    transcribe_all_audio()