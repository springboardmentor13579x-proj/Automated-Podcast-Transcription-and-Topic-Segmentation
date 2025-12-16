import os
import whisper

CLEAN_DIR = "../clean_audio"
OUTPUT_DIR = "../transcripts"

model = whisper.load_model("base")   # You can use "small", "medium", "large"


def transcribe_audio(file_name):
    print(f"\n Transcribing: {file_name}")

    input_path = os.path.join(CLEAN_DIR, file_name)
    result = model.transcribe(input_path)

    # Create output text file name
    text_file = file_name.replace(".wav", ".txt")
    output_path = os.path.join(OUTPUT_DIR, text_file)

    # Save transcript
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    print(f" Transcript saved: {output_path}")


def run_transcription():
    for file in os.listdir(CLEAN_DIR):
        if file.endswith(".wav"):
            transcribe_audio(file)


if __name__ == "__main__":
    run_transcription()
