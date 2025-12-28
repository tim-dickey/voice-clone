# Voice Clone Development Guide

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- Virtual environment tool (venv or conda)

### Setup Development Environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/voice-clone.git
cd voice-clone
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements.txt
pip install -e ".[dev]"
```

## Project Structure

```
voice-clone/
├── src/voice_clone/           # Main package
│   ├── core/                  # Core functionality
│   │   ├── config.py         # Configuration management
│   │   └── application.py    # Main application logic
│   ├── modules/              # Processing modules
│   │   ├── audio_handler.py
│   │   ├── voice_embedder.py
│   │   └── synthesis_engine.py
│   ├── ui/                   # User interface
│   │   └── main_window.py
│   └── utils/               # Utilities
│       └── helpers.py
├── tests/                   # Test suite
├── docs/                    # Documentation
├── main.py                 # Application entry point
├── setup.py               # Package setup
├── requirements.txt       # Dependencies
└── Makefile             # Development commands
```

## Development Workflow

### Running the Application

```bash
python main.py
```

Or using the Makefile:
```bash
make run
```

### Running Tests

```bash
pytest tests/ -v --cov=src/voice_clone
```

Or:
```bash
make test
```

### Code Quality

Format code with Black:
```bash
black src/ main.py setup.py
```

Lint with Pylint:
```bash
pylint src/ main.py
```

Type checking with mypy:
```bash
mypy src/
```

Or use the convenient command:
```bash
make format  # Format
make lint    # Lint + type check
```

## Adding New Features

### 1. Create Feature Branch
```bash
git checkout -b feature/my-feature
```

### 2. Implement Changes
- Add code in appropriate modules
- Write unit tests
- Update documentation

### 3. Test Thoroughly
```bash
make test   # Run all tests
make lint   # Check code quality
```

### 4. Commit and Push
```bash
git add .
git commit -m "Add feature: description"
git push origin feature/my-feature
```

### 5. Create Pull Request
- Describe your changes
- Reference any related issues
- Request review

## Module Development Guidelines

### Audio Handler
- Handle audio I/O operations
- Implement audio validation logic
- Export WAV files with proper formatting

### Voice Embedder
- Extract voice characteristics
- Manage voice profile storage
- Implement voice profile loading

### Synthesis Engine
- Implement TTS synthesis
- Parameter validation
- Audio generation

### Main Application
- Coordinate workflows
- Handle errors gracefully
- Provide logging

### UI
- Create responsive interfaces
- Implement user feedback
- Handle file dialogs and progress

## Testing Guidelines

### Unit Tests
- Test individual functions
- Mock external dependencies
- Aim for >80% coverage

### Integration Tests
- Test module interactions
- Test full workflows
- Validate end-to-end behavior

### Example Test
```python
def test_audio_validation():
    """Test audio validation"""
    from voice_clone.modules.audio_handler import AudioHandler
    from voice_clone.core.config import Config
    
    config = Config()
    handler = AudioHandler(config)
    
    # Load test audio
    audio_data = handler.load_audio("test_audio.wav")
    
    # Validate
    result = handler.validate_audio(audio_data)
    assert result['is_valid']
```

## Documentation

### Code Documentation
- Add docstrings to all functions
- Use type hints
- Document parameters and return values

### Documentation Files
- ARCHITECTURE.md - System architecture
- DEVELOPMENT.md - Development guide (this file)
- README.md - Project overview

### Example Docstring
```python
def synthesize(self, text: str, voice_embedding: np.ndarray,
              speech_rate: float = 1.0) -> Tuple[np.ndarray, int]:
    """
    Synthesize speech with cloned voice.
    
    Args:
        text: Text to synthesize
        voice_embedding: Speaker embedding vector
        speech_rate: Speech rate multiplier (0.8-1.5)
        
    Returns:
        Tuple of (waveform, sample_rate)
        
    Raises:
        ValueError: If parameters are invalid
    """
```

## Building Installers

### PyInstaller Build
```bash
pyinstaller voice_clone.spec
```

Output will be in `dist/voice-clone/`

### Platform-Specific Builds

**Windows:**
```bash
pyinstaller voice_clone.spec --onefile -w
```

**macOS:**
```bash
pyinstaller voice_clone.spec --onefile --osx-bundle-identifier=com.voiceclone
```

**Linux:**
```bash
pyinstaller voice_clone.spec --onefile
```

## Debugging

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Use Python Debugger
```python
import pdb
pdb.set_trace()  # Breakpoint
```

### Qt Debugging
- Use Qt Designer for UI layout
- Qt Creator for debugging signals/slots
- Enable Qt debug logs in config

## Performance Optimization

### Profiling
```bash
python -m cProfile -s cumulative main.py
```

### Memory Profiling
```bash
pip install memory-profiler
python -m memory_profiler main.py
```

## Contributing

1. Read CONTRIBUTING.md guidelines
2. Follow PEP 8 style
3. Write meaningful commit messages
4. Include tests for new features
5. Update documentation

## Troubleshooting

### ImportError: No module named 'voice_clone'
```bash
pip install -e .
```

### PyTorch CUDA Issues
```bash
pip install torch::cuda # Install CUDA-compatible version
```

### PyQt6 Display Issues
- On Linux: Install `libdbus-1-dev`
- On macOS: Run `pip install pyqt6[webengine]`

## Resources

- [PyTorch Documentation](https://pytorch.org/docs/)
- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [librosa Documentation](https://librosa.org/)
- [pytest Documentation](https://docs.pytest.org/)
