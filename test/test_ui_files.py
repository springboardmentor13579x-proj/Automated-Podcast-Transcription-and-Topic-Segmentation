import os

def test_ui_folder_exists():
    assert os.path.exists("ui"), "ui folder does not exist"

def test_app_file_exists():
    assert os.path.exists("ui/app.py"), "app.py file not found in ui folder"
