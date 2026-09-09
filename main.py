from fastapi import FastAPI
import json

app = FastAPI()

def usersJson():
    archive = open("users.json", 'r')
    users = json.load(archive)
    return users

@app.get('/')
def raiz ():
    return {"Status": "OK"}

@app.get('/user')
def listar_Usuarios():
    users = usersJson()
    return users

@app.get('/user/{user_id}')
def buscar_Usuario(user_id):
    users = usersJson()
    return users[f'{user_id}']

@app.post('/user/new')
def novo_Usuario(nome: str, senha: str):
    users = usersJson()
    dados = {'nome': f'{nome}', 'Status': 'Ativo', 'Senha': f'{senha}'}
    proximo_id = str(max([int(k) for k in users.keys()]) + 1)
    users[proximo_id] = dados

    with open("users.json", "w", encoding="utf-8") as arquivo:
        json.dump(users, arquivo, ensure_ascii=False, indent=4)
    
    return users[proximo_id]
