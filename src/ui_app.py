import streamlit as st
import json
from pathlib import Path
from textblob import TextBlob

from preprocessing import preprocess_audio
from transcription import load_whisper_model, transcribe_audio
from segmentation import load_segmenter, segment_text
from keyword_extraction import extract_keywords

BASE_DIR = Path(__file__).resolve().parent.parent
META_FILE = BASE_DIR / "docs" / "processing_metadata.json"
AUDIO_RAW_DIR = BASE_DIR / "audio_raw"
AUDIO_PROCESSED_DIR = BASE_DIR / "audio_processed"
TRANSCRIPT_DIR = BASE_DIR / "transcripts"
SEGMENT_DIR = BASE_DIR / "segments"

st.set_page_config(layout="wide")
st.title("Podcast Transcript Navigator")

def load_metadata():
    if META_FILE.exists():
        return json.loads(META_FILE.read_text())
    return {}

def save_metadata(meta):
    META_FILE.write_text(json.dumps(meta, indent=2))

def load_json(path):
    p = Path(path)
    if p.exists():
        return json.loads(p.read_text())
    return []

def compute_sentiment(text):
    return round(TextBlob(text).sentiment.polarity, 3)

if "start_time" not in st.session_state:
    st.session_state.start_time = 0

metadata = load_metadata()

st.subheader("Upload Audio")

uploaded = st.file_uploader(
    "Upload audio (mp3 / wav / m4a)",
    type=["mp3", "wav", "m4a"]
)

if uploaded:
    AUDIO_RAW_DIR.mkdir(exist_ok=True)
    audio_path = AUDIO_RAW_DIR / uploaded.name

    if not audio_path.exists():
        audio_path.write_bytes(uploaded.read())
        metadata[uploaded.name] = {
            "preprocessing": {"status": "pending"},
            "transcription": {"status": "pending"},
            "segmentation": {"status": "pending"},
            "keywords": {"status": "pending"}
        }
        save_metadata(metadata)
        st.success("Audio uploaded and registered")
    else:
        st.warning("File already exists")

st.divider()

if not metadata:
    st.error("No audio files available")
    st.stop()

st.subheader("Select Audio")
file_key = st.selectbox("Available Audio Files", sorted(metadata.keys()))
data = metadata[file_key]

audio_path = AUDIO_RAW_DIR / file_key
if not audio_path.exists():
    st.error("Audio file not found")
    st.stop()

st.subheader("Audio Player")
st.audio(str(audio_path), start_time=st.session_state.start_time)

st.divider()

def run_pipeline(file_key):
    AUDIO_PROCESSED_DIR.mkdir(exist_ok=True)
    TRANSCRIPT_DIR.mkdir(exist_ok=True)
    SEGMENT_DIR.mkdir(exist_ok=True)

    raw_audio = AUDIO_RAW_DIR / file_key
    processed_audio = AUDIO_PROCESSED_DIR / f"{Path(file_key).stem}_clean.wav"
    transcript_path = TRANSCRIPT_DIR / f"{file_key}_transcript.txt"
    segment_path = SEGMENT_DIR / f"{file_key}_segments.json"

    st.info("Preprocessing audio")
    preprocess_audio(str(raw_audio), str(processed_audio))
    metadata[file_key]["preprocessing"] = {
        "processed_audio": str(processed_audio),
        "status": "done"
    }
    save_metadata(metadata)

    st.info("Transcribing audio")
    whisper = load_whisper_model("base")
    full_text, chunks = transcribe_audio(whisper, str(processed_audio))
    transcript_path.write_text(full_text)
    metadata[file_key]["transcription"] = {
        "transcript_file": str(transcript_path),
        "status": "done"
    }
    save_metadata(metadata)

    st.info("Segmenting transcript")
    segmenter = load_segmenter()
    segments = segment_text(segmenter, full_text)

    for seg in segments:
        seg["sentiment"] = compute_sentiment(seg["text"])
        seg["keywords"] = extract_keywords(seg["text"])

    segment_path.write_text(json.dumps(segments, indent=2))
    metadata[file_key]["segmentation"] = {
        "segment_file": str(segment_path),
        "status": "done"
    }
    metadata[file_key]["keywords"] = {"status": "done"}
    save_metadata(metadata)

    st.success("Processing complete")

if data.get("segmentation", {}).get("status") != "done":
    if st.button("Run Processing Pipeline"):
        run_pipeline(file_key)
        st.rerun()
    st.stop()

segments = load_json(data["segmentation"]["segment_file"])
if not segments:
    st.warning("No segments available")
    st.stop()

st.subheader("Search Transcript")

all_keywords = sorted({kw for s in segments for kw in s.get("keywords", [])})

c1, c2 = st.columns([2, 3])
with c1:
    selected_keyword = st.selectbox("Select keyword", ["None"] + all_keywords)
with c2:
    typed_keyword = st.text_input("Type keyword or text")

st.divider()

filtered_segments = []

for seg in segments:
    text = seg["text"]
    keywords = seg.get("keywords", [])

    if typed_keyword:
        if typed_keyword.lower() in text.lower() or any(
            typed_keyword.lower() in k.lower() for k in keywords
        ):
            filtered_segments.append(seg)
    elif selected_keyword != "None":
        if selected_keyword in keywords:
            filtered_segments.append(seg)

st.subheader("Transcript Results")

if not filtered_segments:
    st.info("Select or type a keyword to view transcript")
else:
    for idx, seg in enumerate(filtered_segments, start=1):
        c1, c2 = st.columns([1, 6])
        with c1:
            st.markdown(f"{seg['start']:.2f}s")
            if st.button("Play", key=f"play_{idx}"):
                st.session_state.start_time = int(seg["start"])
                st.rerun()
        with c2:
            for para in seg["text"].split(". "):
                if para.strip():
                    st.write(para.strip())
            if seg.get("keywords"):
                st.caption("Keywords: " + ", ".join(seg["keywords"]))
            st.caption(f"Sentiment: {seg['sentiment']}")
        st.divider()

if data.get("transcription", {}).get("status") == "done":
    transcript_path = Path(data["transcription"]["transcript_file"])
    if transcript_path.exists():
        with st.expander("View Full Transcript"):
            full_text = transcript_path.read_text().strip()
            for para in full_text.split("\n\n"):
                if para.strip():
                    st.write(para.strip())
