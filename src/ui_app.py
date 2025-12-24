import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px
import time

# Import Pipeline Agents
from preprocessing import process_audio
from transcription import Transcriber
from segmentation import TopicSegmenter
from summarization import Summarizer
from keyword_extraction import KeywordExtractor
from preprocessing import process_audio
from transcription import Transcriber
from segmentation import TopicSegmenter
from summarization import Summarizer
from keyword_extraction import KeywordExtractor
from indexing import TopicIndexer
from pydub import AudioSegment
import io
import logging
from logger import SessionLogger

# Page Config
st.set_page_config(page_title="Podcast Intelligence", layout="wide", page_icon="🎙️")

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_RAW_DIR = os.path.join(BASE_DIR, 'audio_raw')
AUDIO_PROCESSED_DIR = os.path.join(BASE_DIR, 'audio_processed')
TRANSCRIPT_DIR = os.path.join(BASE_DIR, 'transcripts')
SEGMENTS_DIR = os.path.join(BASE_DIR, 'segments')

# Ensure dirs exist
for d in [AUDIO_RAW_DIR, AUDIO_PROCESSED_DIR, TRANSCRIPT_DIR, SEGMENTS_DIR]:
    os.makedirs(d, exist_ok=True)

# Cache Models (Lazy Loading Logic managed by Agents, but objects shared here)
@st.cache_resource
def load_agents():
    st.write("Initializing AI Agents... (This runs once)")
    
    # Transcription Agent
    transcriber = Transcriber(model_size="base", compute_type="int8")
    
    # Topic Segmentation Agent
    segmenter = TopicSegmenter()
    
    # Summarization Agent
    summarizer = Summarizer()
    
    # Keyword Extraction Agent
    kw_extractor = KeywordExtractor(method='yake')
    
    # Indexing & Navigation Agent
    indexer = TopicIndexer()
    
    return transcriber, segmenter, summarizer, kw_extractor, indexer

@st.cache_resource
def load_audio_file(file_path):
    """
    Loads audio file into memory for fast slicing.
    """
    return AudioSegment.from_file(file_path)

try:
    transcriber, segmenter, summarizer, kw_extractor, indexer = load_agents()
except Exception as e:
    st.error(f"Failed to load AI Agents: {e}")
    st.stop()

st.title("🎙️ Automated Podcast Transcription & Intelligence")

# Sidebar: File Management
st.sidebar.header("Source Selection")
uploaded_file = st.sidebar.file_uploader("Upload Audio", type=["mp3", "wav", "m4a"])

# Refresh list logic helps if files change
files = [f for f in os.listdir(AUDIO_RAW_DIR) if not f.startswith('.')]
selected_file = st.sidebar.selectbox("Select Existing Audio", [""] + files)

