import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

AUDIO_RAW_DIR = os.path.join(DATA_DIR, "raw")
AUDIO_PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
SEGMENTS_DIR = os.path.join(BASE_DIR, "segment_keySearch_summary")  # or "segment_keySearch_summary" if you want
TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "transcripts")

for d in [AUDIO_RAW_DIR, AUDIO_PROCESSED_DIR, SEGMENTS_DIR, TRANSCRIPTS_DIR]:
    os.makedirs(d, exist_ok=True)

WHISPER_MODEL = "small"
FP16 = False
SENTENCES_PER_SEGMENT = 5
MIN_MEDICAL_TERMS = 5
