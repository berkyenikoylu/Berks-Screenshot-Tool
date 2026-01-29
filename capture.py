"""
GameCapture - Ekran Görüntüsü Yakalama
Hızlı ekran yakalama ve çoklu format desteği.
DXcam ile tam ekran oyun desteği + MSS fallback.
"""

import mss
from PIL import Image
from pathlib import Path
from typing import Optional, Tuple
from config import load_config
from detector import get_foreground_app
from naming import get_screenshot_path

# DXcam için (tam ekran DirectX oyunları)
try:
    import dxcam
    DXCAM_AVAILABLE = True
except ImportError:
    DXCAM_AVAILABLE = False
    print("[Capture] DXcam yüklenemedi, sadece MSS kullanılacak")

# Global dxcam instance (performans için)
_dxcam_camera = None


def _get_dxcam_camera(monitor: int = 0):
    """DXcam kamerasını al veya oluştur."""
    global _dxcam_camera
    
    if not DXCAM_AVAILABLE:
        return None
    
    try:
        if _dxcam_camera is None:
            # DXcam'i başlat
            _dxcam_camera = dxcam.create(output_idx=monitor, output_color="RGB")
        return _dxcam_camera
    except Exception as e:
        print(f"[Capture] DXcam başlatılamadı: {e}")
        return None


def capture_screen_dxcam(monitor: int = 0) -> Optional[Image.Image]:
    """
    DXcam ile ekran yakala (DirectX tam ekran oyunları için).
    
    Args:
        monitor: Monitör indeksi (0 = birincil)
    
    Returns:
        PIL Image veya None (başarısız olursa)
    """
    try:
        camera = _get_dxcam_camera(monitor)
        if camera is None:
            return None
        
        # Tek frame yakala
        frame = camera.grab()
        
        if frame is None:
            # Bazen ilk grab None döner, tekrar dene
            import time
            time.sleep(0.05)
            frame = camera.grab()
        
        if frame is not None:
            # numpy array'i PIL Image'a dönüştür
            img = Image.fromarray(frame)
            return img
        
        return None
    except Exception as e:
        print(f"[Capture] DXcam yakalama hatası: {e}")
        return None


def capture_screen_mss(monitor: int = 0) -> Image.Image:
    """
    MSS ile ekran yakala (geleneksel yöntem, fallback).
    
    Args:
        monitor: 0 = birincil monitör, -1 = tüm monitörler, 1+ = belirli monitör
    """
    with mss.mss() as sct:
        if monitor == -1:
            # Tüm monitörleri yakala
            screenshot = sct.grab(sct.monitors[0])
        else:
            # Belirli monitörü yakala (0 = birincil = monitors[1])
            monitor_index = monitor + 1 if monitor >= 0 else 1
            if monitor_index >= len(sct.monitors):
                monitor_index = 1
            screenshot = sct.grab(sct.monitors[monitor_index])
        
        # mss görüntüsünü PIL Image'a dönüştür
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        return img


def capture_screen(monitor: int = 0) -> Image.Image:
    """
    Ekranı yakala ve PIL Image olarak döndür.
    Önce DXcam dener (tam ekran oyunlar için), başarısız olursa MSS kullanır.
    
    Args:
        monitor: 0 = birincil monitör, -1 = tüm monitörler, 1+ = belirli monitör
    """
    # Önce DXcam dene (tam ekran oyunlar için daha iyi)
    if DXCAM_AVAILABLE and monitor >= 0:  # DXcam -1 (tüm monitörler) desteklemez
        img = capture_screen_dxcam(monitor)
        if img is not None:
            # Siyah ekran kontrolü - eğer tamamen siyahsa MSS'e geç
            if not _is_black_image(img):
                return img
            else:
                print("[Capture] DXcam siyah ekran döndü, MSS'e geçiliyor...")
    
    # Fallback: MSS kullan
    return capture_screen_mss(monitor)


