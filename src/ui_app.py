import streamlit as st
import os, re
import numpy as np
import pandas as pd
from pydub import AudioSegment
import plotly.express as px
import plotly.graph_objects as go
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ---------------- NLTK ----------------
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="HR Interview Analyzer",
    layout="wide",
    page_icon="🎤"
)

# ---------------- UI AUDIO FOLDERS ----------------
AUDIO_UI = "audio_UI"
CLIP_DIR = os.path.join(AUDIO_UI, "clips")
os.makedirs(AUDIO_UI, exist_ok=True)
os.makedirs(CLIP_DIR, exist_ok=True)

# ---------------- SESSION STATE ----------------
DEFAULTS = {
    "analyzed": False,
    "audio_path": None,
    "segments": [],
    "clips": {},
    "transcript": "",
    "scores": [],
    "speakers": [],
    "keywords": [],
    "selected_kw": None
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- STYLES ----------------
st.markdown("""
<style>
.header {
    background: linear-gradient(90deg, #22c55e, #0ea5e9, #8b5cf6);
    padding: 26px;
    border-radius: 20px;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.4);
}
.block {
    background: rgba(15,23,42,0.97);
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 20px;
    color: #e5e7eb;
    box-shadow: 0 6px 18px rgba(0,0,0,0.35);
}
.segment {
    padding:16px;
    border-radius:14px;
    margin-bottom:12px;
}
.interviewer { border-left:6px solid #22c55e; background:#022c22; }
.candidate { border-left:6px solid #f97316; background:#2c1a02; }
.narrator { border-left:6px solid #0ea5e9; background:#021c2c; }
.badge {
    display:inline-block;
    padding:4px 12px;
    border-radius:10px;
    font-size:12px;
    margin-right:8px;
    font-weight:700;
}
.badge-i { background:#22c55e; color:black; }
.badge-c { background:#f97316; color:black; }
.badge-n { background:#0ea5e9; color:black; }
.empty-msg {
    padding:12px;
    border-radius:10px;
    background:#1f2937;
    color:#9ca3af;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- UTILS ----------------
def transcribe_with_timestamps(audio_path):
    import whisper
    model = whisper.load_model("base")
    return model.transcribe(audio_path)

def split_into_segments(result):
    segments = []
    for seg in result["segments"]:
        text = seg["text"].strip()
        if len(text) > 8:
            segments.append({
                "text": text,
                "start": float(seg["start"]),
                "end": float(seg["end"])
            })
    return segments

def detect_speaker(text):
    t = text.lower()
    if any(q in t for q in ["tell me", "why", "what is", "how do you", "can you", "where do you", "explain"]):
        return "Interviewer"
    if any(c in t for c in ["i am", "i have", "my experience", "i worked", "i want", "i did"]):
        return "Candidate"
    return "Narrator"

CLOSING_PHRASES = ["like and subscribe", "thanks for listening", "rate us", "follow us", "stay tuned", "leave a review"]

def enforce_conversation_order(segments):
    speakers = [detect_speaker(s["text"]) for s in segments]
    if "Interviewer" not in speakers:
        return segments

    first_interviewer = speakers.index("Interviewer")
    last_conv = max(i for i, s in enumerate(speakers) if s in ["Interviewer", "Candidate"])

    filtered = []
    for i, s in enumerate(segments):
        sp = detect_speaker(s["text"])
        text = s["text"].lower()

        if i < first_interviewer:
            filtered.append(s)
        elif first_interviewer <= i <= last_conv:
            if sp != "Narrator":
                filtered.append(s)
        else:
            if any(p in text for p in CLOSING_PHRASES):
                filtered.append(s)

    return filtered

def generate_audio_clips(audio_path, segments):
    audio = AudioSegment.from_file(audio_path)
    clips = {}
    for i, s in enumerate(segments, 1):
        start_ms = int(s["start"] * 1000)
        end_ms = int(s["end"] * 1000)
        clip = audio[start_ms:end_ms]
        path = os.path.join(CLIP_DIR, f"segment_{i}.wav")
        clip.export(path, format="wav")
        clips[i] = path
    return clips

# ---------------- KEYWORDS ----------------
def clean_text_for_keywords(text):
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text.lower()

def filter_duplicates(keywords):
    final = []
    for kw in keywords:
        if not any(kw in chosen or chosen in kw for chosen in final):
            final.append(kw)
    return final

def extract_keywords(text, top_k=15):
    text = clean_text_for_keywords(text)
    if len(text.split()) < 5:
        return []

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=200)
    tfidf = vectorizer.fit_transform([text])
    scores = tfidf.toarray()[0]
    terms = vectorizer.get_feature_names_out()

    ranked = sorted(zip(terms, scores), key=lambda x: x[1], reverse=True)
    raw_keywords = [term for term, _ in ranked]
    filtered = filter_duplicates(raw_keywords)
    return filtered[:top_k]

# ---------------- EMOTION ----------------
def classify_emotion(score):
    if score > 0.4:
        return "Confidence"
    elif score < -0.4:
        return "Stress"
    elif -0.4 <= score <= -0.1:
        return "Hesitation"
    else:
        return "Neutral"

# ---------------- CANDIDATE SCORING ----------------
def compute_candidate_scores(df):
    cand = df[df["Speaker"] == "Candidate"]
    if cand.empty:
        return {"Communication": 50, "Confidence": 50, "Engagement": 50}

    communication = (cand["Sentiment"].abs().mean()) * 100
    confidence = len(cand[cand["Sentiment"] > 0.2]) / len(cand) * 100
    engagement = len(cand) / len(df) * 100

    return {
        "Communication": round(min(100, communication), 1),
        "Confidence": round(min(100, confidence), 1),
        "Engagement": round(min(100, engagement), 1)
    }

def recruiter_decision(scores):
    avg = np.mean(list(scores.values()))
    if avg >= 65:
        return "✅ HIRE", "Candidate shows strong confidence, engagement, and communication skills."
    elif avg >= 45:
        return "⚠️ HOLD", "Candidate shows moderate potential but needs further evaluation."
    else:
        return "❌ REJECT", "Candidate lacks sufficient confidence, clarity, or engagement."

# ---------------- HEADER ----------------
st.markdown("""
<div class="header">
    <h1>🎤 HR Interview & Meeting Analyzer</h1>
    <p>Enterprise-Grade AI Dashboard • Audio Intelligence • Recruiter Insights</p>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs([
    "📤 Upload",
    "📄 Transcript",
    "🧩 Segments",
    "📊 Visual Analytics",
    "🔑 Keywords",
    "📈 Sentiment Metrics",
    "📌 AI Summary"
])

# =========================================================
# 1️⃣ UPLOAD
# =========================================================
with tabs[0]:
    st.markdown("<div class='block'><h3>Upload Audio</h3></div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload interview / meeting audio", type=["wav", "mp3"])

    if uploaded:
        path = os.path.join(AUDIO_UI, uploaded.name)
        with open(path, "wb") as f:
            f.write(uploaded.read())

        if st.session_state.audio_path != path:
            for k in DEFAULTS:
                st.session_state[k] = DEFAULTS[k]
            st.session_state.audio_path = path

        st.success("Audio uploaded!")

    if st.session_state.audio_path:
        st.audio(st.session_state.audio_path)

        if st.button("🚀 Analyze Audio"):
            with st.spinner("Transcribing, segmenting and analyzing..."):
                result = transcribe_with_timestamps(st.session_state.audio_path)
                raw = split_into_segments(result)
                ordered = enforce_conversation_order(raw)
                clips = generate_audio_clips(st.session_state.audio_path, ordered)

                sia = SentimentIntensityAnalyzer()
                scores = [sia.polarity_scores(s["text"])["compound"] for s in ordered]
                speakers = [detect_speaker(s["text"]) for s in ordered]

                st.session_state.transcript = result["text"]
                st.session_state.segments = ordered
                st.session_state.clips = clips
                st.session_state.scores = scores
                st.session_state.speakers = speakers
                st.session_state.keywords = extract_keywords(result["text"], top_k=15)
                st.session_state.selected_kw = st.session_state.keywords[0] if st.session_state.keywords else None
                st.session_state.analyzed = True

            st.success("Analysis completed!")

# =========================================================
# SAFE GATE
# =========================================================
if not st.session_state.analyzed:
    st.info("Upload an audio file and click **Analyze Audio** to start.")
else:
    segments = st.session_state.segments
    clips = st.session_state.clips
    transcript_text = st.session_state.transcript
    scores = st.session_state.scores
    speakers = st.session_state.speakers
    keywords = st.session_state.keywords

    df = pd.DataFrame({
        "Segment": list(range(1, len(segments) + 1)),
        "Sentiment": scores,
        "Speaker": speakers,
        "Text": [s["text"] for s in segments]
    })
    df["Emotion"] = df["Sentiment"].apply(classify_emotion)

    # =========================================================
    # 2️⃣ TRANSCRIPT
    # =========================================================
    with tabs[1]:
        st.markdown("<div class='block'><h3>Transcript</h3></div>", unsafe_allow_html=True)
        st.text_area("Full Transcript", transcript_text, height=400)

    # =========================================================
    # 3️⃣ SEGMENTS
    # =========================================================
    with tabs[2]:
        st.markdown("<div class='block'><h3>Conversation Segments</h3></div>", unsafe_allow_html=True)
        for i, s in enumerate(segments, 1):
            speaker = detect_speaker(s["text"])
            cls = "interviewer" if speaker == "Interviewer" else "candidate" if speaker == "Candidate" else "narrator"
            badge = "badge-i" if speaker == "Interviewer" else "badge-c" if speaker == "Candidate" else "badge-n"

            st.markdown(f"""
            <div class='segment {cls}'>
                <span class='badge {badge}'>{speaker}</span>
                <b>Segment {i} | ⏱ {round(s['start'],1)}s – {round(s['end'],1)}s</b><br>
                {s['text']}
            </div>
            """, unsafe_allow_html=True)
            st.audio(clips[i])

    # =========================================================
    # 4️⃣ VISUAL ANALYTICS (6 PLOTS)
    # =========================================================
    with tabs[3]:
        st.subheader("📈 1. Sentiment Timeline")
        fig1 = px.line(df, x="Segment", y="Sentiment", color="Speaker", markers=True,
                       hover_data=["Emotion", "Text"])
        st.plotly_chart(fig1, width="stretch")
        st.info("Each point represents a spoken segment. Positive values = confidence, negative = stress.")

        st.subheader("🔥 2. Segment Polarity Heatmap")
        fig2 = px.imshow([df["Sentiment"].values], color_continuous_scale="RdBu", aspect="auto")
        st.plotly_chart(fig2, width="stretch")
        st.info("Blue blocks = positive/confident responses. Red blocks = negative or hesitant answers.")

        st.subheader("🎙 3. Speaker Distribution")
        speaker_counts = df["Speaker"].value_counts().reset_index()
        speaker_counts.columns = ["Speaker", "Count"]
        fig3 = px.bar(speaker_counts, x="Speaker", y="Count", color="Speaker")
        st.plotly_chart(fig3, width="stretch")
        st.info("Shows how much each participant spoke during the interview.")

        st.subheader("📊 4. Average Sentiment by Speaker")
        speaker_avg = df.groupby("Speaker")["Sentiment"].mean().reset_index()
        fig4 = px.bar(speaker_avg, x="Speaker", y="Sentiment", color="Speaker")
        st.plotly_chart(fig4, width="stretch")
        st.info("Candidate positivity indicates confidence. Interviewer neutrality reflects evaluation tone.")

        st.subheader("🧠 5. Emotion Classification")
        emo_counts = df["Emotion"].value_counts().reset_index()
        emo_counts.columns = ["Emotion", "Count"]
        fig5 = px.bar(emo_counts, x="Emotion", y="Count", color="Emotion")
        st.plotly_chart(fig5, width="stretch")
        st.info("Shows confidence, hesitation, stress, and neutral patterns across the interview.")

        st.subheader("📌 6. Candidate Engagement Radar")
        scores_dict = compute_candidate_scores(df)
        fig6 = go.Figure()
        fig6.add_trace(go.Scatterpolar(
            r=list(scores_dict.values()),
            theta=list(scores_dict.keys()),
            fill='toself'
        ))
        fig6.update_layout(polar=dict(radialaxis=dict(range=[0, 100])), showlegend=False)
        st.plotly_chart(fig6, width="stretch")
        st.info("Summarizes candidate performance across communication, confidence, and engagement.")

    # =========================================================
    # 5️⃣ KEYWORDS
    # =========================================================
    with tabs[4]:
        st.markdown("<div class='block'><h3>Keyword Search</h3></div>", unsafe_allow_html=True)
        col_left, col_right = st.columns([2, 1])

        with col_left:
            selected_kw = st.selectbox("🔍 Select a keyword:", keywords)
            matches = [(i, s) for i, s in enumerate(segments, 1) if selected_kw.lower() in s["text"].lower()]
            if matches:
                for i, s in matches:
                    st.markdown(f"**⏱ {round(s['start'],1)}s – {round(s['end'],1)}s**: {s['text']}")
                    st.audio(clips[i])
            else:
                st.markdown("<div class='empty-msg'>No segments found.</div>", unsafe_allow_html=True)

        with col_right:
            wc_text = " ".join(keywords)
            wc = WordCloud(width=500, height=300, background_color="black", colormap="plasma").generate(wc_text)
            fig, ax = plt.subplots()
            ax.imshow(wc)
            ax.axis("off")
            st.pyplot(fig)

    # =========================================================
    # 6️⃣ SENTIMENT METRICS + DECISION
    # =========================================================
    with tabs[5]:
        avg = np.mean(scores)
        pos = len([s for s in scores if s > 0.1]) / len(scores) * 100
        neg = len([s for s in scores if s < -0.1]) / len(scores) * 100
        emotion = "Positive 😊" if avg > 0.1 else "Negative 😟" if avg < -0.1 else "Neutral 😐"

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Avg Sentiment", f"{avg:.2f}")
        c2.metric("Positive %", f"{pos:.1f}%")
        c3.metric("Negative %", f"{neg:.1f}%")
        c4.metric("Overall Tone", emotion)

        st.subheader("🎯 Recruiter Decision")
        scores_dict = compute_candidate_scores(df)
        decision, reason = recruiter_decision(scores_dict)
        st.success(decision)
        st.write(reason)

    # =========================================================
    # 7️⃣ AI SUMMARY
    # =========================================================
    with tabs[6]:
        st.markdown("<div class='block'><h3>AI Interview Summary</h3></div>", unsafe_allow_html=True)
        sentences = re.split(r'(?<=[.!?])\s+', transcript_text)
        key_sentences = [s for s in sentences if any(k in s.lower() for k in keywords)]
        summary = " ".join(key_sentences[:6])
        st.success(summary if summary else "AI summary could not be generated.")
