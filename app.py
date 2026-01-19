import streamlit as st
import os, json, re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from config import AUDIO_PROCESSED_DIR, SEGMENTS_DIR

nltk.data.path.append(r"C:\Users\USER\nltk_data")

# ---------------- HELPERS ----------------
POS = {
    "improve","improvement","improving","recovery","recover","recovered",
    "effective","efficacy","successful","success","stable","stabilized",
    "normal","normalized","safe","safer","safely","benefit","beneficial",
    "controlled","relief","relieved","relieving",
    "healed","healing","cured","curable","responsive","responding",
    "reduced","reduction","lowered","favorable","promising",
    "managed","manageable","resolution","resolved",
    "asymptomatic","remission","positive"
}

NEG = {
    "pain","painful","severe","risk","risky","infection","infected",
    "failure","failed","critical","life-threatening","complication",
    "worsen","worsening","deterioration","death","fatal","mortality",
    "bleeding","toxic","toxicity","adverse","hospitalized","icu",
    "chronic","incurable","malignant","relapse","recurrence",
    "uncontrolled","unstable","poor","negative"
}

def extract_sentiment_words(text):
    words = re.findall(r"\b[a-z]+\b", text.lower())
    return {
        "Positive": [w for w in words if w in POS],
        "Negative": [w for w in words if w in NEG],
        "Neutral":  [w for w in words if w not in POS and w not in NEG]
    }

# -------- AUTO CLINICAL SUMMARY --------
def generate_clinical_summary(pos, neg):
    neg_count = len(neg)

    if neg_count >= 10:
        risk = "HIGH RISK"
        advice = "Immediate medical consultation is required."
    elif neg_count >= 4:
        risk = "MODERATE RISK"
        advice = "Consult a physician and monitor symptoms regularly."
    else:
        risk = "LOW RISK"
        advice = "Continue routine care and follow-up if necessary."

    return {
        "risk": risk,
        "advice": advice,
        "positive": list(set(pos))[:5],
        "negative": list(set(neg))[:5]
    }

# ---------------- UI STYLE ----------------
st.set_page_config("MEDI-LENS", layout="wide")

