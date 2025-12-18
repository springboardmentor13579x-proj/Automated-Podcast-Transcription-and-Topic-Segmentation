from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import subprocess
import json
import shutil
import config  # Imports your config.py

app = Flask(__name__)
CORS(app)

# Ensure directories exist
os.makedirs(config.RAW_AUDIO_FOLDER, exist_ok=True)
os.makedirs(config.PROCESSED_FOLDER, exist_ok=True)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        print("\n" + "="*50)
        print("🚀 STARTING NEW UPLOAD PROCESS")
        print("="*50)

        # 1. CLEAN UP OLD DATA
        print("🧹 Cleaning old files...")
        for folder in [config.RAW_AUDIO_FOLDER, config.PROCESSED_FOLDER]:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"   ⚠️ Could not delete {filename}: {e}")

        # 2. SAVE NEW FILE
        filename = file.filename
        save_path = os.path.join(config.RAW_AUDIO_FOLDER, filename)
        file.save(save_path)
        print(f"✅ File saved to: {save_path}")

        # 3. RUN PIPELINE (VISIBLE MODE)
        print("\n⏳ RUNNING PIPELINE NOW (Watch below)...")
        print("-" * 30)
        
        try:
            # This runs the pipeline and lets it print to your terminal
            result = subprocess.run(["python", "run_pipeline.py"], check=False)
            
            if result.returncode != 0:
                print("❌ PIPELINE CRASHED! (Check errors above)")
                return jsonify({"error": "Pipeline script failed. Check terminal for details."}), 500
                
        except Exception as e:
            print(f"❌ Execution Error: {e}")
            return jsonify({"error": str(e)}), 500

        print("-" * 30)
        print("✅ Pipeline finished.")

        # 4. FIND THE RESULT
        print(f"🧐 Looking for JSON in: {config.PROCESSED_FOLDER}")
        
        all_files = os.listdir(config.PROCESSED_FOLDER)
        print(f"📂 Files actually in folder: {all_files}")

        files = [f for f in all_files if f.startswith("summary_") and f.endswith(".json")]
        
        if not files:
            print("❌ ERROR: Pipeline finished, but NO 'summary_*.json' file was created.")
            print("   -> Did run_pipeline.py actually save the file?")
            return jsonify({"error": "No JSON file created. Check terminal logs."}), 500
        
        # Pick the file
        latest_file = files[0]
        print(f"🎉 SUCCESS! Serving file: {latest_file}")
        
        with open(os.path.join(config.PROCESSED_FOLDER, latest_file), "r", encoding="utf-8") as f:
            data = json.load(f)
            
        return jsonify(data)

if __name__ == '__main__':
    print(f"🚀 Server running on http://localhost:5000")
    print(f"📂 Monitoring Data Folder: {config.DATA_FOLDER}")
    app.run(debug=True, port=5000)