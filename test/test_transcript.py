import os
from src.transcript import get_audio_files, ensure_output_dir

def test_ensure_output_dir(tmp_path):
    dir_path = tmp_path / "output"
    ensure_output_dir(dir_path)
    assert os.path.exists(dir_path)

def test_get_audio_files(tmp_path):
    file1 = tmp_path / "test.wav"
    file2 = tmp_path / "test.mp3"
    file1.touch()
    file2.touch()

    files = get_audio_files(tmp_path, (".wav", ".mp3"))
    assert len(files) == 2
