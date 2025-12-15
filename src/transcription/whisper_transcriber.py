import whisper
import json
import os

model = whisper.load_model("small")

def transcribe_audio(audio_path, output_path):
    result = model.transcribe(audio_path)
    
    transcript_json = {
        "audio_file": audio_path,
        "language": result["language"],
        "segments": []
    }
    
    for seg in result["segments"]:
        transcript_json["segments"].append({
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"]
        })
        
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(transcript_json, f, indent=4)
        
        
    print(f"Saved transcript: {output_path}")