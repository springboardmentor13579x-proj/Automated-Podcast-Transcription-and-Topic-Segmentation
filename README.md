# Automated Podcast Transcription and Topic Segmentation  
## An AI-Based System for HR Interviews, Corporate Meetings, and Spoken Content Analysis

------------------------------------------------------------------------

## 1. Overview

The **Automated Podcast Transcription and Topic Segmentation** project presents an end-to-end artificial intelligence system for processing long-form spoken content such as **HR interviews, corporate meetings, podcasts, webinars, and lectures**. The system automatically converts audio into text, identifies topic boundaries, segments conversations into coherent sections, and generates summaries, keywords, sentiment insights, and evaluation metrics.

The primary motivation of this work is to support **organizational communication analysis**, with a strong emphasis on **human resource (HR) interviews and professional meetings**, where efficient navigation, summarization, and structured evaluation of spoken content are critical. By integrating **speech recognition, natural language processing (NLP), audio feature analysis, and interactive visualization**, the system enables scalable analysis of otherwise unstructured audio data.

------------------------------------------------------------------------

## 2. Methodological Approach

The system is designed as a modular processing pipeline. Each stage can be independently developed, evaluated, and extended.

```
Audio Input → Preprocessing → ASR Transcription → Topic Segmentation
                   ↓
          Summarization & Keyword Extraction
                   ↓
      Evaluation, Visualization & Interactive UI
```

### 2.1 Audio Preprocessing
- Converts audio into a standardized format and sampling rate  
- Applies noise reduction and amplitude normalization  
- Ensures consistent input quality for downstream ASR models  

### 2.2 Automatic Speech Recognition (ASR)
- Uses **OpenAI Whisper** to transcribe audio into text  
- Supports conversational speech common in interviews and meetings  

### 2.3 Topic Segmentation
- Identifies topic boundaries using sentence structure and semantic cues  
- Divides transcripts into meaningful segments representing discussion units  

### 2.4 Summarization
- Produces concise, segment-level and document-level summaries  
- Removes filler content and non-informative phrases  

### 2.5 Keyword Extraction
- Extracts representative keywords related to HR and professional contexts  
- Filters stopwords and noise terms to avoid redundancy  

### 2.6 Sentiment and Emotion Analysis
- Applies sentiment scoring to each segment  
- Enables comparison between **interviewer and candidate sentiment trends**  

### 2.7 Transcription Evaluation
- Computes transcription quality metrics:
  - Word Error Rate (WER)  
  - Accuracy estimates  

### 2.8 Reporting and Visualization
- Interactive Streamlit dashboard for transcript review, keyword search, and timeline playback  
- Automated **PDF report generation** summarizing interview insights  

------------------------------------------------------------------------

## 3. Technology Stack

### Core Technologies
- Python 3.12  
- OpenAI Whisper (ASR)  
- Librosa, FFmpeg, PyDub (audio processing)  

### Natural Language Processing
- NLTK  
- Scikit-learn  
- HuggingFace Transformers (optional)  

### Visualization and Interface
- Streamlit  
- Plotly  
- Matplotlib  
- WordCloud  

### Evaluation and Reporting
- jiwer (WER metrics)  
- ReportLab (PDF report generation)  
- CSV and TXT outputs  

### Testing and CI
- PyTest (unit testing)  
- GitHub Actions (automated test pipeline)  

------------------------------------------------------------------------

