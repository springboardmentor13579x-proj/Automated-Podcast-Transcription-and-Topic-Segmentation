import os
import json
import shutil
import warnings
import numpy as np
import librosa
import soundfile as sf
import torch
import nltk
import whisper
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
from nltk.sentiment import SentimentIntensityAnalyzer

# Suppress warnings
warnings.filterwarnings("ignore")

def setup_directories(base_dir):
    dirs = {
        "audio": os.path.join(base_dir, "audio"),
        "processed": os.path.join(base_dir, "processed_audio"),
        "transcripts": os.path.join(base_dir, "transcripts"),
        "summary": os.path.join(base_dir, "short_summary"),
        "topics": os.path.join(base_dir, "semantic_segments"),
        "keywords": os.path.join(base_dir, "keywords"),
        "sentiment": os.path.join(base_dir, "sentiment_data")
    }
    for d in dirs.values():
        os.makedirs(d, exist_ok=True)
    return dirs

def setup_nltk():
    resources = ['punkt', 'punkt_tab', 'vader_lexicon']
    for r in resources:
        try:
            nltk.data.find(f'tokenizers/{r}') if 'punkt' in r else nltk.data.find(f'sentiment/{r}')
        except LookupError:
            nltk.download(r, quiet=True)

# --- 1. PREPROCESSING ---
def preprocess_audio(input_path, output_path):
    target_sr = 16000
    try:
        y, sr = librosa.load(input_path, sr=target_sr, mono=True)
        # Normalize
        if np.max(np.abs(y)) > 0:
            y = y / np.max(np.abs(y))
        sf.write(output_path, y, sr)
        return True
    except Exception as e:
        print(f"Error preprocessing: {e}")
        return False

# --- 2. TRANSCRIPTION & SUMMARY ---
def transcribe_and_summarize(audio_path, transcript_path, summary_path, model_size="base"):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Transcribe
    model = whisper.load_model(model_size, device=device)
    result = model.transcribe(str(audio_path), fp16=False)
    
    # Save Transcript
    with open(transcript_path.replace('.json', '.txt'), "w", encoding="utf-8") as f:
        f.write(result["text"].strip())
    with open(transcript_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)
        
    # Generate Summary
    text = result["text"]
    summary = "Summary could not be generated." # Default message
    try:
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        # Chunk text if too long
        chunk = text[:3500]
        # Adjusted settings for better short summaries
        summary_result = summarizer(chunk, max_length=200, min_length=50, do_sample=False)
        summary = summary_result[0]['summary_text']
    except Exception as e:
        print(f"Summary AI Error: {e}. Using fallback.")
        # Fallback to simple extraction
        sentences = text.split('.')
        summary = ". ".join(sentences[:15]) + "."
        
    # Ensure summary is saved
    try:
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)
        print(f"Summary saved to: {summary_path}")
    except Exception as e:
        print(f"Error saving summary file: {e}")

# --- 3. SENTIMENT ---
def analyze_sentiment(transcript_path, output_path):
    setup_nltk()
    sia = SentimentIntensityAnalyzer()
    
    with open(transcript_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if "segments" not in data:
        return

    timeline = []
    for segment in data["segments"]:
        text = segment["text"].strip()
        scores = sia.polarity_scores(text)
        comp = scores['compound']
        label = "Positive" if comp >= 0.05 else "Negative" if comp <= -0.05 else "Neutral"
        
        timeline.append({
            "start": segment["start"],
            "end": segment["end"],
            "text": text,
            "score": comp,
            "label": label
        })
        
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(timeline, f, indent=4)

# --- 4. KEYWORDS ---
def extract_keywords(transcript_dir, output_dir):
    files = list(Path(transcript_dir).glob("*.json"))
    if not files: return

    documents = []
    filenames = []
    
    for p in files:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
            documents.append(data["text"])
            filenames.append(p.stem)
            
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_features=5000)
    try:
        tfidf_matrix = vectorizer.fit_transform(documents)
        feature_names = vectorizer.get_feature_names_out()
        
        for i, filename in enumerate(filenames):
            scores = tfidf_matrix[i].toarray().flatten()
            top_indices = scores.argsort()[-10:][::-1]
            
            keywords = []
            for idx in top_indices:
                if scores[idx] > 0:
                    keywords.append(f"{feature_names[idx]}")
            
            out_file = os.path.join(output_dir, f"{filename}_keywords.txt")
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(f"=== KEYWORDS FOR: {filename} ===\n")
                f.write("\n".join(keywords))
    except ValueError:
        pass 