current_file = None
if uploaded_file:
    # Save uploaded file
    file_path = os.path.join(AUDIO_RAW_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    current_file = uploaded_file.name
    st.sidebar.success(f"Uploaded: {current_file}")
elif selected_file:
    current_file = selected_file

if current_file:
    # Set paths
    raw_path = os.path.join(AUDIO_RAW_DIR, current_file)
    base_name = os.path.splitext(current_file)[0]
    
    # Check for existing outputs
    t_path = os.path.join(TRANSCRIPT_DIR, f"{base_name}.txt")
    s_path = os.path.join(SEGMENTS_DIR, f"{base_name}.json")
    
    st.sidebar.markdown("---")
    
    # Process Button
    if st.sidebar.button("🚀 Process Audio"):
        st.write("### ⚙️ Processing Pipeline")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Initialize Logging Session
        session_id, log_path = SessionLogger.start_new_session()
        logger = SessionLogger.get_logger(__name__)
        logger.info(f"Processing started for file: {current_file} | Session ID: {session_id}")
        st.info(f"Session Log: `{log_path}`")

        try:
            # 1. Preprocessing
            logger.info("Starting Audio Preprocessing...")
            status_text.text("Step 1/5: Audio Preprocessing...")
            processed_path = process_audio(raw_path, AUDIO_PROCESSED_DIR)
            logger.info(f"Audio Preprocessing complete. Processed file: {processed_path}")
            progress_bar.progress(20)
            
            # 2. Transcription
            logger.info("Starting Transcription...")
            status_text.text("Step 2/5: Speech Transcription (Faster-Whisper)...")
            # Note: process_file saves intermediate files
            result = transcriber.process_file(processed_path, TRANSCRIPT_DIR, SEGMENTS_DIR)
            logger.info(f"Transcription complete. Language: {result.get('language')}")
            progress_bar.progress(40)
            
            # 3. Topic Segmentation
            logger.info("Starting Topic Segmentation...")
            status_text.text("Step 3/5: Semantic Topic Segmentation...")
            # We need standard segment list for this
            whisper_segments = result['segments']
            topics = segmenter.segment_transcript(whisper_segments)
            logger.info(f"Segmentation complete. Found {len(topics)} topics.")
            progress_bar.progress(60)
            
            # 4. Summarization (Enrich Topics)
            status_text.text("Step 4/5: Adaptive Summarization...")
            logger.info("Starting Summarization...")
            topics = summarizer.summarize_topics(topics)
            logger.info("Summarization complete.")
            progress_bar.progress(80)
            
            # 5. Keyword Extraction (Enrich Topics)
            status_text.text("Step 5/5: Medical Keyword Extraction...")
            logger.info("Starting Keyword Extraction...")
            topics = kw_extractor.extract_topics(topics)
            
            # Save Final Enriched Segments
            with open(s_path, 'w', encoding='utf-8') as f:
                json.dump({"language": result.get('language'), "topics": topics}, f, indent=2, ensure_ascii=False)
                
            progress_bar.progress(100)
            status_text.text("Processing Complete!")
            logger.info("Pipeline processing completed successfully.")
            st.success("Analysis Complete!")
            time.sleep(1)
            st.rerun()
            
        except Exception as e:
            logger.error(f"Processing Failed: {e}", exc_info=True)
            st.error(f"Processing Failed: {e}")
            st.stop()

    # Display Results
    if os.path.exists(s_path):
        with open(s_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            topics = data.get('topics', [])

        if not topics:
            st.warning("No topics found in segmentation.")
        else:
            # Pre-load audio for slicing
            if os.path.exists(raw_path):
                 full_audio = load_audio_file(raw_path)
            else:
                 full_audio = None

            # Index Topics (Idempotent / Session State check)
            if 'indexed_file' not in st.session_state or st.session_state.indexed_file != current_file:
                with st.spinner("Indexing topics for search..."):
                    indexer.index_topics(topics)
                    st.session_state.indexed_file = current_file
            
            # --- Sidebar Search UI ---
            st.sidebar.markdown("---")
            st.sidebar.header("🔍 Semantic Search")
            search_query = st.sidebar.text_input("Search topics...", placeholder="e.g., 'neural networks'")
            
            if search_query:
                results = indexer.search(search_query, top_n=3)
                st.sidebar.write("Results:")
                for res in results:
                    score_fmt = f"{res['score']:.2f}"
                    # Allow jumping to topic
                    if st.sidebar.button(f"▶ {res['title']} ({score_fmt})", key=f"btn_{res['id']}"):
                         # We use query params or just a message for now as Streamlit audio can't easily be controlled 
                         # dynamically without rerun or session state tricks.
                         # But we can display the timestamp to drag manually or try to render an audio player at that time.
                         st.session_state.seek_time = int(res['start'])
                         st.rerun()

            # Handle Seek (if clicked)
            start_offset = st.session_state.get('seek_time', 0)
            if start_offset > 0:
                 st.sidebar.info(f"Jumped to: {time.strftime('%M:%S', time.gmtime(start_offset))}")
            
            # Stats
            total_duration = topics[-1]['end'] - topics[0]['start']
            avg_duration = total_duration / len(topics)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Topics", len(topics))
            col1.metric("Language", data.get('language', 'Unknown'))
            col2.metric("Total Duration", f"{total_duration/60:.1f} min")
            col3.metric("Avg Topic Length", f"{avg_duration:.1f} sec")
            
            # Timeline Visualization
            st.subheader("📊 Episode Timeline")
            df = pd.DataFrame(topics)
            df['duration'] = df['end'] - df['start']
            # Creating a label for the chart
            df['label'] = df.apply(lambda x: x.get('title', f"Topic {x['id']}"), axis=1)
            
            fig = px.bar(df, x='duration', y='id', orientation='h', 
                         hover_data=['title', 'tldr'], 
                         title="Topic Structure & Duration",
                         labels={'id': 'Topic Sequence', 'duration': 'Duration (s)'})
            st.plotly_chart(fig, use_container_width=True)
            
            # --- Full Transcript View (New Request) ---
            st.subheader("📝 Complete Transcript")
            with st.expander("View Full Text", expanded=False):
                # Try to load raw text from t_path first for fidelity, else join topics
                if os.path.exists(t_path):
                     with open(t_path, 'r', encoding='utf-8') as f:
                        full_text = f.read()
                else:
                    full_text = "\n\n".join([t.get('text', '') for t in topics])
                
                st.markdown(f"<div style='height: 300px; overflow-y: scroll; padding: 10px; background-color: #f0f2f6; border-radius: 5px; color: #31333F;'>{full_text.replace(chr(10), '<br><br>')}</div>", unsafe_allow_html=True)
            
            # Detailed Topic View
            st.subheader("📑 Topic Details")
            
            for topic in topics:
                start_fmt = time.strftime('%M:%S', time.gmtime(topic['start']))
                end_fmt = time.strftime('%M:%S', time.gmtime(topic['end']))
                title = topic.get('title', f"Topic {topic['id']}")
                
                with st.expander(f"**{start_fmt} - {end_fmt}** | {title}"):
                    # Tabs for different views
                    tab1, tab2, tab3 = st.tabs(["Highlights", "Transcript", "Audio"])
                    
                    with tab1:
                        st.markdown(f"**Summary:** {topic.get('summary', 'N/A')}")
                        st.markdown("**Key Takeaways:**")
                        for bullet in topic.get('bullets', []):
                            st.markdown(f"- {bullet}")
                        
                        st.markdown("**Keywords:**")
                        kw_html = " ".join([f"`{k}`" for k in topic.get('keywords', [])])
                        st.markdown(kw_html)
                        
                    with tab2:
                        st.text_area("Full Text", topic.get('text', ''), height=150)
                        
                    with tab3:
                        # Slice Audio for this Topic
                        if full_audio:
                            start_ms = int(topic['start'] * 1000)
                            end_ms = int(topic['end'] * 1000)
                            # Safety check
                            if start_ms < 0: start_ms = 0
                            if end_ms > len(full_audio): end_ms = len(full_audio)
                            
                            if start_ms < end_ms:
                                topic_audio = full_audio[start_ms:end_ms]
                                # Export to buffer
                                buf = io.BytesIO()
                                topic_audio.export(buf, format="mp3")
                                st.audio(buf, format="audio/mp3")
                            else:
                                st.warning("Invalid timestamp range.")
                        else:
                            st.error("Audio file not found.")

    elif os.path.exists(t_path):
        st.info("Transcript found, but no topic analysis. Re-run processing to generate topics.")
        with open(t_path, 'r', encoding='utf-8') as f:
             st.text_area("Raw Transcript", f.read(), height=300)
             
else:
    st.info("Please upload or select an audio file to begin.")
