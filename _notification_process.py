"""
GameCapture - Bildirim Process (PyQt6)
Bu script ayrı bir process olarak çalışır ve ana uygulamayı bloklamaz.
Doğrudan çalıştırılmak için tasarlanmıştır.
"""

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QFont
import sys


class NotificationWidget(QWidget):
    """Bildirim penceresi widget'ı."""
    
    def __init__(self, message: str, duration: float, dark_mode: bool):
        super().__init__()
        self.message = message
        self.duration = duration
        self.dark_mode = dark_mode
        
        self._setup_window()
        self._create_widgets()
        self._start_animation()
    
    def _setup_window(self):
        """Pencere ayarları."""
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Boyut
        self.width_size = 300
        self.height_size = 80
        
        # Pozisyon hesapla
        screen = QApplication.primaryScreen().geometry()
        self.x_pos = (screen.width() - self.width_size) // 2
        self.start_y = -self.height_size
        self.end_y = 50
        
        self.setGeometry(self.x_pos, self.start_y, self.width_size, self.height_size)
    
    def _create_widgets(self):
        """Widget'ları oluştur."""
        # Tema renkleri
        if self.dark_mode:
            bg_color = "#1e1e1e"
            fg_color = "#ffffff"
            accent_color = "#0078d4"
        else:
            bg_color = "#ffffff"
            fg_color = "#1e1e1e"
            accent_color = "#0078d4"
        
        # Ana container
        container = QFrame(self)
        container.setGeometry(0, 0, self.width_size, self.height_size)
        container.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 2px solid {accent_color};
                border-radius: 10px;
            }}
        """)
        
        # Layout
        layout = QHBoxLayout(container)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(15)
        
        # Kamera ikonu
        icon_label = QLabel("📸")
        icon_label.setFont(QFont("Segoe UI Emoji", 24))
        icon_label.setStyleSheet(f"color: {fg_color}; background: transparent; border: none;")
        layout.addWidget(icon_label)
        
        # Metin container
        text_widget = QWidget()
        text_widget.setStyleSheet("background: transparent; border: none;")
        text_layout = QHBoxLayout(text_widget)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(0)
        
        # Metin widget
        from PyQt6.QtWidgets import QVBoxLayout
        text_inner = QWidget()
        text_inner.setStyleSheet("background: transparent; border: none;")
        text_inner_layout = QVBoxLayout(text_inner)
        text_inner_layout.setContentsMargins(0, 0, 0, 0)
        text_inner_layout.setSpacing(2)
        
        # Başlık
        title_label = QLabel("Ekran Görüntüsü Alındı")
        title_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {fg_color}; background: transparent; border: none;")
        text_inner_layout.addWidget(title_label)
        
        # Dosya adı
        display_message = self.message
        if len(display_message) > 35:
            display_message = display_message[:32] + "..."
        
        msg_label = QLabel(display_message)
        msg_label.setFont(QFont("Segoe UI", 9))
        msg_label.setStyleSheet("color: #888888; background: transparent; border: none;")
        text_inner_layout.addWidget(msg_label)
        
        text_layout.addWidget(text_inner)
        layout.addWidget(text_widget, 1)
    
    def _start_animation(self):
        """Animasyonu başlat."""
        # Giriş animasyonu
        self.anim_in = QPropertyAnimation(self, b"geometry")
        self.anim_in.setDuration(300)
        self.anim_in.setStartValue(QRect(self.x_pos, self.start_y, self.width_size, self.height_size))
        self.anim_in.setEndValue(QRect(self.x_pos, self.end_y, self.width_size, self.height_size))
        self.anim_in.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim_in.finished.connect(self._wait_and_hide)
        self.anim_in.start()
    
    def _wait_and_hide(self):
        """Bekle ve çıkış animasyonu başlat."""
        QTimer.singleShot(int(self.duration * 1000), self._start_hide_animation)
    
    def _start_hide_animation(self):
        """Çıkış animasyonu."""
        self.anim_out = QPropertyAnimation(self, b"geometry")
        self.anim_out.setDuration(300)
        self.anim_out.setStartValue(QRect(self.x_pos, self.end_y, self.width_size, self.height_size))
        self.anim_out.setEndValue(QRect(self.x_pos, self.start_y, self.width_size, self.height_size))
        self.anim_out.setEasingCurve(QEasingCurve.Type.InCubic)
        self.anim_out.finished.connect(self._close_app)
        self.anim_out.start()
    
    def _close_app(self):
        """Uygulamayı kapat."""
        QApplication.quit()


def main():
    if len(sys.argv) < 4:
        print("Kullanım: python _notification_process.py <message> <duration> <dark_mode>")
        sys.exit(1)
    
    message = sys.argv[1]
    duration = float(sys.argv[2])
    dark_mode = sys.argv[3].lower() == "true"
    
    try:
        app = QApplication(sys.argv)
        notification = NotificationWidget(message, duration, dark_mode)
        notification.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Bildirim hatası: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
