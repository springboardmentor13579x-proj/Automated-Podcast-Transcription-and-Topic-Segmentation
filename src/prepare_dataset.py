import pandas as pd
import os

# ==========================================
# 1. CONFIGURATION (Your Specific Paths)
# ==========================================
# We use r"..." (raw string) to handle the backslashes correctly on Windows.

# The folder where your MP3 files are located:
AUDIO_FOLDER_PATH = r"E:\speech_to_text\archive\AUDIO"

# The path to the CSV file inside your 'archive (2)' folder:
# NOTE: Make sure the file name is exactly 'ted_talk.csv'. 
# If it is 'ted_talk_data.csv', change the name below.
CSV_FILE_PATH = r"E:\speech_to_text\archive (2)\TED_Talk.csv"

# ==========================================
# 2. LOAD AND INSPECT DATA
# ==========================================
print("⏳ Step 1: Loading the CSV file...")

if not os.path.exists(CSV_FILE_PATH):
    print(f"❌ Error: Could not find the CSV file at: {CSV_FILE_PATH}")
    print("   -> Check if the file is named 'ted_talk.csv' or 'ted_talk_data.csv'")
    exit()

df = pd.read_csv(CSV_FILE_PATH)
print(f"   ✅ CSV Loaded! Found {len(df)} rows.")

# Check for the correct ID column name (datasets vary)
if 'talk__id' in df.columns:
    id_col = 'talk__id'
elif 'talk_id' in df.columns:
    id_col = 'talk_id'
else:
    print(f"❌ Error: Could not find an ID column. Columns found: {df.columns.tolist()}")
    exit()

print(f"   ℹ️  Using ID column: '{id_col}'")

# ==========================================
# 3. MATCHING LOGIC
# ==========================================
print("\n⏳ Step 2: Linking Audio files to Transcripts...")

valid_pairs = []
missing_count = 0

for index, row in df.iterrows():
    # Get the ID (e.g., 1001)
    talk_id = row[id_col]
    
    # Construct the expected filename (e.g., "1001.mp3")
    audio_filename = f"{talk_id}.mp3"
    
    # Create the full path to check
    full_audio_path = os.path.join(AUDIO_FOLDER_PATH, audio_filename)
    
    # Check if the file actually exists on your E: drive
    if os.path.exists(full_audio_path):
        # SUCCESS: We found the audio!
        # We save specific columns needed for the project
        valid_pairs.append({
            'talk_id': talk_id,
            'title': row.get('title', 'Unknown Title'), # Safe get if title is missing
            'transcript': row.get('transcript', ''),    # The text we need
            'audio_path': full_audio_path               # The path to the MP3
        })
    else:
        missing_count += 1

# ==========================================
# 4. SAVE AND REPORT
# ==========================================
print("\n" + "="*40)
print("📊 FINAL REPORT")
print("="*40)

if len(valid_pairs) > 0:
    # Convert list to DataFrame
    df_final = pd.DataFrame(valid_pairs)
    
    # Save to a new CSV in your current working directory
    output_filename = "final_project_dataset.csv"
    df_final.to_csv(output_filename, index=False)
    
    print(f"🎉 SUCCESS! Found {len(df_final)} matching Audio-Transcript pairs.")
    print(f"❌ Skipped {missing_count} rows (Audio file missing).")
    print(f"💾 SAVED: The clean dataset is saved as '{output_filename}'")
    print("\n   👉 You can now use this CSV for your AI model!")
    
    # Show a sample to verify
    print("\n   [Sample Data - Row 1]")
    print(f"   Title: {df_final.iloc[0]['title']}")
    print(f"   Audio: {df_final.iloc[0]['audio_path']}")
    print(f"   Text Start: {str(df_final.iloc[0]['transcript'])[:50]}...")
    
else:
    print("⚠️ FAILURE: No matching audio files were found.")
    print("   -> Check if your MP3 filenames match the IDs in the CSV.")
    print("   -> Example: Is the file '1.mp3' or 'bill_gates.mp3'?")