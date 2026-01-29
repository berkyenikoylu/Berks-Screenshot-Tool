"""
GameCapture - Oyun ve Uygulama Algılama
Aktif pencereyi, işlem adını ve tam ekran durumunu algılar.
"""

import ctypes
from ctypes import wintypes
import win32gui
import win32process
import win32api
import win32con
import psutil
from pathlib import Path

# Windows API sabitleri
user32 = ctypes.windll.user32


def get_foreground_window_handle() -> int:
    """Aktif (ön plan) pencerenin handle'ını al."""
    return win32gui.GetForegroundWindow()


def get_window_title(hwnd: int) -> str:
    """Pencere başlığını al."""
    try:
        return win32gui.GetWindowText(hwnd)
    except:
        return ""


def get_process_from_window(hwnd: int) -> dict:
    """Pencereden işlem bilgilerini al."""
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        return {
            "pid": pid,
            "name": process.name(),
            "exe": process.exe()
        }
    except (psutil.NoSuchProcess, psutil.AccessDenied, Exception):
        return {
            "pid": 0,
            "name": "Unknown",
            "exe": ""
        }


def get_monitor_info(hwnd: int) -> dict:
    """Pencerenin bulunduğu monitör bilgilerini al."""
    try:
        monitor = win32api.MonitorFromWindow(hwnd, win32con.MONITOR_DEFAULTTONEAREST)
        monitor_info = win32api.GetMonitorInfo(monitor)
        return {
            "work_area": monitor_info["Work"],
            "monitor_area": monitor_info["Monitor"]
        }
    except:
        # Varsayılan ekran boyutları
        return {
            "work_area": (0, 0, 1920, 1080),
            "monitor_area": (0, 0, 1920, 1080)
        }


def is_fullscreen(hwnd: int = None) -> bool:
    """Pencerenin tam ekran olup olmadığını kontrol et."""
    if hwnd is None:
        hwnd = get_foreground_window_handle()
    
    if not hwnd:
        return False
    
    try:
        # Pencere boyutlarını al
        rect = win32gui.GetWindowRect(hwnd)
        window_width = rect[2] - rect[0]
        window_height = rect[3] - rect[1]
        
        # Monitör boyutlarını al
        monitor_info = get_monitor_info(hwnd)
        monitor_rect = monitor_info["monitor_area"]
        monitor_width = monitor_rect[2] - monitor_rect[0]
        monitor_height = monitor_rect[3] - monitor_rect[1]
        
        # Pencere monitörü tamamen kaplıyor mu?
        is_full = (window_width >= monitor_width and window_height >= monitor_height)
        
        return is_full
    except:
        return False


def clean_app_name(process_name: str, window_title: str) -> str:
    """İşlem adından temiz bir uygulama adı oluştur."""
    # .exe uzantısını kaldır
    name = process_name.replace(".exe", "").replace(".EXE", "")
    
    # Bilinen sistem işlemleri için pencere başlığını kullan
    system_processes = ["explorer", "ApplicationFrameHost", "TextInputHost"]
    if name in system_processes and window_title:
        # Pencere başlığından ilk anlamlı kısmı al
        name = window_title.split(" - ")[0].split(" | ")[0]
    
    # Özel karakterleri temizle (dosya adı için)
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, "")
    
    # Boşlukları ve fazla karakterleri düzelt
    name = name.strip()
    if not name:
        name = "Screen"
    
    return name


def get_foreground_app() -> dict:
    """Aktif uygulamanın tüm bilgilerini al."""
    hwnd = get_foreground_window_handle()
    
    if not hwnd:
        return {
            "process_name": "Desktop",
            "window_title": "Desktop",
            "clean_name": "Desktop",
            "is_fullscreen": False,
            "hwnd": 0
        }
    
    window_title = get_window_title(hwnd)
    process_info = get_process_from_window(hwnd)
    fullscreen = is_fullscreen(hwnd)
    clean_name = clean_app_name(process_info["name"], window_title)
    
    return {
        "process_name": process_info["name"],
        "window_title": window_title,
        "clean_name": clean_name,
        "is_fullscreen": fullscreen,
        "hwnd": hwnd,
        "pid": process_info["pid"],
        "exe_path": process_info["exe"]
    }


if __name__ == "__main__":
    # Test
    import time
    print("5 saniye içinde bir pencereye tıklayın...")
    time.sleep(5)
    info = get_foreground_app()
    print(f"\nAktif Uygulama Bilgileri:")
    print(f"  İşlem Adı: {info['process_name']}")
    print(f"  Pencere Başlığı: {info['window_title']}")
    print(f"  Temiz Ad: {info['clean_name']}")
    print(f"  Tam Ekran: {info['is_fullscreen']}")
