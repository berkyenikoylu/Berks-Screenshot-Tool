"""
Berk's Screenshot Tool - Internationalization (i18n)
Türkçe ve İngilizce dil desteği.
"""

from config import load_config, update_config

# Desteklenen diller
SUPPORTED_LANGUAGES = ["tr", "en"]

# Çeviri sözlüğü
TRANSLATIONS = {
    # === Uygulama Genel ===
    "app_name": {
        "tr": "Berk's Screenshot Tool",
        "en": "Berk's Screenshot Tool"
    },
    "app_description": {
        "tr": "Ekran Görüntüsü Aracı",
        "en": "Screenshot Tool"
    },
    
    # === Konsol Mesajları ===
    "console_title": {
        "tr": "Berk's Screenshot Tool - Ekran Goruntusu Araci",
        "en": "Berk's Screenshot Tool - Screenshot Utility"
    },
    "hotkey_label": {
        "tr": "Kısayol Tuşu",
        "en": "Hotkey"
    },
    "format_label": {
        "tr": "Format",
        "en": "Format"
    },
    "save_path_label": {
        "tr": "Kayıt Yeri",
        "en": "Save Path"
    },
    "theme_label": {
        "tr": "Tema",
        "en": "Theme"
    },
    "theme_dark": {
        "tr": "Karanlık",
        "en": "Dark"
    },
    "theme_light": {
        "tr": "Aydınlık",
        "en": "Light"
    },
    "running_in_tray": {
        "tr": "Sistem tepsisinde çalışıyor...",
        "en": "Running in system tray..."
    },
    "exit_hint": {
        "tr": "Çıkmak için tepsi simgesine sağ tıklayın.",
        "en": "Right-click tray icon to exit."
    },
    "hotkey_active": {
        "tr": "Kisayol tusu aktif",
        "en": "Hotkey active"
    },
    "saved": {
        "tr": "Kaydedildi",
        "en": "Saved"
    },
    "screenshot_failed": {
        "tr": "Ekran görüntüsü alınamadı",
        "en": "Screenshot failed"
    },
    
    # === Sistem Tepsisi Menüsü ===
    "menu_take_screenshot": {
        "tr": "📸 Ekran Görüntüsü Al",
        "en": "📸 Take Screenshot"
    },
    "menu_open_folder": {
        "tr": "📁 Klasörü Aç",
        "en": "📁 Open Folder"
    },
    "menu_settings": {
        "tr": "⚙️ Ayarlar",
        "en": "⚙️ Settings"
    },
    "menu_exit": {
        "tr": "❌ Çıkış",
        "en": "❌ Exit"
    },
    
    # === Ayarlar Penceresi ===
    "settings_title": {
        "tr": "⚙️ Ayarlar",
        "en": "⚙️ Settings"
    },
    "settings_capture": {
        "tr": "📸 Yakalama",
        "en": "📸 Capture"
    },
    "settings_hotkey": {
        "tr": "Kısayol Tuşu:",
        "en": "Hotkey:"
    },
    "settings_click_to_set": {
        "tr": "Tıkla ve tuşa bas...",
        "en": "Click and press key..."
    },
    "settings_waiting_key": {
        "tr": "⌨️ Tuşa basın...",
        "en": "⌨️ Press a key..."
    },
    "settings_format": {
        "tr": "Format:",
        "en": "Format:"
    },
    "settings_quality": {
        "tr": "Kalite:",
        "en": "Quality:"
    },
    "settings_estimated_size": {
        "tr": "Tahmini boyut",
        "en": "Estimated size"
    },
    "settings_monitor": {
        "tr": "Monitör:",
        "en": "Monitor:"
    },
    "settings_select_monitor": {
        "tr": "Seç...",
        "en": "Select..."
    },
    "settings_all_monitors": {
        "tr": "Tüm Monitörler",
        "en": "All Monitors"
    },
    "settings_monitor_n": {
        "tr": "Monitör",
        "en": "Monitor"
    },
    "settings_storage": {
        "tr": "💾 Depolama",
        "en": "💾 Storage"
    },
    "settings_save_folder": {
        "tr": "Kayıt Klasörü:",
        "en": "Save Folder:"
    },
    "settings_browse": {
        "tr": "Gözat...",
        "en": "Browse..."
    },
    "settings_feedback": {
        "tr": "🔔 Geri Bildirim",
        "en": "🔔 Feedback"
    },
    "settings_sound": {
        "tr": "Ses:",
        "en": "Sound:"
    },
    "settings_sound_none": {
        "tr": "Ses yok",
        "en": "No sound"
    },
    "settings_test_sound": {
        "tr": "🔊 Test",
        "en": "🔊 Test"
    },
    "settings_notification": {
        "tr": "Bildirim göster",
        "en": "Show notification"
    },
    "settings_appearance": {
        "tr": "🎨 Görünüm",
        "en": "🎨 Appearance"
    },
    "settings_dark_mode": {
        "tr": "Karanlık Mod",
        "en": "Dark Mode"
    },
    "settings_language": {
        "tr": "Dil:",
        "en": "Language:"
    },
    "settings_save": {
        "tr": "✓ Kaydet",
        "en": "✓ Save"
    },
    "settings_cancel": {
        "tr": "✗ İptal",
        "en": "✗ Cancel"
    },
    
    # === Monitör Seçici ===
    "monitor_selector_title": {
        "tr": "🖥️ Monitör Seçimi",
        "en": "🖥️ Monitor Selection"
    },
    "monitor_selector_desc": {
        "tr": "Tıklayarak ekran görüntüsü alınacak monitörü seçin",
        "en": "Click to select monitor for screenshots"
    },
    "monitor_primary": {
        "tr": "(Birincil)",
        "en": "(Primary)"
    },
    "monitor_combined": {
        "tr": "Birleşik ekran",
        "en": "Combined screen"
    },
    
    # === Bildirimler ===
    "notification_title": {
        "tr": "📸 Ekran Görüntüsü",
        "en": "📸 Screenshot"
    },
    "notification_screenshot_taken": {
        "tr": "Ekran Görüntüsü Alındı",
        "en": "Screenshot Taken"
    },
    
    # === Algılama ===
    "desktop": {
        "tr": "Masaustu",
        "en": "Desktop"
    },
    "unknown": {
        "tr": "Bilinmeyen",
        "en": "Unknown"
    },
    "screen": {
        "tr": "Ekran",
        "en": "Screen"
    },
    
    # === Hatalar ===
    "error_save": {
        "tr": "Kayıt hatası",
        "en": "Save error"
    },
    "error_screenshot": {
        "tr": "Ekran görüntüsü hatası",
        "en": "Screenshot error"
    },
    "error_hotkey": {
        "tr": "Kısayol tuşu hatası",
        "en": "Hotkey error"
    },
}

