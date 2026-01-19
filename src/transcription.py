import os
import whisper

def transcribe_audio(audio_dir, output_dir, model_size="base"):
    print("=== WHISPER TRANSCRIPTION ===")
    print("Audio input directory:", os.path.abspath(audio_dir))
    print("Transcript output directory:", os.path.abspath(output_dir))

    if not os.path.exists(audio_dir):
        print("ERROR: audio directory does not exist")
        return

    os.makedirs(output_dir, exist_ok=True)

    files = os.listdir(audio_dir)
    print("Files found:", files)

    if len(files) == 0:
        print("ERROR: No audio files found")
        return

    print("Loading Whisper model:", model_size)
    model = whisper.load_model(model_size)

    for filename in files:
        if not filename.lower().endswith(".wav"):
            print("Skipping (not wav):", filename)
            continue

        audio_path = os.path.join(audio_dir, filename)
        print("Transcribing:", audio_path)

        try:
            result = model.transcribe(audio_path, verbose=False, fp16=False)

            output_file = os.path.join(
                output_dir, filename.replace(".wav", ".txt")
            )

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result["text"].strip())

            print("Saved transcript:", output_file)

        except Exception as e:
            print("ERROR transcribing:", filename)
            print(e)
