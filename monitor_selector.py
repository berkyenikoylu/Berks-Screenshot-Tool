"""
Berk's Screenshot Tool - Monitör Seçici (PyQt6)
Çoklu monitör desteği ve görsel monitör seçimi.
"""

from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QWidget, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QCursor
from typing import List, Optional
import sys
import os
import mss

# Ana modülü import edebilmek için path ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import load_config, save_config
from i18n import t


def get_monitors_info() -> List[dict]:
    """
    Tüm monitörlerin bilgilerini al.
    Returns: [{"id": 1, "name": "Monitor 1", "width": 1920, "height": 1080, "x": 0, "y": 0, "primary": True}, ...]
    """
    monitors = []
    
    with mss.mss() as sct:
        # monitors[0] tüm monitörlerin birleşimi, gerçek monitörler 1'den başlar
        for i, mon in enumerate(sct.monitors[1:], start=1):
            monitors.append({
                "id": i,
                "name": f"{t('settings_monitor_n')} {i}",
                "width": mon["width"],
                "height": mon["height"],
                "x": mon["left"],
                "y": mon["top"],
                "primary": i == 1  # İlk monitör genellikle birincil
            })
    
    return monitors


class MonitorCard(QFrame):
    """Tek bir monitör kartı widget'ı."""
    
    clicked = pyqtSignal(int)
    
    def __init__(self, monitor_id: int, name: str, resolution: str, 
                 is_primary: bool, is_selected: bool, dark_mode: bool):
        super().__init__()
        self.monitor_id = monitor_id
        self.is_selected = is_selected
        self.dark_mode = dark_mode
        
        # Sabit boyut
        self.setFixedSize(130, 130)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        # Layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(5)
        
        # Monitör ikonu
        icon_label = QLabel("🖥️")
        icon_label.setFont(QFont("Segoe UI Emoji", 28))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        # Monitör adı
        name_label = QLabel(name)
        name_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name_label)
        
        # Çözünürlük
        res_label = QLabel(resolution)
        res_label.setFont(QFont("Segoe UI", 9))
        res_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        res_label.setStyleSheet("color: #888888;")
        layout.addWidget(res_label)
        
        # Birincil badge
        if is_primary:
            primary_label = QLabel(t("monitor_primary"))
            primary_label.setFont(QFont("Segoe UI", 8))
            primary_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            primary_label.setStyleSheet("color: #4caf50;")
            layout.addWidget(primary_label)
        
        self._update_style()
    
    def _update_style(self):
        """Kart stilini güncelle."""
        if self.is_selected:
            bg_color = "#0078d4"
            border_color = "#0078d4"
        else:
            bg_color = "#3d3d3d" if self.dark_mode else "#e0e0e0"
            border_color = "#4d4d4d" if self.dark_mode else "#d0d0d0"
        
        fg_color = "#ffffff" if self.dark_mode or self.is_selected else "#1e1e1e"
        
        self.setStyleSheet(f"""
            MonitorCard {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 8px;
            }}
            QLabel {{
                color: {fg_color};
                background: transparent;
            }}
        """)
    
    def set_selected(self, selected: bool):
        """Seçili durumunu değiştir."""
        self.is_selected = selected
        self._update_style()
    
    def mousePressEvent(self, event):
        """Tıklama olayı."""
        self.clicked.emit(self.monitor_id)


