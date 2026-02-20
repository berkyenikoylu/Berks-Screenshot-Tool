; Berk's Screenshot Tool - Inno Setup Installer Script
; Build: iscc installer.iss

#define MyAppName "Berk's Screenshot Tool"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Berk"
#define MyAppURL "https://github.com/berkyenikoylu/berks-screenshot-tool"
#define MyAppExeName "BerksScreenshotTool.exe"

[Setup]
; Application info
AppId={{A3B2C1D0-E5F6-4A7B-8C9D-0E1F2A3B4C5D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases
VersionInfoVersion={#MyAppVersion}
DefaultDirName={autopf}\BerksScreenshotTool
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
; License file
LicenseFile=LICENSE
; Output settings
OutputDir=dist
OutputBaseFilename=BerksScreenshotTool-Setup
; Compression
Compression=lzma2/ultra64
SolidCompression=yes
; UI settings
WizardStyle=modern
; Privileges
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
; Uninstaller
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}
; Architecture
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
; Güncelleme için
UsePreviousAppDir=yes
UsePreviousGroup=yes
UsePreviousTasks=yes
; Çalışan uygulamayı kapat
CloseApplications=force
CloseApplicationsFilter=*.exe
RestartApplications=no
; Minimum Windows versiyonu
MinVersion=10.0

[Languages]
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "startupicon"; Description: "Windows ile başlat / Start with Windows"; GroupDescription: "Başlangıç / Startup:"; Flags: unchecked

[Files]
; Main executable
Source: "dist\BerksScreenshotTool.exe"; DestDir: "{app}"; Flags: ignoreversion
; Sounds folder
Source: "sounds\*.wav"; DestDir: "{app}\sounds"; Flags: ignoreversion recursesubdirs createallsubdirs
; License
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
; README
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: startupicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\config.json"
Type: filesandordirs; Name: "{app}\__pycache__"
Type: filesandordirs; Name: "{app}\sounds"

[UninstallRun]
; Kaldırma öncesi programı kapat
Filename: "taskkill"; Parameters: "/F /IM {#MyAppExeName}"; Flags: runhidden nowait; RunOnceId: "KillApp"

[Code]
// Kurulum başlamadan önce çalışan programı kapat
function PrepareToInstall(var NeedsRestart: Boolean): String;
var
  ResultCode: Integer;
begin
  Result := '';
  // Çalışan programı kapat
  Exec('taskkill', '/F /IM {#MyAppExeName}', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  Sleep(500);
end;

