import requests
from getpass import getpass

api_url = "https://suap.ifrn.edu.br/api/"

token = ""
#user = input("user: ")
#password = getpass()

#data = {"username":user,"password":password}

#response = requests.post(api_url+"token/pair", json=data)
#token = response.json()["access"]
#print(response.json())

headers = {
    "Authorization": f'Bearer {token}'
}

#print(headers)
ano_letivo = int(input("Digite o ano letivo: "))
periodo_letivo = int(input("Digite o período letivo: "))
response = requests.get(api_url+f"ensino/meu-boletim/{ano_letivo}/{periodo_letivo}/", headers=headers)

print(response)

disciplinas = response.json()["results"]

for disciplina in disciplinas:
    print(
        f"{disciplina['disciplina']} -"
        f"{disciplina['nota_etapa_1']} -"
        f"{disciplina['nota_etapa_2']} -"
        f"{disciplina['nota_etapa_3']} -"
        f"{disciplina['nota_etapa_4']}"
    )
print(response)