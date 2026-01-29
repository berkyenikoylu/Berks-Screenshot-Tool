"""
GameCapture - Akıllı Dosya İsimlendirme
Shadowplay benzeri dosya isimlendirme sistemi.
"""

from datetime import datetime
from pathlib import Path
from config import load_config


def generate_filename(app_name: str, format: str = None) -> str:
    """
    Akıllı dosya adı oluştur.
    Örnek: Cyberpunk 2077_2026-01-24_17-45-30.png
    """
    config = load_config()
    
    if format is None:
        format = config.get("format", "png")
    
    # Şu anki tarih ve saat
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M-%S")
    
    # İsimlendirme kalıbını al
    pattern = config.get("naming_pattern", "{app}_{date}_{time}")
    
    # Kalıbı doldur
    filename = pattern.format(
        app=app_name,
        date=date_str,
        time=time_str
    )
    
    # Uzantı ekle
    filename = f"{filename}.{format.lower()}"
    
    return filename


def get_unique_filepath(save_dir: Path, filename: str) -> Path:
    """
    Benzersiz dosya yolu oluştur.
    Dosya zaten varsa sayaç ekle: dosya_1.png, dosya_2.png, vb.
    """
    filepath = save_dir / filename
    
    if not filepath.exists():
        return filepath
    
    # Dosya varsa, sayaç ekle
    stem = filepath.stem
    suffix = filepath.suffix
    counter = 1
    
    while filepath.exists():
        new_filename = f"{stem}_{counter}{suffix}"
        filepath = save_dir / new_filename
        counter += 1
    
    return filepath


def get_screenshot_path(app_name: str, format: str = None, save_dir: Path = None) -> Path:
    """
    Ekran görüntüsü için tam dosya yolunu al.
    """
    config = load_config()
    
    if save_dir is None:
        save_dir = Path(config.get("save_path", Path.home() / "Pictures" / "GameCapture"))
    
    # Klasörün var olduğundan emin ol
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # Dosya adı oluştur
    filename = generate_filename(app_name, format)
    
    # Benzersiz yol al
    filepath = get_unique_filepath(save_dir, filename)
    
    return filepath


if __name__ == "__main__":
    # Test
    test_path = get_screenshot_path("Cyberpunk 2077", "png")
    print(f"Örnek dosya yolu: {test_path}")
    
    test_path2 = get_screenshot_path("Masaustu", "jpg")
    print(f"Örnek dosya yolu 2: {test_path2}")
