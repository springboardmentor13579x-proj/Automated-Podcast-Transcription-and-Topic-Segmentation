import whisper
import os

model = whisper.load_model("base")

audio_dir = "../audio/raw"
output_dir = "../transcripts/predicted"

os.makedirs(output_dir, exist_ok=True)

for file in os.listdir(audio_dir):
    if file.endswith(".mp3"):
        audio_path = os.path.join(audio_dir, file)
        print(f"Transcribing {file}...")

        result = model.transcribe(audio_path)

        out_file = os.path.join(output_dir, file.replace(".mp3", ".txt"))
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(result["text"])

print("All files transcribed")