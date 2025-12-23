
---

# Automated Medical Podcast Transcription and Topic Segmentation

## Project Overview

Medical podcasts contain valuable discussions on diseases, treatments, research findings, and clinical experiences. However, these podcasts are often long and difficult to navigate.

This project aims to build an AI-powered system that automatically transcribes medical podcast audio, detects topic boundaries, and segments the content into meaningful medical topics with summaries and keywords.

The system helps students, researchers, and healthcare professionals quickly access relevant medical information without listening to the entire podcast episode.

---

## Use Case (Medical Domain)

This project is designed specifically for medical podcasts, including:

* Clinical discussions
* Disease awareness talks
* Medical education podcasts
* Expert interviews and panel discussions
* Public health awareness programs

### Benefits

* Quickly locate discussions about specific diseases or treatments
* Navigate podcasts using topic-wise chapters
* Understand content through summaries and keywords
* Save time for medical students and professionals

---

## Project Objectives

### 1. Transcription (Speech-to-Text)

* Convert long medical podcast audio into text using ASR models
* Handle noisy, real-world medical audio
* Generate timestamps for each transcribed segment

### 2. Topic Segmentation

* Detect topic shifts in medical discussions
* Segment transcripts into meaningful medical chapters
* Use NLP techniques such as:

  * TextTiling
  * Embedding similarity (Sentence Transformers / BERT)
  * Change-point detection methods

### 3. Summarization and Keyword Extraction

* Generate short summaries for each topic segment
* Extract important medical keywords

### 4. Frontend UI for Navigation

* Topic-wise transcript navigation
* Timestamp-based audio playback
* Visualization of summaries and keywords

---

## System Architecture Flow

```text
+---------------------+
|     Audio Input     |
+---------------------+
           |
           v
+---------------------+
| Audio Preprocessing |
+---------------------+
           |
           v
+------------------------------+
| Medical Speech-to-Text (ASR) |
+------------------------------+
           |
           v
+---------------------+
| Transcript Cleaning |
+---------------------+
           |
           v
+---------------------+
|  Embedding Model    |
+---------------------+
           |
           v
+---------------------+
|  Topic Segmentation |
+---------------------+
           |
           v
+--------------------------------+
| Medical Summaries & Keywords   |
+--------------------------------+
           |
           v
+---------------------+
|      Indexing       |
+---------------------+
           |
           v
+---------------------------------------------+
| Frontend UI                                 |
| (Search, Playback, Visualization)           |
+---------------------------------------------+
```

---

## Tech Stack

### Backend

* Python 3.9+
* Flask
* Whisper (OpenAI) / Faster-Whisper
* Librosa, PyDub, FFmpeg

### NLP and Machine Learning

* NLTK
* SpaCy
* HuggingFace Transformers
* Sentence Transformers
* KeyBERT / YAKE / RAKE

### Frontend

* React.js
* HTML, CSS, JavaScript
* REST API integration

### Visualization

* Plotly
* Matplotlib

### Storage

* JSON / CSV
* SQLite (optional)
* FAISS / Vector Database (optional)

---

## Project Structure

```text
Automated-Medical-Podcast-Transcription-and-Topic-Segmentation/
│
├── Data/                               # Audio datasets (not committed)
│   ├── audio_raw/
│   ├── audio_processed/
│
├── src/                                # Backend processing logic
│   ├── preprocessing.py               # Audio preprocessing
│   ├── transcription.py               # ASR transcription
│   ├── segmentation.py                # Topic segmentation
│   ├── summarization.py               # Summaries
│   ├── keyword_extraction.py           # Keywords
│   └── evaluation_summary.py           # Evaluation
│
├── ui_app/                             # Frontend (React)
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── App.js
│   │   ├── api.js
│   │   └── index.js
│   ├── package.json
│   └── .gitignore
│
├── Inference/                          # Outputs (not committed)
│   ├── transcripts/
│   ├── segments/
│   └── keywords/
│
├── notebooks/                          # Experiments
├── docs/                               # Documentation
├── tests/                              # Test cases
│
├── README.md
├── requirements.txt
├── LICENSE
└── .env.example
```

---

## Milestone-wise Implementation

### Milestone 1: Audio Preprocessing & Transcription

* Audio normalization
* ASR-based transcription

### Milestone 2: Topic Segmentation & Keywords

* Topic boundary detection
* Keyword extraction

### Milestone 3: Frontend Integration

* React-based UI
* Timestamp navigation

### Milestone 4: Documentation & Final Delivery

* Technical documentation
* Final demo

---

## Data and Privacy Considerations

* Raw audio not committed
* Environment variables for API keys
* Only source code is version-controlled

---

## Future Enhancements

* Medical entity recognition
* Speaker diarization
* Semantic search
* Multi-language support

---

## Intended Users

* Medical students
* Healthcare professionals
* Researchers
* Medical educators

---

## License

This project is licensed under the **MIT License**.

---
