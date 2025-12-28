import logging
import numpy as np
from pathlib import Path
from typing import Dict, Any, Tuple
import librosa
import scipy.io.wavfile as wavfile
from ..core.config import Config

logger = logging.getLogger(__name__)


class AudioHandler:
    """Handle audio loading, validation, and export"""
    
    def __init__(self, config: Config):
        self.config = config
        self.audio_config = config.audio
    
    def load_audio(self, audio_path: str) -> Tuple[np.ndarray, int]:
        """Load audio file and return waveform and sample rate"""
        try:
            audio_path = Path(audio_path)
            if not audio_path.exists():
                raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
            # Load audio using librosa
            waveform, sr = librosa.load(str(audio_path), sr=None)
            logger.info(f"Loaded audio: {audio_path}, sr={sr}, duration={len(waveform)/sr:.2f}s")
            return waveform, sr
        except Exception as e:
            logger.error(f"Failed to load audio: {e}")
            raise
    
    def validate_audio(self, audio_data: Tuple[np.ndarray, int]) -> Dict[str, Any]:
        """Validate audio quality"""
        waveform, sr = audio_data
        issues = []
        
        # Check duration
        duration = len(waveform) / sr
        if duration < self.audio_config.min_duration:
            issues.append(f"Duration too short: {duration:.1f}s (min {self.audio_config.min_duration}s)")
        if duration > self.audio_config.max_duration:
            issues.append(f"Duration too long: {duration:.1f}s (max {self.audio_config.max_duration}s)")
        
        # Check signal-to-noise ratio (simplified)
        rms = np.sqrt(np.mean(waveform**2))
        noise_floor = np.percentile(np.abs(waveform), 5)
        snr_db = 20 * np.log10(rms / (noise_floor + 1e-10))
        
        if snr_db < self.audio_config.min_snr:
            issues.append(f"SNR too low: {snr_db:.1f}dB (min {self.audio_config.min_snr}dB)")
        
        # Check for clipping
        if np.max(np.abs(waveform)) > 0.95:
            issues.append("Audio appears to be clipped")
        
        return {
            'is_valid': len(issues) == 0,
            'issues': issues,
            'duration': duration,
            'snr_db': snr_db,
            'sample_rate': sr
        }
    
    def export_wav(self, audio_data: Tuple[np.ndarray, int], output_path: str,
                  bit_depth: int = 16, channels: int = 1):
        """Export audio as WAV file"""
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            waveform, sr = audio_data
            
            # Resample if needed
            if sr != self.audio_config.sample_rate:
                waveform = librosa.resample(waveform, orig_sr=sr, target_sr=self.audio_config.sample_rate)
                sr = self.audio_config.sample_rate
            
            # Normalize audio
            max_val = np.max(np.abs(waveform))
            if max_val > 0:
                waveform = waveform / max_val * 0.95
            
            # Convert to appropriate bit depth
            if bit_depth == 16:
                waveform_int = np.int16(waveform * 32767)
            elif bit_depth == 24:
                waveform_int = np.int32(waveform * 8388607)
            else:
                waveform_int = np.int16(waveform * 32767)
            
            # Write WAV file
            wavfile.write(str(output_path), sr, waveform_int)
            logger.info(f"Exported WAV: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export WAV: {e}")
            return False
    
    def resample_audio(self, audio_data: Tuple[np.ndarray, int], target_sr: int) -> Tuple[np.ndarray, int]:
        """Resample audio to target sample rate"""
        waveform, sr = audio_data
        if sr == target_sr:
            return audio_data
        
        resampled = librosa.resample(waveform, orig_sr=sr, target_sr=target_sr)
        return resampled, target_sr
    
    def normalize_loudness(self, waveform: np.ndarray, target_lufs: float = -16.0) -> np.ndarray:
        """Normalize audio loudness using LUFS"""
        # Simplified loudness normalization
        rms = np.sqrt(np.mean(waveform**2))
        target_rms = 10 ** (target_lufs / 20)
        
        if rms > 0:
            waveform = waveform * (target_rms / rms)
        
        # Soft clipping to prevent distortion
        waveform = np.tanh(waveform)
        return waveform
