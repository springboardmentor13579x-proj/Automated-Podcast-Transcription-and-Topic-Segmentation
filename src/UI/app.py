mport os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import json
import shutil
from flask import Flask, render_template, send_from_directory, abort, request, redirect, url_for
from werkzeug.utils import secure_filename

# --- IMPORT AI PIPELINE MODULES ---
# (Make sure these files exist from previous steps)
from src.models.transcriber import PodcastTranscriber
from src.segmentation.semantic_segmenter import SemanticSegmenter
from src.summarization.content_processor import ContentProcessor
from pydub import AudioSegment, effects

app = Flask(__name__)

# ==========================================
# 👇 CONFIGURATION 👇
BASE_DIR = r"C:\Users\ADRAJ\Downloads\Podcast_Transcription"
DATA_DIR = r"C:\Users\ADRAJ\Downloads\Podcast_Transcription\data\final_output"
TEMP_DIR = r"C:\Users\ADRAJ\Downloads\Podcast_Transcription\data\temp_processing"

# Update this to your 'PodcastFillers' folder
AUDIO_DIR = r"C:\Users\ADRAJ\Downloads\Internship_Dataset\Processed_audio"

# Ensure dirs exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
# ==========================================

# Initialize AI Models (Load once at startup to save time)
print("⏳ Initializing AI Models... (Please wait)")
transcriber_model = PodcastTranscriber(model_name="openai/whisper-tiny")
segmenter_model = SemanticSegmenter()
processor_model = ContentProcessor()
print("✅ Models Ready!")

def process_single_file(filepath, filename):
    """Runs the full pipeline on a single file."""
    try:
        # 1. Preprocessing (Normalize)
        print(f"   -> normalizing {filename}...")
        raw_audio = AudioSegment.from_file(filepath)
        norm_audio = effects.normalize(raw_audio)
        # Convert to 16kHz Mono for Whisper
        norm_audio = norm_audio.set_frame_rate(16000).set_channels(1)
        
        # Save processed audio to AUDIO_DIR so the player can find it
        final_audio_path = os.path.join(AUDIO_DIR, filename)
        # Force export as WAV for consistency
        if not filename.lower().endswith(".wav"):
            filename = os.path.splitext(filename)[0] + ".wav"
            final_audio_path = os.path.join(AUDIO_DIR, filename)
            
        norm_audio.export(final_audio_path, format="wav")

        # 2. Transcription
        print("   -> Transcribing...")
        full_text, chunks = transcriber_model.transcribe(final_audio_path)
        
        # Prepare data for segmentation
        sentences = [c['text'].strip() for c in chunks if c['text'].strip()]
        timestamps = [c['timestamp'] for c in chunks if c['text'].strip()]

        # 3. Segmentation
        print("   -> Segmenting topics...")
        segments = segmenter_model.segment(sentences, timestamps, threshold=0.5)

        # 4. Enrichment (Summary, Keywords, Sentiment)
        print("   -> Generating insights...")
        for seg in segments:
            seg['summary'] = processor_model.generate_summary(seg['text'])
            seg['keywords'] = processor_model.extract_keywords(seg['text'])
            seg['sentiment'] = processor_model.analyze_sentiment(seg['text'])

        # 5. Save Final JSON
        json_filename = os.path.splitext(filename)[0] + "_final.json"
        json_path = os.path.join(DATA_DIR, json_filename)
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(segments, f, indent=4)
            
        return json_filename

    except Exception as e:
        print(f"❌ Processing Error: {e}")
        return None

@app.route('/')
def index():
    """Homepage with list & search."""
    query = request.args.get('q', '').lower().strip()
    episodes = []
    
    if os.path.exists(DATA_DIR):
        for fname in os.listdir(DATA_DIR):
            if fname.endswith("_final.json"):
                path = os.path.join(DATA_DIR, fname)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        summary = data[0].get('summary', '') if data else ""
                        keywords = []
                        for s in data: keywords.extend(s.get('keywords', []))
                        
                        # Filtering Logic
                        display_name = fname.replace("_final.json", "")
                        match = True
                        if query:
                            match = (query in display_name.lower() or 
                                     query in summary.lower() or 
                                     any(query in k.lower() for k in keywords))
                        
                        if match:
                            episodes.append({
                                "name": display_name,
                                "filename": fname,
                                "description": summary,
                                "keywords": list(set(keywords))[:4]
                            })
                except: pass
    
    return render_template('index.html', episodes=episodes, query=query)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle File Uploads."""
    if 'file' not in request.files:
        return redirect(request.url)
        
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        temp_path = os.path.join(TEMP_DIR, filename)
        file.save(temp_path)
        
        print(f"🚀 Received Upload: {filename}")
        
        # Run the Pipeline!
        result_json = process_single_file(temp_path, filename)
        
        # Cleanup temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        if result_json:
            return redirect(url_for('player', filename=result_json))
        else:
            return "Error processing file. Check console logs."

@app.route('/player/<filename>')
def player(filename):
    """Player Page."""
    json_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(json_path): return abort(404)

    with open(json_path, 'r', encoding='utf-8') as f:
        segments = json.load(f)

    base_name = filename.replace("_final.json", "")
    audio_file = None
    # Check .wav first (since we convert uploads to wav)
    if os.path.exists(os.path.join(AUDIO_DIR, base_name + ".wav")):
        audio_file = base_name + ".wav"
    elif os.path.exists(os.path.join(AUDIO_DIR, base_name + ".mp3")):
        audio_file = base_name + ".mp3"
            
    return render_template('player.html', segments=segments, episode_name=base_name, audio_file=audio_file)

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory(AUDIO_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
