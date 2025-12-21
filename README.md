# Automated-Podcast-Transcription-and-Topic-Segmentation
## Project Statement
The goal of this project is to develop an AI-powered system that automatically transcribes
podcast audio recordings and segments them into distinct topical sections. The system
leverages speech-to-text technology and natural language processing to help users navigate
podcast content efficiently without listening to entire episodes.

## Outcomes
- Understanding speech recognition techniques for converting audio to text
- Implementing NLP methods for topic segmentation and keyword extraction
- Building an end-to-end pipeline for audio ingestion, transcription, and segmentation
- Generating topic-wise keywords and summaries
- Preparing structured documentation of methodology and results

## Project Status
**Completed up to Milestone 2 (Topic Segmentation and Keyword Extraction)**

## Dataset
The project uses Indian languages audio podcasts for transcription and topic segmentation.  
Open datasets such as the Spotify Podcast Dataset and Podcast Transcripts Dataset from Kaggle are also used.  
Due to large file sizes, datasets are not included in this repository.

**Download Link for Raw and Clean Dataset Files:**  
[Google Drive Folder]https://drive.google.com/drive/folders/12CVyb0ZlP5LsRnAFRkbii5Cl-SkjiTuM?lfhs=2

## Implemented Modules

### 1. Dataset Acquisition and Exploration
- Collected podcast audio files and available transcripts
- Analyzed audio length, quality, and transcript formats

### 2. Audio Preprocessing and Speech-to-Text
- Performed audio cleaning and normalization
- Applied automatic speech recognition (ASR) models to generate transcripts
- Evaluated transcription quality using WER and CER metrics

### 3. Topic Segmentation and Identification (Milestone 2)
- Segmented transcripts into meaningful topic sections
- Extracted keywords for each topic
- Generated topic-wise summaries

## Folder Structure
ML/
├── Automated-Podcast-Transcription/
├── cleaned_audio/
├── Indian_Languages_Audio_Dataset/
├── topic_outputs/
│   ├── keywords/
│   ├── summaries/
│   ├── combined_transcript.txt
│   ├── topic_0.txt
│   ├── topic_1.txt
│   ├── topic_2.txt
│   ├── topic_3.txt
│   └── topic_4.txt
├── transcripts/
│   └── asr_transcripts.txt
├── Project.ipynb
├── wer_cer_results.csv
├── requirements.txt
├── README.md
└── .gitattributes

## Technologies Used
### Audio Processing
- LibROSA
- PyDub

### Speech-to-Text
- Whisper

### NLP
- NLTK(BERT)
- SpaCy
- Hugging Face Transformers

### Machine Learning
- Scikit-learn
- PyTorch

## Output
- Automatically generated transcripts
- Topic-wise segmentation of podcast content
- Extracted keywords and summaries for each segment
- Transcription evaluation metrics (WER, CER)

## Future Work
- Build a user interface for topic navigation
- Add interactive visualizations for segment timelines
- Improve segmentation accuracy using transformer-based models
- Deploy the system as a web application

## How to Run
1. Install dependencies:
   pip install -r requirements.txt
2. Open and execute:
   Project.ipynb
