import numpy as np
from src.preprocessing import (
    load_audio,
    normalize_audio,
    trim_silence
)

def test_normalize_audio():
    audio = np.array([0.1, -0.2, 0.3])
    normalized = normalize_audio(audio)
    assert np.max(np.abs(normalized)) <= 1.0

def test_trim_silence():
    audio = np.concatenate([
        np.zeros(100),
        np.ones(100),
        np.zeros(100)
    ])

    trimmed = trim_silence(audio)

    # basic correctness checks
    assert isinstance(trimmed, np.ndarray)
    assert trimmed.ndim == 1
    assert len(trimmed) > 0


