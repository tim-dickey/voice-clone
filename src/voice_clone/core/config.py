import os
import json
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
import logging

logger = logging.getLogger(__name__)


class AudioConfig(BaseModel):
    """Audio processing configuration"""
    sample_rate: int = 44100
    bit_depth: int = 16
    channels: int = 1
    min_duration: float = 30.0
    max_duration: float = 120.0
    min_snr: float = 15.0


class ModelConfig(BaseModel):
    """ML model configuration"""
    voice_embedding_model: str = "fish-speech-v1.5"
    tts_model: str = "fish-speech-v1.5"
    device: str = "cuda"
    dtype: str = "fp16"
    max_cache_size: int = 5


class UIConfig(BaseModel):
    """UI configuration"""
    theme: str = "light"
    window_width: int = 1200
    window_height: int = 800
    show_debug_panel: bool = False


class Config(BaseSettings):
    """Main application configuration"""
    
    # Application Info
    app_name: str = "Voice Clone"
    app_version: str = "1.0.0"
    
    # Paths
    app_dir: Path = Field(default_factory=lambda: Path.home() / ".voice_clone")
    models_dir: Path = Field(default_factory=lambda: Path.home() / ".voice_clone" / "models")
    voices_dir: Path = Field(default_factory=lambda: Path.home() / ".voice_clone" / "voices")
    exports_dir: Path = Field(default_factory=lambda: Path.home() / "Documents" / "Voice Clone Exports")
    logs_dir: Path = Field(default_factory=lambda: Path.home() / ".voice_clone" / "logs")
    
    # Feature flags
    enable_telemetry: bool = False
    enable_crash_reporting: bool = False
    
    # Sub-configurations
    audio: AudioConfig = Field(default_factory=AudioConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)
    ui: UIConfig = Field(default_factory=UIConfig)
    
    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
    
    def __init__(self, **data):
        super().__init__(**data)
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary application directories"""
        for directory in [self.app_dir, self.models_dir, self.voices_dir, 
                         self.exports_dir, self.logs_dir]:
            directory.mkdir(parents=True, exist_ok=True)
