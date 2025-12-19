# AUTOMATED PODCAST TRANSCRIPTION AND TOPIC SEGMENTATION

I. OVERVIEW

This project provides an end-to-end pipeline to automatically convert meeting or podcast audio into accurate text transcripts, followed by topic-based segmentation, summarization, and keyword extraction using natural language processing techniques. It is designed to efficiently process long-form audio and is suitable for real-world applications such as automated meeting minutes, podcast summarization, and interview analysis.

II. OBJECTIVES

- Convert audio recordings into accurate text transcripts  
- Segment long conversations into meaningful topics  
- Generate concise summaries  
- Extract important keywords for quick understanding  

III. KEY FEATURES 

- Automatic speech recognition using FastWhisper  
- Topic segmentation for long transcripts  
- Summary generation for segmented content  
- Keyword extraction using KeyBERT  
- Optimized for long meeting and podcast audio  

IV. DATASET

This project can be evaluated using the MeetingBank – Denver Audio Dataset.  
Source: HuggingFace – MeetingBank Audio Dataset.  
Real-world meeting recordings suitable for long-form transcription and topic segmentation tasks.

V. TECH STACK

- Python 3.9  
- FastWhisper – Speech-to-text  
- NLTK – Sentence tokenization  
- KeyBERT – Keyword extraction  
- HuggingFace Transformers  

VI. PROJECT STRUCTURE  

AUTOMATED-PODCAST-TRANSCRIPTION-AND-TOPIC-SEGMENTATION/  
│  
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
│       ├── UI_APP.PY  
│  
├── DOCS/  
├── TESTS/  
├── README.MD  
├── REQUIREMENTS.TXT  
└── LICENSE  

VII. HOW TO RUN THE PROJECT  

1. CREATE AND ACTIVATE VIRTUAL ENVIRONMENT  
python -m venv venv  
venv\Scripts\activate  

2. INSTALL DEPENDENCIES  
pip install -r requirements.txt  

3. PREPARE AUDIO FILES  
Supported formats: .mp3, .wav  
Place audio files in the AUDIO_RAW directory.  

Example:  
AUDIO_RAW/  
├── DENVER-1.MP3  
├── DENVER-2.MP3  

4. RUN TRANSCRIPTION  
python meeting_council.py  

Output directory:  
/TRANSCRIPTS/  

5. GENERATE SUMMARIES AND KEYWORDS  
python summary_generator.py  

Output directory:  
/SUMMARIES/  

VIII. SYSTEM ARCHITECTURE  

AUDIO FILES (.MP3 / .WAV)  
        │  
        ▼  
FASTWHISPER (ASR)  
        │  
        ▼  
TRANSCRIPT FILES  
        │  
        ▼  
TOPIC SEGMENTATION (NLTK)  
        │  
        ▼  
KEYWORD EXTRACTION (KEYBERT)  
        │  
        ▼  
SUMMARY GENERATION  
        │  
        ▼  
STRUCTURED OUTPUT (JSON / TXT)  

IX. USE CASES 

- Automated meeting minutes  
- Podcast summarization  
- Interview analysis  
- Research documentation  



