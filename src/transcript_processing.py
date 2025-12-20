import os
import re
from collections import defaultdict

def get_session_name(filename):
    match = re.match(r"(ES\d{4}[a-d])", filename)
    return match.group(1) if match else None

def combine_asr_transcripts(asr_path, final_path):
    os.makedirs(final_path, exist_ok=True)
    transcript_files = [f for f in os.listdir(asr_path) if f.endswith(".txt") and not f.endswith("_segments.txt")]
    session_transcripts = defaultdict(list)

    for file in transcript_files:
        session = get_session_name(file)
        if session:
            with open(os.path.join(asr_path, file), "r") as f:
                text = f.read().strip()
            session_transcripts[session].append((file, text))

    for session, parts in session_transcripts.items():
        # Sort by part letter A/B/C/D
        sorted_parts = sorted(parts, key=lambda x: re.search(r"\.([A-D])", x[0]).group(1) if re.search(r"\.([A-D])", x[0]) else "Z")
        combined_text = "\n".join([text for fname, text in sorted_parts])
        out_file = os.path.join(final_path, f"{session}.txt")
        with open(out_file, "w") as f:
            f.write(combined_text)
        print(f"Combined transcript saved for session {session} -> {out_file}")
