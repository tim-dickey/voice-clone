# Voice Clone - Professional Voice Synthesis Application

A consumer-grade voice cloning application that enables users to clone their voice using standard personal computer hardware.

## Features

- Voice Cloning Module: Clone voices from 30-60 seconds of reference audio
- Text-to-Speech Synthesis: Convert text to speech using cloned voices
- WAV Export: Export synthesized audio in Audiate-compatible WAV format
- Voice Library Management: Store and manage multiple voice profiles

## Installation

From Source:
`git clone https://github.com/yourusername/voice-clone.git`
`cd voice-clone`
`pip install -r requirements.txt`
`python main.py`

## Project Structure

voice-clone/
├── src/voice_clone/
│   ├── core/ - Core configuration and app logic
│   ├── modules/ - Voice processing modules
│   ├── ui/ - PyQt6 user interface
│   └── utils/ - Helper utilities

## Development

Run tests: `pytest tests/ -v --cov=src/voice_clone`
Format code: `black src/ main.py`
Lint: `pylint src/`
Type checking: `mypy src/`

## Building Installer

`pyinstaller voice_clone.spec`

## License

MIT License - see LICENSE file for details
