from twisted.internet import stdio, reactor
from twisted.internet.protocol import ClientFactory, Protocol

class DataWrapper(Protocol):
    output = None

    def dataReceived(self, data: bytes):
        if data.decode() == 'exit\n':
            reactor.callFromThread(reactor.stop)

        if self.output:
            self.output.write(data)

class UserProtocol(DataWrapper):

    def wrap_input(self):
        input_forwarder = DataWrapper()
        input_forwarder.output = self.transport

        stdio_wrapper = stdio.StandardIO(input_forwarder)
        self.output = stdio_wrapper

    def connectionMade(self):
        print("Connected [OK]")
        self.transport.write(f'login: {self.factory.login}'.encode())
        self.wrap_input()

class UserFactory(ClientFactory):
    protocol = UserProtocol
    login: str

    def __init__(self, user_login: str):
        self.login = user_login

    def startedConnecting(self, connector):
        print("Connecting to the server...")

    def clientConnectionLost(self, connector, reason):
        print("Disconnected")
        reactor.callFromThread(reactor.stop)

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed")
        reactor.callFromThread(reactor.stop)

if __name__ == '__main__':
    reactor.connectTCP(
        "localhost", 
        7410, 
        UserFactory(input("Your login >>> "))
    )
    reactor.run()