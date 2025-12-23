
# Automated Medical Podcast Transcription and Topic Segmentation 

## Project Overview

Medical podcasts contain rich and valuable discussions related to diseases, treatments, clinical practices, medical research, and healthcare awareness. However, these podcasts are usually long in duration, making it difficult for listeners to quickly find relevant information.

This project presents an **AI-based system** that automatically **transcribes medical podcast audio**, **detects topic boundaries**, and **segments the content into meaningful medical topics** along with **summaries and keywords**.

The system processes **4–5 medical podcast audio files** and divides each transcript into approximately **8 meaningful topic segments**, helping users easily navigate and understand the content without listening to the full podcast.

---

## Use Case (Medical Domain)

The project is designed specifically for **medical audio content**, including:

* Clinical discussions
* Disease awareness programs
* Medical education podcasts
* Expert interviews and panel discussions
* Public health awareness talks

---

## Benefits

* Quickly locate discussions about specific diseases or treatments
* Navigate podcasts using topic-wise segmentation
* Understand content through summaries and keywords
* Save time for medical students and healthcare professionals

---

## Project Objectives

### 1. Transcription (Speech-to-Text)

* Convert long medical podcast audio into text using ASR models
* Process **4–5 audio recordings**
* Handle noisy and real-world medical audio
* Generate timestamps for transcribed segments

### 2. Topic Segmentation

* Detect topic changes in medical discussions
* Segment transcripts into approximately **8 meaningful medical topics**
* Apply NLP techniques such as:

  * Text similarity using embeddings
  * Sentence Transformers / BERT-based embeddings
  * Change-point detection approaches

### 3. Summarization and Keyword Extraction

For each topic segment:

* Generate short, meaningful summaries
* Create bullet-point notes
* Extract important medical keywords

### 4. Frontend UI for Navigation

* Display transcripts with topic-wise segmentation
* Enable click-to-jump using timestamps
* Provide audio playback controls
* Show summaries and extracted keywords
* Communicate with backend APIs

---

## System Architecture

**Audio Input**
↓
**Audio Preprocessing**
↓
**Medical Speech-to-Text (ASR)**
↓
**Transcript Cleaning**
↓
**Embedding Generation**
↓
**Topic Segmentation**
↓
**Summarization & Keyword Extraction**
↓
**Indexed Results**
↓
**Frontend UI (Search, Playback, Visualization)**

---

## Tech Stack

### Backend

* Python 3.9+
* Flask
* Whisper / Faster-Whisper
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

* JSON / CSV for metadata
* SQLite (optional)
* FAISS / Vector Database (optional)

---

## Project Structure

```
Automated-Medical-Podcast-Transcription/
│
├── Data/                           # Audio datasets (not committed)
│   ├── audio_raw/                 # Original podcast audio files
│   └── audio_processed/           # Cleaned audio files
│
├── src/                            # Backend processing logic
│   ├── preprocessing.py           # Audio preprocessing
│   ├── transcription.py           # Speech-to-text transcription
│   ├── segmentation.py            # Topic segmentation logic
│   ├── summarization.py           # Segment summarization
│   ├── keyword_extraction.py      # Medical keyword extraction
│   └── evaluation_summary.py      # Result evaluation
│
├── frontend/                       # React frontend UI
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Home.jsx
│   │   │   ├── Segments.jsx
│   │   │   ├── Transcription.jsx
│   │   │   ├── TopicSearch.jsx
│   │   │   └── Downloads.jsx
│   │   ├── App.js
│   │   ├── api.js
│   │   └── index.js
│   ├── package.json
│   └── package-lock.json
│
├── Inference/                      # Generated outputs (not committed)
│   ├── transcripts/
│   ├── segments/
│   └── keywords/
│
├── notebooks/                      # Experiments and analysis
├── docs/                           # Documentation
├── tests/                          # Test cases
├── README.md
├── requirements.txt
├── LICENSE
└── .env.example
```

---

## Milestone-wise Implementation

### Milestone 1: Audio Preprocessing and Transcription

* Audio cleaning and normalization
* Transcription of **4–5 medical podcast audio files**

### Milestone 2: Topic Segmentation and Keyword Extraction

* Detection of topic boundaries
* Segmentation into **approximately 8 topics**
* Medical keyword extraction
* Initial summaries

### Milestone 3: Frontend Integration and Visualization

* React UI for transcript navigation
* Timestamp-based audio playback
* Summary and keyword visualization

### Milestone 4: Documentation and Final Delivery

* Complete technical documentation
* Final project presentation and demo

---

## Data and Privacy Considerations

* Raw audio files are not committed to GitHub
* API keys are stored using environment variables
* Only source code and configuration files are version-controlled

---

## Future Enhancements

* Medical entity recognition (diseases, drugs, symptoms)
* Speaker diarization
* Semantic medical search
* Online deployment
* Multi-language podcast support

---

## Intended Users

* Medical students
* Healthcare professionals
* Researchers
* Podcast listeners
* Medical educators

---

## License

This project is licensed under the **MIT License**.

---

 