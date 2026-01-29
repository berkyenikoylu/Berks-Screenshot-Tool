; Berk's Screenshot Tool - Inno Setup Installer Script
; Build: iscc installer.iss
; Özellikler: Güncelleme algılama, temiz kurulum seçeneği, çalışan programı kapatma

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
SetupIconFile=
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

; === GÜNCELLEME ÖZELLİKLERİ ===
; Önceki kurulum dizinini kullan
UsePreviousAppDir=yes
; Önceki grup adını kullan
UsePreviousGroup=yes
; Önceki görevleri kullan
UsePreviousTasks=yes
; Çalışan uygulamayı kapat
CloseApplications=force
CloseApplicationsFilter=*.exe
RestartApplications=yes
; Minimum versiyon kontrolü (güncelleme için)
MinVersion=10.0

[Languages]
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[CustomMessages]
; Türkçe mesajlar
turkish.UpdateDetected=Bilgisayarınızda {#MyAppName} sürüm %1 kurulu.%n%nNe yapmak istiyorsunuz?
turkish.UpdateOption=Güncelle (ayarları koru)
turkish.CleanInstallOption=Temiz Kurulum (her şeyi sil)
turkish.InstalledVersion=Kurulu Sürüm: %1
turkish.NewVersion=Yeni Sürüm: {#MyAppVersion}
turkish.ClosingApp=Program kapatılıyor...
turkish.CleaningOldFiles=Eski dosyalar temizleniyor...
; İngilizce mesajlar
english.UpdateDetected={#MyAppName} version %1 is installed on your computer.%n%nWhat would you like to do?
english.UpdateOption=Update (keep settings)
english.CleanInstallOption=Clean Install (delete everything)
english.InstalledVersion=Installed Version: %1
english.NewVersion=New Version: {#MyAppVersion}
english.ClosingApp=Closing application...
english.CleaningOldFiles=Cleaning old files...

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "startupicon"; Description: "Windows ile başlat / Start with Windows"; GroupDescription: "Başlangıç / Startup:"; Flags: unchecked

[Files]
; Main executable
Source: "dist\BerksScreenshotTool.exe"; DestDir: "{app}"; Flags: ignoreversion
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

[UninstallRun]
; Kaldırma öncesi programı kapat
Filename: "taskkill"; Parameters: "/F /IM {#MyAppExeName}"; Flags: runhidden nowait; RunOnceId: "KillApp"

[Code]
var
  UpdatePage: TInputOptionWizardPage;
  InstalledVersion: String;
  IsUpgrade: Boolean;
  CleanInstall: Boolean;

// Registry'den kurulu versiyonu oku
function GetInstalledVersion(): String;
var
  Version: String;
begin
  Result := '';
  if RegQueryStringValue(HKEY_CURRENT_USER, 
    'Software\Microsoft\Windows\CurrentVersion\Uninstall\{A3B2C1D0-E5F6-4A7B-8C9D-0E1F2A3B4C5D}_is1',
    'DisplayVersion', Version) then
  begin
    Result := Version;
  end
  else if RegQueryStringValue(HKEY_LOCAL_MACHINE,
    'Software\Microsoft\Windows\CurrentVersion\Uninstall\{A3B2C1D0-E5F6-4A7B-8C9D-0E1F2A3B4C5D}_is1',
    'DisplayVersion', Version) then
  begin
    Result := Version;
  end;
end;

// Kurulu olup olmadığını kontrol et
function IsAppInstalled(): Boolean;
begin
  InstalledVersion := GetInstalledVersion();
  Result := (InstalledVersion <> '');
end;

// Çalışan programı kapat
procedure KillRunningApp();
var
  ResultCode: Integer;
begin
  Exec('taskkill', '/F /IM {#MyAppExeName}', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  Sleep(500); // Programın kapanmasını bekle
end;

// Eski dosyaları temizle (temiz kurulum için)
procedure CleanOldInstallation();
var
  InstallPath: String;
begin
  InstallPath := ExpandConstant('{app}');
  if DirExists(InstallPath) then
  begin
    DelTree(InstallPath, True, True, True);
  end;
end;

// Güncelleme sayfasını oluştur
procedure InitializeWizard();
begin
  IsUpgrade := IsAppInstalled();
  CleanInstall := False;
  
  if IsUpgrade then
  begin
    UpdatePage := CreateInputOptionPage(wpWelcome,
      'Kurulum Türü / Installation Type',
      ExpandConstant('{cm:InstalledVersion,' + InstalledVersion + '}') + #13#10 + 
      ExpandConstant('{cm:NewVersion}'),
      ExpandConstant('{cm:UpdateDetected,' + InstalledVersion + '}'),
      True, False);
    
    UpdatePage.Add(ExpandConstant('{cm:UpdateOption}'));
    UpdatePage.Add(ExpandConstant('{cm:CleanInstallOption}'));
    UpdatePage.Values[0] := True; // Varsayılan: Güncelle
  end;
end;

// Sayfa değiştiğinde
function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
  
  if IsUpgrade and (CurPageID = UpdatePage.ID) then
  begin
    CleanInstall := UpdatePage.Values[1];
    
    // Çalışan programı kapat
    WizardForm.StatusLabel.Caption := ExpandConstant('{cm:ClosingApp}');
    KillRunningApp();
    
    // Temiz kurulum seçildiyse eski dosyaları sil
    if CleanInstall then
    begin
      WizardForm.StatusLabel.Caption := ExpandConstant('{cm:CleaningOldFiles}');
      CleanOldInstallation();
    end;
  end;
end;

// Kurulum başlamadan önce
function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  Result := '';
  // Çalışan programı kapat (güvenlik için tekrar)
  KillRunningApp();
end;
