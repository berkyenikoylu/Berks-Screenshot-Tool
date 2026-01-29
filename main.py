"""
Berk's Screenshot Tool - Windows Ekran Görüntüsü Aracı
Ana uygulama ve sistem tepsisi.
"""

import os
import sys
import threading
import subprocess
from pathlib import Path

# PIL ve pystray import
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as Item

# Yerel modüller
from config import load_config, get_save_path, update_config
from capture import take_screenshot, cleanup_dxcam
from hotkeys import start_hotkey_listener, stop_hotkey_listener, hotkey_manager
from detector import get_foreground_app
from notification import show_notification
from i18n import t, get_language


class BerksScreenshotTool:
    """Ana uygulama sınıfı."""
    
    def __init__(self):
        self.config = load_config()
        self.icon = None
        self.running = False
        self._screenshot_count = 0
        self._last_screenshot_time = 0  # Cooldown için son screenshot zamanı
        self._screenshot_cooldown = 1.0  # Minimum 1 saniye bekleme
    
    def create_icon_image(self, color="green"):
        """Sistem tepsisi simgesi oluştur."""
        size = 64
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Kamera simgesi çiz
        if color == "green":
            fill_color = (76, 175, 80)  # Yeşil - aktif
        elif color == "red":
            fill_color = (244, 67, 54)  # Kırmızı - yakalama anı
        else:
            fill_color = (158, 158, 158)  # Gri - pasif
        
        # Kamera gövdesi
        draw.rounded_rectangle([8, 16, 56, 48], radius=5, fill=fill_color)
        
        # Kamera lensi
        draw.ellipse([24, 22, 44, 42], fill=(255, 255, 255))
        draw.ellipse([28, 26, 40, 38], fill=fill_color)
        
        # Flaş
        draw.rectangle([44, 18, 52, 24], fill=(255, 255, 255))
        
        return image
    
    def play_capture_sound(self):
        """Yakalama sesi çal."""
        if not self.config.get("play_sound", True):
            return
        
        sound_file = self.config.get("sound_file", "none")
        if sound_file == "none":
            return
        
        try:
            import winsound
            sounds_dir = Path(__file__).parent / "sounds"
            sound_path = sounds_dir / sound_file
            
            if sound_path.exists():
                winsound.PlaySound(str(sound_path), winsound.SND_FILENAME | winsound.SND_ASYNC)
            else:
                # Varsayılan Windows sesi
                winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)
        except:
            pass
    
    def on_screenshot_hotkey(self):
        """Kısayol tuşuna basıldığında çağrılır."""
        import time
        
        # Cooldown kontrolü - tuş basılı kalsa bile hızlı çekim engellenir
        current_time = time.time()
        if current_time - self._last_screenshot_time < self._screenshot_cooldown:
            return  # Cooldown süresi dolmadı, atlat
        
        self._last_screenshot_time = current_time
        
        # Her ekran görüntüsünde ayarları yeniden yükle (ses, format vb. için)
        self.config = load_config()
        self._screenshot_count += 1
        
        # Ekran görüntüsü al
        success, filepath, app_name = take_screenshot()
        
        if success:
            # Ses çal
            self.play_capture_sound()
            
            # iPhone tarzı bildirim göster
            if self.config.get("show_notification", True):
                dark_mode = self.config.get("dark_mode", True)
                show_notification(filepath.name, duration=2.0, dark_mode=dark_mode)
            
            print(f"✓ [{self._screenshot_count}] {t('saved')}: {filepath}")
        else:
            print(f"✗ {t('screenshot_failed')}")
    
    def open_screenshots_folder(self, icon=None, item=None):
        """Ekran görüntüleri klasörünü aç."""
        save_path = get_save_path()
        os.startfile(str(save_path))
    
    def open_settings(self, icon=None, item=None):
        """Ayarlar penceresini aç."""
        import subprocess
        import sys
        import time
        
        # Mevcut hotkey'i kaydet
        old_hotkey = self.config.get("hotkey", "F12")
        
        # Ayarları ayrı process olarak aç (PyQt6 thread sorunu çözümü)
        settings_script = Path(__file__).parent / "ui" / "settings_dialog.py"
        subprocess.Popen([sys.executable, str(settings_script)], 
                       creationflags=subprocess.CREATE_NO_WINDOW)
        
        # Config değişikliğini kontrol eden thread
        def check_config_changes():
            time.sleep(1)  # Ayarlar penceresinin açılmasını bekle
            
            old_hotkey = self.config.get("hotkey", "F12")
            old_language = self.config.get("language", "tr")
            last_config = self.config.copy()
            
            while True:
                time.sleep(0.5)  # Her 500ms'de bir kontrol et
                
                try:
                    new_config = load_config()
                    new_hotkey = new_config.get("hotkey", "F12")
                    new_language = new_config.get("language", "tr")
                    
                    # Hotkey değiştiyse güncelle
                    if new_hotkey != old_hotkey:
                        print(f"[Settings] Hotkey: {old_hotkey} -> {new_hotkey}")
                        hotkey_manager.update_hotkey(new_hotkey)
                        old_hotkey = new_hotkey
                        self.config = new_config
                    
                    # Dil değiştiyse güncelle ve menüyü yenile
                    if new_language != old_language:
                        print(f"[Settings] Language: {old_language} -> {new_language}")
                        old_language = new_language
                        self.config = new_config
                        # Menüyü yeniden oluştur
                        if self.icon:
                            self.icon.menu = self.create_menu()
                            self.icon.update_menu()
                    
                    # Diğer değişiklikler için de config'i güncelle
                    if new_config != last_config:
                        self.config = new_config
                        last_config = new_config.copy()
                        
                except:
                    pass
                
                # 60 saniye sonra timeout (ayarlar uzun süre açık kalabilir)
                if time.time() - start_time > 60:
                    break
            
            # Son kontrol - thread bittiğinde güncel config'i al
            self.config = load_config()
        
        start_time = time.time()
        threading.Thread(target=check_config_changes, daemon=True).start()
    
    def take_screenshot_now(self, icon=None, item=None):
        """Menüden ekran görüntüsü al."""
        self.on_screenshot_hotkey()
    
    def quit_app(self, icon=None, item=None):
        """Uygulamadan çık."""
        self.running = False
        stop_hotkey_listener()
        cleanup_dxcam()  # DXcam kaynaklarını temizle
        if self.icon:
            self.icon.stop()
    
    def create_menu(self):
        """Sistem tepsisi menüsü oluştur - dinamik dil desteği ile."""
        # Lambda kullanarak her seferinde güncel dil çevirisini al
        return pystray.Menu(
            Item(lambda text: t("menu_take_screenshot"), self.take_screenshot_now, default=True),
            Item(lambda text: t("menu_open_folder"), self.open_screenshots_folder),
            pystray.Menu.SEPARATOR,
            Item(lambda text: t("menu_settings"), self.open_settings),
            pystray.Menu.SEPARATOR,
            Item(lambda text: t("menu_exit"), self.quit_app)
        )
    
    def run(self):
        """Uygulamayı başlat."""
        theme = t("theme_dark") if self.config.get("dark_mode", True) else t("theme_light")
        
        print("=" * 50)
        print(f"  {t('console_title')}")
        print("=" * 50)
        print(f"  {t('hotkey_label')}: {self.config.get('hotkey', 'F12')}")
        print(f"  {t('format_label')}: {self.config.get('format', 'png').upper()}")
        print(f"  {t('save_path_label')}: {self.config.get('save_path')}")
        print(f"  {t('theme_label')}: {theme}")
        print("=" * 50)
        print(f"  {t('running_in_tray')}")
        print(f"  {t('exit_hint')}")
        print("=" * 50)
        
        self.running = True
        
        # Kısayol dinleyiciyi başlat
        start_hotkey_listener(self.on_screenshot_hotkey)
        
        # Sistem tepsisi simgesi oluştur
        self.icon = pystray.Icon(
            "BerksScreenshotTool",
            self.create_icon_image(),
            t("app_name"),
            self.create_menu()
        )
        
        # Tepsi simgesini çalıştır (bu blocking bir çağrı)
        self.icon.run()


def main():
    """Ana giriş noktası."""
    app = BerksScreenshotTool()
    app.run()


if __name__ == "__main__":
    main()
