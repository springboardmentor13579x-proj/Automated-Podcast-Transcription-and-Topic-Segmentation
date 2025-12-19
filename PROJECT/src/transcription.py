import os
import numpy as np
from jiwer import wer
from faster_whisper import WhisperModel
# PATHS
AUDIO_FOLDER = r"C:\Users\Dell\Desktop\meeting_workspace\clean_wav"
TRANSCRIPT_FOLDER = r"C:\Users\Dell\Desktop\meeting_workspace\transcripts"
SUMMARY_FOLDER = r"C:\Users\Dell\Desktop\meeting_workspace\summaries"

os.makedirs(TRANSCRIPT_FOLDER, exist_ok=True)
os.makedirs(SUMMARY_FOLDER, exist_ok=True)
# LOAD MODEL

print("Loading LOCAL Faster-Whisper (base)...")
model = WhisperModel(
    r"C:\Users\Dell\Desktop\meeting_workspace\local_faster_whisper_base",
    device="cpu",
    compute_type="int8"
)

# MAKE PARAGRAPHS

def make_paragraphs(text, max_len=800):
    words = text.split()
    result, chunk = [], []
    for w in words:
        chunk.append(w)
        if len(chunk) >= max_len:
            result.append(" ".join(chunk))
            chunk = []
    if chunk:
        result.append(" ".join(chunk))
    return "\n\n".join(result)
# SAFE ACCURACY CHECK
def calculate_accuracy(audio_file, text):
    try:
        print(" → Checking accuracy with tiny model…")
        tiny = WhisperModel("tiny", device="cpu", compute_type="int8")
        segs, _ = tiny.transcribe(audio_file)
        tiny_text = " ".join([s.text for s in segs])
        score = wer(tiny_text, text)
        print(f"   ✔ WER Accuracy Score: {score:.4f}")
        return score
    except Exception as e:
        print(f"    Accuracy skipped: {e}")
        return None
# GET PROCESSED NAMES (SMART)
def get_processed():
    processed = set()

    # transcripts
    for f in os.listdir(TRANSCRIPT_FOLDER):
        if f.endswith(".txt"):
            base = os.path.splitext(f)[0].lower().replace("_transcription", "")
            processed.add(base)

    # summaries
    for f in os.listdir(SUMMARY_FOLDER):
        if f.endswith(".txt"):
            base = os.path.splitext(f)[0].lower()
            processed.add(base)

    print(f"\nAlready processed count: {len(processed)}")
    return processed

processed = get_processed()
# MULTI-LEVEL SAFE CHUNK TRANSCRIBER

def safe_transcribe(audio_path):
    """
    Tries several chunk sizes to avoid NumPy memory crash.
    Guarantees a return (even partial).
    """
    chunk_sizes = [30, 20, 10, 5]   # seconds

    # Try normal mode first
    try:
        print(" → Transcribing (normal mode)…")
        segs, _ = model.transcribe(audio_path)
        return " ".join([s.text for s in segs])
    except Exception as e:
        print("  NumPy memory error detected — switching to SAFE CHUNK MODE.")

    # Try reduced chunk sizes
    for c in chunk_sizes:
        try:
            print(f" → Transcribing in SAFE CHUNKS (chunk={c}s)…")
            segs, _ = model.transcribe(audio_path, chunk_length=c)
            return " ".join([s.text for s in segs])
        except Exception as e:
            print(f"    Chunk mode {c}s failed: {e}")

    # If nothing works
    print("    All chunk-modes failed — returning partial blank text.")
    return ""
# MAIN

audio_files = [f for f in os.listdir(AUDIO_FOLDER) if f.lower().endswith(".wav")]
print(f"\nTotal audio files: {len(audio_files)}")

for file in audio_files:
    base = os.path.splitext(file)[0].lower()
    audio_path = os.path.join(AUDIO_FOLDER, file)

    if base in processed:
        print(f" Skipping (already processed): {file}")
        continue

    print("\n----------------------------")
    print(f"Processing: {file}")
    print("----------------------------")

    # SAFE TRANSCRIBE
    text = safe_transcribe(audio_path)

    # Paragraphs
    paragraphs = make_paragraphs(text)

    # Save transcript
    out_path = os.path.join(TRANSCRIPT_FOLDER, base + "_transcription.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(paragraphs)

    print(f"  Transcript saved: {out_path}")

    # Accuracy (safe)
    calculate_accuracy(audio_path, text)

print("\n=========== ALL REMAINING FILES PROCESSED ===========")










