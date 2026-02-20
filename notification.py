"""
GameCapture - Özel Bildirim Sistemi
Windows Toast tarzı bildirim - subprocess ile güvenilir.
"""

import subprocess
import sys
import os


def show_notification(message: str = "", duration: float = 2.0, dark_mode: bool = True, title: str = "Screenshot Taken"):
    """
    Bildirim göster - ayrı bir Python process'inde çalışır.
    Bu yaklaşım Tkinter thread sorunlarını tamamen önler.
    """
    try:
        # EXE mi yoksa Python script mi kontrol et
        if getattr(sys, 'frozen', False):
            # Frozen EXE - notification modunu ayrı process olarak başlat
            subprocess.Popen(
                [sys.executable, "--notification", message, str(duration), str(dark_mode), title],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        else:
            # Python script - doğrudan _notification_process.py'yi çalıştır
            script_path = os.path.join(os.path.dirname(__file__), "_notification_process.py")
            subprocess.Popen(
                [sys.executable, script_path, message, str(duration), str(dark_mode), title],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
    except Exception as e:
        print(f"Bildirim baslatilamadi: {e}")


if __name__ == "__main__":
    # Test
    import time
    print("Bildirim testi başlıyor...")
    show_notification("Test_Screenshot_2026-01-24.webp", duration=2.0, dark_mode=True)
    time.sleep(5)
    show_notification("Light mode test", duration=2.0, dark_mode=False)
    time.sleep(5)
    print("Test tamamlandı.")
