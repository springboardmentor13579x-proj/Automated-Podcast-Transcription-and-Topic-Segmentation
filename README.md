<!-- README UPDATED SUCCESSFULLY -->
# Automated-Podcast-Transcription-and-Topic-Segmentation
Automated Podcast Transcription and Topic Segmentation

Overview:

This project provides an end-to-end pipeline to automatically convert meeting or podcast audio into text transcripts, then generate topic-based summaries and keyword extraction using NLP techniques. It is designed to work efficiently with long-form meeting audio and is suitable for real-world applications such as meeting minutes and podcast analysis.

Objectives:

Convert audio recordings into accurate text
Segment long conversations into meaningful topics
Generate concise summaries
Extract important keywords for quick understanding

Key Features:

Automatic Speech Recognition using FastWhisper
Topic segmentation for long transcripts
Summary generation
Keyword extraction using KeyBERT
Optimized for long meeting audio
Clean separation of code and generated outputs

Dataset:

This project can be evaluated using the MeetingBank – Denver Audio Dataset.

Source: HuggingFace – MeetingBank Audio

Real-world meeting recordings ,Suitable for long-form transcription tasks

Tech Stack:

Python 3.9
FastWhisper– Speech-to-text
NLTK – Sentence tokenization
KeyBERT – Keyword extraction
HuggingFace Transformers**


📁Project Structure:

Automated-Podcast-Transcription-and-Topic-Segmentation/
project/
│── audio_raw/
│── audio_processed/
│── transcripts/
│── segments/
│── notebooks/
│── src/
│   ├── preprocessing.py
│   ├── transcription.py
│   ├── segmentation.py
│   ├── summarization.py
│   ├── keyword_extraction.py
│   ├── ui_app.py
│── docs/
│── tests/
│── README.md
│── requirements.txt
│── LICENSE

How to Run the Project:

1️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Prepare Audio Files

Supported formats: .mp3, .wav
Place files in the input directory

Example:
Fastwhispermodel_work/
└── audio/
    ├── Denver-1.mp3
    ├── Denver-2.mp3



4️⃣ Run Transcription
python meeting_council.py

Output:
/transcripts/

5️⃣ Generate Summaries & Keywords
python summary_generator.py

Output:
/summaries/

System Architecture:

Audio Files (.mp3 / .wav)
        │
        ▼
FastWhisper (ASR)
        │
        ▼
Transcript Files
        │
        ▼
Topic Segmentation (NLTK)
        │
        ▼
Keyword Extraction (KeyBERT)
        │
        ▼
Summary Generation
        │
        ▼
Structured Output (JSON / TXT)

Use Cases:

Automated meeting minutes

Podcast summarization

Interview analysis

Research documentation
