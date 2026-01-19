import os
import subprocess

video_ids = [
    "JkwvVpjjob8",
    "3JZ_D3ELwOQ",
    "UOcfda7oBVs",
    "eD7q4B0iDls",
    "BoZpcibb-JI",
    "V-qSYaAhH0Q",
    "GWkzCr3i0o0"
]

output_dir = "audio_raw"
os.makedirs(output_dir, exist_ok=True)

for vid in video_ids:
    url = f"https://www.youtube.com/watch?v={vid}"
    print(f"\nDownloading audio for: {vid}")

    cmd = [
        "yt-dlp",
        "-x",
        "--audio-format", "wav",
        "-o", f"{output_dir}/%(id)s.%(ext)s",
        url
    ]

    subprocess.run(cmd, check=True)

print("\n✅ All audio files downloaded.")
