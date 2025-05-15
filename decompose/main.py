import wx
import requests
import webbrowser
import tempfile
import os
import subprocess

GITHUB_REPO_API = "https://api.github.com/repos/vinaynmcci/decompose/releases/latest"
CURRENT_VERSION = "5.0.0"



class USBTestFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='USBTEST', size=(400, 200))
        self.panel = wx.Panel(self)

        # Menu Bar
        menu_bar = wx.MenuBar()

        # File Menu
        file_menu = wx.Menu()
        close_item = file_menu.Append(wx.ID_EXIT, 'Close\tCtrl+Q', 'Close the application')
        menu_bar.Append(file_menu, 'File')
        self.Bind(wx.EVT_MENU, self.on_close, close_item)

        # Help Menu
        help_menu = wx.Menu()
        version_item = help_menu.Append(wx.ID_ABOUT, f'v{CURRENT_VERSION}', 'Show version')
        menu_bar.Append(help_menu, 'Help')
        self.Bind(wx.EVT_MENU, self.on_version, version_item)
        
        setting_menu = wx.Menu()
        menu_bar.Append(setting_menu, 'Setting')
        self.Bind(wx.EVT_MENU, self.on_version, version_item)
        
        

        self.SetMenuBar(menu_bar)

        # UI Elements
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.label = wx.StaticText(self.panel, label="Text")
        vbox.Add(self.label, flag=wx.ALL | wx.EXPAND, border=10)

        self.text_ctrl = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)
        vbox.Add(self.text_ctrl, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)

        self.send_button = wx.Button(self.panel, label='Send')
        vbox.Add(self.send_button, flag=wx.ALL | wx.ALIGN_RIGHT, border=10)
        self.send_button.Bind(wx.EVT_BUTTON, self.on_send)
        
        
        self.label = wx.StaticText(self.panel, label="Text")
        vbox.Add(self.label, flag=wx.ALL | wx.EXPAND, border=10)

        self.text_ctrl = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)
        vbox.Add(self.text_ctrl, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)

        self.send_button = wx.Button(self.panel, label='Send')
        vbox.Add(self.send_button, flag=wx.ALL | wx.ALIGN_RIGHT, border=10)
        self.send_button.Bind(wx.EVT_BUTTON, self.on_send)

        # --- New IP Section ---
        self.ip_label = wx.StaticText(self.panel, label="IP Address")
        vbox.Add(self.ip_label, flag=wx.ALL | wx.EXPAND, border=10)

        self.ip_text_ctrl = wx.TextCtrl(self.panel, value="192.168.1.100")
        vbox.Add(self.ip_text_ctrl, flag=wx.ALL | wx.EXPAND, border=10)

        self.ip_button = wx.Button(self.panel, label="Print IP")
        vbox.Add(self.ip_button, flag=wx.ALL | wx.ALIGN_RIGHT, border=10)
        self.ip_button.Bind(wx.EVT_BUTTON, self.on_print_ip)
        # ----------------------

        self.panel.SetSizer(vbox)

        # Status Bar with version
        self.CreateStatusBar()
        self.SetStatusText(f"v{CURRENT_VERSION}")

        self.Centre()
        self.Show()

        # Check GitHub for updates on startup
        self.check_for_updates()

    def on_send(self, event):
        self.text_ctrl.SetValue("welcome USBTEST")
    
    def on_print_ip(self, event):
        ip_value = self.ip_text_ctrl.GetValue()
        print(f"IP Address: {ip_value}")


    def on_close(self, event):
        self.Close(True)

    def on_version(self, event):
        wx.MessageBox(f"USBTEST Version: v{CURRENT_VERSION}", "Version", wx.OK | wx.ICON_INFORMATION)

    def check_for_updates(self):
        try:
            response = requests.get(GITHUB_REPO_API, timeout=5)
            response.raise_for_status()
            latest_release = response.json()
            latest_version = latest_release['tag_name'].lstrip('v')

            if self.is_newer_version(latest_version, CURRENT_VERSION):
                dlg = wx.MessageDialog(
                    self,
                    f"Updated version USBTEST v{latest_version} is available.\nClick OK to auto-install.",
                    "Update Available",
                    wx.OK | wx.ICON_INFORMATION
                )
                if dlg.ShowModal() == wx.ID_OK:
                    installer_url = self.get_installer_url(latest_release)
                    if installer_url:
                        self.download_and_install(installer_url)
                dlg.Destroy()
        except Exception as e:
            pass  # Optional: print(e) for debugging

    def get_installer_url(self, release_data):
        for asset in release_data.get("assets", []):
            name = asset.get("name", "")
            if name.lower().endswith(".exe"):
                return asset.get("browser_download_url")
        return None

    def download_and_install(self, url):
        try:
            # Download the installer to a temporary file
            temp_dir = tempfile.gettempdir()
            local_path = os.path.join(temp_dir, "USBTEST-Setup.exe")

            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(local_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            # Launch installer silently
            subprocess.Popen([local_path, "/VERYSILENT", "/NORESTART"])
            self.Close(True)  # Optionally close the app
        except Exception as e:
            wx.MessageBox("Failed to auto-install update.", "Error", wx.OK | wx.ICON_ERROR)

    @staticmethod
    def is_newer_version(latest, current):
        def version_tuple(v): return tuple(map(int, v.split(".")))
        return version_tuple(latest) > version_tuple(current)


if __name__ == '__main__':
    app = wx.App(False)
    frame = USBTestFrame()
    app.MainLoop()
