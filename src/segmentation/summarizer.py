from transformers import pipeline

summarizer = pipeline("summarization", model="t5-small")

def summarize_segment(text):
    result = summarizer(
        text,
        max_length=80,
        min_length=20,
        do_sample=False
    )
    return result[0]["summary_text"]