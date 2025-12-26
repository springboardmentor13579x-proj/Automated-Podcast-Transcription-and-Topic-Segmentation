# Automated Podcast Transcription and Topic Segmentation

## 📌 Project Overview

The **Automated Podcast Transcription & Topic Segmentation** project aims to build an end-to-end AI system that can:

- Convert podcast audio into accurate transcripts.
- Detect topic boundaries automatically.
- Segment the transcript into meaningful chapters.
- Extract keywords and summaries for each topic.
- Provide a UI to navigate the podcast episode by topics & timestamps.
- Display segment-level visual analytics.

This project focuses on applying **AI, Speech Processing, NLP, and ML engineering** to create a practical real-world audio intelligence tool.

---

## 🎯 Project Objectives

### 1. Transcription (Speech-to-Text)
- Convert long podcast audio files into text using ASR models.
- Support noisy, multi-speaker, real-world audio.
- Produce timestamps for each transcribed segment.

### 2. Topic Segmentation
- Detect shifts in content and break the transcript into chapters.
- **Techniques Used**
  - TextTiling (Classic NLP)
  - Embedding similarity (BERT / Sentence Transformers)
  - Change-point detection methods

### 3. Summarization & Keyword Extraction
Generate per-topic:

- Short abstractive summaries *(DistilBART)*
- Keywords and keyphrases *(KeyBERT)*
- Sentiment Analysis *(TextBlob)*

### 4. UI for Navigation
- Show transcript & segment list.

---

## 🏗 System Architecture

```
Audio Input 
→ Preprocessing 
→ Transcription (ASR) 
→ Transcript Cleaning 
→ Embedding Model 
→ Topic Segmentation 
→ Segment Summaries & Keywords 
→ Indexing 
→ UI (Search, Playback, Visualization)
```

- Clickable segments → jump to timestamp  
- Playback visualization (Sentiment Timeline, Keyword Clouds)

---

## 🛠 Tech Stack

### Core
- Python 3.9+
- Whisper (OpenAI)
- Librosa, PyDub, ffmpeg

### NLP
- NLTK (TextTiling)
- HuggingFace Transformers
- Sentence Transformers
- KeyBERT
- TextBlob

### Visualization & UI
- Flask
- Plotly
- HTML/CSS/JS

### Storage
- JSON structured metadata

---

## 📁 Folder Structure

```
Podcast_Transcription1/
│
├── data/
│   ├── raw/                    # Source audio files
│   ├── transcripts/
│   ├── segmented_topics/
│   └── final_output/
│
├── src/
│   ├── transcriber.py          # Whisper model wrapper
│   ├── data_loader.py          # MP3 → WAV audio loader
│   ├── semantic_segmenter.py   # BERT-based segmentation
│   ├── content_processor.py    # Summary, Keywords & Sentiment
│   ├── file_utils.py           # Utility helpers
│   └── web_app/
│       ├── templates/
│       │   ├── index.html      # Homepage UI
│       │   └── player.html     # Transcript Player
│       └── app.py              # Flask server entrypoint
│
├── main.py                     # Step 1: Transcription
├── run_segmentation.py         # Step 2: Topic Segmentation
├── run_processing.py           # Step 3: Summary & Keywords
├── evaluate_accuracy.py        # WER evaluation
├── requirements.txt            # Dependencies
└── README.md                   # Project documentation
```

---

## ⚙ Installation & Setup

### Clone Project
```bash
git clone <repo-url>
cd Podcast_Transcription1
```

### Create Environment
```bash
python -m venv venv
source venv/bin/activate      # Mac / Linux
.env\Scriptsctivate       # Windows
```

### Install Dependencies
```bash
pip install flask transformers torch torchaudio sentence-transformers textblob keybert jiwer plotly pydub nltk scikit-learn openai-whisper
```

### Install FFmpeg
- Windows: download from gyan.dev  
- macOS: `brew install ffmpeg`

---

## 🚀 Run Pipeline

```bash
# Step 1: Transcribe
python main.py

# Step 2: Segment Topics
python run_segmentation.py

# Step 3: Summaries + Keywords
python run_processing.py
```

### Launch Web UI

```bash
python src/web_app/app.py
```

Open browser:  
`http://127.0.0.1:5000`

---

## 📂 Dataset Access
Due to the large size of the audio files, the dataset is hosted externally.

**📥 [https://drive.google.com/drive/folders/1yN69e6oQ2PJtBvhJ90a-YYtRfbIz7vcW?usp=drive_link] 

### **Setup Instructions**
1. Download the dataset from the link above.
2. Extract the folder.
3. Place the audio files in a folder named `audio_raw` inside the project root.
4. Update the `AUDIO_DIR` path in `.env` if necessary.

