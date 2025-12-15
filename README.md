# Automated-Podcast-Transcription-and-Topic-Segmentation
🎙️ AI Podcast Analytics & Transcription System

A comprehensive AI pipeline that automatically transcribes podcasts, segments them into topics, analyzes sentiment, and generates searchable keywords using state-of-the-art Natural Language Processing (NLP) models.

🚀 Project Overview

This project is an end-to-end solution for processing long-form audio content. Instead of listening to a full hour of audio, users can upload a podcast and instantly get:

Full Text Transcription (Speech-to-Text)

Smart Summaries (Abstractive)

Topic Segmentation (Chapters)

Emotional Timeline (Sentiment Graph)

Searchable Keywords (Tags)

The system features a Streamlit dashboard for easy interaction and visualization.

✨ Key Features

** automated Transcription:** Uses OpenAI Whisper to convert speech to text with high accuracy and precise timestamps.

Topic Segmentation: Mathematically detects topic shifts using TF-IDF and Cosine Similarity to break the podcast into distinct chapters.

Smart Summarization: Uses Hugging Face Transformers (DistilBART) to read the text and write concise summaries for each segment.

Sentiment Analysis: Tracks the emotional tone (Positive/Negative/Neutral) of the conversation over time using NLTK VADER.

Keyword Extraction: Identifies unique tags and themes specific to the episode.

Interactive Dashboard: A web-based UI to upload files, view graphs, and search through transcripts.

🛠️ Tech Stack & Models

Component

Technology / Library

Role

Frontend

Streamlit, Plotly

User Interface & Interactive Graphs

Audio Processing

Librosa, Soundfile

Resampling (16kHz), Mono Conversion

ASR (Speech-to-Text)

OpenAI Whisper (Base)

Converting Audio to Text

Summarization

DistilBART (Hugging Face)

Generating Abstractive Summaries

Sentiment

NLTK VADER

Lexicon-based Emotion Detection

NLP Logic

Scikit-Learn (TF-IDF)

Topic Segmentation & Keyword Extraction

📂 Project Structure

├── app.py                     # Main Streamlit Dashboard (Frontend)
├── podcast_backend.py         # Master Logic Engine (AI Pipeline)
├── download_kaggle_subset.py  # Script to fetch data from Kaggle
├── requirements.txt           # List of dependencies
├── README.md                  # Project Documentation
└── podcast_data/              # Data Storage (Created Automatically)
    ├── audio/                 # Raw MP3s
    ├── processed_audio/       # Cleaned 16kHz WAVs
    ├── transcripts/           # JSON Transcripts with timestamps
    ├── semantic_segments/     # Topic breakdowns
    ├── sentiment_data/        # Sentiment scores for graphing
    └── short_summary/         # AI-generated summaries


⚡ Installation & Setup

1. Clone the Repository

git clone [https://github.com/your-username/Automated-Podcast-Transcription.git](https://github.com/your-username/Automated-Podcast-Transcription.git)
cd Automated-Podcast-Transcription


2. Install Dependencies

Ensure you have Python 3.8+ installed.

pip install -r requirements.txt


Note: You also need FFmpeg installed on your system for audio processing.

3. Run the App

streamlit run app.py


The dashboard will open automatically in your browser at http://localhost:8501.

🧠 How It Works (The Pipeline)

When a user uploads a file, the system triggers the podcast_backend.py pipeline:

Preprocessing: The audio is converted to 16kHz Mono WAV. This is the native format for the Whisper model, ensuring speed and accuracy.

Transcription: Whisper processes the audio and outputs a JSON file containing text and start/end timestamps for every sentence.

NLP Analysis:

Sentiment: VADER scans every sentence to calculate a compound emotion score (-1 to +1).

Segmentation: We calculate the semantic similarity between sentences. If the similarity drops below a threshold (0.5), we mark a "Topic Change."

Summarization: Each identified topic segment is fed into the BART model to generate a summary.

Visualization: The Streamlit app reads the generated JSON files and renders the Sentiment Graph and searchable Transcript.

📊 Dataset

This project was developed and tested using a subset of the TED Talks dataset sourced from Kaggle.

Source: TED Talks Audio (Kaggle)

Size: The downloader script fetches ~2GB of diverse talks to ensure robust testing across different speakers and topics.

🤝 Acknowledgments

OpenAI for the Whisper model.

Hugging Face for the Transformers library.

Streamlit for the amazing dashboard framework.