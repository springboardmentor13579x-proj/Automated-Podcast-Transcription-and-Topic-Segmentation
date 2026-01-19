import sys
import os
import pytest

# -------------------------------------------------
# Make project root importable
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# -------------------------------------------------
# Import functions from core
# -------------------------------------------------
from src.core import (
    sentence_based_segments,
    summarize_text,
    detect_speaker
)

# -------------------------------------------------
# Tests for sentence segmentation
# -------------------------------------------------
def test_sentence_based_segments_basic():
    text = "Hello everyone! Welcome to the interview. Are you ready?"
    segments = sentence_based_segments(text)

    assert isinstance(segments, list)
    assert len(segments) >= 3
    assert segments[0]["text"].startswith("Hello")
    assert segments[1]["text"].startswith("Welcome")
    assert segments[2]["text"].startswith("Are you")

def test_sentence_based_segments_empty():
    text = ""
    segments = sentence_based_segments(text)
    assert segments == []

# -------------------------------------------------
# Tests for summarization
# -------------------------------------------------
def test_summarize_text_basic():
    text = (
        "This is a test sentence. "
        "This test is for summarization. "
        "We want to see if the summary works. "
        "Summarization is important in interviews."
    )

    summary = summarize_text(text, top_n=2)

    assert isinstance(summary, str)
    assert len(summary) > 0
    assert "test" in summary.lower() or "summarization" in summary.lower()

def test_summarize_text_short_input():
    text = "Short text."
    summary = summarize_text(text, top_n=3)
    assert summary.strip() != ""

# -------------------------------------------------
# Tests for speaker detection
# -------------------------------------------------
def test_detect_speaker_narrator():
    text = "Welcome to English Conversation Journal. Today we will learn about interviews."
    speaker = detect_speaker(text)
    assert speaker == "Narrator"

def test_detect_speaker_interviewer():
    text = "Can you tell me about yourself?"
    speaker = detect_speaker(text)
    assert speaker == "Interviewer"

def test_detect_speaker_candidate():
    text = "I studied business at City College and I work at a coffee shop."
    speaker = detect_speaker(text)
    assert speaker == "Candidate"

def test_detect_speaker_fallback():
    text = "This is just a neutral sentence without clear context."
    speaker = detect_speaker(text)
    assert speaker in ["Narrator", "Interviewer", "Candidate"]

def test_empty_input():
    assert sentence_based_segments("") == []
    assert summarize_text("") == ""
    assert detect_speaker("") == "Narrator"


def test_short_text_segmentation():
    text = "Hello! How are you?"
    segments = sentence_based_segments(text)
    assert len(segments) == 2


def test_speaker_detection_interviewer():
    text = "Why do you want this job?"
    assert detect_speaker(text) == "Interviewer"


def test_speaker_detection_candidate():
    text = "I want to grow in my career and learn new skills."
    assert detect_speaker(text) == "Candidate"


def test_summarize_length():
    text = "This is sentence one. This is sentence two. This is sentence three."
    summary = summarize_text(text, n_sentences=2)
    assert len(summary.split(".")) <= 3

