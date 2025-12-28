import pytest
from pathlib import Path
from voice_clone.core.config import Config


def test_config_initialization():
    """Test configuration initialization"""
    config = Config()
    assert config.app_name == "Voice Clone"
    assert config.app_version == "1.0.0"
    assert config.voices_dir.exists()
    assert config.models_dir.exists()


def test_config_paths():
    """Test configuration paths"""
    config = Config()
    assert config.app_dir.is_absolute()
    assert config.voices_dir.is_absolute()
    assert config.exports_dir.is_absolute()
