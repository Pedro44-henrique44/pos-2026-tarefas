import json


with open("imobiliaria.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

imoveis_lista = dados["imobiliaria"]["imovel"]

while True:
    print("\nIMOBILIARIA:")

    for imovel in imoveis_lista:
        print(f"{imovel['ID']} - {imovel['descricao']}")

    id_escolhido = input("digite o id do imovel para saber mais sobre ou 0 para sair: ")

    if id_escolhido == "0":
        break

    encontrado = False

    for imovel in imoveis_lista:
        if id_escolhido == imovel["ID"]:
            proprietario = imovel["proprietario"]
            endereco = imovel["endereco"]
            caracteristicas = imovel["caracteristicas"]

            print("\nIMOVEL:")
            print(f"ID: {imovel['ID']}")
            print(f"Descricao: {imovel['descricao']}")
            print(f"Valor: R$ {imovel['valor']}")

            print("\nPROPRIETARIO:")
            print(f"Nome: {proprietario['nome']}")

            if "email" in proprietario:
                print(f"Email: {proprietario['email']}")

            print(f"Telefone: {', '.join(proprietario['telefone'])}")

            print("\nENDERECO:")
            print(f"Rua: {endereco['rua']}")
            print(f"Bairro: {endereco['bairro']}")
            print(f"Cidade: {endereco['cidade']}")

            if "numero" in endereco:
                print(f"Numero: {endereco['numero']}")

            print("\nCARACTERISTICAS:")
            print(f"Banheiros: {caracteristicas['numBanheiros']}")
            print(f"Quartos: {caracteristicas['numQuartos']}")
            print(f"Tamanho: {caracteristicas['tamanho']} m2")
            print("-" * 40)

            encontrado = True
            break

    if encontrado == False:
        print("\nnao achamos esse imovel na imobiliaria")
