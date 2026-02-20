# -*- mode: python ; coding: utf-8 -*-
"""
Berk's Screenshot Tool - PyInstaller Spec File
Build command: pyinstaller bst.spec
"""

import sys
from pathlib import Path

block_cipher = None

# Proje dizini
project_dir = Path(SPECPATH)

# UPX dizini (sıkıştırma için)
upx_dir = r'C:\upx-5.1.0-win64'

a = Analysis(
    ['main.py', 'ui/settings_dialog.py', 'monitor_selector.py'],  # Tüm entry point'ler
    pathex=[str(project_dir), str(project_dir / 'ui')],
    binaries=[],
    datas=[
        # Ses dosyaları
        ('sounds/*.wav', 'sounds'),
    ],
    hiddenimports=[
        'pystray._win32',
        'PIL._tkinter_finder',
        'win32gui',
        'win32process',
        'win32api',
        'win32con',
        'keyboard',
        'mss',
        'psutil',
        'PyQt6',
        'PyQt6.QtWidgets',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        # Numpy (capture.py'de siyah ekran kontrolü için)
        'numpy',
        'numpy.core',
        'numpy.core.multiarray',
        # DXcam (opsiyonel, tam ekran oyunlar)
        'dxcam',
        # Windows ses
        'winsound',
        'ctypes',
        # UI modülleri
        'settings_dialog',
        'monitor_selector',
        # Yerel modüller
        'config',
        'i18n',
        'capture',
        'detector',
        'hotkeys',
        'naming',
        'notification',
        '_notification_process',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BerksScreenshotTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_dir=upx_dir,  # UPX dizini
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Konsol penceresi gösterme
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='assets/icon.ico',  # İkon dosyası eklendiğinde aktif et
)
