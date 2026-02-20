"""
Berk's Screenshot Tool - Ayarlar Penceresi (PyQt6)
Dark/Light mod destekli, özel kısayol tuşu seçici ve çoklu dil desteği.
"""

from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QFont, QCursor, QTransform
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QWidget, QLineEdit, QComboBox, QSlider,
    QCheckBox, QRadioButton, QFileDialog, QMessageBox, QButtonGroup,
    QGraphicsOpacityEffect
)
import sys
import os
import keyboard as kb
import threading

# Ana modülü import edebilmek için path ekle
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import load_config, save_config
from i18n import t, get_available_languages, set_language, get_language
from pathlib import Path


class RotatingGearLabel(QLabel):
    """Dönen dişli çark etiketi."""
    
    def __init__(self, text="⚙️", parent=None):
        super().__init__(text, parent)
        self._rotation = 0
        self._is_spinning = False
        self._animation = None
        # Kare boyut ayarla (yalpalamayı önlemek için)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def get_rotation(self):
        return self._rotation
    
    def set_rotation(self, value):
        self._rotation = value
        self.update()
    
    rotation = pyqtProperty(float, get_rotation, set_rotation)
    
    def paintEvent(self, event):
        """Override paint event to apply rotation."""
        from PyQt6.QtGui import QPainter, QFontMetrics
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        
        # Widget'ın tam merkezini bul
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        # Font metrics ile metin boyutunu hesapla
        painter.setFont(self.font())
        fm = QFontMetrics(self.font())
        text = self.text()
        text_width = fm.horizontalAdvance(text)
        text_height = fm.height()
        
        # Merkeze taşı, döndür, geri al
        painter.translate(center_x, center_y)
        painter.rotate(self._rotation)
        
        # Metni merkezde çiz (orijinden hesapla)
        painter.drawText(int(-text_width / 2), int(text_height / 4), text)
        painter.end()
    
    def start_spin(self):
        """Dönmeye başla."""
        if self._is_spinning:
            return
        
        self._is_spinning = True
        self._animation = QPropertyAnimation(self, b"rotation")
        self._animation.setDuration(800)
        self._animation.setStartValue(self._rotation)
        self._animation.setEndValue(self._rotation + 360)
        self._animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self._animation.finished.connect(self._on_animation_finished)
        self._animation.start()
    
    def _on_animation_finished(self):
        """Animasyon bittiğinde."""
        self._is_spinning = False
        self._rotation = self._rotation % 360


class KeyListenerThread(QThread):
    """Tuş dinleyici thread."""
    key_pressed = pyqtSignal(str)
    
    def run(self):
        try:
            event = kb.read_event(suppress=False)
            if event.event_type == kb.KEY_DOWN:
                key_name = event.name
                
                modifiers = []
                if kb.is_pressed('ctrl'):
                    modifiers.append('Ctrl')
                if kb.is_pressed('shift'):
                    modifiers.append('Shift')
                if kb.is_pressed('alt'):
                    modifiers.append('Alt')
                
                if key_name.lower() in ['ctrl', 'shift', 'alt', 'control']:
                    final_key = key_name.upper()
                elif modifiers:
                    final_key = '+'.join(modifiers) + '+' + key_name.upper()
                else:
                    final_key = key_name.upper() if len(key_name) > 1 else key_name
                
                self.key_pressed.emit(final_key)
        except Exception as e:
            print(f"Key read error: {e}")


