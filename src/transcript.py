import os
import whisper

# ---------------------------------------------------------
# 1. LOAD WHISPER MODEL
# ---------------------------------------------------------
def load_model(name="small"):
    print(f"Loading Whisper model: {name} ...")
    model = whisper.load_model(name)
    print("Model loaded successfully.\n")
    return model


# ---------------------------------------------------------
# 2. TRANSCRIBE SINGLE AUDIO FILE
# ---------------------------------------------------------
def transcribe_file(model, audio_path, output_path):
    print(f"Transcribing: {os.path.basename(audio_path)}")

    result = model.transcribe(
        audio_path,
        fp16=False,     # safer for CPU systems
        verbose=False
    )

    text = result["text"]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Saved transcript → {output_path}\n")


# ---------------------------------------------------------
# 3. GET AUDIO FILES
# ---------------------------------------------------------
def get_audio_files(audio_dir, extensions):
    return [
        os.path.join(audio_dir, f)
        for f in os.listdir(audio_dir)
        if f.lower().endswith(extensions)
    ]


# ---------------------------------------------------------
# 4. ENSURE OUTPUT DIRECTORY EXISTS
# ---------------------------------------------------------
def ensure_output_dir(path):
    os.makedirs(path, exist_ok=True)


# ---------------------------------------------------------
# 5. MAIN FUNCTION (RESUME-SAFE)
# ---------------------------------------------------------
def main():
    AUDIO_DIR = r"C:\Users\ramay\Desktop\AI_podcast_transcript\data\processed"
    OUTPUT_DIR = r"C:\Users\ramay\Desktop\AI_podcast_transcript\transcripts"
    MODEL_NAME = "small"

    AUDIO_EXTENSIONS = (".wav", ".mp3", ".m4a", ".flac")

    ensure_output_dir(OUTPUT_DIR)

    model = load_model(MODEL_NAME)

    audio_files = get_audio_files(AUDIO_DIR, AUDIO_EXTENSIONS)

    print("Starting transcription process...\n")

    for audio_path in audio_files:
        file_name = os.path.basename(audio_path)
        output_file = file_name + ".txt"
        output_path = os.path.join(OUTPUT_DIR, output_file)

        # 🔁 Skip already transcribed files
        if os.path.exists(output_path):
            print(f"Skipping (already transcribed): {file_name}")
            continue

        transcribe_file(model, audio_path, output_path)

    print("\n Transcription completed for all remaining files!")


# ---------------------------------------------------------
# 6. ENTRY POINT
# ---------------------------------------------------------
if __name__ == "__main__":
    main()
