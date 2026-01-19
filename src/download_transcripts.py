import os
from youtube_transcript_api import YouTubeTranscriptApi

video_ids = [
    "JkwvVpjjob8",
    "3JZ_D3ELwOQ",
    "UOcfda7oBVs",
    "eD7q4B0iDls",
    "BoZpcibb-JI",
    "V-qSYaAhH0Q",
    "GWkzCr3i0o0"
]

OUTPUT_DIR = "transcripts/raw_reference"
os.makedirs(OUTPUT_DIR, exist_ok=True)

api = YouTubeTranscriptApi()

for vid in video_ids:
    print(f"\nFetching transcript for: {vid}")
    try:
        transcript = api.fetch(vid)

        out_path = os.path.join(OUTPUT_DIR, f"{vid}.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            for snippet in transcript:
                f.write(snippet.text.strip() + "\n")

        print(f"✅ Saved: {out_path}")

    except Exception as e:
        print(f"❌ Could not fetch transcript for {vid}")
        print(f"   Reason: {e}")
