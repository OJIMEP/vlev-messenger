import sys
from PyQt5 import QtWidgets
import design
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
        self.factory.window.plainTextEdit.appendPlainText(message)

class ChatFactory(ClientFactory):

    window: 'ExampleApp'
    def __init__(self, window):
        self.window = window

    def buildProtocol(self, addr):
        return ChatClient(self)

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    protocol: ChatClient
    reactor = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_handlers()

    def init_handlers(self):
        self.pushButton.clicked.connect(self.send_message)

    def closeEvent(self, event):
        self.reactor.callFromThread(self.reactor.stop)

    def send_message(self):
        self.protocol.sendLine(self.lineEdit.text().encode())
        self.lineEdit.setText('')

def main():
    app = QtWidgets.QApplication(sys.argv)

    import qt5reactor

    window = ExampleApp()
    window.show()

    qt5reactor.install()

    from twisted.internet import reactor

    reactor.connectTCP("localhost", 7410, ChatFactory(window))

    window.reactor = reactor
    reactor.run()

if __name__ == '__main__':
    main()