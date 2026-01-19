from src.segment_keySearch import (
    segment_text,
    extract_keywords,
    summarize_text
)

def test_segment_text():
    text = "This is sentence one. This is sentence two. This is sentence three."
    segments = segment_text(text, sentences_per_segment=2)
    assert len(segments) == 2

def test_extract_keywords():
    text = "machine learning improves data science models"
    keywords = extract_keywords(text, top_k=3)
    assert isinstance(keywords, list)
    assert len(keywords) <= 3

def test_summarize_text():
    text = "AI is powerful. AI is transforming industries. AI helps automation."
    summary = summarize_text(text, num_sentences=1)
    assert isinstance(summary, str)