class MonitorSelector(QDialog):
    """Görsel monitör seçici penceresi."""
    
    _app_instance = None  # QApplication referansını tut
    
    def __init__(self, parent=None, on_select_callback=None, dark_mode=None):
        # QApplication yoksa oluştur
        if QApplication.instance() is None:
            MonitorSelector._app_instance = QApplication(sys.argv)
        
        super().__init__(parent)
        self.on_select_callback = on_select_callback
        self.config = load_config()
        # dark_mode parametresi verilmişse onu kullan, yoksa config'den oku
        self.is_dark_mode = dark_mode if dark_mode is not None else self.config.get("dark_mode", True)
        self.selected_monitor = self.config.get("monitor", 0)
        self.monitor_cards = []
        
        self._setup_window()
        self._create_widgets()
    
    def _setup_window(self):
        """Pencere ayarları."""
        self.setWindowTitle(t("monitor_selector_title"))
        self.setFixedSize(500, 350)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        
        # Tema
        if self.is_dark_mode:
            self.setStyleSheet("""
                QDialog {
                    background-color: #1e1e1e;
                }
                QLabel {
                    color: #ffffff;
                }
            """)
        else:
            self.setStyleSheet("""
                QDialog {
                    background-color: #f5f5f5;
                }
                QLabel {
                    color: #1e1e1e;
                }
            """)
    
    def _create_widgets(self):
        """Widget'ları oluştur."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 20, 30, 20)
        
        # Başlık
        title_label = QLabel(t("monitor_selector_title"))
        title_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Açıklama
        desc_label = QLabel(t("monitor_selector_desc"))
        desc_label.setFont(QFont("Segoe UI", 10))
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("color: #888888;")
        layout.addWidget(desc_label)
        
        # Kartlar container
        cards_widget = QWidget()
        cards_layout = QHBoxLayout(cards_widget)
        cards_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cards_layout.setSpacing(15)
        
        # "Tüm Monitörler" seçeneği
        all_card = MonitorCard(
            monitor_id=-1,
            name=t("settings_all_monitors"),
            resolution=t("monitor_combined"),
            is_primary=False,
            is_selected=(self.selected_monitor == -1),
            dark_mode=self.is_dark_mode
        )
        all_card.clicked.connect(self._on_card_clicked)
        cards_layout.addWidget(all_card)
        self.monitor_cards.append(all_card)
        
        # Her monitör için kart
        monitors = get_monitors_info()
        for mon in monitors:
            card = MonitorCard(
                monitor_id=mon["id"] - 1,  # 0-indexed
                name=mon["name"],
                resolution=f"{mon['width']}×{mon['height']}",
                is_primary=mon["primary"],
                is_selected=(self.selected_monitor == mon["id"] - 1),
                dark_mode=self.is_dark_mode
            )
            card.clicked.connect(self._on_card_clicked)
            cards_layout.addWidget(card)
            self.monitor_cards.append(card)
        
        layout.addWidget(cards_widget)
        layout.addStretch()
        
        # Kaydet butonu
        save_btn = QPushButton(t("settings_save"))
        save_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        save_btn.setFixedSize(150, 45)
        save_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #1084d8;
            }
            QPushButton:pressed {
                background-color: #006cbd;
            }
        """)
        save_btn.clicked.connect(self._save_selection)
        
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_layout.addWidget(save_btn)
        layout.addWidget(btn_container)
    
    def _on_card_clicked(self, monitor_id: int):
        """Kart tıklandığında."""
        self.selected_monitor = monitor_id
        
        # Tüm kartların seçili durumunu güncelle
        for card in self.monitor_cards:
            card.set_selected(card.monitor_id == monitor_id)
    
    def _save_selection(self):
        """Seçimi kaydet ve pencereyi kapat."""
        self.config["monitor"] = self.selected_monitor
        save_config(self.config)
        
        if self.on_select_callback:
            self.on_select_callback(self.selected_monitor)
        
        self.accept()
    
    def show(self):
        """Pencereyi göster."""
        self.exec()


def show_monitor_selector(parent=None, on_select_callback=None):
    """Monitör seçici penceresini göster."""
    selector = MonitorSelector(parent, on_select_callback)
    return selector


if __name__ == "__main__":
    # Test
    monitors = get_monitors_info()
    print("Found monitors:")
    for mon in monitors:
        print(f"  {mon['name']}: {mon['width']}x{mon['height']} @ ({mon['x']}, {mon['y']})")
    
    app = QApplication(sys.argv)
    selector = MonitorSelector()
    selector.show()
    sys.exit(app.exec())
