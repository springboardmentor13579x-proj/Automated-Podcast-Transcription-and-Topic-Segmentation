import streamlit as st
import pandas as pd
import os
import sys
import time
import base64
from dotenv import load_dotenv

# ==========================================
# 0. SETUP & IMPORTS
# ==========================================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from src.preprocessing import preprocess_audio 
    from src.transcription import load_whisper_model, transcribe_audio
    from src.segmentation import load_segmenter, segment_text, create_word_timeline
    from src.summarization import load_summarizer, generate_summary
    from src.keyword_extraction import extract_keywords
except ImportError as e:
    st.error(f"❌ Import Error: {e}. Please run this app from the main project folder.")
    st.stop()

load_dotenv()
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_FILE = os.getenv("OUTPUT_FILE", os.path.join(BASE_DIR, "data", "final_search_index_fixed.csv"))
AUDIO_FOLDER = os.getenv("CLEAN_AUDIO_DIR", os.path.join(BASE_DIR, "audio_processed"))
RAW_UPLOAD_FOLDER = os.getenv("RAW_AUDIO_DIR", os.path.join(BASE_DIR, "audio_raw"))

for folder in [AUDIO_FOLDER, RAW_UPLOAD_FOLDER, os.path.dirname(DATA_FILE)]:
    os.makedirs(folder, exist_ok=True)

st.set_page_config(page_title="Lecture Navigator", page_icon="🎓", layout="wide")