## 4. System Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/springboardmentor13579x-proj/Automated-Podcast-Transcription-and-Topic-Segmentation.git
cd Automated-Podcast-Transcription-and-Topic-Segmentation
git checkout intern-vanshika
```

### Step 2: Create Virtual Environment (Optional)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Execute the Backend Pipeline

```bash
python -m src.main
```

### Step 5: Launch the Streamlit Dashboard

```bash
streamlit run src/ui_app.py
```

------------------------------------------------------------------------

## 5. Directory Structure

```
Automated-Podcast-Transcription-and-Topic-Segmentation/
│
├── src/
│   ├── preprocessing.py        # Audio cleaning, normalization
│   ├── transcription.py        # Whisper-based ASR
│   ├── segmentation.py         # Topic & speaker segmentation
│   ├── summarization.py        # AI / extractive summarization
│   ├── keyword_extraction.py   # TF-IDF keyword extraction
│   ├── evaluate_asr.py         # WER, CER, Accuracy evaluation
│   ├── core.py                 # Pipeline controller
│   ├── ui_app.py               # Streamlit enterprise dashboard
│   └── main.py                 # Backend pipeline entry point
│
├── audio_raw/                  # Original uploaded audio files
│
├── audio_processed/            # Cleaned & normalized audio for ASR
│
├── audio_ui/                   # UI session audio
│
├── transcripts/
│   ├── asr/                    # Raw ASR-generated transcripts
│   ├── final/                  # Cleaned / summarized transcripts
│   └── raw_reference/          # Ground-truth / manual transcripts for evaluation
│
├── segments/                   # Speaker-labeled and timestamped segments
│
├── docs/
│   ├── asr_evaluation.csv      # WER, CER, Accuracy values
│   ├── asr_evaluation_table.txt# Tabular ASR results
│   └── keywords.txt            # Extracted keywords
│   └── Documentation.pdf       # Final report (PDF)
│   └── HR_Interview_Analyzer_Presentation.pptx   #Presentation
│   
├── notebooks/                  # Experiments and analysis (optional)
│
├── tests/
│   └── test_core_functions.py  # Unit tests for backend modules
│
│── workflows/
│       └── tests.yml           # GitHub Actions CI for automated testing
│    
│
├── venv/                       # Python virtual environment (ignored by Git)
│
├── .gitattributes
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt

```

------------------------------------------------------------------------

## 6. Use Cases

### 6.1 HR Interviews (Primary Application)
- Automated transcription of interviews  
- Topic segmentation (skills, experience, behavioral, closing)  
- Keyword extraction for job-relevant terms  
- Sentiment and stress analysis  
- Executive summaries and structured PDF reports  
- Fair, scalable interview evaluation  

### 6.2 Corporate Meetings
- Agenda-based segmentation  
- Decision and outcome tracking  
- Sentiment trend analysis  

### 6.3 Podcasts and Webinars
- Topic chaptering  
- Keyword-based navigation  
- Content summarization  

### 6.4 Academic Lectures
- Modular segmentation  
- Key concept extraction  
- Learning support  

### 6.5 Accessibility
- Text-based access for hearing-impaired users  
- Inclusive communication  

------------------------------------------------------------------------

## 7. Testing and Validation

### Unit Testing

```bash
pytest
```

All core logic is validated:
- Segmentation  
- Summarization  
- Keyword extraction  
- Speaker and sentiment detection  

### Continuous Integration

GitHub Actions automatically executes tests on:
- Code pushes  
- Pull requests  

------------------------------------------------------------------------

## 8. Troubleshooting

**ASR Not Running Correctly**  
- Ensure Whisper and FFmpeg are installed  
- Verify audio exists in input directory  

**Segmentation Produces No Output**  
- Confirm transcripts exist in `transcripts/asr/`  

**Keyword Search Not Working**  
- Check text cleaning and stopword filtering  

**Evaluation Errors**  
- Reference transcripts must match ASR filenames  

**Large File Issues**  
- GitHub limits 100MB files  
- Use `.gitignore` or external storage  

------------------------------------------------------------------------

## 9. Limitations

- ASR accuracy may degrade for noisy or accented speech  
- Topic boundaries may miss subtle transitions  
- Summarization is extractive, not abstractive  
- Pipeline is batch-based (not real-time)  
- Large audio files are excluded from version control  

------------------------------------------------------------------------

## 10. Future Scope

- Multi-speaker diarization  
- Semantic search with embeddings  
- Advanced emotion & confidence detection  
- Abstractive summarization with transformers  
- Cloud deployment (Streamlit Cloud)  
- YouTube audio ingestion  

------------------------------------------------------------------------

## 11. References

1. Radford, A., et al. (2022). *Whisper: Robust Speech Recognition via Large-Scale Weak Supervision*. OpenAI.  
2. JiWER: https://github.com/jitsi/jiwer  
3. Hearst, M. (1997). *TextTiling*. Computational Linguistics.  
4. NLTK: https://www.nltk.org/  
5. HuggingFace: https://huggingface.co/  
6. Streamlit: https://streamlit.io/  
