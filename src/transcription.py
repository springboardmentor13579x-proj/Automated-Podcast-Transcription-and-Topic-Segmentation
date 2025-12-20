import os
import whisper
from src.config import AUDIO_PROCESSED, ASR_TRANSCRIPTS


def transcribe_audio(
    cleaned_path=AUDIO_PROCESSED,
    transcript_path=ASR_TRANSCRIPTS,
    model_size="base"
):
    """
    Transcribe cleaned audio files using OpenAI Whisper.

    Inputs:
    - cleaned_path: folder with cleaned .wav files
    - transcript_path: output folder for transcripts
    - model_size: whisper model size (tiny/base/small/medium/large)
    """

    # Create output folder if missing
    os.makedirs(transcript_path, exist_ok=True)

    # Load Whisper model
    print(f"Loading Whisper model: {model_size}")
    model = whisper.load_model(model_size)

    # List cleaned audio files
    cleaned_files = [f for f in os.listdir(cleaned_path) if f.endswith(".wav")]
    print("Audio files to transcribe:", cleaned_files)

    for file in cleaned_files:
        audio_file = os.path.join(cleaned_path, file)

        # Transcribe
        result = model.transcribe(audio_file, verbose=False)

        # Save plain transcript
        txt_path = os.path.join(
            transcript_path,
            file.replace(".wav", ".txt")
        )
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(result["text"])

        # Save timestamped segments
        segments_path = os.path.join(
            transcript_path,
            file.replace(".wav", "_segments.txt")
        )
        with open(segments_path, "w", encoding="utf-8") as f:
            for segment in result["segments"]:
                start = segment["start"]
                end = segment["end"]
                text = segment["text"]
                f.write(f"{start:.2f}-{end:.2f} : {text}\n")

        print(f"✅ Transcribed: {file}")
        print(f"   → {txt_path}")
        print(f"   → {segments_path}")


# ===============================
# Script entry point
# ===============================
if __name__ == "__main__":
    transcribe_audio()