# ==========================================
# 1. UI STYLING
# ==========================================
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: linear-gradient(to right bottom, #ffffff, #f0f2f6);
         }}
         .stContainer {{
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 15px;
         }}
         .highlight {{
            background-color: #e3f2fd;
            padding: 2px 6px;
            border-radius: 4px;
            color: #1565c0;
            font-weight: 600;
            font-size: 0.9em;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()

# ==========================================
# 2. SESSION STATE
# ==========================================
if 'active_df' not in st.session_state: st.session_state['active_df'] = None
if 'active_audio_path' not in st.session_state: st.session_state['active_audio_path'] = None
if 'start_time_sec' not in st.session_state: st.session_state['start_time_sec'] = 0

# ==========================================
# 3. AI PIPELINE
# ==========================================
@st.cache_resource
def load_all_models():
    with st.spinner("🧠 Waking up the AI Models..."):
        return load_whisper_model("base"), load_segmenter(), load_summarizer()

def run_streaming_pipeline(uploaded_file, models):
    whisper_model, segmenter, summarizer = models
    
    # --- PHASE 1: PREPROCESSING ---
    st.info("🎙️ **Step 1/3:** Cleaning Audio Signal...")
    
    raw_path = os.path.join(RAW_UPLOAD_FOLDER, uploaded_file.name)
    with open(raw_path, "wb") as f: f.write(uploaded_file.getbuffer())
    
    clean_name = f"cleaned_{os.path.splitext(uploaded_file.name)[0]}.wav"
    clean_path = os.path.join(AUDIO_FOLDER, clean_name)
    
    if not preprocess_audio(raw_path, clean_path):
        clean_path = raw_path 
    
    st.success("✅ Audio Cleaned!")
    st.audio(clean_path, format="audio/wav")
    
    # --- PHASE 2: TRANSCRIPTION ---
    st.info("✍️ **Step 2/3:** Transcribing Speech to Text...")
    
    full_text, segments_json = transcribe_audio(whisper_model, clean_path)
    if not full_text: 
        st.error("Transcription Failed.")
        return None, None
        
    st.success("✅ Transcription Complete!")
    # Show text immediately during loading
    with st.expander("📄 Read Full Transcript", expanded=True):
        st.write(full_text)
    
    # --- PHASE 3: INTELLIGENCE ---
    st.info("🧠 **Step 3/3:** Segmenting Topics & Summarizing...")
    
    timeline = create_word_timeline(segments_json)
    segments = segment_text(segmenter, full_text)
    
    new_rows = []
    current_idx = 0
    talk_id = int(time.time())
    
    live_status = st.empty()

    for i, seg_text in enumerate(segments):
        clean_text = seg_text.replace("\n", " ").strip()
        words = clean_text.split()
        if not words: continue
        
        start_i = current_idx
        end_i = min(current_idx + len(words) - 1, len(timeline) - 1)
        real_start = timeline[start_i]['start'] if start_i < len(timeline) else 0
        real_end = timeline[end_i]['end'] if end_i < len(timeline) else 0
        
        summ = generate_summary(summarizer, clean_text)
        keys = extract_keywords(clean_text)
        
        live_status.caption(f"⚡ Analyzed Segment {i+1}: {summ[:50]}...")
        
        new_rows.append({
            "talk_id": talk_id,
            "filename": os.path.basename(clean_path),
            "topic_id": i+1,
            "start_time": f"{int(real_start//60):02d}:{int(real_start%60):02d}",
            "start_seconds": int(real_start),
            "summary": summ,
            "keywords": keys,
            "full_text": clean_text
        })
        current_idx += len(words)

    live_status.empty()
    st.success("✅ All Topics Extracted!")
    
    df = pd.DataFrame(new_rows)
    df.to_csv(DATA_FILE, mode='a', header=not os.path.exists(DATA_FILE), index=False)
    
    return df, clean_path

# ==========================================
# 4. RENDER RESULTS (THE FINAL VIEW)
# ==========================================
def render_results(df, audio_path):
    st.divider()
    
    # 1. Main Player
    st.markdown("### 🎧 Interactive Player")
    if os.path.exists(audio_path):
        st.audio(audio_path, format="audio/wav", start_time=st.session_state['start_time_sec'])

    # ==========================================
    # 👇 NEW: FULL TRANSCRIPT BUTTON (PERMANENT)
    # ==========================================
    with st.expander("📄 View Full Transcript (Read All)"):
        # We join all the segment texts together to recreate the full script
        full_transcript = " ".join(df['full_text'].tolist())
        st.write(full_transcript)
    # ==========================================

    # 2. Search
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("🔍 Filter Topics...", placeholder="Search keywords...")

    if 'keywords' not in df.columns: df['keywords'] = ""
    df['keywords'] = df['keywords'].fillna("").astype(str)
    
    if query:
        filtered = df[
            df['summary'].str.contains(query, case=False) | 
            df['keywords'].str.contains(query, case=False)
        ]
    else:
        filtered = df

    # 3. Cards
    for idx, row in filtered.iterrows():
        with st.container():
            c1, c2 = st.columns([1, 6])
            with c1:
                st.markdown(f"**⏱ {row['start_time']}**")
                if st.button("▶ Play", key=f"play_{idx}"):
                    st.session_state['start_time_sec'] = int(row['start_seconds'])
                    st.rerun()
            with c2:
                st.markdown(f"**{row['summary']}**")
                st.markdown(f"<span class='highlight'>{row['keywords']}</span>", unsafe_allow_html=True)
                with st.expander("Read Text"):
                    st.write(row['full_text'])

# ==========================================
# 5. MAIN APP
# ==========================================
def main():
    st.title("🎓 Smart Lecture Navigator")
    
    # SIDEBAR
    with st.sidebar:
        st.header("📂 Library")
        if os.path.exists(DATA_FILE):
            history_df = pd.read_csv(DATA_FILE)
            files = history_df['filename'].unique()
            selected = st.selectbox("Select Lecture:", ["-- Current --"] + list(files))
            
            if selected != "-- Current --":
                path = os.path.join(AUDIO_FOLDER, selected)
                if st.session_state['active_audio_path'] != path:
                    st.session_state['active_df'] = history_df[history_df['filename'] == selected]
                    st.session_state['active_audio_path'] = path
                    st.session_state['start_time_sec'] = 0
                    st.rerun()

    # UPLOAD SECTION
    if st.session_state['active_df'] is None:
        st.markdown("### 📤 Upload New Lecture")
        uploaded_file = st.file_uploader("", type=["mp3", "wav"])
        
        if uploaded_file:
            if st.button("🚀 Analyze Now"):
                models = load_all_models()
                df, path = run_streaming_pipeline(uploaded_file, models)
                
                if df is not None:
                    st.session_state['active_df'] = df
                    st.session_state['active_audio_path'] = path
                    st.session_state['start_time_sec'] = 0
                    st.rerun() 

    # RESULTS SECTION
    if st.session_state['active_df'] is not None:
        render_results(st.session_state['active_df'], st.session_state['active_audio_path'])
        
        if st.button("🔄 Upload Another File"):
            st.session_state['active_df'] = None
            st.rerun()

if __name__ == "__main__":
    main()