class SettingsDialog(QDialog):
    """Ayarlar penceresi - Dark/Light mod ve çoklu dil destekli."""
    
    _app_instance = None  # QApplication referansını tut
    
    def __init__(self, parent=None, on_save_callback=None):
        # QApplication yoksa oluştur (pystray'dan çağrıldığında gerekli)
        if QApplication.instance() is None:
            SettingsDialog._app_instance = QApplication(sys.argv)
        
        super().__init__(parent)
        self.on_save_callback = on_save_callback
        self.config = load_config()
        self.is_dark_mode = self.config.get("dark_mode", True)
        self._listening_for_key = False
        self.key_listener_thread = None
        
        self._setup_window()
        self._apply_theme()
        self._create_widgets()
        self._load_current_settings()
    
    def _setup_window(self):
        """Pencere ayarları."""
        self.setWindowTitle(f"{t('app_name')} - {t('settings_title')}")
        self.setFixedSize(520, 750)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
    
    def _apply_theme(self):
        """Tema renklerini uygula."""
        if self.is_dark_mode:
            self.bg_color = "#1e1e1e"
            self.fg_color = "#ffffff"
            self.accent_color = "#0078d4"
            self.entry_bg = "#2d2d2d"
            self.entry_fg = "#ffffff"
            self.hover_color = "#3d3d3d"
        else:
            self.bg_color = "#f5f5f5"
            self.fg_color = "#1e1e1e"
            self.accent_color = "#0078d4"
            self.entry_bg = "#ffffff"
            self.entry_fg = "#1e1e1e"
            self.hover_color = "#e0e0e0"
        
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {self.bg_color};
            }}
            QLabel {{
                color: {self.fg_color};
                background: transparent;
            }}
            QLineEdit {{
                background-color: {self.entry_bg};
                color: {self.entry_fg};
                border: 1px solid {self.hover_color};
                border-radius: 4px;
                padding: 6px;
            }}
            QComboBox {{
                background-color: {self.entry_bg};
                color: {self.entry_fg};
                border: 1px solid {self.hover_color};
                border-radius: 4px;
                padding: 6px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: {self.entry_bg};
                color: {self.entry_fg};
                selection-background-color: {self.accent_color};
            }}
            QSlider::groove:horizontal {{
                background: {self.entry_bg};
                height: 8px;
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                background: {self.accent_color};
                width: 18px;
                height: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }}
            QCheckBox {{
                color: {self.fg_color};
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {self.hover_color};
                border-radius: 4px;
                background: {self.entry_bg};
            }}
            QCheckBox::indicator:checked {{
                background: {self.accent_color};
                border-color: {self.accent_color};
            }}
            QRadioButton {{
                color: {self.fg_color};
                spacing: 8px;
            }}
            QRadioButton::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {self.hover_color};
                border-radius: 9px;
                background: {self.entry_bg};
            }}
            QRadioButton::indicator:checked {{
                background: {self.accent_color};
                border-color: {self.accent_color};
            }}
        """)
    
    def _toggle_theme(self):
        """Temayı değiştir."""
        self.is_dark_mode = not self.is_dark_mode
        self.config["dark_mode"] = self.is_dark_mode
        
        # Tema ikonunu güncelle
        theme_icon = "🌙" if self.is_dark_mode else "☀️"
        self.theme_btn.setText(theme_icon)
        
        # Temayı yeniden uygula
        self._apply_theme()
    
    def _create_widgets(self):
        """Widget'ları oluştur."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(25, 15, 25, 20)
        
        # === Üst Bar ===
        top_bar = QHBoxLayout()
        
        # Dönen dişli çark
        self.gear_label = RotatingGearLabel("⚙️")
        self.gear_label.setFont(QFont("Segoe UI Emoji", 18))
        self.gear_label.setFixedSize(30, 30)
        top_bar.addWidget(self.gear_label)
        
        # Uygulama adı
        app_name_label = QLabel(f" {t('app_name')}")
        app_name_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        top_bar.addWidget(app_name_label)
        
        top_bar.addStretch()
        
        theme_icon = "🌙" if self.is_dark_mode else "☀️"
        self.theme_btn = QPushButton(theme_icon)
        self.theme_btn.setFont(QFont("Segoe UI Emoji", 16))
        self.theme_btn.setFixedSize(40, 40)
        self.theme_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.theme_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
            }}
            QPushButton:hover {{
                background: {self.hover_color};
                border-radius: 20px;
            }}
        """)
        self.theme_btn.clicked.connect(self._toggle_theme)
        top_bar.addWidget(self.theme_btn)
        
        layout.addLayout(top_bar)
        
        # === Yakalama Bölümü ===
        self._add_section_label(layout, t("settings_capture"))
        
        # Kısayol Tuşu
        hotkey_layout = QHBoxLayout()
        hotkey_label = QLabel(t("settings_hotkey"))
        hotkey_label.setFont(QFont("Segoe UI", 10))
        hotkey_label.setFixedWidth(100)
        hotkey_layout.addWidget(hotkey_label)
        
        self.hotkey_display = QLineEdit()
        self.hotkey_display.setReadOnly(True)
        self.hotkey_display.setFont(QFont("Segoe UI", 11))
        self.hotkey_display.setFixedWidth(100)
        self.hotkey_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hotkey_layout.addWidget(self.hotkey_display)
        
        self.hotkey_btn = QPushButton(t("settings_click_to_set"))
        self.hotkey_btn.setFont(QFont("Segoe UI", 9))
        self.hotkey_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.hotkey_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.accent_color};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
            }}
            QPushButton:hover {{
                background-color: #1084d8;
            }}
        """)
        self.hotkey_btn.clicked.connect(self._start_key_listener)
        hotkey_layout.addWidget(self.hotkey_btn)
        
        self.hotkey_status = QLabel("")
        self.hotkey_status.setFont(QFont("Segoe UI", 9))
        self.hotkey_status.setStyleSheet("color: #ff9800;")
        hotkey_layout.addWidget(self.hotkey_status)
        
        hotkey_layout.addStretch()
        layout.addLayout(hotkey_layout)
        
        # Format
        format_layout = QHBoxLayout()
        format_label = QLabel(t("settings_format"))
        format_label.setFont(QFont("Segoe UI", 10))
        format_label.setFixedWidth(100)
        format_layout.addWidget(format_label)
        
        self.format_group = QButtonGroup(self)
        formats = ["PNG", "JPG", "BMP", "WEBP"]
        self.format_radios = {}
        
        for fmt in formats:
            rb = QRadioButton(fmt)
            rb.setFont(QFont("Segoe UI", 10))
            rb.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            rb.toggled.connect(self._on_format_change)
            self.format_group.addButton(rb)
            self.format_radios[fmt.lower()] = rb
            format_layout.addWidget(rb)
        
        format_layout.addStretch()
        layout.addLayout(format_layout)
        
        # Kalite
        quality_layout = QHBoxLayout()
        quality_label = QLabel(t("settings_quality"))
        quality_label.setFont(QFont("Segoe UI", 10))
        quality_label.setFixedWidth(100)
        quality_layout.addWidget(quality_label)
        
        self.quality_slider = QSlider(Qt.Orientation.Horizontal)
        self.quality_slider.setRange(10, 100)
        self.quality_slider.setValue(95)
        self.quality_slider.setFixedWidth(180)
        self.quality_slider.valueChanged.connect(self._update_quality_label)
        quality_layout.addWidget(self.quality_slider)
        
        self.quality_label = QLabel("95%")
        self.quality_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.quality_label.setStyleSheet(f"color: {self.accent_color};")
        self.quality_label.setFixedWidth(120)
        quality_layout.addWidget(self.quality_label)
        
        quality_layout.addStretch()
        layout.addLayout(quality_layout)
        
        self.lossless_info = QLabel("")
        self.lossless_info.setFont(QFont("Segoe UI", 9, italic=True))
        self.lossless_info.setStyleSheet("color: #4caf50;")
        layout.addWidget(self.lossless_info)
        
        # Monitör
        monitor_layout = QHBoxLayout()
        monitor_label = QLabel(t("settings_monitor"))
        monitor_label.setFont(QFont("Segoe UI", 10))
        monitor_label.setFixedWidth(100)
        monitor_layout.addWidget(monitor_label)
        
        self.monitor_display = QLabel(t("settings_all_monitors"))
        self.monitor_display.setFont(QFont("Segoe UI", 10))
        self.monitor_display.setStyleSheet(f"""
            QLabel {{
                background-color: {self.accent_color};
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
            }}
        """)
        monitor_layout.addWidget(self.monitor_display)
        
        monitor_btn = QPushButton(t("settings_select_monitor"))
        monitor_btn.setFont(QFont("Segoe UI", 9))
        monitor_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        monitor_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.accent_color};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
            }}
            QPushButton:hover {{
                background-color: #1084d8;
            }}
        """)
        monitor_btn.clicked.connect(self._open_monitor_selector)
        monitor_layout.addWidget(monitor_btn)
        
        monitor_layout.addStretch()
        layout.addLayout(monitor_layout)
        
        # === Depolama Bölümü ===
        self._add_section_label(layout, t("settings_storage"))
        
        path_layout = QHBoxLayout()
        path_label = QLabel(t("settings_save_folder"))
        path_label.setFont(QFont("Segoe UI", 10))
        path_label.setFixedWidth(100)
        path_layout.addWidget(path_label)
        
        self.path_entry = QLineEdit()
        self.path_entry.setFont(QFont("Segoe UI", 9))
        path_layout.addWidget(self.path_entry, 1)
        
        browse_btn = QPushButton(t("settings_browse"))
        browse_btn.setFont(QFont("Segoe UI", 9))
        browse_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        browse_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.accent_color};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
            }}
            QPushButton:hover {{
                background-color: #1084d8;
            }}
        """)
        browse_btn.clicked.connect(self._browse_folder)
        path_layout.addWidget(browse_btn)
        
        layout.addLayout(path_layout)
        
        # === Geri Bildirim Bölümü ===
        self._add_section_label(layout, t("settings_feedback"))
        
        # Ses
        sound_layout = QHBoxLayout()
        sound_label = QLabel(t("settings_sound"))
        sound_label.setFont(QFont("Segoe UI", 10))
        sound_label.setFixedWidth(100)
        sound_layout.addWidget(sound_label)
        
        self.sound_combo = QComboBox()
        self.sound_combo.setFixedWidth(150)
        
        # Ses dosyalarını bul
        sounds_dir = Path(__file__).parent.parent / "sounds"
        self.sound_options = [("settings_sound_none", "none")]
        
        if sounds_dir.exists():
            for wav_file in sounds_dir.glob("*.wav"):
                self.sound_options.append((wav_file.stem.capitalize(), wav_file.name))
        
        for name, _ in self.sound_options:
            display_name = t(name) if name.startswith("settings_") else name
            self.sound_combo.addItem(display_name)
        
        sound_layout.addWidget(self.sound_combo)
        
        test_sound_btn = QPushButton(t("settings_test_sound"))
        test_sound_btn.setFont(QFont("Segoe UI", 9))
        test_sound_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        test_sound_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.accent_color};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
            }}
            QPushButton:hover {{
                background-color: #1084d8;
            }}
        """)
        test_sound_btn.clicked.connect(self._test_sound)
        sound_layout.addWidget(test_sound_btn)
        
        self.sound_enabled_check = QCheckBox("")
        self.sound_enabled_check.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        sound_layout.addWidget(self.sound_enabled_check)
        
        sound_layout.addStretch()
        layout.addLayout(sound_layout)
        
        # Bildirim
        self.notification_check = QCheckBox(t("settings_notification"))
        self.notification_check.setFont(QFont("Segoe UI", 10))
        self.notification_check.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        layout.addWidget(self.notification_check)
        
        # === Görünüm Bölümü ===
        self._add_section_label(layout, t("settings_appearance"))
        
        # Dil
        lang_layout = QHBoxLayout()
        lang_label = QLabel(t("settings_language"))
        lang_label.setFont(QFont("Segoe UI", 10))
        lang_label.setFixedWidth(100)
        lang_layout.addWidget(lang_label)
        
        self.lang_combo = QComboBox()
        self.lang_combo.setFixedWidth(150)
        
        self.available_languages = get_available_languages()
        for lang in self.available_languages:
            self.lang_combo.addItem(lang["name"], lang["code"])
        
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()
        layout.addLayout(lang_layout)
        
        # Karanlık mod
        self.dark_mode_check = QCheckBox(t("settings_dark_mode"))
        self.dark_mode_check.setFont(QFont("Segoe UI", 10))
        self.dark_mode_check.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.dark_mode_check.setChecked(self.is_dark_mode)
        self.dark_mode_check.stateChanged.connect(self._on_dark_mode_change)
        layout.addWidget(self.dark_mode_check)
        
        # === Boşluk ===
        layout.addStretch()
        
        # === Butonlar ===
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton(t("settings_cancel"))
        cancel_btn.setFont(QFont("Segoe UI", 11))
        cancel_btn.setFixedSize(100, 40)
        cancel_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.hover_color};
                color: {self.fg_color};
                border: none;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {self.entry_bg};
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton(t("settings_save"))
        save_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        save_btn.setFixedSize(120, 40)
        save_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.accent_color};
                color: white;
                border: none;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: #1084d8;
            }}
        """)
        save_btn.clicked.connect(self._save_settings)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
        
        # === Ayar değişikliği bağlantıları (dişli çark animasyonu için) ===
        self.quality_slider.valueChanged.connect(self._on_setting_changed)
        self.sound_combo.currentIndexChanged.connect(self._on_setting_changed)
        self.sound_enabled_check.stateChanged.connect(self._on_setting_changed)
        self.notification_check.stateChanged.connect(self._on_setting_changed)
        self.lang_combo.currentIndexChanged.connect(self._on_setting_changed)
        self.path_entry.textChanged.connect(self._on_setting_changed)
        # Format radyo butonları
        for rb in self.format_radios.values():
            rb.toggled.connect(self._on_setting_changed)
    
    def _add_section_label(self, layout, text):
        """Bölüm etiketi ekle."""
        label = QLabel(text)
        label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        label.setStyleSheet(f"color: {self.accent_color}; margin-top: 8px;")
        layout.addWidget(label)
    
    def _on_setting_changed(self):
        """Herhangi bir ayar değiştiğinde dişli çarkı döndür."""
        if hasattr(self, 'gear_label'):
            self.gear_label.start_spin()
    
    def _on_dark_mode_change(self, state):
        """Karanlık mod değiştiğinde."""
        self.is_dark_mode = state == Qt.CheckState.Checked.value
        theme_icon = "🌙" if self.is_dark_mode else "☀️"
        self.theme_btn.setText(theme_icon)
        self._apply_theme()
        self._on_setting_changed()  # Dişli çarkı döndür
    
    def _get_screen_resolution(self):
        """Ekran çözünürlüğünü al."""
        try:
            import ctypes
            user32 = ctypes.windll.user32
            width = user32.GetSystemMetrics(0)
            height = user32.GetSystemMetrics(1)
            return width, height
        except:
            return 1920, 1080
    
    def _estimate_file_size(self, format_type: str, quality: int) -> str:
        """Tahmini dosya boyutunu hesapla."""
        width, height = self._get_screen_resolution()
        raw_size = width * height * 3
        
        if format_type == "bmp":
            size_bytes = raw_size
        elif format_type == "png":
            size_bytes = raw_size * 0.40
        elif format_type in ["jpg", "jpeg"]:
            compression_ratio = 0.05 + (quality / 100) * 0.55
            size_bytes = raw_size * compression_ratio
        elif format_type == "webp":
            compression_ratio = 0.03 + (quality / 100) * 0.40
            size_bytes = raw_size * compression_ratio
        else:
            size_bytes = raw_size * 0.30
        
        if size_bytes >= 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / 1024:.0f} KB"
    
    def _on_format_change(self):
        """Format değiştiğinde kalite slider'ını güncelle."""
        format_type = self._get_selected_format()
        
        lossless_msg = "ℹ️ " + ("Kayıpsız format" if get_language() == "tr" else "Lossless format")
        
        if format_type in ["png", "bmp"]:
            self.quality_slider.setEnabled(False)
            self.quality_slider.setValue(100)
            self.lossless_info.setText(lossless_msg)
        else:
            self.quality_slider.setEnabled(True)
            self.lossless_info.setText("")
        
        self._update_quality_label()
    
    def _get_selected_format(self):
        """Seçili formatı al."""
        for fmt, rb in self.format_radios.items():
            if rb.isChecked():
                return fmt
        return "png"
    
    def _update_quality_label(self):
        """Kalite etiketini güncelle."""
        quality = self.quality_slider.value()
        format_type = self._get_selected_format()
        size_estimate = self._estimate_file_size(format_type, quality)
        self.quality_label.setText(f"{quality}% (~{size_estimate})")
    
    def _browse_folder(self):
        """Klasör seçme dialogu."""
        title = "Select Screenshot Folder" if get_language() == "en" else "Ekran Görüntüsü Klasörü Seç"
        folder = QFileDialog.getExistingDirectory(
            self,
            title,
            self.path_entry.text()
        )
        if folder:
            self.path_entry.setText(folder)
    
    def _start_key_listener(self):
        """Tuş dinlemeye başla."""
        if self._listening_for_key:
            return
        
        self._listening_for_key = True
        self.hotkey_btn.setText(t("settings_waiting_key"))
        self.hotkey_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
            }
        """)
        
        self.key_listener_thread = KeyListenerThread()
        self.key_listener_thread.key_pressed.connect(self._set_hotkey)
        self.key_listener_thread.start()
    
    def _set_hotkey(self, key: str):
        """Kısayol tuşunu ayarla."""
        self._listening_for_key = False
        self.hotkey_display.setText(key)
        self.hotkey_btn.setText(t("settings_click_to_set"))
        self.hotkey_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.accent_color};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
            }}
            QPushButton:hover {{
                background-color: #1084d8;
            }}
        """)
        self.hotkey_status.setText(f"✓ {key}")
        self.hotkey_status.setStyleSheet("color: #4caf50;")
    
    def _test_sound(self):
        """Seçilen sesi test et."""
        sound_idx = self.sound_combo.currentIndex()
        
        if sound_idx < len(self.sound_options):
            _, filename = self.sound_options[sound_idx]
            if filename == "none":
                return
            
            sounds_dir = Path(__file__).parent.parent / "sounds"
            sound_path = sounds_dir / filename
            
            if sound_path.exists():
                try:
                    import winsound
                    winsound.PlaySound(str(sound_path), winsound.SND_FILENAME | winsound.SND_ASYNC)
                except Exception as e:
                    print(f"Sound error: {e}")
    
    def _load_current_settings(self):
        """Mevcut ayarları yükle."""
        self.hotkey_display.setText(self.config.get("hotkey", "F12"))
        
        format_type = self.config.get("format", "png")
        if format_type in self.format_radios:
            self.format_radios[format_type].setChecked(True)
        
        self.quality_slider.setValue(self.config.get("quality", 95))
        self.path_entry.setText(self.config.get("save_path", ""))
        self.notification_check.setChecked(self.config.get("show_notification", True))
        self.sound_enabled_check.setChecked(self.config.get("play_sound", True))
        self.dark_mode_check.setChecked(self.config.get("dark_mode", True))
        
        # Ses seçimi
        sound_file = self.config.get("sound_file", "none")
        for i, (name, filename) in enumerate(self.sound_options):
            if filename == sound_file:
                self.sound_combo.setCurrentIndex(i)
                break
        
        # Dil seçimi
        current_lang = self.config.get("language", "tr")
        for i, lang in enumerate(self.available_languages):
            if lang["code"] == current_lang:
                self.lang_combo.setCurrentIndex(i)
                break
        
        # Monitör
        monitor = self.config.get("monitor", 0)
        self._update_monitor_label(monitor)
        
        self._on_format_change()
    
    def _update_monitor_label(self, monitor_id: int):
        """Monitör etiketini güncelle."""
        if monitor_id == -1:
            self.monitor_display.setText(t("settings_all_monitors"))
        elif monitor_id == 0:
            text = f"{t('settings_monitor_n')} 1 ({t('monitor_primary')})"
            self.monitor_display.setText(text)
        else:
            self.monitor_display.setText(f"{t('settings_monitor_n')} {monitor_id + 1}")
    
    def _open_monitor_selector(self):
        """Monitör seçici penceresini aç."""
        try:
            from monitor_selector import MonitorSelector
            
            def on_monitor_selected(monitor_id):
                self.config["monitor"] = monitor_id
                self._update_monitor_label(monitor_id)
            
            # Tema bilgisini geçir
            selector = MonitorSelector(self, on_monitor_selected, dark_mode=self.is_dark_mode)
            selector.exec()
        except Exception as e:
            print(f"Monitor selector error: {e}")
    
    def _save_settings(self):
        """Ayarları kaydet."""
        # Ses dosya adını bul
        sound_file = "none"
        sound_idx = self.sound_combo.currentIndex()
        if sound_idx < len(self.sound_options):
            _, sound_file = self.sound_options[sound_idx]
        
        # Dil
        lang_idx = self.lang_combo.currentIndex()
        language = self.available_languages[lang_idx]["code"] if lang_idx < len(self.available_languages) else "tr"
        
        new_config = {
            "hotkey": self.hotkey_display.text(),
            "format": self._get_selected_format(),
            "quality": self.quality_slider.value(),
            "save_path": self.path_entry.text(),
            "naming_pattern": self.config.get("naming_pattern", "{app}_{date}_{time}"),
            "show_notification": self.notification_check.isChecked(),
            "play_sound": self.sound_enabled_check.isChecked(),
            "sound_file": sound_file,
            "dark_mode": self.is_dark_mode,
            "monitor": self.config.get("monitor", 0),
            "language": language
        }
        
        if save_config(new_config):
            if self.on_save_callback:
                self.on_save_callback(new_config)
            
            msg = "Settings saved!" if language == "en" else "Ayarlar kaydedildi!"
            title = "Success" if language == "en" else "Başarılı"
            QMessageBox.information(self, title, msg)
            self.accept()
        else:
            msg = "Could not save settings!" if language == "en" else "Ayarlar kaydedilemedi!"
            title = "Error" if language == "en" else "Hata"
            QMessageBox.critical(self, title, msg)
    
    def show(self):
        """Pencereyi göster."""
        self.exec()


def open_settings(parent=None, on_save_callback=None):
    """Ayarlar penceresini aç."""
    dialog = SettingsDialog(parent, on_save_callback)
    return dialog


if __name__ == "__main__":
    # Test
    app = QApplication(sys.argv)
    dialog = SettingsDialog()
    dialog.show()
    sys.exit(app.exec())
