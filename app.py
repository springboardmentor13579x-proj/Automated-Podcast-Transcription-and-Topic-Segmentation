import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
import re
from pathlib import Path
import podcast_backend

# Configuration
BASE_DIR = r"D:\farrakh important\internship_project infosys\podcast_data"
TRANSCRIPT_DIR = os.path.join(BASE_DIR, "transcripts")
SUMMARY_DIR = os.path.join(BASE_DIR, "short_summary")
TOPIC_DIR = os.path.join(BASE_DIR, "semantic_segments")
KEYWORD_DIR = os.path.join(BASE_DIR, "keywords")
SENTIMENT_DIR = os.path.join(BASE_DIR, "sentiment_data")

# Page Config
st.set_page_config(page_title="AI Podcast Insights", layout="wide")

# Custom CSS for UI
st.markdown("""
<style>
    .big-font { font-size:24px !important; font-weight: bold; color: #4F8BF9; }
    .card { background-color: #f9f9f9; padding: 20px; border-radius: 10px; border-left: 5px solid #4F8BF9; margin-bottom: 20px; }
    .highlight { background-color: #FFFF00; color: black; padding: 2px 5px; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

st.title("AI Podcast Insights Dashboard")
st.markdown("Automated analysis of audio content: Transcription, Topic Segmentation, and Sentiment.")

# Sidebar: File Upload and Search
with st.sidebar:
    st.header("Add New Content")
    uploaded_file = st.file_uploader("Upload Audio", type=["mp3", "wav", "m4a"])
    
    if uploaded_file is not None:
        if st.button("Process File", type="primary"):
            status_box = st.empty()
            status_box.info("AI is processing...")
            try:
                status = podcast_backend.process_new_upload(uploaded_file, BASE_DIR)
                if status == "Success":
                    status_box.success("Complete! Reloading...")
                    st.rerun()
                else:
                    status_box.error(f"Error: {status}")
            except Exception as e:
                status_box.error(f"Critical Error: {str(e)}")
    
    st.divider()
    st.header("Search Analysis")
    search_query = st.text_input("Filter by Keyword:", placeholder="e.g. music, nature")

# Helper Functions
def get_files_with_keywords(query):
    if not os.path.exists(TRANSCRIPT_DIR): return []
    raw_files = [f.replace(".json", "") for f in os.listdir(TRANSCRIPT_DIR) if f.endswith(".json")]
    
    if not query: return raw_files
    
    filtered = []
    query = query.lower()
    for fname in raw_files:
        kw_path = os.path.join(KEYWORD_DIR, f"{fname}_keywords.txt")
        tr_path = os.path.join(TRANSCRIPT_DIR, f"{fname}.json")
        
        found = False
        if os.path.exists(kw_path):
            with open(kw_path, "r", encoding="utf-8") as f:
                if query in f.read().lower(): found = True
        
        if not found and os.path.exists(tr_path):
            with open(tr_path, "r", encoding="utf-8") as f:
                if query in json.load(f)["text"].lower(): found = True
        
        if found: filtered.append(fname)
    return filtered

def load_file(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f: return f.read()
    return None

def load_json_file(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f: return json.load(f)
    return None

# File selection
files = get_files_with_keywords(search_query)
if not files:
    st.warning("No files found.")
    st.stop()

selected_file = st.sidebar.selectbox("Select Episode:", files)

# Summary and Keywords Display
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="big-font">Smart Summary</div>', unsafe_allow_html=True)
    summary = load_file(os.path.join(SUMMARY_DIR, f"{selected_file}_summary.txt"))
    if summary:
        st.info(summary)
    else:
        st.warning("Summary not available.")

with col2:
    st.markdown('<div class="big-font">Key Topics</div>', unsafe_allow_html=True)
    keywords = load_file(os.path.join(KEYWORD_DIR, f"{selected_file}_keywords.txt"))
    if keywords:
        clean_keys = [k for k in keywords.splitlines() if not k.startswith("===")]
        st.write(clean_keys)
    else:
        st.caption("No keywords extracted.")

st.divider()

# Sentiment Analysis Visualization
st.markdown('<div class="big-font">Emotional Journey</div>', unsafe_allow_html=True)
sent_data = load_json_file(os.path.join(SENTIMENT_DIR, f"{selected_file}_sentiment.json"))

if sent_data:
    df = pd.DataFrame(sent_data)
    df["Smoothed Trend"] = df["score"].rolling(window=10, min_periods=1).mean()
    
    fig = px.bar(df, x="start", y="score", color="label",
                title="Sentiment Analysis",
                labels={"start": "Time (seconds)", "score": "Score"},
                color_discrete_map={'Positive': '#28a745', 'Negative': '#dc3545', 'Neutral': '#cccccc'},
                opacity=0.3)

    fig.add_scatter(x=df["start"], y=df["Smoothed Trend"], mode='lines', name='Trend', 
                    line=dict(color='#ff7f0e', width=3))

    fig.update_layout(yaxis_range=[-1, 1], showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No sentiment data.")

st.divider()

# Topics and Transcript Display
col_topic, col_trans = st.columns([1, 2])

with col_topic:
    st.markdown('<div class="big-font">Topic Segments</div>', unsafe_allow_html=True)
    topics = load_file(os.path.join(TOPIC_DIR, f"{selected_file}_topics.txt"))
    if topics:
        st.text_area("Detected Topics", topics, height=400)
    else:
        st.caption("No segmentation available.")

with col_trans:
    st.markdown('<div class="big-font">Full Transcript</div>', unsafe_allow_html=True)
    transcript_data = load_json_file(os.path.join(TRANSCRIPT_DIR, f"{selected_file}.json"))
    
    if transcript_data:
        full_text = transcript_data["text"]
        if search_query:
            pattern = re.compile(re.escape(search_query), re.IGNORECASE)
            highlighted_text = pattern.sub(lambda m: f":red[**{m.group(0)}**]", full_text)
            count = len(re.findall(pattern, full_text))
            st.caption(f"Found {count} occurrences of '{search_query}'")
            st.markdown(highlighted_text)
        else:
            st.write(full_text)
    else:
        st.warning("Transcript not found.")