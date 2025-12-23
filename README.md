#  Automated Podcast Transcription and Topic Segmentation

## I. Overview

This project provides an end-to-end pipeline to automatically convert meeting or podcast audio into accurate text transcripts, followed by topic-based segmentation, summarization, and keyword extraction using natural language processing techniques. It is designed to efficiently process long-form audio and is suitable for real-world applications such as automated meeting minutes, podcast summarization, and interview analysis.

---

## II. Objectives

- Convert audio recordings into accurate text transcripts  
- Segment long conversations into meaningful topics  
- Generate concise summaries  
- Extract important keywords for quick understanding  

---

## III. Key Features

- Automatic speech recognition using **FastWhisper**
- Topic segmentation for long transcripts
- Summary generation for segmented content
- Keyword extraction using **KeyBERT**
- Optimized for long meeting and podcast audio

---

## IV. Dataset

This project can be evaluated using the **MeetingBank – Denver Audio Dataset**.

- **Source:** HuggingFace – MeetingBank Audio Dataset  
- Real-world meeting recordings suitable for long-form transcription and topic segmentation tasks

---

## V. Tech Stack

- Python 3.9  
- FastWhisper – Speech-to-text  
- NLTK – Sentence tokenization  
- KeyBERT – Keyword extraction  
- HuggingFace Transformers  

---

## VI. Project Structure

AUTOMATED-PODCAST-TRANSCRIPTION-AND-TOPIC-SEGMENTATION/  
├── PROJECT/  
│   ├── AUDIO_RAW/  
│   ├── AUDIO_PROCESSED/  
│   ├── TRANSCRIPTS/  
│   ├── SUMMARIES/  
│   ├── NOTEBOOKS/  
│   ├── SRC/  
│   │   ├── PREPROCESSING.PY  
│   │   ├── TRANSCRIPTION.PY  
│   │   ├── SUMMARIZATION.PY  
│   ├── UI_APP.PY  
├── DOCS/  
├── TESTS/  
├── README.MD  
├── REQUIREMENTS.TXT  
└── LICENSE  

---

## VII. How to Run the Project

### 1. Create and Activate Virtual Environment

Create a virtual environment using:  
`python -m venv venv`

Activate the environment (Windows):  
`venv\Scripts\activate`

---

### 2. Install Dependencies

Install all required packages using:  
`pip install -r requirements.txt`

---

### 3. Prepare Audio Files

- Supported formats: `.mp3`, `.wav`
- Place audio files inside the `AUDIO_RAW` directory

Example structure:

AUDIO_RAW/  
├── DENVER-1.MP3  
├── DENVER-2.MP3  

---

### 4. Run Transcription

Execute the transcription pipeline using:  
`python meeting_council.py`

Output files will be generated in the `TRANSCRIPTS/` directory.

---

### 5. Generate Summaries and Keywords

Run the summarization and keyword extraction script using:  
`python summary_generator.py`

Output files will be stored in the `SUMMARIES/` directory.

---

## VIII. System Architecture

AUDIO FILES (.MP3 / .WAV)  
       ↓  
FASTWHISPER (ASR)  
       ↓  
TRANSCRIPT FILES  
       ↓  
TOPIC SEGMENTATION (NLTK)  
       ↓  
KEYWORD EXTRACTION (KEYBERT)  
       ↓  
SUMMARY GENERATION  
       ↓  
STRUCTURED OUTPUT (JSON / TXT)

---

## IX. Use Cases

- Automated meeting minutes  
- Podcast summarization  
- Interview analysis  
- Research documentation  

---
  



