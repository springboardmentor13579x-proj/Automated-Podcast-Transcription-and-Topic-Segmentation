# Automated Medical Podcast Transcription and Topic Segmentation

## Project Overview

Medical podcasts contain valuable discussions on diseases, treatments, research findings, and clinical experiences. However, these podcasts are often long and difficult to navigate.

This project aims to build an AI-powered system that automatically transcribes medical podcast audio, detects topic boundaries, and segments the content into meaningful medical topics with summaries and keywords.

The system helps students, researchers, and healthcare professionals quickly access relevant medical information without listening to the entire podcast episode.

---

## Use Case (Medical Domain)

This project is designed specifically for medical podcasts, including:

- Clinical discussions  
- Disease awareness talks  
- Medical education podcasts  
- Expert interviews and panel discussions  
- Public health awareness programs  

### Benefits
- Quickly locate discussions about specific diseases or treatments  
- Navigate podcasts using topic-wise chapters  
- Understand content through summaries and keywords  
- Save time for medical students and professionals  

---

## Project Objectives

### 1. Transcription (Speech-to-Text)
- Convert long medical podcast audio into text using ASR models  
- Handle noisy, real-world medical audio  
- Generate timestamps for each transcribed segment  

---

### 2. Topic Segmentation
- Detect topic shifts in medical discussions  
- Segment transcripts into meaningful medical chapters  
- Use NLP techniques such as:
  - TextTiling  
  - Embedding similarity (Sentence Transformers / BERT)  
  - Change-point detection methods  

---

### 3. Summarization and Keyword Extraction
For each medical topic segment:
- Generate short summaries  
- Produce bullet-point notes  
- Extract important medical keywords  

---

### 4. Frontend UI for Navigation
- Display transcripts with topic-wise segmentation  
- Enable click-to-jump using timestamps  
- Provide audio playback controls  
- Visualize segments, summaries, and keywords  
- Interact with backend APIs for transcription and analysis  

---
## System Architecture

Audio Input
↓
Audio Preprocessing
↓
Medical Speech-to-Text (ASR)
↓
Transcript Cleaning
↓
Embedding Model
↓
Topic Segmentation
↓
Medical Summaries and Keywords
↓
Indexing
↓
Frontend UI (Search, Playback, Visualization)

---

## Tech Stack

### Backend
- Python 3.9+
- Flask
- Whisper (OpenAI) / Faster-Whisper
- Librosa, PyDub, FFmpeg

### NLP and Machine Learning
- NLTK
- SpaCy
- HuggingFace Transformers
- Sentence Transformers
- KeyBERT / YAKE / RAKE

### Frontend
- React.js
- HTML, CSS, JavaScript
- REST API integration with backend

### Visualization
- Plotly
- Matplotlib

### Storage
- JSON / CSV for metadata
- SQLite (optional)
- FAISS / Vector Database (optional)

---

## Project Structure


---

## Tech Stack

### Backend
- Python 3.9+
- Flask
- Whisper (OpenAI) / Faster-Whisper
- Librosa, PyDub, FFmpeg

### NLP and Machine Learning
- NLTK
- SpaCy
- HuggingFace Transformers
- Sentence Transformers
- KeyBERT / YAKE / RAKE

### Frontend
- React.js
- HTML, CSS, JavaScript
- REST API integration with backend

### Visualization
- Plotly
- Matplotlib

### Storage
- JSON / CSV for metadata
- SQLite (optional)
- FAISS / Vector Database (optional)

---

## Project Structure
Automated-Podcast-Transcription-and-Topic-Segmentation/
│
├── Data/ # Backend (Flask)
│ ├── app.py
│ ├── src/
│ │ ├── preprocessing.py
│ │ ├── transcription.py
│ │ ├── segmentation.py
│ │ ├── summarization.py
│ │ ├── keyword_extraction.py
│ │ └── evaluation_summary.py
│ └── requirements.txt
│
├── frontend/ # React frontend UI
│ ├── public/
│ ├── src/
│ │ ├── components/
│ │ │ ├── Home.jsx
│ │ │ ├── Segments.jsx
│ │ │ ├── Transcription.jsx
│ │ │ ├── TopicSearch.jsx
│ │ │ └── Downloads.jsx
│ │ ├── App.js
│ │ ├── api.js
│ │ └── index.js
│ ├── package.json
│ ├── package-lock.json
│ └── .gitignore
│
├── Inference/ # Generated outputs (not committed)
│ ├── transcripts/
│ ├── segments/
│ └── keywords/
│
├── notebooks/ # Experiments and analysis
├── docs/ # Documentation
├── tests/ # Test cases
│
├── README.md
├── requirements.txt
├── LICENSE
└── .env.example

---

## Milestone-wise Implementation

### Milestone 1: Audio Preprocessing and Transcription
- Audio cleaning and normalization  
- Medical podcast transcription using ASR  

### Milestone 2: Topic Segmentation and Keyword Extraction
- Detection of topic boundaries  
- Medical keyword extraction  
- Initial summaries  

### Milestone 3: Frontend Integration and Visualization
- React UI for transcript and segment navigation  
- Timestamp-based audio playback  
- Keyword and summary display  

### Milestone 4: Documentation and Final Delivery
- Technical documentation  
- Final presentation and demo  

---

## Data and Privacy Considerations
- Raw audio and large files are not committed to GitHub  
- API keys are managed using environment variables  
- Only source code and configuration files are version-controlled  

---

## Future Enhancements
- Medical entity recognition (diseases, drugs)  
- Speaker diarization  
- Semantic medical search  
- Online deployment  
- Multi-language support  

---

## Intended Users
- Medical students  
- Healthcare professionals  
- Researchers  
- Podcast listeners  
- Medical educators  

---

## License
This project is licensed under the MIT License.

