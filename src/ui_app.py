import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px
from preprocessing import process_audio
from transcription import Transcriber
from segmentation import TopicSegmenter
from summarization import Summarizer
from keyword_extraction import KeywordExtractor

# Page Config
st.set_page_config(page_title="Podcast Intelligence", layout="wide")

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_RAW_DIR = os.path.join(BASE_DIR, 'audio_raw')
AUDIO_PROCESSED_DIR = os.path.join(BASE_DIR, 'audio_processed')
TRANSCRIPT_DIR = os.path.join(BASE_DIR, 'transcripts')
SEGMENTS_DIR = os.path.join(BASE_DIR, 'segments')

# Ensure dirs exist
for d in [AUDIO_RAW_DIR, AUDIO_PROCESSED_DIR, TRANSCRIPT_DIR, SEGMENTS_DIR]:
    os.makedirs(d, exist_ok=True)

# Cache models
@st.cache_resource
def load_models():
    transcriber = Transcriber(model_size="base")
    segmenter = TopicSegmenter()
    summarizer = Summarizer()
    kw_extractor = KeywordExtractor()
    return transcriber, segmenter, summarizer, kw_extractor

transcriber, segmenter, summarizer, kw_extractor = load_models()

st.title("🎙️ Automated Podcast Transcription & Topic Segmentation")

# Sidebar
st.sidebar.header("Upload or Select")
uploaded_file = st.sidebar.file_uploader("Upload Audio", type=["mp3", "wav", "m4a"])
files = [f for f in os.listdir(AUDIO_RAW_DIR) if not f.startswith('.')]
selected_file = st.sidebar.selectbox("Or select from processed", [""] + files)

if uploaded_file:
    # Save uploaded file
    file_path = os.path.join(AUDIO_RAW_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    selected_file = uploaded_file.name

if selected_file:
    file_path = os.path.join(AUDIO_RAW_DIR, selected_file)
    st.sidebar.success(f"Selected: {selected_file}")
    
    # Process Button
    if st.sidebar.button("Process Audio"):
        with st.spinner("Processing audio..."):
            processed_path = process_audio(file_path, AUDIO_PROCESSED_DIR)
        
        with st.spinner("Transcribing... (this may take a while)"):
            result = transcriber.transcribe(processed_path)
            # Save raw transcript
            t_path = os.path.join(TRANSCRIPT_DIR, f"{selected_file}.json")
            transcriber.save_transcript(result, t_path)
            
        with st.spinner("Segmenting & Summarizing..."):
            segments = segmenter.segment_transcript(result['segments'])
            
            # Enrich segments with summary and keywords
            for seg in segments:
                seg['summary'] = summarizer.summarize(seg['text'])
                seg['keywords'] = kw_extractor.extract(seg['text'])
            
            # Save enriched segments
            s_path = os.path.join(SEGMENTS_DIR, f"{selected_file}_segments.json")
            with open(s_path, 'w') as f:
                json.dump(segments, f, indent=2)
                
        st.success("Processing Complete!")

    # Display Results
    t_path = os.path.join(TRANSCRIPT_DIR, f"{selected_file}.json")
    s_path = os.path.join(SEGMENTS_DIR, f"{selected_file}_segments.json")
    
    if os.path.exists(s_path):
        with open(s_path, 'r') as f:
            segments = json.load(f)
            
        # Visualization
        st.subheader("Topic Timeline")
        df = pd.DataFrame(segments)
        df['duration'] = df['end'] - df['start']
        fig = px.bar(df, x='duration', y='id', orientation='h', text='keywords', hover_data=['summary'], title="Episode Structure")
        st.plotly_chart(fig, use_container_width=True)
        
        # Navigation
        st.subheader("Navigate Topics")
        for seg in segments:
            with st.expander(f"Topic {seg['id']}: {seg['keywords'][:3]}"):
                st.write(f"**Summary:** {seg['summary']}")
                st.write(f"**Time:** {seg['start']:.2f}s - {seg['end']:.2f}s")
                st.audio(file_path, start_time=int(seg['start']))
                st.text(seg['text'])
                
    elif os.path.exists(t_path):
        st.warning("Transcript exists but no segments found. Re-run processing.")
        with open(t_path, 'r') as f:
            data = json.load(f)
        st.text_area("Full Transcript", data['text'], height=300)

else:
    st.info("Upload an audio file to get started.")
