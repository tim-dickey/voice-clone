import logging
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QLineEdit, QTextEdit, QSlider,
    QListWidget, QListWidgetItem, QFileDialog, QSpinBox,
    QDoubleSpinBox, QComboBox, QProgressBar, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from pathlib import Path
from ..core.application import VoiceCloneApp
from ..core.config import Config

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.config = Config.load_config()
        self.app = VoiceCloneApp(self.config)
        
        self.setWindowTitle("Voice Clone - Professional Voice Synthesis")
        self.setGeometry(100, 100, self.config.ui.window_width, self.config.ui.window_height)
        
        self.init_ui()
        logger.info("Main window initialized")
    
    def init_ui(self):
        """Initialize user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        
        # Left sidebar - Voice Library
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("Voice Library"))
        
        self.voice_list = QListWidget()
        self.voice_list.itemSelectionChanged.connect(self.on_voice_selected)
        left_panel.addWidget(self.voice_list)
        
        clone_btn = QPushButton("Clone New Voice")
        clone_btn.clicked.connect(self.on_clone_voice)
        left_panel.addWidget(clone_btn)
        
        delete_btn = QPushButton("Delete Voice")
        delete_btn.clicked.connect(self.on_delete_voice)
        left_panel.addWidget(delete_btn)
        
        # Center panel - Synthesis
        center_panel = QVBoxLayout()
        
        center_panel.addWidget(QLabel("Text to Synthesize"))
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Enter text to synthesize...")
        center_panel.addWidget(self.text_input)
        
        # Parameters
        params_layout = QVBoxLayout()
        
        # Speech rate
        params_layout.addWidget(QLabel("Speech Rate (0.8 - 1.5)"))
        self.speech_rate_slider = QSlider(Qt.Orientation.Horizontal)
        self.speech_rate_slider.setMinimum(8)
        self.speech_rate_slider.setMaximum(15)
        self.speech_rate_slider.setValue(10)
        params_layout.addWidget(self.speech_rate_slider)
        
        # Pitch
        params_layout.addWidget(QLabel("Pitch (-15 - +15%)"))
        self.pitch_slider = QSlider(Qt.Orientation.Horizontal)
        self.pitch_slider.setMinimum(-15)
        self.pitch_slider.setMaximum(15)
        self.pitch_slider.setValue(0)
        params_layout.addWidget(self.pitch_slider)
        
        # Tone
        params_layout.addWidget(QLabel("Tone"))
        self.tone_combo = QComboBox()
        self.tone_combo.addItems(["Neutral", "Warm", "Energetic"])
        params_layout.addWidget(self.tone_combo)
        
        center_panel.addLayout(params_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        preview_btn = QPushButton("Preview")
        preview_btn.clicked.connect(self.on_preview)
        button_layout.addWidget(preview_btn)
        
        export_btn = QPushButton("Export as WAV")
        export_btn.clicked.connect(self.on_export)
        button_layout.addWidget(export_btn)
        
        center_panel.addLayout(button_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        center_panel.addWidget(self.progress_bar)
        
        # Main layout
        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(center_panel, 2)
        
        central_widget.setLayout(main_layout)
        self.refresh_voice_list()
    
    def refresh_voice_list(self):
        """Refresh list of available voices"""
        self.voice_list.clear()
        voices = self.app.get_voice_list()
        for voice_name in voices:
            self.voice_list.addItem(QListWidgetItem(voice_name))
    
    def on_voice_selected(self):
        """Handle voice selection"""
        current_item = self.voice_list.currentItem()
        if current_item:
            logger.info(f"Selected voice: {current_item.text()}")
    
    def on_clone_voice(self):
        """Handle voice cloning"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Audio File", "",
            "Audio Files (*.wav *.mp3 *.m4a);;All Files (*)"
        )
        
        if not file_path:
            return
        
        voice_name, ok = self._get_voice_name_dialog()
        if not ok or not voice_name:
            return
        
        success = self.app.clone_voice(file_path, voice_name)
        if success:
            QMessageBox.information(self, "Success", f"Voice '{voice_name}' cloned successfully!")
            self.refresh_voice_list()
        else:
            QMessageBox.critical(self, "Error", "Failed to clone voice. Check audio quality.")
    
    def on_delete_voice(self):
        """Handle voice deletion"""
        current_item = self.voice_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a voice to delete.")
            return
        
        voice_name = current_item.text()
        reply = QMessageBox.question(self, "Confirm", f"Delete voice '{voice_name}'?")
        
        if reply == QMessageBox.StandardButton.Yes:
            self.app.delete_voice(voice_name)
            self.refresh_voice_list()
    
    def on_preview(self):
        """Handle preview generation"""
        current_item = self.voice_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a voice.")
            return
        
        text = self.text_input.toPlainText()[:100]  # Preview first 100 chars
        if not text:
            QMessageBox.warning(self, "Warning", "Please enter text to synthesize.")
            return
        
        voice_name = current_item.text()
        speech_rate = self.speech_rate_slider.value() / 10.0
        pitch = self.pitch_slider.value()
        tone = self.tone_combo.currentText().lower()
        
        self.progress_bar.setVisible(True)
        logger.info(f"Generating preview for voice: {voice_name}")
    
    def on_export(self):
        """Handle WAV export"""
        current_item = self.voice_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a voice.")
            return
        
        text = self.text_input.toPlainText()
        if not text:
            QMessageBox.warning(self, "Warning", "Please enter text to synthesize.")
            return
        
        voice_name = current_item.text()
        speech_rate = self.speech_rate_slider.value() / 10.0
        pitch = self.pitch_slider.value()
        tone = self.tone_combo.currentText().lower()
        
        self.progress_bar.setVisible(True)
        output_path = self.app.synthesize_speech(voice_name, text, speech_rate, pitch, tone)
        
        if output_path:
            QMessageBox.information(self, "Success", f"Exported to: {output_path}")
        else:
            QMessageBox.critical(self, "Error", "Failed to synthesize speech.")
        
        self.progress_bar.setVisible(False)
    
    def _get_voice_name_dialog(self) -> tuple:
        """Get voice name from user"""
        from PyQt6.QtWidgets import QInputDialog
        text, ok = QInputDialog.getText(self, "Voice Name", "Enter a name for this voice:")
        return text, ok
