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
from config import load_config, get_save_path, update_config, get_resource_dir, get_app_dir
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
        self._settings_proc = None  # Ayarlar subprocess
    
    def create_icon_image(self, color="green"):
        """Sistem tepsisi simgesi oluştur."""
        size = 64
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Kamera simgesi çiz - Yeni mavi tema renkleri
        if color == "green":
            fill_color = (33, 150, 243)   # Mavi - aktif (#2196F3)
        elif color == "red":
            fill_color = (244, 67, 54)    # Kırmızı - yakalama anı
        elif color == "white":
            fill_color = (255, 255, 255)  # Beyaz - flash parlak
        elif color == "yellow":
            fill_color = (100, 181, 246)  # Açık mavi - flash geçiş (#64B5F6)
        else:
            fill_color = (25, 118, 210)   # Koyu mavi - pasif (#1976D2)
        
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
            
            # Bundled kaynaklar için doğru dizini kullan
            sounds_dir = get_resource_dir() / "sounds"
            
            sound_path = sounds_dir / sound_file
            
            if sound_path.exists():
                winsound.PlaySound(str(sound_path), winsound.SND_FILENAME | winsound.SND_ASYNC)
            else:
                # Varsayılan Windows sesi
                print(f"[Sound] Ses dosyası bulunamadı: {sound_path}")
                winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)
        except Exception as e:
            print(f"[Sound] Hata: {e}")
    
    def flash_tray_icon(self):
        """Tray ikonunu flash efekti ile yanıp söndür."""
        if not self.icon:
            return
        
        def flash_sequence():
            import time
            # Flash 1: Beyaz (parlak)
            self.icon.icon = self.create_icon_image("white")
            time.sleep(0.1)
            # Flash 2: Sarı 
            self.icon.icon = self.create_icon_image("yellow")
            time.sleep(0.1)
            # Normal: Yeşil
            self.icon.icon = self.create_icon_image("green")
        
        # Flash efektini ayrı thread'de çalıştır
        threading.Thread(target=flash_sequence, daemon=True).start()
    
    def on_screenshot_hotkey(self):
        """Kısayol tuşuna basıldığında çağrılır."""
        import time
        
        # Cooldown kontrolü - tuş basılı kalsa bile hızlı çekim engellenir
        current_time = time.time()
        if current_time - self._last_screenshot_time < self._screenshot_cooldown:
            return  # Cooldown süresi dolmadı, atlat
        
        self._last_screenshot_time = current_time
        
        # Flash efekti başlat (screenshot öncesi)
        self.flash_tray_icon()
        
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
                show_notification(filepath.name, duration=2.0, dark_mode=dark_mode, title=t("notification_screenshot_taken"))
            
            print(f"✓ [{self._screenshot_count}] {t('saved')}: {filepath}")
        else:
            print(f"✗ {t('screenshot_failed')}")
    
    def open_screenshots_folder(self, icon=None, item=None):
        """Ekran görüntüleri klasörünü aç."""
        save_path = get_save_path()
        os.startfile(str(save_path))
    
    def open_settings(self, icon=None, item=None):
        """Ayarlar penceresini aç - subprocess ile."""
        import subprocess
        import sys
        import time
        
        print("[Settings] open_settings çağrıldı")
        
        # Zaten açık bir ayarlar penceresi varsa kontrol et
        if self._settings_proc is not None:
            if self._settings_proc.poll() is None:
                print("[Settings] Ayarlar penceresi zaten açık.")
                return
            else:
                # Process kapanmış, temizle
                print("[Settings] Eski process temizleniyor")
                self._settings_proc = None
        
        # Mevcut config'i kaydet
        old_hotkey = self.config.get("hotkey", "F12")
        old_language = self.config.get("language", "tr")
        
        # Subprocess başlat
        try:
            if getattr(sys, 'frozen', False):
                # Frozen EXE
                cmd = [sys.executable, "--settings"]
                print(f"[Settings] EXE komutu: {cmd}")
            else:
                # Python script
                settings_script = Path(__file__).parent / "ui" / "settings_dialog.py"
                cmd = [sys.executable, str(settings_script)]
                print(f"[Settings] Script komutu: {cmd}")
            
            self._settings_proc = subprocess.Popen(cmd)
            print(f"[Settings] Subprocess başlatıldı: PID={self._settings_proc.pid}")
        except Exception as e:
            print(f"[Settings] Subprocess hatası: {e}")
            return
        
        # Config değişikliğini kontrol eden thread
        def check_config_changes():
            time.sleep(1)
            
            nonlocal old_hotkey, old_language
            
            while self._settings_proc is not None and self._settings_proc.poll() is None:
                time.sleep(0.5)
                
                try:
                    new_config = load_config()
                    new_hotkey = new_config.get("hotkey", "F12")
                    new_language = new_config.get("language", "tr")
                    
                    if new_hotkey != old_hotkey:
                        print(f"[Settings] Hotkey: {old_hotkey} -> {new_hotkey}")
                        hotkey_manager.update_hotkey(new_hotkey)
                        old_hotkey = new_hotkey
                        self.config = new_config
                    
                    if new_language != old_language:
                        print(f"[Settings] Language: {old_language} -> {new_language}")
                        old_language = new_language
                        self.config = new_config
                        if self.icon:
                            self.icon.menu = self.create_menu()
                            self.icon.update_menu()
                except:
                    pass
            
            self._settings_proc = None
            self.config = load_config()
            print("[Settings] Ayarlar penceresi kapandı.")
        
        threading.Thread(target=check_config_changes, daemon=True).start()
    
    def take_screenshot_now(self, icon=None, item=None):
        """Menüden ekran görüntüsü al."""
        self.on_screenshot_hotkey()
    
    def quit_app(self, icon=None, item=None):
        """Uygulamadan çık."""
        print("[App] Kapatılıyor...")
        self.running = False
        
        # ÖNCE settings subprocess'i kapat (eğer açıksa)
        if self._settings_proc is not None:
            try:
                self._settings_proc.terminate()
                self._settings_proc.wait(timeout=2)
                print("[App] Settings subprocess kapatıldı")
            except:
                try:
                    self._settings_proc.kill()
                except:
                    pass
            self._settings_proc = None
        
        # Keyboard hook'larını temizle
        try:
            stop_hotkey_listener()
        except:
            pass
        
        # DXcam kaynaklarını temizle
        try:
            cleanup_dxcam()
        except:
            pass
        
        # Tray icon'u durdur
        if self.icon:
            try:
                self.icon.stop()
            except:
                pass
        
        # Tüm thread'lerin bitmesini biraz bekle
        import time
        time.sleep(0.2)
        
        # Process'in tamamen kapanmasını sağla - os._exit kullan
        import os
        os._exit(0)
    
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


