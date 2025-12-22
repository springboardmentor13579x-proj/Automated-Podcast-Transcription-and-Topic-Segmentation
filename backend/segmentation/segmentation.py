import os
import nltk
import numpy as np
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import pipeline
import json

nltk.download('punkt')

# -------------------------------
# CONFIG (NEW)
# -------------------------------
TOTAL_AUDIO_DURATION = 10 * 60   # 10 minutes (seconds)

# -------------------------------
# Load transcript
# -------------------------------
def load_transcript(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# -------------------------------
# Transformer-based segmentation
# -------------------------------
def embedding_segmentation(text):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    sentences = nltk.sent_tokenize(text)
    embeddings = model.encode(sentences)

    similarities = []
    for i in range(1, len(embeddings)):
        sim = util.cos_sim(embeddings[i], embeddings[i-1]).item()
        similarities.append(sim)

    threshold = np.mean(similarities) - np.std(similarities)

    segments = []
    current_segment = sentences[0]

    for i in range(1, len(sentences)):
        if similarities[i-1] < threshold:
            segments.append(current_segment)
            current_segment = sentences[i]
        else:
            current_segment += " " + sentences[i]

    segments.append(current_segment)
    return segments

# -------------------------------
# Keyword extraction
# -------------------------------
def extract_keywords(segment):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([segment])
    scores = tfidf_matrix.toarray()[0]
    word_scores = list(zip(vectorizer.get_feature_names_out(), scores))
    sorted_words = sorted(word_scores, key=lambda x: x[1], reverse=True)
    return [w[0] for w in sorted_words[:5]]

# -------------------------------
# Summarization
# -------------------------------
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_segment(segment):
    words = segment.split()

    # agar segment bahut chhota hai
    if len(words) < 40:
        return segment  # direct text return

    try:
        max_len = min(70, len(words))
        min_len = min(30, max_len - 5)

        return summarizer(
            segment,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )[0]["summary_text"]

    except:
        return segment[:200]


# -------------------------------
# Helper (NEW)
# -------------------------------
def format_time(seconds):
    m = seconds // 60
    s = seconds % 60
    return f"{int(m):02d}:{int(s):02d}"

# -------------------------------
# Main pipeline
# -------------------------------
def main():
    transcript_dir = "../../data/transcripts"
    output_dir = "../../data/segments"

    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(transcript_dir):
        if file.endswith(".txt"):
            print(f"\n Processing transcript: {file}")
            text = load_transcript(os.path.join(transcript_dir, file))

            segments = embedding_segmentation(text)
            print(f"Total Segments Found: {len(segments)}")

            segment_duration = TOTAL_AUDIO_DURATION // len(segments)

            final_output = []

            for i, seg in enumerate(segments):
                start_sec = i * segment_duration
                end_sec = start_sec + segment_duration

                final_output.append({
                    "segment_number": i + 1,
                    "start_time": format_time(start_sec),
                    "end_time": format_time(end_sec),
                    "text": seg,
                    "keywords": extract_keywords(seg),
                    "summary": summarize_segment(seg)
                })

            json_path = os.path.join(
                output_dir, f"segments_{file.replace('.txt','')}.json"
            )

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(final_output, f, indent=4, ensure_ascii=False)

            print(f"Saved: {json_path}")

if __name__ == "__main__":
    main()
