import requests


resposta = requests.get("https://jsonplaceholder.typicode.com/users/3/todos")
todos = resposta.json()

print("TO-DOS DO USUARIO 3")

for todo in todos:
    print("ID:", todo["id"])
    print("User ID:", todo["userId"])
    print("Titulo:", todo["title"])
    print("Concluido:", todo["completed"])
    print()

print("Atributos dos to-dos:")
print(todos[0].keys())
print()

resposta = requests.get("https://jsonplaceholder.typicode.com/posts/3/comments")
comentarios = resposta.json()

print("COMENTARIOS DO POST 3")

for comentario in comentarios:
    print("ID:", comentario["id"])
    print("Post ID:", comentario["postId"])
    print("Nome:", comentario["name"])
    print("Email:", comentario["email"])
    print("Comentario:", comentario["body"])
    print()

print("Atributos dos comentarios:")
print(comentarios[0].keys())
