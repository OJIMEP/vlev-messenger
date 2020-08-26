import wx

class TestWindow(wx.Frame):

    text_box: wx.TextCtrl
    message_box: wx.TextCtrl
    submit_button: wx.Button

    def __init__(self):
        super().__init__(
            None,
            title="My first app",
            size=wx.Size(350, 500)
        )
        self.build_widgets()
        self.build_handler()

    def build_widgets(self):
        panel = wx.BoxSizer(wx.VERTICAL)

        self.text_box = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.message_box = wx.TextCtrl(self)
        self.submit_button = wx.Button(self, label="Send")

        panel.Add(self.text_box, wx.SizerFlags(1).Expand())
        panel.Add(self.message_box, wx.SizerFlags(0).Expand().Border(wx.ALL, 5))
        panel.Add(self.submit_button, wx.SizerFlags(0).Expand().Border(wx.LEFT | wx.BOTTOM | wx.RIGHT, 5))

        self.SetSizer(panel)

    def build_handler(self):
        self.submit_button.Bind(wx.EVT_BUTTON, self.on_button_click)

    def on_button_click(self, event):
        message = self.message_box.GetValue()
        self.text_box.AppendText(f'{message}\n')
        self.message_box.SetValue('')

if __name__ == "__main__":
    app = wx.App()
    window = TestWindow()
    window.Show()
    app.MainLoop()
