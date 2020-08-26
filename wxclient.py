import wx

from twisted.internet import wxreactor

wxreactor.install()

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineOnlyReceiver

class ChatClient(LineOnlyReceiver):
    factory: 'ChatFactory'

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.window.protocol = self

    def lineReceived(self, line):
        message = line.decode()
        self.factory.window.text_box.AppendText(f'{message}\n')

class ChatFactory(ClientFactory):
    window: 'ChatWindow'

    def __init__(self, window):
        self.window = window

    def buildProtocol(self, addr):
        return ChatClient(self)

class ChatWindow(wx.Frame):
    protocol: ChatClient
    text_box: wx.TextCtrl
    message_box: wx.TextCtrl
    submit_button: wx.Button

    def __init__(self):
        super().__init__(
            None,
            title="ChatWindow",
            size=wx.Size(350, 500)
        )
        self.build_widgets()

    def build_widgets(self):
        panel = wx.BoxSizer(wx.VERTICAL)

        self.text_box = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.message_box = wx.TextCtrl(self)
        self.submit_button = wx.Button(self, label="Send")

        panel.Add(self.text_box, wx.SizerFlags(1).Expand())
        panel.Add(self.message_box, wx.SizerFlags(0).Expand().Border(wx.ALL, 5))
        panel.Add(self.submit_button, wx.SizerFlags(0).Expand().Border(wx.LEFT | wx.BOTTOM | wx.RIGHT, 5))

        self.submit_button.Bind(wx.EVT_BUTTON, self.send_message)
        self.SetSizer(panel)

    def send_message(self, event):

        self.protocol.sendLine(self.message_box.GetValue().encode())
        self.message_box.SetValue('')

if __name__ == "__main__":
    app = wx.App()
    window = ChatWindow()
    window.Show()
    reactor.registerWxApp(app)
    reactor.connectTCP('localhost', 7410, ChatFactory(window))
    reactor.run()