# --- 5. TOPIC SEGMENTATION (FIXED) ---
def segment_topics(transcript_path, output_path):
    setup_nltk()
    with open(transcript_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        text = data["text"]
        
    sentences = nltk.sent_tokenize(text)
    
    # FIXED: If audio is too short, create a "Single Topic" file instead of doing nothing
    if len(sentences) < 5: 
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"=== TOPICS: {Path(transcript_path).stem} ===\n")
            f.write(f"🔹 TOPIC 1: {text[:200]}... (Audio too short for multi-topic segmentation)\n")
        return

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(sentences)
    
    # Settings
    window = 2 
    similarities = []
    
    for i in range(len(sentences) - window):
        v1 = tfidf_matrix[i:i+window].mean(axis=0)
        v2 = tfidf_matrix[i+1:i+1+window].mean(axis=0)
        sim = cosine_similarity(np.asarray(v1), np.asarray(v2))[0][0]
        similarities.append(sim)
        
    segments = []
    curr = []
    threshold = 0.5 
    
    for i, sim in enumerate(similarities):
        curr.append(sentences[i])
        if sim < threshold:
            segments.append(" ".join(curr))
            curr = []
    
    remaining = sentences[len(similarities):]
    curr.extend(remaining)
    # FIXED: Was causing NameError (current_segment -> curr)
    segments.append(" ".join(curr))
    
    # Summarize segments
    try:
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        report = [f"=== TOPICS: {Path(transcript_path).stem} ===\n"]
        for i, seg in enumerate(segments):
            if len(seg) > 50: 
                summ_len = min(60, len(seg.split()) // 2)
                if summ_len > 10:
                    summ = summarizer(seg[:2000], max_length=summ_len + 20, min_length=10, do_sample=False)[0]['summary_text']
                    report.append(f"🔹 TOPIC {i+1}: {summ}\n")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report))
            
    except Exception as e:
        print(f"Topic Error: {e}")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"=== TOPICS (Fallback) ===\n")
            for i, seg in enumerate(segments):
                f.write(f"🔹 TOPIC {i+1}: {seg[:100]}...\n")

# --- MASTER PIPELINE ---
def process_new_upload(file_obj, base_dir):
    dirs = setup_directories(base_dir)
    file_stem = Path(file_obj.name).stem
    
    # 1. Save raw
    raw_path = os.path.join(dirs["audio"], file_obj.name)
    with open(raw_path, "wb") as f:
        f.write(file_obj.getbuffer())
        
    # 2. Preprocess
    proc_path = os.path.join(dirs["processed"], f"{file_stem}.wav")
    if not preprocess_audio(raw_path, proc_path):
        return "Preprocessing failed."
        
    # 3. Transcribe & Summary
    trans_path = os.path.join(dirs["transcripts"], f"{file_stem}.json")
    summ_path = os.path.join(dirs["summary"], f"{file_stem}_summary.txt")
    transcribe_and_summarize(proc_path, trans_path, summ_path)
    
    # 4. Sentiment
    sent_path = os.path.join(dirs["sentiment"], f"{file_stem}_sentiment.json")
    analyze_sentiment(trans_path, sent_path)
    
    # 5. Topics
    top_path = os.path.join(dirs["topics"], f"{file_stem}_topics.txt")
    segment_topics(trans_path, top_path)
    
    # 6. Update Keywords (Global)
    extract_keywords(dirs["transcripts"], dirs["keywords"])
    
    return "Success"