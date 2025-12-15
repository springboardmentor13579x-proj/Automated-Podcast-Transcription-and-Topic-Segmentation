from src.preprocessing.noise_reduction import reduce_noise
from src.preprocessing.normalization import normalize_audio
import os

def preprocess_audio(raw_file, cleaned_file):
    temp_file = "temp.wav"
    
    reduce_noise(raw_file, temp_file)
    
    normalize_audio(temp_file, cleaned_file)
    
    if os.path.exists(temp_file):
        os.remove(temp_file)
    
    print(f"Processed: {cleaned_file}")