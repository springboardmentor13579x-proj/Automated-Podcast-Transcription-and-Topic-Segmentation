# src/config.py
import os

# Get absolute path of project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AUDIO_RAW = os.path.join(BASE_DIR, "audio_raw")
AUDIO_PROCESSED = os.path.join(BASE_DIR, "audio_processed")
ASR_TRANSCRIPTS = os.path.join(BASE_DIR, "asr_transcripts")
FINAL_TRANSCRIPTS = os.path.join(BASE_DIR, "final_session_transcripts")
MANUAL_ANNOTATIONS = os.path.join(BASE_DIR, "manual_annotations")
MANUAL_MERGED = os.path.join(BASE_DIR, "manual_merged")
