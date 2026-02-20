"""
GameCapture - Global Kısayol Tuşu Yönetimi
Oyunlarda bile çalışan sistem genelinde kısayol tuşları.
"""

import keyboard
import threading
from typing import Callable, Optional
from config import load_config


class HotkeyManager:
    """Global kısayol tuşu yöneticisi."""
    
    def __init__(self):
        self._callback: Optional[Callable] = None
        self._hotkey: Optional[str] = None
        self._running = False
        self._hook = None
    
    def set_callback(self, callback: Callable):
        """Kısayol tuşuna basıldığında çağrılacak fonksiyonu ayarla."""
        self._callback = callback
    
    def _on_hotkey(self):
        """Kısayol tuşu basıldığında çağrılır."""
        if self._callback:
            # Callback'i ayrı thread'de çalıştır (UI donmasını önle)
            threading.Thread(target=self._callback, daemon=True).start()
    
    def start(self, hotkey: str = None):
        """Kısayol dinleyiciyi başlat."""
        if self._running:
            self.stop()
        
        config = load_config()
        self._hotkey = hotkey or config.get("hotkey", "F12")
        
        try:
            # Global kısayol kaydet
            keyboard.add_hotkey(self._hotkey, self._on_hotkey, suppress=False)
            self._running = True
            print(f"🎮 Kısayol tuşu aktif: {self._hotkey}")
            return True
        except Exception as e:
            print(f"Kısayol tuşu hatası: {e}")
            return False
    
    def stop(self):
        """Kısayol dinleyiciyi durdur."""
        if self._running and self._hotkey:
            try:
                keyboard.remove_hotkey(self._hotkey)
            except:
                pass
            self._running = False
            self._hotkey = None
        
        # Tüm hook'ları temizle - process'in kapanabilmesi için
        try:
            keyboard.unhook_all()
        except:
            pass
    
    def update_hotkey(self, new_hotkey: str):
        """Kısayol tuşunu değiştir."""
        print(f"[Hotkey] Güncelleme başlıyor: {self._hotkey} -> {new_hotkey}")
        
        callback = self._callback
        old_hotkey = self._hotkey
        
        # Eski hotkey'i kaldır
        if self._running and old_hotkey:
            try:
                keyboard.remove_hotkey(old_hotkey)
                print(f"[Hotkey] Eski hotkey kaldırıldı: {old_hotkey}")
            except Exception as e:
                print(f"[Hotkey] Eski hotkey kaldırma hatası: {e}")
        
        self._running = False
        self._hotkey = None
        self._callback = callback
        
        # Yeni hotkey'i ekle
        result = self.start(new_hotkey)
        print(f"[Hotkey] Yeni hotkey sonucu: {result}")
        return result
    
    def is_running(self) -> bool:
        """Dinleyicinin çalışıp çalışmadığını kontrol et."""
        return self._running


# Global instance
hotkey_manager = HotkeyManager()


def start_hotkey_listener(callback: Callable, hotkey: str = None) -> bool:
    """Kısayol dinleyiciyi başlat."""
    hotkey_manager.set_callback(callback)
    return hotkey_manager.start(hotkey)


def stop_hotkey_listener():
    """Kısayol dinleyiciyi durdur."""
    hotkey_manager.stop()


if __name__ == "__main__":
    # Test
    def test_callback():
        print("📸 Kısayol tuşuna basıldı!")
    
    print("F12 tuşuna basarak test edin. Çıkmak için Ctrl+C...")
    start_hotkey_listener(test_callback, "F12")
    
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        stop_hotkey_listener()
        print("\nDurduruldu.")
