# Automated-Podcast-Transcription-and-Topic-Segmentation

Project Overview
The Automated Podcast Transcription & Topic Segmentation project aims to build an end-to-end AI system that can:
Convert podcast audio into accurate transcripts.
Detect topic boundaries automatically.
Segment the transcript into meaningful chapters.
Extract keywords and summaries for each topic.
Provide a UI to navigate the podcast episode by topics & timestamps.
Display segment-level visual analytics.

This project focuses on applying AI, Speech Processing, NLP, and ML engineering to create a practical real-world audio intelligence tool.

Project Objectives
1. Transcription (Speech-to-Text)
Convert long podcast audio files into text using ASR models.
Support noisy, multi-speaker, real-world audio.
Produce timestamps for each transcribed segment.
2. Topic Segmentation
Detect shifts in content and break the transcript into chapters.
Techniques Used:
TextTiling (Classic NLP)
Embedding similarity (BERT / Sentence Transformers)
Change-point detection methods
3. Summarization & Keyword Extraction
Generate per-topic:
Short abstractive summaries (DistilBART)
Keywords and keyphrases (KeyBERT)
Sentiment Analysis (TextBlob)
4. UI for Navigation
Show transcript & segment list.

System Architecture
Audio Input → Preprocessing → Transcription (ASR) → Transcript Cleaning
Embedding Model → Topic Segmentation → Segment Summaries & Keywords
Indexing → UI (Search, Playback, Visualization)
Allow clicking a segment → jump to timestamp.
Provide playback & visualizations (Sentiment Timeline, Keyword Clouds).

Tech Stack
Core
Python 3.9+
Whisper (OpenAI): State-of-the-art Automatic Speech Recognition.
Librosa, PyDub, ffmpeg: Audio processing and manipulation.
NLP
NLTK: TextTiling for basic segmentation.
HuggingFace Transformers: For summarization models.
Sentence Transformers: For semantic similarity (BERT).
KeyBERT: For keyword extraction.
TextBlob: For sentiment analysis.
Visualization & UI
Flask: Web server and backend logic.
Plotly: Interactive charts (Sentiment timeline, Keyword bubbles).
HTML/CSS/JS: Frontend interface.
Storage
JSON: Structured metadata storage for transcripts and segments.

Folder Structure
Podcast_Transcription1/
│
├── data/
│   ├── raw/                                # Source audio files
│   ├── transcripts/                         
│   ├── segmented_topics/    
│   └── final_output/        
│
├── src/
│   ├── transcriber.py                    # Whisper model wrapper
│   ├── data_loader.py                    # Audio loading, conversion (MP3->WAV), normalization
│   ├── semantic_segmenter.py             #BERT-based segmentation (Active)
│   ├── content_processor.py              #Summarization, Keyword, & Sentiment logic
│   ├── file_utils.py                     #Path management helpers
│   └── web_app/
│       ├── templates/
│       │   ├── index.html               # Homepage (Search & List)
│       │   └── player.html              # Player interface with Visualizations
│       └── app.py                       # Flask Server Entry Point
│
├── main.py                              # Pipeline Step 1: Run Transcription
├── run_segmentation.py                  # Pipeline Step 2: Run Topic Segmentation
├── run_processing.py                    # Pipeline Step 3: Run Summarization/Keywords
├── evaluate_accuracy.py                 # Evaluation: Calculate WER (Word Error Rate)
├── requirements.txt                     # List of dependencies
└── README.md                            # Project Documentation

Installation & Setup
Clone the Repository:cd Podcast_Transcription1
Create a Virtual Environment:python -m venv venv
source venv/bin/activate      # Mac/Linux
.\venv\Scripts\activate       # Windows
Install Dependencies:pip install flask transformers torch torchaudio sentence-transformers textblob keybert jiwer plotly pydub nltk scikit-learn openai-whisper
Install FFmpeg:Required for audio processing. Download from gyan.dev (Windows) or use brew install ffmpeg (Mac).
How to Run
Run the Pipeline
Execute the scripts in order to process your audio data:
Step 1: Transcribe (Audio → Text)
python main.py
Step 2: Segment (Text → Topics)
python run_segmentation.py
Step 3: Process (Topics → Summaries/Keywords)
python run_processing.py
Launch the Web UI
Start the Flask server to explore the results:
python src/web_app/app.py
Open your browser at: http://127.0.0.1:5000
