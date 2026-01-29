# Berk's Screenshot Tool 📸

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Windows](https://img.shields.io/badge/Platform-Windows%2010%2F11-blue.svg)](https://www.microsoft.com/windows)
[![Release](https://img.shields.io/github/v/release/berkyenikoylu/berks-screenshot-tool)](https://github.com/berkyenikoylu/berks-screenshot-tool/releases)

🌍 **Language / Dil:** [English](#-english) | [Türkçe](#-türkçe)

---

## 🇬🇧 English

A fast, lightweight Windows screenshot utility with DirectX game capture support.

### ✨ Features

- 🎮 **DirectX Game Capture** - Capture fullscreen games with DXcam
- ⌨️ **Global Hotkey** - Single key capture (default: F12)
- 📷 **Multiple Formats** - PNG, JPG, WEBP, BMP with quality control
- 🖥️ **Multi-Monitor** - Select specific monitor or capture all
- 📝 **Smart Naming** - Auto-names files based on active app
- 🔔 **Modern Notifications** - iPhone-style notification banner
- 🎵 **Sound Feedback** - Audio confirmation on capture
- 🌙 **Dark/Light Mode** - Beautiful modern UI
- 🌍 **Multi-Language** - English and Turkish

---

### 📥 Download

| Version | Description |
|---------|-------------|
| **[Setup](../../releases)** | Full installer with auto-update support, desktop shortcuts, and proper uninstaller |
| **[Portable](../../releases)** | Single EXE, no installation required |

#### 🔧 Setup Version Features:
- Detects existing installation
- Offers **Update** or **Clean Install** options
- Closes running app automatically
- Creates Start Menu & Desktop shortcuts
- Optional "Start with Windows"

---

### ⌨️ Usage

1. Launch the application
2. Press **F12** to capture
3. Screenshots saved to `Pictures/BerksScreenshots`
4. Right-click tray icon for options

### ⚙️ Settings

| Setting | Options |
|---------|---------|
| Hotkey | F1-F12, PrintScreen, etc. |
| Format | PNG, JPG, WEBP, BMP |
| Quality | 10-100% (JPG/WEBP) |
| Monitor | Primary, All, or specific |
| Sound | Various options |
| Theme | Dark / Light |

---

### 🔧 Build from Source

```bash
git clone https://github.com/berkyenikoylu/berks-screenshot-tool.git
cd berks-screenshot-tool
pip install -r requirements.txt
python main.py
```

#### Build EXE:
```bash
pip install pyinstaller
pyinstaller bst.spec
```

#### Build Installer (requires [Inno Setup](https://jrsoftware.org/isinfo.php)):
```bash
iscc installer.iss
```

---

### 📄 License

MIT License - see [LICENSE](LICENSE)

### 👤 Author

**Berk** - [GitHub](https://github.com/berkyenikoylu)

---

## 🇹🇷 Türkçe

DirectX oyun desteği ile hızlı ve hafif Windows ekran görüntüsü aracı.

### ✨ Özellikler

- 🎮 **DirectX Oyun Yakalama** - DXcam ile tam ekran oyunları yakala
- ⌨️ **Global Kısayol** - Tek tuşla yakalama (varsayılan: F12)
- 📷 **Çoklu Format** - PNG, JPG, WEBP, BMP kalite kontrolü ile
- 🖥️ **Çoklu Monitör** - Belirli monitör veya tümü
- 📝 **Akıllı İsimlendirme** - Aktif uygulamaya göre otomatik adlandırma
- 🔔 **Modern Bildirimler** - iPhone tarzı bildirim
- 🎵 **Ses Geri Bildirimi** - Yakalama sonrası ses
- 🌙 **Karanlık/Aydınlık Mod** - Modern arayüz
- 🌍 **Çoklu Dil** - Türkçe ve İngilizce

---

### 📥 İndirme

| Versiyon | Açıklama |
|----------|----------|
| **[Kurulumlu](../../releases)** | Otomatik güncelleme, masaüstü kısayolları ve düzgün kaldırıcı ile tam kurulum |
| **[Portable](../../releases)** | Tek EXE, kurulum gerektirmez |

#### 🔧 Kurulumlu Versiyon Özellikleri:
- Mevcut kurulumu algılar
- **Güncelle** veya **Temiz Kurulum** seçeneği sunar
- Çalışan programı otomatik kapatır
- Başlat Menüsü ve Masaüstü kısayolları
- İsteğe bağlı "Windows ile başlat"

---

### ⌨️ Kullanım

1. Uygulamayı başlat
2. **F12** ile yakala
3. Ekran görüntüleri `Resimler/BerksScreenshots` klasörüne kaydedilir
4. Seçenekler için tepsi simgesine sağ tıkla

### ⚙️ Ayarlar

| Ayar | Seçenekler |
|------|------------|
| Kısayol | F1-F12, PrintScreen, vb. |
| Format | PNG, JPG, WEBP, BMP |
| Kalite | %10-100 (JPG/WEBP) |
| Monitör | Birincil, Tümü veya belirli |
| Ses | Çeşitli seçenekler |
| Tema | Karanlık / Aydınlık |

---

### 📄 Lisans

MIT Lisansı - [LICENSE](LICENSE) dosyasına bakınız

### 👤 Geliştirici

**Berk** - [GitHub](https://github.com/berkyenikoylu)

---

Made with ❤️ in Turkey | Türkiye'de ❤️ ile yapıldı