st.markdown("""
<style>

/* ---------- GLOBAL BACKGROUND ---------- */
.stApp {
    background: linear-gradient(135deg, #ff7a7a, #b84cff, #4f46e5);
    background-attachment: fixed;
    font-family: 'Segoe UI', sans-serif;
}

/* ---------- GLASS CARD ---------- */
.card {
    background: rgba(255, 255, 255, 0.18);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.18);
    margin-bottom: 16px;
    color: white;
}

/* ---------- CENTER ---------- */
.center { text-align: center; }

/* ---------- TITLE ---------- */
.big {
    font-size: 64px;
    font-weight: 900;
    color: white;
}

/* ---------- TAGLINE ---------- */
.slogan {
    font-size: 22px;
    color: rgba(255,255,255,0.85);
}

/* ---------- BUTTONS ---------- */
.stButton > button {
    background: linear-gradient(135deg, #ff4ecd, #7c5cff);
    color: white;
    border: none;
    padding: 14px 36px;
    font-size: 18px;
    font-weight: 700;
    border-radius: 999px;
    transition: 0.3s ease;
    box-shadow: 0 6px 18px rgba(0,0,0,0.25);
}

.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 28px rgba(0,0,0,0.35);
}

/* ---------- TABS ---------- */
.stTabs [data-baseweb="tab"] {
    font-size: 16px;
    color: white;
}

.stTabs [aria-selected="true"] {
    background: rgba(255,255,255,0.18);
    border-radius: 12px;
}

/* ---------- INPUTS ---------- */
.stTextInput input, .stSelectbox div {
    background: rgba(255,255,255,0.15);
    color: white;
    border-radius: 10px;
}

/* ---------- HEADERS ---------- */
h1, h2, h3, h4 {
    color: white;
}

footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "started" not in st.session_state:
    st.session_state.started = False

# ================= LANDING PAGE =================
if not st.session_state.started:
    st.markdown("""
    <div class="center">
        <div style="
            width:120px;
            height:120px;
            border-radius:50%;
            background: linear-gradient(135deg,#ff4ecd,#7c5cff);
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:48px;
            margin:auto;
            box-shadow:0 10px 30px rgba(0,0,0,0.4);
        ">
            🎙️
        </div>
        <br>
        <div class="big">MEDI-LENS</div>
        <div class="slogan">Medical Audio → Actionable Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='card'>🎧 Audio → Medical Transcripts</div>", unsafe_allow_html=True)
    c2.markdown("<div class='card'>📊 Sentiment & Keyword Analysis</div>", unsafe_allow_html=True)
    c3.markdown("<div class='card'>🩺 Auto Clinical Summary</div>", unsafe_allow_html=True)

    _, mid, _ = st.columns([2,1,2])
    if mid.button("▶ START"):
        st.session_state.started = True
        st.rerun()

    st.stop()

# ================= MAIN APP =================
tab1, tab2 = st.tabs([
    "🎧 Audio Upload",
    "📊 Sentiment & Keyword Explorer"
])

# ================= AUDIO =================
with tab1:
    uploaded = st.file_uploader("Upload audio", type=["mp3","wav"])
    files = [f for f in os.listdir(AUDIO_PROCESSED_DIR) if f.endswith((".mp3",".wav"))]

    if uploaded:
        audio_path = os.path.join(AUDIO_PROCESSED_DIR, uploaded.name)
        with open(audio_path, "wb") as f:
            f.write(uploaded.read())
    elif files:
        audio_path = os.path.join(
            AUDIO_PROCESSED_DIR,
            st.selectbox("Select audio", files)
        )
    else:
        st.info("Upload audio to begin")
        st.stop()

    st.audio(open(audio_path, "rb").read())

    expected_json = os.path.join(
        SEGMENTS_DIR,
        f"{os.path.basename(audio_path)}_segments.json"
    )

    json_files = [f for f in os.listdir(SEGMENTS_DIR) if f.endswith("_segments.json")]

    if os.path.exists(expected_json):
        json_path = expected_json
    elif json_files:
        json_path = os.path.join(
            SEGMENTS_DIR,
            st.selectbox("Select transcript JSON", json_files)
        )
    else:
        st.error("No transcript JSONs found")
        st.stop()

    segments = json.load(open(json_path, "r", encoding="utf-8"))

    c1, c2, c3 = st.columns(3)
    show_full = c1.button("📄 Full Transcription")
    show_seg = c2.button("🧩 Segments")
    clear = c3.button("🧹 Clear")

    search = st.text_input("🔍 Search keyword")

    if clear:
        st.rerun()

    if show_full:
        st.markdown(
            "<div class='card'>" + " ".join(s["text"] for s in segments) + "</div>",
            unsafe_allow_html=True
        )

    if show_seg or search:
        for s in segments:
            if not search or search.lower() in s["text"].lower():
                st.markdown(
                    f"<div class='card'><b>Segment {s['segment_id']}</b><br>{s['text']}</div>",
                    unsafe_allow_html=True
                )

# ================= ANALYSIS =================
with tab2:
    pos, neg, neu = [], [], []

    for s in segments:
        sw = extract_sentiment_words(s["text"])
        pos += sw["Positive"]
        neg += sw["Negative"]
        neu += sw["Neutral"]

    summary = generate_clinical_summary(pos, neg)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Sentiment Analysis")

        fig, ax = plt.subplots(figsize=(3,2))
        ax.bar(
            ["Positive","Neutral","Negative"],
            [len(pos), len(neu), len(neg)]
        )
        ax.set_title("Sentiment Words Count", fontsize=9)
        st.pyplot(fig)

        st.markdown(
            "<div class='card'><b>✅ Positive Words</b><br>" +
            (", ".join(set(pos)) if pos else "—") +
            "</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<div class='card'><b>⚪ Neutral Words</b><br>" +
            (", ".join(list(set(neu))[:12]) if neu else "—") +
            "</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<div class='card'><b>❌ Negative Words</b><br>" +
            (", ".join(set(neg)) if neg else "—") +
            "</div>",
            unsafe_allow_html=True
    )


    with col2:
        st.subheader("☁ Keyword Cloud")
        text = " ".join(s["text"] for s in segments).lower()
        words = re.findall(r"\b[a-z]{3,}\b", text)
        stop = set(TfidfVectorizer(stop_words="english").get_stop_words())
        words = [w for w in words if w not in stop]

        freq = dict(Counter(words).most_common(12))
        wc = WordCloud(width=300, height=200, background_color="white").generate_from_frequencies(freq)

        fig, ax = plt.subplots(figsize=(3,2))
        ax.imshow(wc)
        ax.axis("off")
        st.pyplot(fig)

        kw = st.selectbox("Select keyword", list(freq.keys()))

    st.markdown("---")
    st.subheader("📄 Keyword-based Segments")

    for s in segments:
        if kw in s["text"].lower():
            st.markdown(f"<div class='card'>{s['text']}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🩺 Auto Clinical Summary")

    st.markdown(f"""
    <div class="card">
        <b>📌 OVERALL STATUS</b><br><b>{summary['risk']}</b><br><br>
        <b>📈 POSITIVE INDICATORS</b><br>
        {"• " + "<br>• ".join(summary['positive']) if summary['positive'] else "—"}<br><br>
        <b>⚠️ RISK FACTORS</b><br>
        {"• " + "<br>• ".join(summary['negative']) if summary['negative'] else "—"}<br><br>
        <b>🩺 PATIENT RECOMMENDATION</b><br>
        {summary['advice']}
    </div>
    """, unsafe_allow_html=True)
