# Changelog

## v1.1.0 - 2026-02-20

### 🆕 New Features

- **Tray Icon Flash Animation** — The system tray icon now flashes white → light blue → normal when a screenshot is taken, providing instant visual feedback.
- **Settings Gear Spin Animation** — The gear icon in the settings window spins when any setting is changed, giving visual feedback.
- **Screenshot Cooldown** — Added 1-second cooldown to prevent rapid-fire duplicate screenshots when the hotkey is held down.
- **Figma Slate UI Design** — The settings window and monitor selector have been redesigned with a premium Figma Slate color palette (dark blue-gray gradients, colored section headers, modern button styles).

### 🐛 Bug Fixes

- **Fixed: Notification language mismatch** — The screenshot notification banner now correctly shows "Screenshot Taken" in English or "Ekran Görüntüsü Alındı" in Turkish based on the language setting. Previously, it was hardcoded in Turkish regardless of the selected language.
- **Fixed: Monitor selector dark theme inconsistency** — The monitor selection dialog now uses the same Figma Slate palette as the settings window in dark mode, instead of the old plain dark colors. Light mode remains unchanged.
- **Fixed: Program duplication on settings open** — Opening the settings no longer spawns a duplicate application instance. Settings now run as a controlled subprocess with proper process tracking.
- **Fixed: Double screenshot capture** — Resolved the issue where closing and reopening settings caused screenshots to be taken twice per keypress.
- **Fixed: Background process persistence** — The application now fully terminates when exiting via the tray menu, using `os._exit(0)` and proper cleanup of all subprocesses, keyboard hooks, and DXcam resources.
- **Fixed: Settings window crash** — Resolved crashes when opening the settings window by switching to a subprocess-based architecture for dialogs.
- **Fixed: Sound files not playing** — Sound files are now correctly located using `get_resource_dir()` for both Python script and PyInstaller EXE modes.
- **Fixed: Correct image format saving** — Screenshots are now saved in the user-selected format (PNG, JPG, BMP, WEBP) with proper PIL format mapping.
- **Fixed: Hotkey display visibility in dark mode** — Hotkey text is now clearly visible against dark backgrounds.
- **Fixed: Settings dialog UI overflow** — Fixed layout overflow issues in the settings dialog.
- **Fixed: Fullscreen game black screen** — DXcam now includes a black image detection fallback: if a captured frame is completely black, it automatically falls back to MSS capture.
- **Fixed: EXE subprocess issues** — Fixed PyInstaller-related subprocess spawning issues for both settings and notification windows.

### 🔧 Improvements

- **Subprocess-based Settings & Notifications** — Both settings and notifications now run in separate processes, preventing UI thread blocking and Tkinter conflicts.
- **Robust Hotkey Update** — Changing the hotkey in settings now properly removes the old hotkey and registers the new one without restart.
- **Live Language Switching** — Changing the language in settings immediately updates the tray menu without needing to restart.
- **Live Config Monitoring** — The main process polls for config changes while settings is open, applying hotkey and language changes in real-time.
- **Proper DXcam Cleanup** — DXcam camera resources are properly released on application exit.
- **Professional Installer** — Inno Setup installer with update detection, desktop/start menu shortcuts, and clean uninstaller.