def _is_black_image(img: Image.Image, threshold: int = 10) -> bool:
    """
    Görüntünün tamamen siyah olup olmadığını kontrol et.
    
    Args:
        img: PIL Image
        threshold: Piksel değeri eşiği (altındaki değerler siyah sayılır)
    
    Returns:
        True eğer görüntü tamamen siyahsa
    """
    try:
        # Küçük bir örnek al (performans için)
        small = img.resize((100, 100))
        
        # Piksel verilerini al (Pillow 14+ uyumlu)
        import numpy as np
        pixels = np.array(small)
        
        # Ortalama parlaklık hesapla
        avg = pixels[:, :, :3].mean()
        
        return avg < threshold
    except:
        return False


def save_screenshot(
    image: Image.Image,
    filepath: Path,
    format: str = "png",
    quality: int = 95
) -> bool:
    """
    Görüntüyü belirtilen formatta kaydet.
    
    Args:
        image: PIL Image nesnesi
        filepath: Kayıt yolu
        format: "png", "jpg", "bmp", "webp"
        quality: JPG/WEBP kalitesi (1-100)
    """
    try:
        # Format parametrelerini ayarla
        save_kwargs = {}
        
        if format.lower() in ["jpg", "jpeg"]:
            save_kwargs["quality"] = quality
            save_kwargs["optimize"] = True
            pil_format = "JPEG"
        elif format.lower() == "webp":
            save_kwargs["quality"] = quality
            save_kwargs["method"] = 4  # Daha iyi sıkıştırma
            pil_format = "WEBP"
        elif format.lower() == "png":
            save_kwargs["optimize"] = True
            pil_format = "PNG"
        elif format.lower() == "bmp":
            pil_format = "BMP"
        else:
            pil_format = format.upper()
        
        # Kaydet
        image.save(filepath, format=pil_format, **save_kwargs)
        return True
    except Exception as e:
        print(f"Kayıt hatası: {e}")
        return False


def take_screenshot(
    format: str = None,
    quality: int = None,
    monitor: int = None,
    save_path: Path = None
) -> Tuple[bool, Optional[Path], str]:
    """
    Tam ekran görüntüsü al ve kaydet.
    
    Returns:
        (başarılı, dosya_yolu, uygulama_adı)
    """
    config = load_config()
    
    # Varsayılan değerleri ayarla
    if format is None:
        format = config.get("format", "png")
    if quality is None:
        quality = config.get("quality", 95)
    if save_path is None:
        save_path = Path(config.get("save_path", Path.home() / "Pictures" / "GameCapture"))
    if monitor is None:
        monitor = config.get("monitor", 0)
    
    try:
        # Aktif uygulamayı algıla
        app_info = get_foreground_app()
        app_name = app_info["clean_name"]
        
        # Dosya yolunu oluştur
        filepath = get_screenshot_path(app_name, format, save_path)
        
        # Ekranı yakala (DXcam + MSS fallback)
        image = capture_screen(monitor)
        
        # Kaydet
        success = save_screenshot(image, filepath, format, quality)
        
        if success:
            return True, filepath, app_name
        else:
            return False, None, app_name
            
    except Exception as e:
        print(f"Ekran görüntüsü hatası: {e}")
        return False, None, ""


def cleanup_dxcam():
    """DXcam kaynakları temizle (uygulama kapanırken çağır)."""
    global _dxcam_camera
    if _dxcam_camera is not None:
        try:
            del _dxcam_camera
            _dxcam_camera = None
        except:
            pass


if __name__ == "__main__":
    # Test
    print("Ekran görüntüsü alınıyor...")
    print(f"DXcam durumu: {'Aktif' if DXCAM_AVAILABLE else 'Yok'}")
    
    success, path, app = take_screenshot()
    
    if success:
        print(f"✓ Kaydedildi: {path}")
        print(f"  Uygulama: {app}")
    else:
        print("✗ Ekran görüntüsü alınamadı")
    
    cleanup_dxcam()
