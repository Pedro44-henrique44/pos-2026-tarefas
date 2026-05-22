import requests


api_url = "https://jsonplaceholder.typicode.com/users"


def list():
    resposta = requests.get(api_url)
    return resposta.json()


def read(user_id):
    resposta = requests.get(api_url + "/" + str(user_id))
    return resposta.json()


def create(user):
    resposta = requests.post(api_url, json=user)
    return resposta.json()


def update(user_id, user):
    resposta = requests.put(api_url + "/" + str(user_id), json=user)
    return resposta.json()


def delete(user_id):
    resposta = requests.delete(api_url + "/" + str(user_id))
    return resposta.status_code
