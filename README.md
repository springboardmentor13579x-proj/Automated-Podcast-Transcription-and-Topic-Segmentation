# Automated Podcast Transcription and Topic Segmentation

##  Project Overview

The **Automated Podcast Transcription & Topic Segmentation** project aims to build an end-to-end AI system that can:

- Convert podcast audio into accurate transcripts.
- Detect topic boundaries automatically.
- Segment the transcript into meaningful chapters.
- Extract keywords and summaries for each topic.
- Provide a UI to navigate the podcast episode by topics & timestamps.
- Display segment-level visual analytics.

This project focuses on applying **AI, Speech Processing, NLP, and ML engineering** to create a practical real-world audio intelligence tool.

## Project Objectives

### 1. Transcription (Speech-to-Text)
- Convert long podcast audio files into text using ASR models.
- Support noisy, multi-speaker, real-world audio.
- Produce timestamps for each transcribed segment.

### 2. Topic Segmentation
- Detect shifts in content and break the transcript into chapters.
- **Techniques Used:**
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

## System Architecture

Audio Input → Preprocessing → Transcription (ASR) → Transcript Cleaning → Embedding Model → Topic Segmentation → Segment Summaries & Keywords → Indexing → UI (Search, Playback, Visualization)

- Clickable segments → jump to timestamp.
- Playback visualization (Sentiment Timeline, Keyword Clouds).

## 🛠 Tech Stack

### Core
- Python 3.9+
- Whisper (OpenAI): ASR
- Librosa, PyDub, ffmpeg: Audio processing

### NLP
- NLTK (TextTiling)
- HuggingFace Transformers (Summarization)
- Sentence Transformers (Semantic Similarity)
- KeyBERT (Keywords)
- TextBlob (Sentiment Analysis)

### Visualization & UI
- Flask (Backend)
- Plotly (Interactive visualizations)
- HTML/CSS/JS (Frontend)

### Storage
- JSON (Transcript & metadata storage)

##  Folder Structure
Podcast_Transcription1/
│
├── data/
│ ├── raw/ # Source audio files
│ ├── transcripts/
│ ├── segmented_topics/
│ └── final_output/
│
├── src/
│ ├── transcriber.py # Whisper model wrapper
│ ├── data_loader.py # MP3 → WAV & audio processing
│ ├── semantic_segmenter.py # BERT-based segmentation
│ ├── content_processor.py # Summary, Keywords & Sentiment
│ ├── file_utils.py # Path helpers
│ └── web_app/
│ ├── templates/
│ │ ├── index.html # UI Page 1
│ │ └── player.html # Player with visualizations
│ └── app.py # Flask backend
│
├── main.py # Step 1: Transcription
├── run_segmentation.py # Step 2: Topic segmentation
├── run_processing.py # Step 3: Summaries & keywords
├── evaluate_accuracy.py # WER calculation
├── requirements.txt # Dependencies
└── README.md # Documentation

## ⚙ Installation & Setup

### 1. Clone the Repository
git clone <repo-url>
cd Podcast_Transcription1

### 2. Create Virtual Environment
python -m venv venv
source venv/bin/activate      # Mac/Linux
.env\Scriptsctivate       # Windows

### 3. Install Dependencies
pip install flask transformers torch torchaudio sentence-transformers textblob keybert jiwer plotly pydub nltk scikit-learn openai-whisper

### 4. Install FFmpeg
Required for audio processing.
- Windows: download from gyan.dev  
- Mac: brew install ffmpeg

##  How to Run

### Run the Pipeline

# Step 1: Transcribe (Audio → Text)
python main.py

# Step 2: Segment (Text → Topics)
python run_segmentation.py

# Step 3: Generate Summaries/Keywords
python run_processing.py

### Launch Web UI

python src/web_app/app.py

Then open in browser: http://127.0.0.1:5000

