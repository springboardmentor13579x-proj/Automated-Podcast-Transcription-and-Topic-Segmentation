
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

### 4. UI for Navigation
- Display transcripts with topic-wise segmentation  
- Enable click-to-jump using timestamps  
- Provide audio playback and visual insights  

---

## System Architecture

```

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
UI (Search, Playback, Visualization)

```

---

## Tech Stack

### Core Technologies
- Python 3.9+
- Whisper (OpenAI) / Faster-Whisper
- Librosa, PyDub, FFmpeg

### NLP and Machine Learning
- NLTK
- SpaCy
- HuggingFace Transformers
- Sentence Transformers
- KeyBERT / YAKE / RAKE

### Visualization and UI
- Streamlit / Flask
- Plotly
- Matplotlib

### Storage
- JSON / CSV for metadata
- SQLite (optional)
- FAISS / Vector Database (optional)

---

## Project Folder Structure

```
Automated-Podcast-Transcription-and-Topic-Segmentation/
│
├── frontend/                 # React frontend (UI)
│   ├── src/
│   ├── public/
│   ├── package.json
│
├── src/                      # Backend processing logic
│   ├── preprocessing.py
│   ├── transcription.py
│   ├── segmentation.py
│   ├── summarization.py
│   ├── evaluation_summary.py
│
├── notebooks/                # Experiments and analysis
├── Inference/                # Generated outputs (not committed fully)
├── docs/
├── tests/
│
├── README.md
├── requirements.txt
├── LICENSE


```

---

## Milestone-wise Implementation

### Milestone 1: Audio Preprocessing and Transcription
- Audio cleaning and normalization  
- Medical podcast transcription using ASR  

### Milestone 2: Topic Segmentation and Keyword Extraction
- Detection of topic boundaries  
- Medical keyword extraction  
- Initial summaries  

### Milestone 3: Visualization and Enhancements
- Topic timelines  
- Keyword clouds  
- Improved summaries  

### Milestone 4: Documentation and Final Delivery
- Technical documentation  
- Final presentation and demo  

---

## Data and Privacy Considerations
- Raw audio and sensitive data are not committed to GitHub  
- API keys are stored securely using `.env`  
- Only source code and metadata are version-controlled  

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


