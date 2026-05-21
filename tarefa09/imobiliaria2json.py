import json
from xml.dom.minidom import parse


dom = parse("imobiliaria.xml")
imobiliaria = dom.documentElement

lista_imoveis = []
imoveis = imobiliaria.getElementsByTagName("imovel")

for imovel in imoveis:
    ID = imovel.getAttribute("ID")
    descricao = imovel.getElementsByTagName("descricao")[0].firstChild.data

    proprietario = imovel.getElementsByTagName("proprietario")[0]
    nome = proprietario.getElementsByTagName("nome")[0].firstChild.data

    telefones = []
    telefone_tags = proprietario.getElementsByTagName("telefone")
    for telefone in telefone_tags:
        telefones.append(telefone.firstChild.data)

    dados_proprietario = {
        "nome": nome,
        "telefone": telefones
    }

    email_tags = proprietario.getElementsByTagName("email")
    if len(email_tags) > 0:
        email = email_tags[0].firstChild.data
        dados_proprietario["email"] = email

    endereco = imovel.getElementsByTagName("endereco")[0]
    rua = endereco.getElementsByTagName("rua")[0].firstChild.data
    bairro = endereco.getElementsByTagName("bairro")[0].firstChild.data
    cidade = endereco.getElementsByTagName("cidade")[0].firstChild.data

    dados_endereco = {
        "rua": rua,
        "bairro": bairro,
        "cidade": cidade
    }

    numero_tags = endereco.getElementsByTagName("numero")
    if len(numero_tags) > 0:
        numero = numero_tags[0].firstChild.data
        dados_endereco["numero"] = int(numero)

    caracteristicas = imovel.getElementsByTagName("caracteristicas")[0]
    num_banheiros = caracteristicas.getElementsByTagName("numBanheiros")[0].firstChild.data
    num_quartos = caracteristicas.getElementsByTagName("numQuartos")[0].firstChild.data
    tamanho = caracteristicas.getElementsByTagName("tamanho")[0].firstChild.data

    valor = imovel.getElementsByTagName("valor")[0].firstChild.data

    dados_imovel = {
        "ID": ID,
        "descricao": descricao,
        "proprietario": dados_proprietario,
        "endereco": dados_endereco,
        "caracteristicas": {
            "numBanheiros": int(num_banheiros),
            "numQuartos": int(num_quartos),
            "tamanho": int(tamanho)
        },
        "valor": int(valor)
    }

    lista_imoveis.append(dados_imovel)

dados_imobiliaria = {
    "imobiliaria": {
        "imovel": lista_imoveis
    }
}

with open("imobiliaria.json", "w", encoding="utf-8") as arquivo:
    json.dump(dados_imobiliaria, arquivo, indent=4, ensure_ascii=False)

print("Arquivo imobiliaria.json criado com sucesso.")
