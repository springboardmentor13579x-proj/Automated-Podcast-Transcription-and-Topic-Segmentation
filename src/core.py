import re
from collections import Counter

# -------------------------------------------------
# Sentence Segmentation
# -------------------------------------------------
def sentence_based_segments(text):
    """
    Split text into sentence segments using punctuation (. ? !).
    Returns a list of dictionaries:
    [{"segment_id": 1, "text": "..."}]
    """
    if not text:
        return []

    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    segments = []

    for idx, p in enumerate(parts, start=1):
        if p.strip():
            segments.append({
                "segment_id": idx,
                "text": p.strip()
            })

    return segments


# -------------------------------------------------
# Text Summarization
# -------------------------------------------------
def summarize_text(text, top_n=None, n_sentences=3):
    """
    Generate a frequency-based summary of the text.

    Args:
        text (str or list): Input text OR list of segment dicts
        top_n (int, optional): Alias for n_sentences
        n_sentences (int): Number of sentences to return

    Returns:
        str: Summary text
    """

    # Support both parameter styles used in tests
    if top_n is not None:
        n = top_n
    else:
        n = n_sentences

    if not text:
        return ""

    # If input is a list of segments, extract text
    if isinstance(text, list):
        sentences = []
        for item in text:
            if isinstance(item, dict):
                sentences.append(item.get("text", ""))
            else:
                sentences.append(str(item))
    else:
        segments = sentence_based_segments(text)
        sentences = [s["text"] for s in segments]

    if not sentences:
        return ""

    full_text = " ".join(sentences)

    words = re.findall(r'\b[a-zA-Z]+\b', full_text.lower())
    freq = Counter(words)

    ranked = []
    for s in sentences:
        score = sum(
            freq.get(w.lower(), 0)
            for w in re.findall(r'\b[a-zA-Z]+\b', s)
        )
        ranked.append((score, s))

    ranked = sorted(ranked, reverse=True)
    return " ".join([s for _, s in ranked[:n]])


# -------------------------------------------------
# Speaker Detection
# -------------------------------------------------
def detect_speaker(text):
    """
    Classify speaker type: Narrator, Interviewer, or Candidate
    """
    if not text:
        return "Narrator"

    t = text.lower()

    narrator_markers = [
        "welcome", "today we", "before you go", "remember",
        "thank you for watching", "let's start", "good luck"
    ]

    interviewer_patterns = [
        "what is", "why do you", "how long", "how did you",
        "can you", "do you", "tell me", "where do you",
        "what are your", "may i", "are you"
    ]

    candidate_patterns = [
        "i am", "i'm", "i studied", "i work", "i have been",
        "my experience", "i want", "i can", "i believe",
        "i manage", "i helped"
    ]

    if any(p in t for p in narrator_markers):
        return "Narrator"

    if t.strip().endswith("?") or any(p in t for p in interviewer_patterns):
        return "Interviewer"

    if any(p in t for p in candidate_patterns):
        return "Candidate"

    return "Narrator"
