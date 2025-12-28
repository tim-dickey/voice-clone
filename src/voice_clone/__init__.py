# Voice Clone Application Package
__version__ = "1.0.0"
__author__ = "Voice Clone Development Team"

from .core.config import Config
from .core.application import VoiceCloneApp

__all__ = ["Config", "VoiceCloneApp", "__version__", "__author__"]
