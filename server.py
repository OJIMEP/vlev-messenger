from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.protocols.basic import LineOnlyReceiver

class Client(LineOnlyReceiver):
    ip: str = None
    login: str = None
    factory: 'Chat'

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.ip = self.transport.getPeer().host
        self.factory.clients.append(self)
        
        print(f'Client connected: {self.ip}\n')
        
        self.sendLine('Welcome to the chat 1.0\n'.encode())
        
    def lineReceived(self, data: bytes):
        message = data.decode().replace('\n', '')
        server_message = f"<NEW MESSAGE> {message}"
        self.factory.notify_all_users(server_message)

        #if self.login is not None:
        #    server_message = f"{self.login}: {message}" 
        #    self.factory.notify_all_users(server_message)
        #    print(f'{self.ip}: {server_message}')
        #else:
        #    if message.startswith('login:'):
        #        new_login = message.replace('login:', '')
        #        self.factory.clients_login.append(self.login)
        #        if self.factory.clients_login.count(self.login) == 2:
    #                self.transport.write("Error: login already exists\n".encode())
    #                self.transport.write("Your login >>> ".encode())
    #                self.factory.clients_login.remove(self.login)
    #                self.transport.loseConnection()
        #        else:
        #        self.login = new_login
        #        notification = f"New user connected: {self.login}\n"

        #        self.factory.notify_all_users(notification)
        #        print(notification)
        #    else:
        #        print("Error: Invalid client login")    


    def connectionLost(self, reason=None):
        self.factory.clients.remove(self)
        print(f'Client disconnected: {self.ip}')

class Chat(Factory):
    clients: list
    clients_login: list

    def __init__(self):
        self.clients = []

    def startFactory(self):
        print('Server started [OK]')

    def buildProtocol(self, addr):
        return Client(self)

    def notify_all_users(self, data: str):
        for user in self.clients:
            user.sendLine(data.encode()) 

if __name__ == '__main__':
    reactor.listenTCP(7410, Chat())
    reactor.run()
