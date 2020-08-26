import requests

response = requests.get('http://jsonplaceholder.typicode.com/users')

users = response.json()

email = users[0]['email']

print(email)

new_user = {
    "email": 'jon@mail.ru',
    "first_name": 'john'
}

resp = requests.post('http://jsonplaceholder.typicode.com/users', new_user)

print(resp.json())