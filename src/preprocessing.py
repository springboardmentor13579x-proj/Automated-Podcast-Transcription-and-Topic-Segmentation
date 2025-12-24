import os
import logging
import numpy as np
import librosa
import soundfile as sf
import noisereduce as nr

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_audio(file_path, processed_dir):
    """
    Enhanced pipeline:
    1. Load & Convert to WAV, Force Mono, Resample to 16kHz (librosa does this on load)
    2. Noise Reduction (suppress likely background noise)
    3. Normalize Volume (0.95 headroom)
    4. Save optimized WAV (float32)
    """
    try:
        # 1. Directory Safety
        os.makedirs(processed_dir, exist_ok=True)

        filename = os.path.basename(file_path)
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(processed_dir, f"{name}_processed.wav")
        
        logger.info(f"Processing {filename}...")
        
        # Load, Force Mono, Resample 16000Hz
        y, sr = librosa.load(file_path, sr=16000, mono=True)
        
        # 2. Noise Reduction
        logger.info("Applying noise reduction...")
        # stationary=True uses spectral gating assuming constant noise floor
        y_denoised = nr.reduce_noise(y=y, sr=sr, stationary=True, prop_decrease=0.80)
        
        # 3. Safe Normalization (with 0.95 headroom)
        logger.info("Normalizing audio...")
        max_val = np.max(np.abs(y_denoised))
        if max_val > 0:
            y_normalized = y_denoised / max_val * 0.95
        else:
            y_normalized = y_denoised
        
        # 4. Data Type Control & Save
        # Ensure float32 for ML compatibility
        sf.write(output_path, y_normalized.astype(np.float32), sr)
        
        logger.info(f"Saved processed audio to {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Failed to process audio: {e}")
        # Valid re-raise
        raise
