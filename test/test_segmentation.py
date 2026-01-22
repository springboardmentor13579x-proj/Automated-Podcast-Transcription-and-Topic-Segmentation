import os

def test_segmented_folder_exists():
    assert os.path.exists("segmented"), "segmented folder does not exist"

def test_segmented_files_exist():
    files = os.listdir("segmented")
    assert len(files) > 0, "No segmented files found"