def open_settings_only():
    """Sadece ayarlar penceresini aç (EXE için --settings modu)."""
    import sys
    import os
    from PyQt6.QtWidgets import QApplication
    
    # EXE ve script modları için doğru import yollarını ayarla
    base_dir = str(get_app_dir())
    resource_dir = str(get_resource_dir())
    
    if getattr(sys, 'frozen', False):
        ui_dir = resource_dir  # EXE'de her şey _MEIPASS altında
    else:
        ui_dir = str(Path(__file__).parent / "ui")
    
    for d in [base_dir, resource_dir, ui_dir]:
        if d not in sys.path:
            sys.path.insert(0, d)
    
    from settings_dialog import SettingsDialog
    
    qt_app = QApplication(sys.argv)
    dialog = SettingsDialog()
    dialog.show()
    sys.exit(qt_app.exec())


def show_notification_only():
    """Sadece bildirim göster (EXE için --notification modu)."""
    import sys
    from _notification_process import main as notification_main
    notification_main()


if __name__ == "__main__":
    import sys
    import multiprocessing
    
    # PyInstaller için multiprocessing desteği (EXE'de subprocess spawning sorunu çözer)
    multiprocessing.freeze_support()
    
    # --settings argümanı varsa sadece ayarları aç
    if "--settings" in sys.argv:
        open_settings_only()
    # --notification argümanı varsa sadece bildirim göster
    elif "--notification" in sys.argv:
        # --notification'dan sonraki argümanları al
        idx = sys.argv.index("--notification")
        if len(sys.argv) > idx + 4:
            sys.argv = [sys.argv[0], sys.argv[idx + 1], sys.argv[idx + 2], sys.argv[idx + 3], sys.argv[idx + 4]]
        elif len(sys.argv) > idx + 3:
            sys.argv = [sys.argv[0], sys.argv[idx + 1], sys.argv[idx + 2], sys.argv[idx + 3]]
        show_notification_only()
    else:
        main()



