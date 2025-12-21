# Automated Podcast Transcription & Topic Segmentation

This project implements an AI-powered system to automatically transcribe podcast audio files and segment them into meaningful topical sections. It combines speech-to-text technology with natural language processing to help users navigate long audio content efficiently.

---

### Project Overview
Podcasts and long-form audio recordings often span several hours, making it difficult to locate specific discussions. This system addresses this problem by converting audio into text, identifying topic boundaries, extracting keywords, and presenting the results through an interactive user interface.

### Objectives
* **Convert** podcast audio into text using advanced speech-to-text models.
* **Preprocess** audio (VAD & normalization) for improved transcription quality.
* **Segment** transcripts based on semantic topic changes.
* **Extract** keywords and generate summaries for each topic segment.
* **Provide** a seamless user interface for browsing, searching, and playback.

---

### Project Structure
```text
Automated-Podcast-Transcription-and-Topic-Segmentation/
│── audio_raw/              # Storage for original uploaded audio files
│── audio_processed/        # Cleaned and normalized audio (WAV format)
│── data/                   # Data storage and CSV databases
│   ├── clean_project_dataset_sorted.csv  # Cleaned dataset sorted by key metrics
│   ├── clean_transcripts.csv             # Raw clean transcripts
│   ├── final_project_dataset_sorted.csv  # Final processed dataset ready for analysis
│   ├── final_search_index_fixed.csv      # Main search index used by the App
│── src/                    # Main source code modules
│   ├── preprocessing.py    # Audio cleaning, VAD, and normalization
│   ├── transcription.py    # Whisper AI speech-to-text pipeline
│   ├── segmentation.py     # Topic segmentation logic
│   ├── summarization.py    # Text summarization (BART/Transformers)
│   ├── keyword_extraction.py # Keyword extraction (YAKE/NLTK)
│   ├── ui_app.py           # Streamlit user interface (Main Entry Point)
│── tests/                  # Testing and Validation
│   ├── measure_accuracy.py # Tool to benchmark model performance
│── requirements.txt        # Python dependencies
│── README.md               # Project documentation
│── .env                    # Environment variables (Configuration)
```

### Technology Stack

**Programming Language**

* Python 3.9+

**Speech-to-Text**

* **OpenAI Whisper:** State-of-the-art automatic speech recognition (ASR).
* **Faster Whisper:** Optimized inference for faster processing.

**Audio Processing**

* **Silero VAD:** Voice Activity Detection to remove silence and background noise.
* **Librosa / SoundFile:** For audio signal processing and I/O.
* **PyTorch:** Deep learning framework backend.

**Natural Language Processing**

* **NLTK:** Tokenization and text processing.
* **Transformers (Hugging Face):** For abstractive summarization (BART/T5).
* **Scikit-learn:** For semantic analysis and clustering.
* **KeyBERT / YAKE:** For keyword extraction.

**Visualization and UI**

* **Streamlit:** Interactive web dashboard creation.
* **Pandas:** Data manipulation and management.

---

### Workflow

1. **Audio Ingestion:** Audio ingestion from local files or uploads via the interface.
2. **Audio Preprocessing:** Includes noise reduction and normalization using VAD.
3. **Transcription:** Transcription using speech-to-text models (Whisper).
4. **Topic Segmentation:** Segmentation based on semantic similarity and pauses.
5. **Keyword Extraction:** Keyword extraction and summarization for each segment.
6. **Visualization:** Visualization and browsing using a web interface.

---

### How to Run the Project

**1. Setup Environment**
Clone the repository and install the required dependencies:

```bash
git clone [https://github.com/springboardmentor13579x-proj/Automated-Podcast-Transcription-and-Topic-Segmentation.git](https://github.com/springboardmentor13579x-proj/Automated-Podcast-Transcription-and-Topic-Segmentation.git)
cd Automated-Podcast-Transcription-and-Topic-Segmentation
pip install -r requirements.txt

```

**2. Run the Application**
Launch the interactive dashboard using Streamlit:

```bash
streamlit run src/ui_app.py

```

**3. Usage**

* Open your browser to the local URL provided (usually `http://localhost:8501`).
* Upload an audio file to start the pipeline.
* Use the search interface to find specific topics and play audio segments.
