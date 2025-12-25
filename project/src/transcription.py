import os
import whisper

# ---------------------------------------------------------
# 1. LOAD MODEL
# ---------------------------------------------------------
def load_model(name="small"):
    print(f"Loading Whisper model: {name}")
    model = whisper.load_model(name)
    print("Model loaded successfully\n")
    return model

# ---------------------------------------------------------
# 2. TRANSCRIBE SINGLE AUDIO
# ---------------------------------------------------------
def transcribe_file(model, audio_path, output_dir):
    print(f"Transcribing: {audio_path}")

    result = model.transcribe(audio_path)
    text = result["text"]

    # output filename (same name, .txt)
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    output_path = os.path.join(output_dir, base_name + ".txt")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Saved transcription → {output_path}\n")

# ---------------------------------------------------------
# 3. MAIN
# ---------------------------------------------------------
def main():
    AUDIO_DIR = r"C:\Users\hp\Desktop\Automated transcription project\project\cleaned_audio"
    OUTPUT_DIR = r"C:\Users\hp\Desktop\Automated transcription project\project\transcripts"

    audio_extensions = (".wav", ".mp3", ".m4a", ".flac")

    # folder check
    print(f" Audio folder: {AUDIO_DIR}")
    print(f" Transcript folder: {OUTPUT_DIR}")

    if not os.path.exists(AUDIO_DIR):
        print(" cleaned_audio folder NOT FOUND")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    audio_files = [
        os.path.join(AUDIO_DIR, f)
        for f in os.listdir(AUDIO_DIR)
        if f.lower().endswith(audio_extensions)
    ]

    if not audio_files:
        print(" No audio files found in cleaned_audio")
        return

    model = load_model("small")


    print(" Starting transcription...\n")

    for audio in audio_files:
        transcribe_file(model, audio, OUTPUT_DIR)

    print(" ALL TRANSCRIPTIONS COMPLETED SUCCESSFULLY")

# ---------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------
if __name__ == "__main__":
    main()
