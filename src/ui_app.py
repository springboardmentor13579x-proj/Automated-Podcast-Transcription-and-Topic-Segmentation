import streamlit as st
import json
import subprocess
from pathlib import Path
from textblob import TextBlob
from collections import Counter
import plotly.express as px
from wordcloud import WordCloud

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
META_FILE = BASE_DIR / "docs" / "processing_metadata.json"
AUDIO_RAW_DIR = BASE_DIR / "audio_raw"

st.set_page_config(layout="wide")
st.title("Podcast Transcript Navigator")

def load_metadata():
    if META_FILE.exists():
        return json.loads(META_FILE.read_text())
    return {}

def save_metadata(meta):
    META_FILE.write_text(json.dumps(meta, indent=4))

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

    if audio_path.exists():
        st.warning("File already exists")
    else:
        audio_path.write_bytes(uploaded.read())
        metadata[uploaded.name] = {
            "preprocessing": {"status": "pending"},
            "transcription": {"status": "pending"},
            "segmentation": {"status": "pending"},
            "keywords": {"status": "pending"}
        }
        save_metadata(metadata)
        st.success("Audio uploaded and registered")

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

def run_pipeline():
    subprocess.run(["python", "preprocessing.py"], cwd=SRC_DIR)
    subprocess.run(["python", "transcription.py"], cwd=SRC_DIR)
    subprocess.run(["python", "segmentation.py"], cwd=SRC_DIR)
    subprocess.run(["python", "keyword_extraction.py"], cwd=SRC_DIR)

if data.get("segmentation", {}).get("status") != "done":
    if st.button("Run Processing Pipeline"):
        run_pipeline()
        st.rerun()
    st.info("This audio is uploaded but not processed yet")
    st.stop()

segments = load_json(data["segmentation"]["segment_file"])
if not segments:
    st.warning("No segments available")
    st.stop()

for s in segments:
    s.setdefault("sentiment", compute_sentiment(s.get("text", "")))

st.subheader("Sentiment Timeline")

timeline_df = {
    "Start (sec)": [s["start"] for s in segments],
    "Sentiment": [s["sentiment"] for s in segments],
    "Preview": [s["text"][:120] for s in segments]
}

timeline_fig = px.scatter(
    timeline_df,
    x="Start (sec)",
    y="Sentiment",
    hover_data=["Preview"],
    height=350
)

st.plotly_chart(timeline_fig, width="stretch")

st.divider()

st.subheader("Keyword Cloud")

all_keywords = []
for s in segments:
    all_keywords.extend(s.get("keywords", []))

if all_keywords:
    wc = WordCloud(width=900, height=300, background_color="white")
    wc.generate_from_frequencies(Counter(all_keywords))
    st.image(wc.to_image(), use_container_width=True)

st.divider()

st.subheader("Search Transcript")

c1, c2 = st.columns([2, 3])
with c1:
    selected_keyword = st.selectbox("Select keyword", ["None"] + sorted(set(all_keywords)))
with c2:
    typed_keyword = st.text_input("Type keyword or text")

st.divider()

filtered = []

for seg in segments:
    text = seg["text"]
    keywords = seg.get("keywords", [])

    if typed_keyword:
        if typed_keyword.lower() in text.lower() or any(
            typed_keyword.lower() in k.lower() for k in keywords
        ):
            filtered.append(seg)
    elif selected_keyword != "None":
        if selected_keyword in keywords:
            filtered.append(seg)

st.subheader("Transcript Results")

if not filtered:
    st.info("Select or type a keyword to view transcript")
else:
    for idx, seg in enumerate(filtered, start=1):
        c1, c2 = st.columns([1, 6])

        with c1:
            st.markdown(f"{seg['start']:.2f}s")
            if st.button("Play", key=f"play_{idx}"):
                st.session_state.start_time = int(seg["start"])
                st.rerun()

        with c2:
            st.markdown(seg["text"])
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
