import os
import logging
from pydub import AudioSegment
import librosa
import soundfile as sf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_to_wav(input_path, output_path):
    """
    Converts any audio file supported by pydub to WAV format.
    """
    try:
        logger.info(f"Converting {input_path} to {output_path}")
        audio = AudioSegment.from_file(input_path)
        audio = audio.set_channels(1) # Mono for better speech recognition
        audio.export(output_path, format="wav")
        return output_path
    except Exception as e:
        logger.error(f"Error converting audio: {e}")
        raise

def resample_audio(input_path, output_path, target_sr=16000):
    """
    Resamples audio to target sample rate (16kHz for Whisper).
    """
    try:
        logger.info(f"Resampling {input_path} to {target_sr}Hz")
        y, sr = librosa.load(input_path, sr=target_sr)
        sf.write(output_path, y, target_sr)
        return output_path
    except Exception as e:
        logger.error(f"Error resampling audio: {e}")
        raise

def process_audio(file_path, processed_dir):
    """
    Full pipeline: Convert -> Resample -> Save to processed_dir
    """
    filename = os.path.basename(file_path)
    name, _ = os.path.splitext(filename)
    
    wav_path = os.path.join(processed_dir, f"{name}.wav")
    
    # Step 1: Convert to WAV and mono
    convert_to_wav(file_path, wav_path)
    
    # Step 2: Resample (overwrite or new file? Overwriting for simplicity as step 1 created a wav)
    # Actually, let's keep it separate if needed, but here we can just update the wav
    final_path = os.path.join(processed_dir, f"{name}_16k.wav")
    resample_audio(wav_path, final_path)
    
    # Clean up intermediate file
    if os.path.exists(wav_path) and wav_path != final_path:
        os.remove(wav_path)
        
    return final_path
