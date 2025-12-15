import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
import re
from pathlib import Path
import podcast_backend

# --- CONFIGURATION ---
BASE_DIR = r"D:\farrakh important\internship_project infosys\podcast_data"
TRANSCRIPT_DIR = os.path.join(BASE_DIR, "transcripts")
SUMMARY_DIR = os.path.join(BASE_DIR, "short_summary")
TOPIC_DIR = os.path.join(BASE_DIR, "semantic_segments")
KEYWORD_DIR = os.path.join(BASE_DIR, "keywords")
SENTIMENT_DIR = os.path.join(BASE_DIR, "sentiment_data")

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Podcast Insights", layout="wide", page_icon="🎙️")

# --- CUSTOM CSS FOR STYLING ---
st.markdown("""
<style>
    .big-font { font-size:24px !important; font-weight: bold; color: #4F8BF9; }
    .card { background-color: #f9f9f9; padding: 20px; border-radius: 10px; border-left: 5px solid #4F8BF9; margin-bottom: 20px; }
    .highlight { background-color: #FFFF00; color: black; padding: 2px 5px; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

st.title("🎙️ AI Podcast Insights Dashboard")
st.markdown("Automated analysis of audio content: Transcription, Topic Segmentation, and Emotional Intelligence.")

# --- SIDEBAR: UPLOAD ---
with st.sidebar:
    st.header("📂 Add New Content")
    uploaded_file = st.file_uploader("Upload Audio", type=["mp3", "wav", "m4a"])
    
    if uploaded_file is not None:
        if st.button("🚀 Process File", type="primary"):
            status_box = st.empty()
            status_box.info("⏳ AI is processing... (Transcription + NLP + Sentiment)")
            try:
                status = podcast_backend.process_new_upload(uploaded_file, BASE_DIR)
                if status == "Success":
                    status_box.success("✅ Complete! Reloading...")
                    st.rerun()
                else:
                    status_box.error(f"Error: {status}")
            except Exception as e:
                status_box.error(f"Critical Error: {str(e)}")
    
    st.divider()
    st.header("🔍 Search Analysis")
    search_query = st.text_input("Filter by Keyword:", placeholder="e.g. loops, music, nature")

# --- HELPER FUNCTIONS ---
def get_files_with_keywords(query):
    if not os.path.exists(TRANSCRIPT_DIR): return []
    raw_files = [f.replace(".json", "") for f in os.listdir(TRANSCRIPT_DIR) if f.endswith(".json")]
    
    if not query: return raw_files
    
    filtered = []
    query = query.lower()
    for fname in raw_files:
        # Check keywords file
        kw_path = os.path.join(KEYWORD_DIR, f"{fname}_keywords.txt")
        # Check transcript file
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

# --- FILE SELECTION ---
files = get_files_with_keywords(search_query)
if not files:
    st.warning("No files found matching your search.")
    st.stop()

selected_file = st.sidebar.selectbox("Select Episode:", files)

# --- LAYOUT ---

# ROW 1: Summary & Keywords
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="big-font">📝 Smart Summary</div>', unsafe_allow_html=True)
    summary = load_file(os.path.join(SUMMARY_DIR, f"{selected_file}_summary.txt"))
    if summary:
        st.info(summary)
    else:
        st.warning("Summary not available.")

with col2:
    st.markdown('<div class="big-font">🔑 Key Topics</div>', unsafe_allow_html=True)
    keywords = load_file(os.path.join(KEYWORD_DIR, f"{selected_file}_keywords.txt"))
    if keywords:
        clean_keys = [k for k in keywords.splitlines() if not k.startswith("===")]
        st.write(clean_keys)
    else:
        st.caption("No keywords extracted.")

st.divider()

# ROW 2: Sentiment Graph (IMPROVED)
st.markdown('<div class="big-font">📈 Emotional Journey</div>', unsafe_allow_html=True)
st.caption("This graph shows how the mood changes throughout the audio. The trend line (orange) smooths out sudden spikes.")

sent_data = load_json_file(os.path.join(SENTIMENT_DIR, f"{selected_file}_sentiment.json"))

if sent_data:
    df = pd.DataFrame(sent_data)
    
    # Add a Rolling Average to smooth the graph
    df["Smoothed Trend"] = df["score"].rolling(window=10, min_periods=1).mean()
    
    # Color mapping for raw bars
    df['Color'] = df['label'].map({'Positive': '#28a745', 'Negative': '#dc3545', 'Neutral': '#6c757d'})

    fig = px.bar(df, x="start", y="score", color="label",
                 title="Raw Sentiment vs. Smoothed Trend",
                 labels={"start": "Time (seconds)", "score": "Sentiment Score (-1 to +1)"},
                 color_discrete_map={'Positive': '#28a745', 'Negative': '#dc3545', 'Neutral': '#cccccc'},
                 opacity=0.3) # Make bars faint so line stands out

    # Add the Trend Line on top
    fig.add_scatter(x=df["start"], y=df["Smoothed Trend"], mode='lines', name='Trend Line', 
                    line=dict(color='#ff7f0e', width=3))

    fig.update_layout(yaxis_range=[-1, 1], showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No sentiment data available.")

st.divider()

# ROW 3: Topics & Transcript
col_topic, col_trans = st.columns([1, 2])

with col_topic:
    st.markdown('<div class="big-font">📚 Topic Segments</div>', unsafe_allow_html=True)
    topics = load_file(os.path.join(TOPIC_DIR, f"{selected_file}_topics.txt"))
    if topics:
        st.text_area("Detected Topics", topics, height=400)
    else:
        st.caption("No segmentation available.")

with col_trans:
    st.markdown('<div class="big-font">📜 Full Transcript (Searchable)</div>', unsafe_allow_html=True)
    
    transcript_data = load_json_file(os.path.join(TRANSCRIPT_DIR, f"{selected_file}.json"))
    
    if transcript_data:
        full_text = transcript_data["text"]
        
        # KEYWORD HIGHLIGHTING LOGIC
        if search_query:
            # Case-insensitive replacement using regex
            pattern = re.compile(re.escape(search_query), re.IGNORECASE)
            # Use Streamlit's red syntax for highlighting: :red[text]
            highlighted_text = pattern.sub(lambda m: f":red[**{m.group(0)}**]", full_text)
            
            # Show search count
            count = len(re.findall(pattern, full_text))
            st.caption(f"Found {count} occurrences of '{search_query}'")
            st.markdown(highlighted_text)
        else:
            st.write(full_text)
    else:
        st.warning("Transcript not found.")