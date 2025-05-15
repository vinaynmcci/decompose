[Setup]
AppName=USBTEST
AppVersion=5.0.0
DefaultDirName={pf}\USBTEST
DefaultGroupName=USBTEST
OutputBaseFilename=USBTEST-Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "..\exe\dist\USBTEST\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\USBTEST"; Filename: "{app}\USBTEST.exe"
Name: "{group}\Uninstall USBTEST"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\USBTEST.exe"; Description: "Launch USBTEST"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
var
  UninstallPath: string;
  ResultCode: Integer;
begin
  UninstallPath := ExpandConstant('{pf}\USBTEST\unins000.exe');
  if FileExists(UninstallPath) then
  begin
    ShellExec('', UninstallPath, '/VERYSILENT /NORESTART', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  end;
  Result := True;
end;
