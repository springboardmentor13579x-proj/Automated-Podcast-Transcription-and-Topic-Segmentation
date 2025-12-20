import os
import xml.etree.ElementTree as ET

def merge_manual_session(manual_path, merged_path, sessions, speakers=["A","B","C","D"]):
    os.makedirs(merged_path, exist_ok=True)

    for session_id in sessions:
        words = []
        for speaker in speakers:
            fname = f"{session_id}.{speaker}.words.xml"
            fpath = os.path.join(manual_path, fname)
            if not os.path.exists(fpath):
                print(f"⚠️ Missing manual file: {fname}")
                continue
            tree = ET.parse(fpath)
            root = tree.getroot()
            for elem in root.iter():
                tag = elem.tag.split("}")[-1]
                if tag == "w" and elem.text:
                    words.append(elem.text.strip())
        out_file = os.path.join(merged_path, f"{session_id}_manual.txt")
        with open(out_file, "w") as f:
            f.write(" ".join(words))
        print(f"✅ {session_id} merged. Total words: {len(words)}, saved to: {out_file}")
