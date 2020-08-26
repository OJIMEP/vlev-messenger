from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

class Client(Protocol):
    ip: str = None
    login: str = None
    factory: 'Chat'

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.ip = self.transport.getHost().host
        self.factory.clients.append(self)
        
        print(f'Client connected: {self.ip}\n')
        
        self.transport.write('Welcome to the chat 1.0\n'.encode())
        
    def dataReceived(self, data: bytes):
        message = data.decode().replace('\n', '')

        if self.login is not None:
            server_message = f"{self.login}: {message}" 
            self.factory.notify_all_users(server_message)
            print(f'{self.ip}: {server_message}')
        else:
            if message.startswith('login:'):
                new_login = message.replace('login:', '')
                for user in self.factory.clients:
                    if user.login == new_login:
                        self.transport.write("Error: login already exists\n".encode())
                        self.connectionLost()
                        return

                self.login = new_login
                notification = f"New user connected: {self.login}\n"

                self.factory.notify_all_users(notification)
                print(notification)
            else:
                print("Error: Invalid client login")    


    def connectionLost(self, reason=None):
        self.factory.clients.remove(self)

class Chat(Factory):
    clients: list

    def __init__(self):
        self.clients = []

    def startFactory(self):
        print('Server started [OK]')

    def buildProtocol(self, addr):
        return Client(self)

    def notify_all_users(self, data: str):
        for user in self.clients:
            user.transport.write(data.encode()) 

if __name__ == '__main__':
    reactor.listenTCP(7410, Chat())
    reactor.run()
