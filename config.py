"""
GameCapture - Ayar Yönetimi
Kullanıcı ayarlarını JSON dosyasından yükler ve kaydeder.
"""

import json
import os
from pathlib import Path

# Varsayılan ayarlar
DEFAULT_CONFIG = {
    "hotkey": "F12",
    "format": "png",
    "quality": 95,
    "save_path": str(Path.home() / "Pictures" / "BerksScreenshots"),
    "naming_pattern": "{app}_{date}_{time}",
    "show_notification": True,
    "play_sound": True,
    "sound_file": "none",
    "dark_mode": True,
    "monitor": 0,  # 0 = birincil, -1 = tüm monitörler
    "language": "tr"  # tr = Türkçe, en = English
}

# Ayar dosyası yolu
CONFIG_DIR = Path(__file__).parent
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_config() -> dict:
    """Ayarları dosyadan yükle, yoksa varsayılanları kullan."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                # Eksik ayarları varsayılanlarla doldur
                for key, value in DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                return config
        except (json.JSONDecodeError, IOError):
            pass
    return DEFAULT_CONFIG.copy()


def save_config(config: dict) -> bool:
    """Ayarları dosyaya kaydet."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        return True
    except IOError:
        return False


def get_save_path() -> Path:
    """Ekran görüntüsü kayıt klasörünü al ve oluştur."""
    config = load_config()
    save_path = Path(config["save_path"])
    save_path.mkdir(parents=True, exist_ok=True)
    return save_path


def update_config(key: str, value) -> bool:
    """Tek bir ayarı güncelle."""
    config = load_config()
    config[key] = value
    return save_config(config)


# Modül yüklendiğinde kayıt klasörünü oluştur
get_save_path()
