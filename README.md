# Automated Podcast Transcription & Topic Segmentation

A comprehensive system to transcribe podcast audio, segment it by topic, and provide an interactive navigation UI.

## Features
- **Transcription**: Powered by OpenAI Whisper.
- **Segmentation**: Semantic topic detection using Sentence Transformers.
- **Intelligence**: Auto-generated summaries and keyword extraction for each topic.
- **Interactive UI**: Navigate through long audio files by topic.

## Installation

1.  **Clone/Open the project**
2.  **Install Python Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **System Dependencies**:
    - Ensure `ffmpeg` is installed and in your system PATH.

## Usage

Run the Streamlit app:

```bash
python -m streamlit run src/ui_app.py
```

1.  Upload an audio file in the Sidebar.
2.  Click "Process Audio".
3.  View the generated transcript, timeline, and topic summaries.

## Directory Structure
- `src/`: Source code for all modules.
- `audio_raw/`: Place your input audio files here (or upload via UI).
- `processed_audio/`: Intermediate WAV files.
- `transcripts/`: Raw JSON transcripts from Whisper.
- `segments/`: Enriched segment metadata with summaries.
