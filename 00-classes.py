class Human:
    first_name: str
    last_name: str

    def __init__(self, first_name, last_name="Undefind"):
        self.first_name = first_name
        self.last_name = last_name
    
    def __str__(self):
        return f'User: {self.first_name} {self.last_name}'


class User(Human):
    __passport: str = "124334353 3434"
    
    def hello(self):
        print(f'hello, {self.first_name} {self.last_name}')

john = User("John", "Doe")
john.hello()

artur = User("Artur")
artur.hello()

print(john)