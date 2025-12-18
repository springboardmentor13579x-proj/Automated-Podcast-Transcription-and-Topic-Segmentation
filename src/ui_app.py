import streamlit as st
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
META_FILE = PROJECT_ROOT / "docs" / "processing_metadata.json"
AUDIO_RAW = PROJECT_ROOT / "audio_raw"

st.set_page_config(layout="wide")
st.title("Legal (AI Automated Argument Transcription)")

AUDIO_RAW.mkdir(exist_ok=True)

def load_metadata():
    if META_FILE.exists():
        return json.loads(META_FILE.read_text())
    return {}

def save_uploaded_file(uploaded_file):
    path = AUDIO_RAW / uploaded_file.name
    if not path.exists():
        with open(path, "wb") as f:
            f.write(uploaded_file.read())
    return path

def load_transcript_text(path):
    p = Path(path)
    if not p.exists():
        return ""
    lines = p.read_text().splitlines()
    cleaned = [re.sub(r"\[.*?\]\s*", "", l) for l in lines]
    return " ".join(cleaned)

def load_segments(path):
    p = Path(path)
    if p.exists():
        return json.loads(p.read_text())
    return []

meta = load_metadata()

uploaded = st.file_uploader("Upload audio file", type=["wav", "mp3", "m4a"])

if uploaded:
    save_uploaded_file(uploaded)
    st.success("File uploaded")
    st.stop()

if not meta:
    st.write("No processed audio available")
    st.stop()

selected_key = st.selectbox("Select audio file", list(meta.keys()))
search_query = st.text_input("Search text or keywords")

data = meta[selected_key]

st.subheader(selected_key)

show_transcript = st.button("Show Transcription")

if show_transcript:
    if "segmentation" in data:
        segments = load_segments(data["segmentation"]["segment_file"])

        for seg in segments:
            text = seg.get("text", "").strip()
            keywords = seg.get("keywords", [])
            start = seg.get("start", 0.0)
            end = seg.get("end", 0.0)

            match = False
            if search_query:
                if search_query.lower() in text.lower():
                    match = True
                for kw in keywords:
                    if search_query.lower() in kw.lower():
                        match = True
            else:
                match = True

            if not match:
                continue

            st.write(f"[{start:.2f} – {end:.2f}]")
            st.write(text)

            if keywords:
                st.write("Keywords:", ", ".join(keywords))

            st.write("")

    elif "transcription" in data:
        transcript_text = load_transcript_text(
            data["transcription"]["transcript_file"]
        )
        if search_query:
            if search_query.lower() in transcript_text.lower():
                st.write(transcript_text)
        else:
            st.write(transcript_text)
