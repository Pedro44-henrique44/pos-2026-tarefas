import requests
from getpass import getpass

token = input("Token do Github: ")

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

while True:
    print("\n1 - Listar seguidores")
    print("2 - Seguir usuário")
    print("3 - Parar de seguir usuário")
    print("4 - Sair")

    opcao = input("Escolha: ")

    if opcao == "1":
        response = requests.get(
            "https://api.github.com/user/followers",
            headers=headers
        )

        seguidores = response.json()
        #print(response.status_code)
        #print(seguidores)

        print("\nSeguidores:")
        for seguidor in seguidores:
            print("-", seguidor["login"])
    elif opcao == "2":
        usuario = input("Usuário a seguir: ")

        response = requests.put(
            f"https://api.github.com/user/following/{usuario}",
            headers=headers
        )

        if response.status_code == 204:
            print("Usuário seguido com sucesso.")
        else:
            print("Erro ao seguir usuário.")

    elif opcao == "3":
        usuario = input("Usuário para deixar de seguir: ")

        response = requests.delete(
            f"https://api.github.com/user/following/{usuario}",
            headers=headers
        )

        if response.status_code == 204:
            print("Usuário removido com sucesso.")
        else:
            print("Erro ao deixar de seguir usuário.")

    elif opcao == "4":
        break

    else:
        print("Opção inválida.")