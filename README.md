# Berk's Screenshot Tool 📸

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Windows](https://img.shields.io/badge/Platform-Windows%2010%2F11-blue.svg)](https://www.microsoft.com/windows)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)

🌍 **Language / Dil:** [English](#english) | [Türkçe](#türkçe)

---

<a name="english"></a>
## 🇬🇧 English

A fast, lightweight Windows screenshot utility with hotkey support, multiple monitor selection, and DirectX fullscreen game capture.

### ✨ Features

- 🎮 **DirectX Game Support** - Capture fullscreen games with DXcam (Fall back to MSS for compatibility)
- ⌨️ **Global Hotkey** - Capture screenshots with a single key press (default: F12)
- 📷 **Multiple Formats** - PNG, JPG, WEBP, BMP support with quality control
- 🖥️ **Multi-Monitor Support** - Select specific monitor or capture all screens
- 📝 **Smart Naming** - Auto-names files based on active application
- 🔔 **Modern Notifications** - iPhone-style notification banner on capture
- 🎵 **Customizable Sounds** - Audio feedback on capture
- 🌙 **Dark/Light Mode** - Beautiful modern UI
- 🌍 **Multi-Language** - English and Turkish support
- ⏱️ **Cooldown Protection** - Prevents rapid-fire captures if key is held

---

### 🚀 Installation

#### Option 1: Portable Version (Recommended for most users)
1. Download `BerksScreenshotTool-Portable.zip` from the [Releases](../../releases) page
2. Extract to any folder
3. Run `BerksScreenshotTool.exe`

#### Option 2: Installer Version
1. Download `BerksScreenshotTool-Setup.exe` from the [Releases](../../releases) page
2. Run installer and follow the prompts
3. Launch from Start Menu or Desktop shortcut

#### Option 3: Run from Source
```bash
# Clone the repository
git clone https://github.com/berkyenikoylu/berks-screenshot-tool.git
cd berks-screenshot-tool

# Create virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

---

### 📋 Requirements

- **Windows 10/11** (64-bit recommended)
- **Python 3.8+** (only if running from source)

---

### ⌨️ Usage

1. Launch the application
2. Press **F12** (or your configured hotkey) to capture
3. Screenshots are saved to `Pictures/BerksScreenshots` by default
4. Right-click the tray icon for options

---

### ⚙️ Settings

Access settings via **right-click** on the system tray icon → **Settings**

| Setting | Description |
|---------|-------------|
| **Hotkey** | Keyboard shortcut for capture (F1-F12, PrintScreen, etc.) |
| **Format** | PNG, JPG, WEBP, or BMP |
| **Quality** | 10-100% (for JPG/WEBP) |
| **Monitor** | Select which screen to capture |
| **Sound** | Audio feedback on capture |
| **Notification** | Show/hide visual notification |
| **Theme** | Dark or Light mode |
| **Language** | English or Turkish |

---

### 📁 File Naming

Screenshots are automatically named with the pattern:
```
{ActiveApp}_{Date}_{Time}.{format}
```
**Example:** `Chrome_2026-01-29_15-30-45.png`

---

### 🎮 Game Capture

This tool uses **DXcam** for DirectX fullscreen game capture. If DXcam returns a black screen, it automatically falls back to **MSS** (multi-screenshot) method.

**Tested Games:**
- ✅ Counter-Strike 2
- ✅ Minecraft
- ✅ Most DirectX/OpenGL games

---

### 🔧 Building from Source

#### Build Portable EXE
```bash
# Install PyInstaller
pip install pyinstaller

# Build using spec file
pyinstaller bst.spec

# Output: dist/BerksScreenshotTool.exe
```

Or simply run the build script:
```bash
build.bat
```

#### Build Installer (requires Inno Setup)
1. Install [Inno Setup](https://jrsoftware.org/isinfo.php)
2. Build the portable EXE first
3. Run: `iscc installer.iss`

---

### 📦 Project Structure

```
berks-screenshot-tool/
├── main.py                 # Main application & system tray
├── capture.py              # Screen capture (DXcam + MSS)
├── config.py               # Configuration management
├── detector.py             # Active app detection
├── hotkeys.py              # Global hotkey listener
├── i18n.py                 # Internationalization
├── naming.py               # File naming logic
├── notification.py         # Notification launcher
├── _notification_process.py # Notification window (subprocess)
├── monitor_selector.py     # Monitor selection UI
├── ui/
│   └── settings_dialog.py  # Settings window (PyQt6)
├── sounds/
│   ├── banjo.wav          # Sound effect
│   └── crispy.wav         # Sound effect
├── requirements.txt        # Python dependencies
├── bst.spec               # PyInstaller spec file
├── build.bat              # Build script
└── installer.iss          # Inno Setup script
```

---

### 📄 License

MIT License - see [LICENSE](LICENSE) file.

---

### 👤 Author

**Berk** - [GitHub](https://github.com/berkyenikoylu)

---

<a name="türkçe"></a>
## 🇹🇷 Türkçe

Kısayol tuşu desteği, çoklu monitör seçimi ve DirectX tam ekran oyun yakalama özellikli hızlı ve hafif bir Windows ekran görüntüsü aracı.

### ✨ Özellikler

- 🎮 **DirectX Oyun Desteği** - DXcam ile tam ekran oyunları yakala (uyumluluk için MSS fallback)
- ⌨️ **Global Kısayol** - Tek tuşla ekran görüntüsü al (varsayılan: F12)
- 📷 **Çoklu Format** - Kalite kontrolü ile PNG, JPG, WEBP, BMP desteği
- 🖥️ **Çoklu Monitör Desteği** - Belirli bir monitör seç veya tüm ekranları yakala
- 📝 **Akıllı İsimlendirme** - Aktif uygulamaya göre otomatik dosya adlandırma
- 🔔 **Modern Bildirimler** - Çekim sonrası iPhone tarzı bildirim
- 🎵 **Özelleştirilebilir Sesler** - Çekim sonrası sesli geri bildirim
- 🌙 **Karanlık/Aydınlık Mod** - Modern ve şık arayüz
- 🌍 **Çoklu Dil** - İngilizce ve Türkçe desteği
- ⏱️ **Cooldown Koruması** - Tuş basılı kalırsa hızlı çekimleri engeller

---

### 🚀 Kurulum

#### Seçenek 1: Portable Versiyon (Çoğu kullanıcı için önerilir)
1. [Releases](../../releases) sayfasından `BerksScreenshotTool-Portable.zip` indirin
2. Herhangi bir klasöre çıkartın
3. `BerksScreenshotTool.exe` dosyasını çalıştırın

#### Seçenek 2: Kurulumlu Versiyon
1. [Releases](../../releases) sayfasından `BerksScreenshotTool-Setup.exe` indirin
2. Kurulum programını çalıştırın ve yönergeleri takip edin
3. Başlat Menüsü veya Masaüstü kısayolundan başlatın

#### Seçenek 3: Kaynak Koddan Çalıştır
```bash
# Depoyu klonlayın
git clone https://github.com/berkyenikoylu/berks-screenshot-tool.git
cd berks-screenshot-tool

# Sanal ortam oluşturun (önerilir)
python -m venv .venv
.venv\Scripts\activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Çalıştırın
python main.py
```

---

### 📋 Gereksinimler

- **Windows 10/11** (64-bit önerilir)
- **Python 3.8+** (kaynak koddan çalıştırıyorsanız)

---

### ⌨️ Kullanım

1. Uygulamayı başlatın
2. Ekran görüntüsü almak için **F12** (veya ayarladığınız kısayol) tuşuna basın
3. Ekran görüntüleri varsayılan olarak `Resimler/BerksScreenshots` klasörüne kaydedilir
4. Seçenekler için tepsi simgesine sağ tıklayın

---

### ⚙️ Ayarlar

Ayarlara erişmek için sistem tepsisi simgesine **sağ tıklayın** → **Ayarlar**

| Ayar | Açıklama |
|------|----------|
| **Kısayol** | Çekim için klavye kısayolu (F1-F12, PrintScreen, vb.) |
| **Format** | PNG, JPG, WEBP veya BMP |
| **Kalite** | %10-%100 arası (JPG/WEBP için) |
| **Monitör** | Hangi ekranın yakalanacağını seçin |
| **Ses** | Çekim sonrası sesli geri bildirim |
| **Bildirim** | Görsel bildirimi göster/gizle |
| **Tema** | Karanlık veya Aydınlık mod |
| **Dil** | İngilizce veya Türkçe |

---

### 📁 Dosya Adlandırma

Ekran görüntüleri otomatik olarak şu şablonla adlandırılır:
```
{AktifUygulama}_{Tarih}_{Saat}.{format}
```
**Örnek:** `Chrome_2026-01-29_15-30-45.png`

---

### 🎮 Oyun Yakalama

Bu araç, DirectX tam ekran oyun yakalama için **DXcam** kullanır. DXcam siyah ekran döndürürse, otomatik olarak **MSS** (multi-screenshot) yöntemine geçer.

**Test Edilen Oyunlar:**
- ✅ Counter-Strike 2
- ✅ Minecraft
- ✅ Çoğu DirectX/OpenGL oyunu

---

### 🔧 Kaynak Koddan Derleme

#### Portable EXE Oluşturma
```bash
# PyInstaller'ı yükleyin
pip install pyinstaller

# Spec dosyası ile derleyin
pyinstaller bst.spec

# Çıktı: dist/BerksScreenshotTool.exe
```

Veya basitçe build scriptini çalıştırın:
```bash
build.bat
```

#### Kurulum Dosyası Oluşturma (Inno Setup gerektirir)
1. [Inno Setup](https://jrsoftware.org/isinfo.php) yükleyin
2. Önce portable EXE'yi oluşturun
3. Çalıştırın: `iscc installer.iss`

---

### 📄 Lisans

MIT Lisansı - [LICENSE](LICENSE) dosyasına bakınız.

---

### 👤 Geliştirici

**Berk** - [GitHub](https://github.com/berkyenikoylu)

---
