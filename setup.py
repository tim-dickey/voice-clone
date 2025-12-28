from setuptools import setup, find_packages

setup(
    name="voice-clone",
    version="1.0.0",
    description="Professional voice cloning application for consumer hardware",
    author="Voice Clone Development Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "torch>=2.0.1",
        "torchaudio>=2.0.2",
        "librosa>=0.10.0",
        "scipy>=1.11.4",
        "numpy>=1.24.3",
        "PyQt6>=6.6.1",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "sounddevice>=0.4.6",
        "mutagen>=1.46.0",
        "click>=8.1.7",
        "tqdm>=4.66.1",
        "pyinstaller>=6.2.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "pylint>=3.0.3",
            "mypy>=1.7.1",
        ]
    },
    entry_points={
        "console_scripts": [
            "voice-clone=voice_clone.__main__:main",
        ]
    },
)
