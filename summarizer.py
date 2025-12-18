import os
import nltk
import json  
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from heapq import nlargest
import config

def generate_summary(text, num_sentences=2):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    
    freq_table = {}
    for word in words:
        word = word.lower()
        if word not in stop_words and word.isalnum():
            freq_table[word] = freq_table.get(word, 0) + 1

    sentences = sent_tokenize(text)
    sentence_scores = {}
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in freq_table:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + freq_table[word]

    summary_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    return ' '.join(summary_sentences)

def extract_keywords(text, num=5):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    filtered = [w.lower() for w in words if w.lower() not in stop_words and w.isalnum()]
    return [w for w, c in nltk.FreqDist(filtered).most_common(num)]

def process_summaries():
    print("\n--- Generating Summaries (JSON format) ---")
    files = [f for f in os.listdir(config.PROCESSED_FOLDER) if f.startswith("segments_")]
    
    all_processed_topics = [] # <--- Added this to collect data

    for filename in files:
        input_path = os.path.join(config.PROCESSED_FOLDER, filename)
        
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        topics = content.split("=== TOPIC")
        
        print(f"Processing: {filename}")
        for i in range(1, len(topics)):
            lines = topics[i].split("\n", 1)
            if len(lines) < 2: continue
            
            topic_num = lines[0].replace(" ===", "").strip()
            text_body = lines[1]
            
            if len(text_body) < 20: continue

            summary = generate_summary(text_body)
            keywords = extract_keywords(text_body)
            
            topic_entry = {
                "topic_id": topic_num,
                "keywords": keywords,
                "summary": summary,
                "full_text_snippet": text_body[:100] + "..."
            }
            all_processed_topics.append(topic_entry) # <--- Fill the list
            
    return all_processed_topics # <--- CRITICAL: Return the data to run_pipeline.py