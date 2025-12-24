

1) Project Overview

This project focuses on automated podcast/audio transcription using AI-based speech recognition and natural language processing techniques. The system converts raw audio into text, evaluates transcription quality, segments text into meaningful units, and extracts important keywords for better content understanding.


---

2)  Use Case

Podcast transcription

Audiobook conversion

Interview transcription

Lecture notes generation

Accessibility for hearing-impaired users

Content indexing and search



---

3)  Benefits

Automates manual transcription

Saves time and cost

High transcription accuracy using AI

Enables text analysis (keywords, segmentation)

Scalable for large audio datasets

Works offline (no cloud dependency)



---

4)  Project Objectives

Convert audio files into accurate text

Evaluate transcription quality using WER & CER

Segment long transcripts into sentences

Extract meaningful keywords from transcripts

Build an end-to-end automated transcription pipeline



---

5)   System Architecture

Audio Files (LibriVox)
        ↓
Audio Preprocessing (FFmpeg)
        ↓
Speech-to-Text Engine (Whisper ASR)
        ↓
Predicted Transcripts
        ↓
Ground Truth Text (Project Gutenberg)
        ↓
Evaluation (WER / CER using jiwer)
        ↓
Sentence Segmentation (NLTK)
        ↓
Keyword Extraction (TF-IDF)
        ↓
Final Text Analytics Output


---

6)  Tech Stack

Layer	Technology

Programming Language	Python 3.9
Speech Recognition	OpenAI Whisper
Audio Processing	FFmpeg
Text Processing	NLTK
Evaluation Metrics	jiwer
Keyword Extraction	Scikit-learn (TF-IDF)
Data Format	WAV, MP3, TXT, CSV
OS	Windows



---

7) Project Folder Structure

project/
│
├── data/
│   └── audio/
│
├── ground_truth/
│   └── pg1661_clean.txt
│
├── transcripts/
│   └── predicted/
│       └── *.txt
│
├── segmented/
│   └── *_segments.txt
│
├── keywords/
│   └── *_keywords.txt
│
├── script/
│   ├── transcribe.py
│   ├── evaluate_all.py
│   ├── segment_text.py
│   └── extract_keywords.py
│
├── evaluation_report.csv
└── README.md


