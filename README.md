# Automated-Podcast-Transcription-and-Topic-Segmentation

*A Springboard Internship Program Project*


## **Project Overview**

The **Automated Podcast Transcription & Topic Segmentation** project aims to build an end-to-end AI system that can:

* Convert podcast audio into accurate transcripts
* Detect topic boundaries automatically
* Segment the transcript into meaningful chapters
* Extract keywords and summaries for each topic
* Provide a UI to navigate the podcast episode by topics & timestamps
* Display segment-level visual analytics

This project focuses on applying **AI, Speech Processing, NLP, and ML engineering** to create a practical real-world audio intelligence tool.  

______________________________________________________________________________________________________________________________________
_______________________________________

## Key Features

- **Automatic Audio Transcription:** High-quality speech-to-text with Whisper, supports long audio files  
- **Topic Segmentation:** Sentence-level segmentation with NLTK & TF-IDF  
- **Keyword Extraction & Summarization:** Topic-focused keywords and concise summaries  
- **Global Transcript Search:** Search across all segments  
- **Sentiment Analysis:** Positive, neutral, negative sentiment per segment  
- **Interactive UI:** Streamlit-based, easy navigation between segments
   __________________________________________________________________________________________________________________________________
   ___________________________________

  ##  Tech Stack

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
  ____________________________________________________________________________________________________________________________________
  _________________________________

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

______________________________________________________________________________________________________________________________________
______________________________

    ## **System Architecture**

```
Audio Input → Preprocessing → Transcription (ASR) → Transcript Cleaning
             ↓
    Embedding Model → Topic Segmentation → Segment Summaries & Keywords
             ↓
          Indexing → UI (Search, Playback, Visualization)

_____________________________________________________________________________________________________________________________________-____________________________________

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
______________________________________________________________________________________________________________________________________
____________________________________
                                            
# **License**

This project uses the **MIT License**.
Create a `LICENSE` file from GitHub’s license picker.
