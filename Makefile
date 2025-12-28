.PHONY: help install install-dev test lint format clean build

help:
@echo "Voice Clone - Development Commands"
@echo "===================================="
@echo "make install      - Install dependencies"
@echo "make install-dev  - Install dev dependencies"
@echo "make test         - Run tests"
@echo "make lint         - Run code linting"
@echo "make format       - Format code"
@echo "make clean        - Clean build artifacts"
@echo "make build        - Build installer"
@echo "make run          - Run application"

install:
pip install -r requirements.txt

install-dev:
pip install -r requirements.txt
pip install -e .[dev]

test:
pytest tests/ -v --cov=src/voice_clone

lint:
pylint src/ main.py
mypy src/

format:
black src/ main.py setup.py

clean:
rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

build:
pyinstaller voice_clone.spec

run:
python main.py

.PHONY: docker-build docker-run

docker-build:
docker build -t voice-clone:latest .

docker-run:
docker run -it voice-clone:latest
