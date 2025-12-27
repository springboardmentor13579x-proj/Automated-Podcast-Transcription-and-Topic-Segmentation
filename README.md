# Automated-Podcast-Transcription-and-Topic-Segmentation
An end-to-end AI-based audio intelligence system that transcribes long-form audio (medical podcasts, interviews, lectures), performs topic segmentation, keyword extraction, sentiment analysis, and provides a searchable, timestamped UI.

Designed for scalability, clarity, and real-world AI workflows.
____________________________________________________________________________________________________________________________________________________________________
## Project Overview

Medical podcasts contain discussions on diseases, treatments, and research. Long durations make it hard to access specific content quickly.

This project solves that by:

- Converting podcast audio into accurate text using OpenAI Whisper  
- Segmenting transcripts into topic-based sections  
- Extracting keywords and summaries  
- Performing **sentiment analysis**  
- Providing a searchable and interactive Streamlit interface  

____________________________________________________________________________________________________________________________________________________________________
## Key Features

- **Automatic Audio Transcription:** High-quality speech-to-text with Whisper, supports long audio files  
- **Topic Segmentation:** Sentence-level segmentation with NLTK & TF-IDF  
- **Keyword Extraction & Summarization:** Topic-focused keywords and concise summaries  
- **Global Transcript Search:** Search across all segments  
- **Sentiment Analysis:** Positive, neutral, negative sentiment per segment  
- **Interactive UI:** Streamlit-based, easy navigation between segments
   __________________________________________________________________________________________________________________________________________________________________

  ## 🛠️ Tech Stack

- **Programming Language:** Python  
- **Audio Processing:** LibROSA, PyDub  
- **Speech-to-Text (ASR):** OpenAI Whisper  
- **Natural Language Processing:** NLTK, SpaCy, Hugging Face Transformers  
- **Topic Segmentation:** TextTiling, BERT / GPT  
- **Keyword Extraction:** TF-IDF  
- **Sentiment Analysis:** VADER, Transformer Models  
- **Data Storage:** JSON  
- **Visualization & UI:** Streamlit, Plotly  
- **Version Control:** Git, GitHub
  ___________________________________________________________________________________________________________________________________________________________________

  ##  Workflow / Pipeline

1. **Audio Input:**  
   - Upload audio files in formats like MP3, WAV, etc.  

2. **Audio Preprocessing:**  
   - Clean audio, remove noise, split into manageable segments using LibROSA/PyDub.  

3. **Speech-to-Text (ASR):**  
   - Convert audio segments into text using OpenAI Whisper.  

4. **Text Processing:**  
   - Clean and normalize transcripts.  
   - Tokenization, lemmatization using NLTK or SpaCy.  

5. **Topic Segmentation:**  
   - Break transcripts into topics using TextTiling or BERT/GPT embeddings.  

6. **Keyword Extraction:**  
   - Identify important keywords from each segment using TF-IDF.  

7. **Sentiment Analysis:**  
   - Analyze sentiment for each segment using VADER or transformer-based models.  

8. **Data Storage:**  
   - Store transcripts, keywords, and sentiment analysis in JSON files.  

9. **Visualization & UI:**  
   - Display results, transcripts, and keyword search using Streamlit and interactive plots with Plotly.  

10. **Version Control:**  
    - Track all code and updates using Git and GitHub
# Project Structure

```text
AI_PODCAST_TRANSCRIPT/
├── audio_raw/                         # Original podcast audio files
├── audio_processed/                   # Preprocessed audio chunks
├── audio_segment_keySearch_summary/   # Topic segments, keywords, summaries
├── data/                              # Additional datasets (ignored in git)
├── env/                               # Virtual environment (ignored in git)
├── segment_keySearch_summary/         # Older summary folder (ignored)
├── src/                               # Core source code
│   ├── preprocessing.py               # Audio preprocessing logic
│   ├── transcript.py                  # Whisper transcription module
│   └── segment_keySearch.py           # Topic segmentation & keyword extraction
├── transcripts/                       # Generated transcripts
├── README.md                           # Project documentation
└── .gitignore                          # Git ignore rules
___________________________________________________________________________________________________________________________________________________________________
                                            




