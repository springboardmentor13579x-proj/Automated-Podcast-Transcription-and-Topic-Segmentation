from faster_whisper import WhisperModel
import json
import os

# Load Faster-Whisper model (same size as before)
model = WhisperModel(
    "small",
    device="cpu",        # change to "cuda" if GPU available
    compute_type="int8"  # fastest on CPU
)

def transcribe_audio(audio_path, output_path):
    segments, info = model.transcribe(audio_path)

    transcript_json = {
        "audio_file": audio_path,
        "language": info.language,
        "segments": []
    }

    for seg in segments:
        transcript_json["segments"].append({
            "start": seg.start,
            "end": seg.end,
            "text": seg.text
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(transcript_json, f, indent=4)

    print(f"Saved transcript: {output_path}")
