🎧 Automated Podcast Transcription & Topic Segmentation
A Springboard Internship Program Project

📌 Project Overview
The Automated Podcast Transcription & Topic Segmentation project focuses on converting long-form podcast audio into structured, readable, and analyzable text.

This system processes Indian language podcast audio and performs:

Speech-to-text transcription

Transcript segmentation

Segment-level summarization

Keyword extraction

The goal is to make spoken content easier to understand, explore, and reuse for analysis and future UI-based navigation.

🎯 Project Objectives
1. Transcription (Speech-to-Text)
Convert podcast audio into text using Whisper ASR

Support Indian languages (Hindi, Bengali, Gujarati, Marathi, Punjabi, Kannada, Urdu)

Handle real-world noisy podcast audio

2. Topic Segmentation
Break long transcripts into smaller, meaningful segments

Use sentence-based segmentation with timestamps

3. Summarization
Generate short summaries for each transcript segment

Use NLP-based extractive summarization

4. Keyword Extraction
Extract important keywords from each segment

Enable topic understanding and future search functionality

🧠 Current Project Status
✅ Audio preprocessing
✅ Transcription using Whisper
✅ Transcript segmentation
✅ Segment-level summarization
✅ Keyword extraction
🚧 UI & advanced topic modeling (future work)

🗂️ Folder Structure
project/
│── cleaned_audio/          # Preprocessed audio files
│── Raw_audio/              # Original dataset (Indian languages)
│   ├── Hindi/
│   ├── Bengali/
│   ├── Gujarati/
│   ├── Marathi/
│   ├── Punjabi/
│   ├── Kannada/
│   └── Urdu/
│── transcripts/            # Generated text transcripts
│── segments/               # Segmented transcript JSON files
│── Summarization/          # Output summaries
│── keyword/                # Keyword extraction outputs
│── notebooks/              # Experiment notebooks
│── src/
│   ├── preprocessing.py
│   ├── transcription.py
│   ├── segmentation.py
│   ├── summarization.py
│   ├── keyword_extraction.py
│   └── ui_app.py
│── docs/
│── tests/
│── README.md
│── requirements.txt
│── LICENSE
│── .gitignore
🏗️ System Architecture (High Level)
Audio Input
   ↓
Audio Preprocessing
   ↓
Whisper ASR (Transcription)
   ↓
Transcript Cleaning
   ↓
Text Segmentation
   ↓
Summarization + Keyword Extraction
   ↓
Structured JSON Output
🧪 Tech Stack
Core
Python 3.9+

Whisper ASR

FFmpeg

PyDub

NLP
NLTK

Scikit-learn (TF-IDF)

Storage
JSON files for structured outputs

Tools
VS Code

Git & GitHub

🚀 How to Run
1️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Run transcription
python src/transcription.py
4️⃣ Run segmentation
python src/segmentation.py
5️⃣ Run summarization
python src/summarization.py
6️⃣ Run keyword extraction
python src/keyword_extraction.py

📊 Output Format (Example)
Each segment contains:

{
  "segment_id": 1,
  "start_time": 0.0,
  "end_time": 45.2,
  "text": "Segment transcript text",
  "summary": "Short summary",
  "keywords": ["podcast", "topic", "discussion"]
}
🔮 Future Enhancements
Advanced topic segmentation (TextTiling, embeddings)

Semantic search across segments

Interactive transcript UI

Audio playback with timestamp navigation

Deployment using Streamlit

📜 License
This project is licensed under the MIT License.

👩‍💻 Author
Muskan Yadav
Springboard Internship Program
