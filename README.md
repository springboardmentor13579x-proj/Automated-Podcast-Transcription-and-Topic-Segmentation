
# Automated-Podcast-Transcription-and-Topic-Segmentation

## **Project Overview**

The **Automated Podcast Transcription & Topic Segmentation** project aims to build an end-to-end AI system that can:

* Convert podcast audio into accurate transcripts
* Detect topic boundaries automatically
* Segment the transcript into meaningful chapters
* Extract keywords and summaries for each topic
* Provide a UI to navigate the podcast episode by topics & timestamps
* Display segment-level visual analytics

This project focuses on applying **AI, Speech Processing, NLP, and ML engineering** to create a practical real-world audio intelligence tool.


##  **Project Objectives**

### 1. **Transcription (Speech-to-Text)**

* Convert long podcast audio files into text using ASR models
* Support noisy, multi-speaker, real-world audio
* Produce timestamps for each transcribed segment

### 2. **Topic Segmentation**

* Detect shifts in content and break the transcript into chapters
* Use NLP techniques such as:

  * TextTiling
  * Embedding similarity (BERT / Sentence Transformers)
  * Change-point detection methods

### 3. **Summarization & Keyword Extraction**

* Generate per-topic:

  * Short summaries
  * Bullet-point notes
  * Keywords

### 4. **UI for Navigation**

* Show transcript & segment list
* Allow clicking a segment → jump to timestamp
* Provide playback & visualizations


## **System Architecture**

```
Audio Input → Preprocessing → Transcription (ASR) → Transcript Cleaning
             ↓
    Embedding Model → Topic Segmentation → Segment Summaries & Keywords
             ↓
          Indexing → UI (Search, Playback, Visualization)
```

## Key Features

- **Automatic Audio Transcription:** High-quality speech-to-text with Whisper, supports long audio files  
- **Topic Segmentation:** Sentence-level segmentation with NLTK & TF-IDF  
- **Keyword Extraction & Summarization:** Topic-focused keywords and concise summaries  
- **Global Transcript Search:** Search across all segments  
- **Sentiment Analysis:** Positive, neutral, negative sentiment per segment  
- **Interactive UI:** Streamlit-based, easy navigation between segments

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
```
______________________________________________________________________________________________________________________________________

## **Testing**

This project uses **pytest** to ensure that each module works correctly and the full pipeline runs smoothly.  

### 1. **Unit Testing with pytest**
- Test files included:
  - `test_preprocessing.py` → tests audio preprocessing functions
  - `test_transcript.py` → tests transcription functionality using Whisper
  - `test_segment_keySearch.py` → tests topic segmentation, keyword extraction, and summarization
- Run all tests with:
  ```bash
  pytest

### 2. **Integration Testing**

Verified end-to-end pipeline:

```Audio Upload → Preprocessing → Transcription → Topic Segmentation → Keyword Extraction → Visualization```


Checked segment timestamps match audio playback in the UI.

### 3. **Manual Testing**

Streamlit UI tested for:

- Uploading audio files

- Navigating between segments

- Searching keywords

- Viewing summaries and sentiment per segment

- Verified correct display for long podcast episodes (~1–2 hours).

 ### 4. **Performance & Accuracy Validation**

- Transcription accuracy checked on different audio qualities.

- Topic segmentation manually validated against natural topic changes.

- Keywords and summaries reviewed for relevance.

- Future improvements: add automated benchmark tests for transcription accuracy and segmentation quality.

  ## References

1. OpenAI Whisper — https://github.com/openai/whisper  
2. Librosa Audio Processing Library — https://librosa.org/doc/main/index.html  
3. NLTK (Natural Language Toolkit) — https://www.nltk.org/  
4. Scikit‑learn Documentation — https://scikit-learn.org/  
5. Streamlit Documentation — https://docs.streamlit.io/  
6. WordCloud Library — https://github.com/amueller/word_cloud  
7. Matplotlib Documentation — https://matplotlib.org/stable/  
8. Speech and Language Processing (Jurafsky & Martin) — https://web.stanford.edu/~jurafsky/slp3/

                                            
# **License**

This project uses the **MIT License**.


