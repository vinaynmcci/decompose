import wx

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
        version_item = help_menu.Append(wx.ID_ABOUT, 'v1.0.0', 'Show version')
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
        self.SetStatusText("v1.0.0")

        self.Centre()
        self.Show()

    def on_send(self, event):
        self.text_ctrl.SetValue("welcome USBTEST")

    def on_close(self, event):
        self.Close(True)

    def on_version(self, event):
        wx.MessageBox("USBTEST Version: v1.0.0", "Version", wx.OK | wx.ICON_INFORMATION)


if __name__ == '__main__':
    app = wx.App(False)
    frame = USBTestFrame()
    app.MainLoop()
