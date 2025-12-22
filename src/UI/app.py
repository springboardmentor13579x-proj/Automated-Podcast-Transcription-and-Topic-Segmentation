import os
import json
from flask import Flask, render_template, send_from_directory, abort, request

app = Flask(__name__)

# ==========================================
# 👇 CONFIGURATION 👇
# Update this if your path is different
DATA_DIR =r"C:\Users\ADRAJ\Downloads\Podcast_Transcription\data\final_output"
# Update this to your actual audio folder
AUDIO_DIR = r"C:\Users\ADRAJ\Downloads\Internship_Dataset\Processed_audio"
# ==========================================

@app.route('/')
def index():
    """Homepage: Lists episodes with Search & Filtering."""
    query = request.args.get('q', '').lower().strip()
    episodes = []
    
    if not os.path.exists(DATA_DIR):
        return f"❌ Error: Data directory not found at {DATA_DIR}"

    # Scan all processed JSON files
    for filename in os.listdir(DATA_DIR):
        if filename.endswith("_final.json"):
            display_name = filename.replace("_final.json", "")
            filepath = os.path.join(DATA_DIR, filename)
            
            description = "No summary available."
            keywords = []
            
            # 1. Load Data
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data and len(data) > 0:
                        # Get summary from first topic
                        description = data[0].get('summary', '')
                        # Collect all keywords from all topics
                        for topic in data:
                            keywords.extend(topic.get('keywords', []))
            except:
                pass

            # 2. Search Logic (Filtering)
            # If there is a query, check if it matches Title, Summary, or Keywords
            match_found = True
            if query:
                # Check if query is in title, description, or any keyword
                in_title = query in display_name.lower()
                in_desc = query in description.lower()
                in_keywords = any(query in kw.lower() for kw in keywords)
                
                if not (in_title or in_desc or in_keywords):
                    match_found = False

            # 3. Add to list only if it matches
            if match_found:
                # Deduplicate and limit keywords for display
                unique_keywords = list(set(keywords))[:5] 
                
                episodes.append({
                    "name": display_name,
                    "filename": filename,
                    "description": description,
                    "keywords": unique_keywords
                })
    
    return render_template('index.html', episodes=episodes, query=query)

@app.route('/player/<filename>')
def player(filename):
    """Player Page: Displays audio, transcript, and topics."""
    json_path = os.path.join(DATA_DIR, filename)
    
    if not os.path.exists(json_path):
        return abort(404)

    with open(json_path, 'r', encoding='utf-8') as f:
        segments = json.load(f)

    base_name = filename.replace("_final.json", "")
    
    # Check for audio file (.wav or .mp3)
    audio_file = None
    for ext in [".wav", ".mp3"]:
        if os.path.exists(os.path.join(AUDIO_DIR, base_name + ext)):
            audio_file = base_name + ext
            break
            
    return render_template('player.html', 
                           segments=segments, 
                           episode_name=base_name, 
                           audio_file=audio_file)

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory(AUDIO_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
