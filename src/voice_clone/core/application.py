import logging
from typing import Optional
from pathlib import Path
from .config import Config
from ..modules.voice_embedder import VoiceEmbedder
from ..modules.synthesis_engine import SynthesisEngine
from ..modules.audio_handler import AudioHandler

logger = logging.getLogger(__name__)


class VoiceCloneApp:
    """Main application class orchestrating all modules"""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the application"""
        self.config = config or Config.load_config()
        logger.info(f"Initializing {self.config.app_name} v{self.config.app_version}")
        
        # Initialize modules
        self.audio_handler = AudioHandler(self.config)
        self.voice_embedder = VoiceEmbedder(self.config)
        self.synthesis_engine = SynthesisEngine(self.config)
        
        logger.info("Application initialization complete")
    
    def clone_voice(self, audio_path: str, voice_name: str) -> bool:
        """Clone a voice from reference audio"""
        try:
            logger.info(f"Starting voice cloning: {voice_name}")
            
            # Load and validate audio
            audio_data = self.audio_handler.load_audio(audio_path)
            validation_result = self.audio_handler.validate_audio(audio_data)
            
            if not validation_result['is_valid']:
                logger.error(f"Audio validation failed: {validation_result['issues']}")
                return False
            
            # Extract voice embedding
            embedding = self.voice_embedder.extract_embedding(audio_data)
            
            # Save voice profile
            voice_profile_path = self.config.voices_dir / f"{voice_name}.npz"
            self.voice_embedder.save_voice_profile(embedding, voice_profile_path, voice_name)
            
            logger.info(f"Voice cloning completed: {voice_name}")
            return True
            
        except Exception as e:
            logger.error(f"Voice cloning failed: {e}")
            return False
