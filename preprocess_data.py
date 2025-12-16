import pandas as pd
import re

# ==========================================
# 1. CONFIGURATION
# ==========================================
input_csv = "final_project_dataset.csv"  # The file you created in Phase 1
output_csv = "clean_project_dataset.csv" # The new clean file we will create

# ==========================================
# 2. LOAD DATA
# ==========================================
print(f"⏳ Loading {input_csv}...")
try:
    df = pd.read_csv(input_csv)
    print(f"   ✅ Loaded {len(df)} rows.")
except FileNotFoundError:
    print("❌ Error: Could not find 'final_project_dataset.csv'. Did you run the previous step?")
    exit()

# ==========================================
# 3. DEFINE CLEANING FUNCTION
# ==========================================
def clean_transcript(text):
    """
    Cleans raw TED transcripts by removing non-speech metadata.
    """
    if not isinstance(text, str):
        return ""
    
    # Step A: Remove content inside round brackets like (Applause), (Laughter), (Music)
    # Regex explanation: \s* matches spaces, \( matches opening (, .*? matches content, \) matches closing )
    text = re.sub(r'\s*\(.*?\)\s*', ' ', text)
    
    # Step B: Remove content inside square brackets like [Music], [Applause] (sometimes used)
    text = re.sub(r'\s*\[.*?\]\s*', ' ', text)
    
    # Step C: Remove extra spaces (convert "  " to " ")
    text = " ".join(text.split())
    
    return text

# ==========================================
# 4. APPLY CLEANING
# ==========================================
print("\n🧹 Cleaning transcripts (Removing 'Applause', 'Laughter', etc.)...")

# Apply the function to the 'transcript' column
df['clean_transcript'] = df['transcript'].apply(clean_transcript)

# ==========================================
# 5. VERIFY & SAVE
# ==========================================
# Show a "Before vs After" example from the first row
print("\n" + "="*50)
print("🔍 PREPROCESSING CHECK (Row 1)")
print("="*50)
print(f"🔴 RAW TEXT:\n   {df['transcript'].iloc[0][:100]}...")
print(f"\n🟢 CLEAN TEXT:\n   {df['clean_transcript'].iloc[0][:100]}...")

# Save the clean data
df.to_csv(output_csv, index=False)

print("\n" + "="*50)
print(f"🎉 SUCCESS! Clean data saved to '{output_csv}'")
print(f"👉 Use '{output_csv}' for your Topic Segmentation now.")
print("="*50)