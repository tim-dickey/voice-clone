# Voice Clone Architecture Documentation

## Overview

Voice Clone is a modular, Python-based voice cloning application designed for consumer hardware. The architecture follows clear separation of concerns with minimal cross-module dependencies.

## Module Organization

### Core Module (`src/voice_clone/core/`)

**config.py**
- Application configuration management
- Directory structure setup
- Logging configuration
- Settings for audio, model, and UI parameters

**application.py**
- Main orchestration logic
- Workflow coordination
- Voice cloning pipeline
- Text-to-speech synthesis pipeline

### Processing Modules (`src/voice_clone/modules/`)

**audio_handler.py**
- Audio file loading (WAV, MP3, M4A, FLAC)
- Audio validation (SNR, duration, clipping detection)
- WAV export with normalization
- Resampling and loudness normalization

**voice_embedder.py**
- Speaker embedding extraction
- Voice profile storage and retrieval
- Metadata management

**synthesis_engine.py**
- Text-to-speech synthesis
- Parameter validation (speech rate, pitch, tone)
- Audio generation

### User Interface (`src/voice_clone/ui/`)

**main_window.py**
- PyQt6-based main application window
- Voice library management
- Synthesis parameter controls
- File dialogs and progress tracking

### Utilities (`src/voice_clone/utils/`)

**helpers.py**
- Filename sanitization
- Duration formatting
- File size calculation

## Data Flow

### Voice Cloning Workflow

```
User Action: Clone Voice
    ↓
[Main Window] - UI interaction
    ↓
[Application] - Orchestration
    ↓
[AudioHandler] - Load and validate audio
    ↓
[VoiceEmbedder] - Extract embeddings
    ↓
[File System] - Store voice profile
    ↓
[Main Window] - Display result
```

### Text-to-Speech Workflow

```
User Action: Synthesize Speech
    ↓
[Main Window] - Collect parameters
    ↓
[Application] - Orchestration
    ↓
[VoiceEmbedder] - Load voice profile
    ↓
[SynthesisEngine] - Generate audio
    ↓
[AudioHandler] - Export as WAV
    ↓
[Main Window] - Display result
```

## Configuration Structure

```
~/.voice_clone/
├── config.json          # Application settings
├── voices/              # Voice profile storage
│   └── voice_name.npz   # Voice embedding data
├── models/              # ML model cache
├── logs/                # Application logs
└── exports/             # User-exported audio files
```

## Key Design Principles

1. **Modularity**: Each component has a single responsibility
2. **Abstraction**: Clear interfaces between modules
3. **Extensibility**: Plugin architecture for models
4. **Local-First**: All processing happens locally
5. **User-Centric**: Clear feedback and error handling

## Technology Stack

- **UI Framework**: PyQt6 (cross-platform)
- **Audio Processing**: librosa, scipy, sounddevice
- **ML Framework**: PyTorch
- **Data Validation**: Pydantic
- **Packaging**: PyInstaller

## Performance Considerations

- Audio processing uses numpy for efficiency
- Models loaded on-demand to minimize memory
- Configuration cached after first load
- Voice profiles compressed with numpy

## Error Handling

- Graceful degradation with user-facing messages
- Comprehensive logging at all levels
- Validation at entry points
- Recovery mechanisms for common failures

## Testing Strategy

- Unit tests for core modules
- Integration tests for workflows
- Mocking of heavy operations
- Coverage targets >80%
