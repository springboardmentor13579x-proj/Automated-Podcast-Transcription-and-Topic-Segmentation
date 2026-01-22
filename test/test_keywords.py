import os

def test_keywords_folder_exists():
    assert os.path.exists("keywords"), "keywords folder does not exist"

def test_keywords_files_exist():
    files = os.listdir("keywords")
    assert len(files) > 0, "No keyword files found"
