import json
import time
import subprocess
import sys
import wave
import os
from pathlib import Path
from vosk import Model, KaldiRecognizer
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
TRANSCRIPTS_DIR = PROJECT_ROOT / "transcripts"

META_FILE = DOCS_DIR / "processing_metadata.json"

VOSK_MODEL_PATH = os.getenv("VOSK_MODEL_PATH")
if not VOSK_MODEL_PATH:
    raise RuntimeError("VOSK_MODEL_PATH is not set in .env")

VOSK_MODEL_PATH = Path(VOSK_MODEL_PATH).expanduser().resolve()

CHUNK_DURATION = 300  # seconds (5 minutes)

DOCS_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

if not META_FILE.exists():
    META_FILE.write_text("{}")

model = Model(str(VOSK_MODEL_PATH))

def load_metadata():
    return json.loads(META_FILE.read_text())

def save_metadata(data):
    META_FILE.write_text(json.dumps(data, indent=4))

def get_audio_duration(audio_path: Path):
    output = subprocess.check_output(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(audio_path)
        ]
    )
    return int(float(output.strip()))

def print_progress(done, total):
    percent = int((done / total) * 100)
    sys.stdout.write(f"\rProgress: {percent}%")
    sys.stdout.flush()

def force_create_file(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.touch()

def transcribe_audio(audio_path: Path, file_key: str):
    start_time = time.time()
    duration = get_audio_duration(audio_path)
    total_chunks = (duration // CHUNK_DURATION) + 1

    transcript_name = f"{file_key}_transcript.txt"
    txt_path = TRANSCRIPTS_DIR / transcript_name
    txt_path.parent.mkdir(parents=True, exist_ok=True)

    transcript_chunks = []

    with txt_path.open("w", encoding="utf-8") as out:
        for chunk_id, chunk_start in enumerate(range(0, duration, CHUNK_DURATION)):
            chunk_end = min(chunk_start + CHUNK_DURATION, duration)
            temp_chunk = TRANSCRIPTS_DIR / f"tmp_{file_key}_{chunk_id}.wav"

            subprocess.run(
                [
                    "ffmpeg", "-y",
                    "-ss", str(chunk_start),
                    "-t", str(chunk_end - chunk_start),
                    "-i", str(audio_path),
                    "-ac", "1",
                    "-ar", "16000",
                    "-f", "wav",
                    str(temp_chunk)
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            wf = wave.open(str(temp_chunk), "rb")
            rec = KaldiRecognizer(model, wf.getframerate())
            rec.SetWords(True)

            while True:
                data = wf.readframes(4000)
                if not data:
                    break
                rec.AcceptWaveform(data)

            result = json.loads(rec.FinalResult())
            wf.close()
            temp_chunk.unlink(missing_ok=True)

            if "result" not in result:
                continue

            sentence_words = []
            sent_start = None
            last_end = None

            for w in result["result"]:
                word = w["word"]
                w_start = w["start"] + chunk_start
                w_end = w["end"] + chunk_start

                if sent_start is None:
                    sent_start = w_start

                if last_end and (w_start - last_end > 0.8 or len(sentence_words) >= 14):
                    sent_text = " ".join(sentence_words)
                    out.write(f"[{sent_start:.2f}-{last_end:.2f}] {sent_text}\n")

                    transcript_chunks.append({
                        "chunk_id": chunk_id,
                        "start": round(sent_start, 2),
                        "end": round(last_end, 2),
                        "text": sent_text
                    })

                    sentence_words = []
                    sent_start = w_start

                sentence_words.append(word)
                last_end = w_end

            if sentence_words:
                sent_text = " ".join(sentence_words)
                out.write(f"[{sent_start:.2f}-{last_end:.2f}] {sent_text}\n")

                transcript_chunks.append({
                    "chunk_id": chunk_id,
                    "start": round(sent_start, 2),
                    "end": round(last_end, 2),
                    "text": sent_text
                })

            print_progress(chunk_id + 1, total_chunks)

    elapsed = round(time.time() - start_time, 2)
    print("\nTranscription completed")

    return str(txt_path), transcript_chunks, elapsed, duration

def process_all_transcriptions():
    metadata = load_metadata()

    for file_key, data in metadata.items():
        if "transcription" in data:
            continue

        audio_path = Path(data["preprocessing"]["processed_audio"]).resolve()
        if audio_path.suffix.lower() not in [".mp3", ".wav"]:
            continue

        txt_path, chunks, time_taken, duration = transcribe_audio(
            audio_path, file_key
        )

        data["transcription"] = {
            "engine": "vosk-kaldi",
            "audio_duration_sec": duration,
            "chunk_duration_sec": CHUNK_DURATION,
            "total_chunks": len(chunks),
            "transcript_file": txt_path,
            "chunks": chunks,
            "time_taken_sec": time_taken,
            "status": "done"
        }

        save_metadata(metadata)

if __name__ == "__main__":
    process_all_transcriptions()
