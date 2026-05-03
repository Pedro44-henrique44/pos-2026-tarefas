from xml.dom.minidom import parse
dom = parse("cardapio.xml")

cardapio = dom.documentElement

pratos_lista = []
pratos = cardapio.getElementsByTagName('prato')

for prato in pratos:
    ID = prato.getAttribute('ID')
    nome_prato = prato.getElementsByTagName('nome_prato')[0].firstChild.data
    descricao = prato.getElementsByTagName('descricao')[0].firstChild.data

    ingredientes = prato.getElementsByTagName('ingredientes')[0]
    ingrediente = ingredientes.getElementsByTagName('ingrediente')

    lista_ingredientes = []
    for item in ingrediente:
        lista_ingredientes.append(item.firstChild.data)

    preco = prato.getElementsByTagName('preco')[0].firstChild.data
    calorias = prato.getElementsByTagName('calorias')[0].firstChild.data
    tempo_preparo = prato.getElementsByTagName('tempo_preparo')[0].firstChild.data

    
    pratos_lista.append({
        "ID": ID,
        "nome_prato": nome_prato,
        "descricao": descricao,
        "ingredientes": lista_ingredientes,
        "preco": preco,
        "calorias": calorias,
        "tempo_preparo": tempo_preparo
    })
    
chave = True

while True:
    print("\nCARDÁPIO:")
    
    for prato in pratos_lista:
        print(f"{prato['ID']} - {prato['nome_prato']}")
    id_escolhido = input("digite o id do prato para saber mais sobre ou 0 para sair: " )

    if id_escolhido == '0':
        break
    encontrado = False
        

    for prato in pratos_lista:
        if id_escolhido == prato["ID"]:
            print("\nCARDÁPIO:")
            print(f"Nome: {prato['nome_prato']}")
            print(f"Descrição: {prato['descricao']}")
            print(f"Ingredientes: {', '.join(prato['ingredientes'])}")
            print(f"Preço: R$ {prato['preco']}")
            print(f"Calorias: {prato['calorias']}")
            print(f"Tempo de preparo: {prato['tempo_preparo']}")
            print("-" * 40)

            encontrado = True
            break

    if encontrado == False:
        print("\nnão achamos o seu prato, ou não há em nosso cardapio")