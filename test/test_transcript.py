import os

def test_transcripts_folder_exists():
    assert os.path.exists("transcripts"), "transcripts folder does not exist"

def test_transcripts_not_empty():
    files = os.listdir("transcripts")
    assert len(files) > 0, "No transcript files found"
