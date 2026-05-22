import users_wrapper as users


while True:
    print("\nMENU USERS")
    print("1 - Listar usuarios")
    print("2 - Buscar usuario")
    print("3 - Criar usuario")
    print("4 - Atualizar usuario")
    print("5 - Deletar usuario")
    print("0 - Sair")

    opcao = input("Digite uma opcao: ")

    if opcao == "0":
        break

    elif opcao == "1":
        users_list = users.list()

        for user in users_list:
            print("ID:", user["id"])
            print("Nome:", user["name"])
            print("Username:", user["username"])
            print("Email:", user["email"])
            print()

    elif opcao == "2":
        user_id = input("Digite o ID do usuario: ")
        user = users.read(user_id)

        print("ID:", user["id"])
        print("Nome:", user["name"])
        print("Username:", user["username"])
        print("Email:", user["email"])
        print("Telefone:", user["phone"])
        print("Site:", user["website"])

    elif opcao == "3":
        nome = input("Digite o nome: ")
        username = input("Digite o username: ")
        email = input("Digite o email: ")

        user = {
            "name": nome,
            "username": username,
            "email": email
        }

        novo_user = users.create(user)
        print("Usuario criado:")
        print(novo_user)

    elif opcao == "4":
        user_id = input("Digite o ID do usuario: ")
        nome = input("Digite o novo nome: ")
        username = input("Digite o novo username: ")
        email = input("Digite o novo email: ")

        user = {
            "name": nome,
            "username": username,
            "email": email
        }

        user_atualizado = users.update(user_id, user)
        print("Usuario atualizado:")
        print(user_atualizado)

    elif opcao == "5":
        user_id = input("Digite o ID do usuario: ")
        status = users.delete(user_id)

        print("Status da requisicao:", status)

        if status == 200:
            print("Usuario deletado")

    else:
        print("Opcao invalida")
