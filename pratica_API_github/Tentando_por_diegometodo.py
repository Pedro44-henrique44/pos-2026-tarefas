import requests
from requests.auth import HTTPBasicAuth
from getpass import getpass

user = input("user: ")
password = getpass()
  
response = requests.get('https://api.github.com/user',
            auth = HTTPBasicAuth(user, password))
  
print(response.text)
print(response)

#esse método não funciona no github a anos. 
#não lembro como diego fez essa atividade, mas o arquivo "API_github.py"
#que fiz, funciona.