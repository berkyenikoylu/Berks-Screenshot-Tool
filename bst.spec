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

a = Analysis(
    ['main.py'],
    pathex=[str(project_dir)],
    binaries=[],
    datas=[
        # Ses dosyaları
        ('sounds/*.wav', 'sounds'),
        # UI modülleri (eğer ayrı klasördeyse)
        ('ui/*.py', 'ui'),
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
