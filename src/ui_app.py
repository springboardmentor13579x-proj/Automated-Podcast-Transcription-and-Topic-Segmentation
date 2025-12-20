import streamlit as st
import os, json, tempfile, re
from sklearn.feature_extraction.text import TfidfVectorizer
from pydub import AudioSegment
import whisper
import nltk

# -----------------------------
# NLTK Offline Setup
# -----------------------------
nltk.data.path.append(r"C:\Users\USER\nltk_data")  # Make sure 'punkt' is here
from nltk.tokenize import sent_tokenize

# -----------------------------
# CONFIG PATHS
# -----------------------------
PROJECT_DIR = r"C:\Users\USER\OneDrive\Desktop\Project"
AUDIO_DIR = os.path.join(PROJECT_DIR, "audio_processed")  # processed audio folder
JSON_DIR = os.path.join(PROJECT_DIR, "segments_keywordExtract_summary")  # updated segment folder
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(JSON_DIR, exist_ok=True)

# -----------------------------
# HELPERS
# -----------------------------
def sec_to_mmss(sec):
    m, s = divmod(int(sec), 60)
    return f"{m:02d}:{s:02d}"

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\[.*?\]", "", text)
    return text.strip()

def segment_text(text, size=5):
    sentences = sent_tokenize(text)
    return [" ".join(sentences[i:i+size]) for i in range(0, len(sentences), size)]

def extract_keywords(text, k=5):
    try:
        v = TfidfVectorizer(stop_words="english")
        x = v.fit_transform([text])
        scores = x.toarray()[0]
        words = v.get_feature_names_out()
        return [words[i] for i in scores.argsort()[-k:][::-1]]
    except:
        return []

def summarize_text(text, n=2):
    sents = sent_tokenize(text)
    if len(sents) <= n:
        return text
    try:
        v = TfidfVectorizer(stop_words="english")
        x = v.fit_transform(sents)
        scores = x.sum(axis=1).A1
        idx = sorted(scores.argsort()[-n:])
        return " ".join(sents[i] for i in idx)
    except:
        return "Summary unavailable."

def process_transcript(text, duration=None):
    chunks = segment_text(text)
    sec = duration / len(chunks) if duration else 0
    segments = []
    for i, chunk in enumerate(chunks, 1):
        segments.append({
            "segment_id": i,
            "start_time": (i-1)*sec,
            "end_time": i*sec,
            "text": chunk,
            "keywords": extract_keywords(chunk),
            "summary": summarize_text(chunk)
        })
    return segments

def save_segments_json(segments, name):
    path = os.path.join(JSON_DIR, f"{name}_segments.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(segments, f, indent=2, ensure_ascii=False)

@st.cache_resource
def load_whisper():
    return whisper.load_model("base")

def transcribe_audio(path):
    return load_whisper().transcribe(path)["text"]

# -----------------------------
# STREAMLIT APP
# -----------------------------
def main():
    st.set_page_config("🎧 Transcript Navigator", layout="wide")
    st.title("🎧 Transcript Navigation with Search & Keywords")

    # Upload transcript or audio
    txt = st.file_uploader("Upload Transcript (.txt)", type="txt")
    audio_file = st.file_uploader("Upload Audio", type=["mp3","wav"])

    segments, audio_path = None, None

    if txt or audio_file:
        if audio_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                f.write(audio_file.read())
                audio_path = f.name

        if txt:
            name = os.path.splitext(txt.name)[0]
            text = clean_text(txt.read().decode())
        else:
            name = "uploaded_audio"
            text = clean_text(transcribe_audio(audio_path))

        duration = len(AudioSegment.from_file(audio_path))/1000 if audio_path else None
        segments = process_transcript(text, duration)
        save_segments_json(segments, name)

    else:
        files = [f for f in os.listdir(JSON_DIR) if f.endswith(".json")]
        if not files:
            st.warning("No segmented files found.")
            return
        selected = st.selectbox("Select segmented file", files)
        with open(os.path.join(JSON_DIR, selected), encoding="utf-8") as f:
            segments = json.load(f)
        base = selected.replace("_segments.json","").lower()
        for f in os.listdir(AUDIO_DIR):
            if base in f.lower():
                audio_path = os.path.join(AUDIO_DIR, f)
                break

    # Audio player
    if audio_path:
        st.audio(open(audio_path,"rb").read())

    # -----------------------------
    # Search & Keyword Filter
    # -----------------------------
    all_keywords = sorted({kw for seg in segments for kw in seg.get("keywords", [])})
    selected_keyword = st.selectbox("🏷 Filter by keyword", ["All"] + all_keywords)
    search_query = st.text_input("🔍 Search in transcripts")

    filtered_segments = []
    for seg in segments:
        if selected_keyword != "All" and selected_keyword not in seg.get("keywords", []):
            continue
        if search_query and search_query.lower() not in seg["text"].lower():
            continue
        filtered_segments.append(seg)

    # -----------------------------
    # CUSTOM CSS
    # -----------------------------
    st.markdown("""
    <style>
    .segment-card {padding:12px; margin-bottom:10px; border-radius:12px; color:white; cursor:pointer; font-weight:bold; transition: transform 0.2s;}
    .segment-card:hover {transform:scale(1.02);}
    .active-segment {border-left:6px solid #facc15; background-color:#111827;}
    .segment-1 {background:linear-gradient(90deg,#f97316,#facc15);}
    .segment-2 {background:linear-gradient(90deg,#10b981,#14b8a6);}
    .segment-3 {background:linear-gradient(90deg,#3b82f6,#6366f1);}
    .segment-4 {background:linear-gradient(90deg,#ec4899,#f472b6);}
    .details-card {background:linear-gradient(120deg,#1e3a8a,#3b82f6); padding:20px; border-radius:14px; color:white;}
    .badge {display:inline-block; padding:4px 8px; border-radius:8px; margin-right:6px; font-size:12px; color:white; font-weight:bold;}
    .badge-1 {background-color:#f97316;}
    .badge-2 {background-color:#10b981;}
    .badge-3 {background-color:#3b82f6;}
    .badge-4 {background-color:#ec4899;}
    </style>
    """, unsafe_allow_html=True)

    # -----------------------------
    # SEGMENTS LIST & DETAILS
    # -----------------------------
    col1, col2 = st.columns([1,2])
    with col1:
        st.subheader(f"🧩 Segments ({len(filtered_segments)})")
        for seg in filtered_segments:
            if st.button(f"Segment {seg['segment_id']} ⏱ {sec_to_mmss(seg['start_time'])}",
                         key=f"seg_{seg['segment_id']}"):
                st.session_state.jump_time = seg["start_time"]
                st.session_state.current_segment = seg
                st.rerun()

    with col2:
        st.subheader("📄 Segment Details")
        if "current_segment" in st.session_state:
            seg = st.session_state.current_segment
            st.markdown('<div class="details-card">', unsafe_allow_html=True)
            st.markdown(f"### ⏱ {sec_to_mmss(seg['start_time'])} → {sec_to_mmss(seg['end_time'])}")
            for i, kw in enumerate(seg["keywords"]):
                badge_class = f"badge-{(i%4)+1}"
                st.markdown(f'<span class="badge {badge_class}">{kw}</span>', unsafe_allow_html=True)
            st.markdown("#### 🧠 Summary")
            st.write(seg["summary"])
            st.markdown("#### 📝 Transcript")
            st.write(seg["text"])
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Select a segment to view details.")

# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    main()
