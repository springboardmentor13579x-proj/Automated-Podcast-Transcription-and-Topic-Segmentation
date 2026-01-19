from src.preprocessing import preprocess_audio
from src.transcription import transcribe_audio
from src.segmentation import segment_transcripts
from src.summarization import summarize_segments
from src.keyword_extraction import run_keyword_extraction
from src.evaluate_asr import evaluate_asr

# Directory paths
AUDIO_RAW = "audio_raw"
AUDIO_PROCESSED = "audio_processed"

REFERENCE_TRANSCRIPTS = "transcripts/raw_reference"
ASR_TRANSCRIPTS = "transcripts/asr"

SEGMENTS_DIR = "segments"
FINAL_TRANSCRIPTS = "transcripts/final"


def main():
    print("\n===== HR INTERVIEW PIPELINE STARTED =====\n")

    print("Step 1: Preprocessing audio...")
    preprocess_audio(AUDIO_RAW, AUDIO_PROCESSED)

    print("\nStep 2: Transcribing audio with Whisper...")
    transcribe_audio(AUDIO_PROCESSED, ASR_TRANSCRIPTS)

    print("\nStep 3: Segmenting transcripts...")
    segment_transcripts(ASR_TRANSCRIPTS, SEGMENTS_DIR)

    print("\nStep 4: Summarizing segments...")
    summarize_segments()

    print("\nStep 5: Extracting keywords...")
    run_keyword_extraction()

    print("\nStep 6: Evaluating ASR quality...")
    evaluate_asr()

    print("\n===== PIPELINE COMPLETED SUCCESSFULLY =====\n")
    print("Generated Outputs:")
    print("• ASR transcripts → transcripts/asr/")
    print("• Segments        → segments/")
    print("• Summaries       → transcripts/final/")
    print("• Keywords        → docs/keywords.txt")
    print("• Evaluation CSV  → docs/asr_evaluation.csv")
    print("• Evaluation Table→ docs/asr_evaluation_table.txt")


if __name__ == "__main__":
    main()