# Aktif dil
_current_language = "tr"


def get_language() -> str:
    """Mevcut dili döndür."""
    global _current_language
    config = load_config()
    _current_language = config.get("language", "tr")
    return _current_language


def set_language(lang: str) -> bool:
    """Dili değiştir."""
    global _current_language
    if lang in SUPPORTED_LANGUAGES:
        _current_language = lang
        update_config("language", lang)
        return True
    return False


def t(key: str, **kwargs) -> str:
    """
    Çeviri al.
    
    Args:
        key: Çeviri anahtarı
        **kwargs: Format parametreleri
        
    Returns:
        Çevrilmiş metin
    """
    global _current_language
    
    # Dili config'den al
    config = load_config()
    _current_language = config.get("language", "tr")
    
    if key in TRANSLATIONS:
        text = TRANSLATIONS[key].get(_current_language, TRANSLATIONS[key].get("en", key))
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                pass
        return text
    return key


def get_available_languages() -> list:
    """Mevcut dilleri döndür."""
    return [
        {"code": "tr", "name": "Türkçe"},
        {"code": "en", "name": "English"}
    ]


# Kısa alias
_ = t


if __name__ == "__main__":
    # Test
    print("=== Türkçe ===")
    set_language("tr")
    print(t("app_name"))
    print(t("console_title"))
    print(t("menu_take_screenshot"))
    
    print("\n=== English ===")
    set_language("en")
    print(t("app_name"))
    print(t("console_title"))
    print(t("menu_take_screenshot"))
