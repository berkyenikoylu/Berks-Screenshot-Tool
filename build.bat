@echo off
echo ================================================
echo   Berk's Screenshot Tool - EXE Builder
echo ================================================
echo.

REM PyInstaller kontrolü
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [*] PyInstaller bulunamadi, yukleniyor...
    pip install pyinstaller
)

echo [*] EXE olusturuluyor...
pyinstaller bst.spec --noconfirm

echo.
if exist "dist\BerksScreenshotTool.exe" (
    echo [OK] EXE basariyla olusturuldu!
    echo [OK] Konum: dist\BerksScreenshotTool.exe
) else (
    echo [HATA] EXE olusturulamadi!
)

echo.
pause
