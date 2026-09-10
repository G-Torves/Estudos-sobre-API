from fastapi import FastAPI
import json

app = FastAPI()

def users_json():
    try:
        archive = open("users.json", 'r')
        users = json.load(archive)
        return users
    except FileNotFoundError:
        with open('users.json', 'w') as arquivo:
            arquivo.write("{\n\n}")
        archive = open("users.json", 'r')
        users = json.load(archive)
        return users

@app.get('/')
def raiz ():
    return {"Status": "OK"}

@app.get('/user')
def listar_Usuarios():
    users = users_json()
    return users

@app.get('/user/{user_id}')
def buscar_Usuario(user_id):
    users = users_json()
    return users[f'{user_id}']

@app.post('/user/new')
def novo_Usuario(name: str, password: str):
    users = users_json()
    dados = {'nome': f'{name}', 'Status': 'Ativo', 'Senha': f'{password}'}
    proximo_id = str(max([int(k) for k in users.keys()]) + 1)
    users[proximo_id] = dados

    with open("users.json", "w", encoding="utf-8") as arquivo:
        json.dump(users, arquivo, ensure_ascii=False, indent=4)
    
    return users[proximo_id]

@app.patch('/user/update')
def atualizar_Usuario(user_id: str, alteration_field: str, alteration_value: str):
    user_old = users_json()
    user_old[user_id][f'{alteration_field}'] = alteration_value
    user_new = user_old
    
    with open("users.json", "w", encoding="utf-8") as arquivo:
        json.dump(user_new, arquivo, ensure_ascii=False, indent=4)
    
    return user_new[user_id]
    
@app.delete('/user/delete')
def deletar_Usuario(user_id):
    users = users_json()
    del users[user_id]
    atualized_users = users

    with open("users.json", "w", encoding="utf-8") as arquivo:
        json.dump(atualized_users, arquivo, ensure_ascii=False, indent=4)

    return {'Id apagado com sucesso' : user_id}