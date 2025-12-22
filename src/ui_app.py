import streamlit as st
import json
from pathlib import Path
from collections import Counter
from textblob import TextBlob
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
META_FILE = PROJECT_ROOT / "docs" / "processing_metadata.json"

st.set_page_config(layout="wide")
st.title("Legal AI Argument Transcription")

def load_metadata():
    if META_FILE.exists():
        return json.loads(META_FILE.read_text())
    return {}

def load_segments(path):
    p = Path(path)
    if p.exists():
        return json.loads(p.read_text())
    return []

def compute_sentiment(text):
    return round(TextBlob(text).sentiment.polarity, 3)

metadata = load_metadata()

if not metadata:
    st.write("No processed audio available")
    st.stop()

file_key = st.selectbox("Select audio file", sorted(metadata.keys()))
data = metadata[file_key]

st.subheader(file_key)

if "segmentation" not in data:
    st.write("Segmentation data not available")
    st.stop()

segments = load_segments(data["segmentation"]["segment_file"])

if not segments:
    st.write("No segments found")
    st.stop()

for seg in segments:
    if "sentiment" not in seg:
        seg["sentiment"] = compute_sentiment(seg.get("text", ""))

timeline_df = {
    "Start Time (sec)": [seg["start"] for seg in segments],
    "Sentiment": [seg["sentiment"] for seg in segments],
    "Preview": [seg["text"][:120] for seg in segments],
}

timeline_fig = px.scatter(
    timeline_df,
    x="Start Time (sec)",
    y="Sentiment",
    hover_data=["Preview"],
    title="Sentiment Timeline"
)

st.plotly_chart(timeline_fig, use_container_width=True)

all_keywords = []
for seg in segments:
    all_keywords.extend(seg.get("keywords", []))

if all_keywords:
    freq = Counter(all_keywords)
    wc = WordCloud(width=900, height=300, background_color="white")
    wc.generate_from_frequencies(freq)

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.imshow(wc)
    ax.axis("off")
    st.subheader("Keyword Cloud")
    st.pyplot(fig)

st.subheader("Segment Details")

search_query = st.text_input("Search text or keywords")

for seg in segments:
    text = seg.get("text", "")
    keywords = seg.get("keywords", [])
    sentiment = seg.get("sentiment", 0.0)

    if search_query:
        if search_query.lower() not in text.lower() and not any(
            search_query.lower() in kw.lower() for kw in keywords
        ):
            continue

    st.write(f"[{seg['start']:.2f} – {seg['end']:.2f}]")
    st.write(text)
    st.write("Sentiment:", sentiment)

    if keywords:
        st.write("Keywords:", ", ".join(keywords))

    st.write("")
