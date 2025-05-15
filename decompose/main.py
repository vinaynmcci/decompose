import wx
import requests
import webbrowser

GITHUB_REPO_API = "https://api.github.com/repos/vinaynmcci/decompose/releases/latest"
CURRENT_VERSION = "2.0.0"
GITHUB_RELEASE_URL = "https://github.com/vinaynmcci/decompose/releases/latest"


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

    def on_close(self, event):
        self.Close(True)

    def on_version(self, event):
        wx.MessageBox(f"USBTEST Version: v{CURRENT_VERSION}", "Version", wx.OK | wx.ICON_INFORMATION)

    def check_for_updates(self):
        try:
            response = requests.get(GITHUB_REPO_API, timeout=5)
            response.raise_for_status()
            latest_release = response.json()
            latest_version = latest_release['tag_name'].lstrip('v')  # e.g., "v2.0.0" -> "2.0.0"

            if self.is_newer_version(latest_version, CURRENT_VERSION):
                dlg = wx.MessageDialog(
                    self,
                    f"Updated version USBTEST v{latest_version} is available. Please click OK.",
                    "Update Available",
                    wx.OK | wx.ICON_INFORMATION
                )
                if dlg.ShowModal() == wx.ID_OK:
                    webbrowser.open(GITHUB_RELEASE_URL)
                dlg.Destroy()
        except Exception as e:
            # Ignore errors silently or log if needed
            pass

    @staticmethod
    def is_newer_version(latest, current):
        def version_tuple(v):
            return tuple(map(int, (v.split("."))))
        return version_tuple(latest) > version_tuple(current)


if __name__ == '__main__':
    app = wx.App(False)
    frame = USBTestFrame()
    app.MainLoop()
