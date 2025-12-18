# Automated Podcast Transcription and Topic Segmentation

This project implements an AI-powered system to automatically transcribe podcast audio files and segment them into meaningful topical sections. It combines speech-to-text technology with natural language processing techniques to help users navigate long audio content efficiently.

---

## Project Overview

Podcasts and long-form audio recordings often span several hours, making it difficult to locate specific discussions. This system addresses the problem by converting audio into text, identifying topic boundaries, extracting keywords, and presenting the results through a simple user interface.

---

## Objectives

- Convert podcast audio into text using speech-to-text models  
- Preprocess audio for improved transcription quality  
- Segment transcripts based on topic changes  
- Extract keywords for each topic segment  
- Provide a user interface for browsing and searching content  

---

## Project Structure

project/  
│── audio_raw/            Original podcast audio files  
│── audio_processed/      Cleaned and normalized audio  
│── transcripts/          Generated transcripts (TXT/JSON)  
│── segments/             Topic-wise segmented text  
│── notebooks/            Experiments and analysis notebooks  
│── src/  
│   ├── preprocessing.py        Audio cleaning and normalization  
│   ├── transcription.py        Speech-to-text pipeline  
│   ├── segmentation.py         Topic segmentation logic  
│   ├── summarization.py        Segment summarization  
│   ├── keyword_extraction.py   Keyword extraction  
│   ├── ui_app.py               Streamlit user interface  
│── docs/                 Documentation and reports  
│── tests/                Unit and integration tests  
│── README.md              Project documentation  
│── requirements.txt       Python dependencies  
│── LICENSE                License file  
│── .env                   Environment variables  

---

## Technology Stack

### Programming Language
- Python 3.9 or higher

### Speech-to-Text
- OpenAI Whisper / Faster Whisper  
- Google Speech-to-Text (optional)

### Audio Processing
- Librosa  
- PyDub  
- ffmpeg  

### Natural Language Processing
- NLTK  
- SpaCy  
- HuggingFace Transformers  
- Sentence Transformers  

### Keyword Extraction
- YAKE  
- RAKE  
- KeyBERT  

### Visualization and UI
- Streamlit or Flask  
- Plotly  
- Matplotlib  

### Storage
- JSON, CSV, SQLite  
- FAISS or vector databases (optional)

---

## Dataset

- Spotify Podcast Dataset  
- Podcast Transcripts Dataset (Kaggle)  
- Custom podcast audio recordings  

---

## Workflow

1. Audio ingestion from local files or uploads  
2. Audio preprocessing including noise reduction and normalization  
3. Transcription using speech-to-text models  
4. Topic segmentation based on semantic similarity  
5. Keyword extraction for each segment  
6. Visualization and browsing using a web interface  

---

## How to Run the Project

Activate the virtual environment:

```bash
source venv/bin/activate

Run the transcription pipeline:

python src/transcription.py


Run the Streamlit user interface:

streamlit run src/ui_app.py
```