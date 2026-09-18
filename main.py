from fastapi import FastAPI, HTTPException
import json
import bcrypt
from basemodel import new_character, show_character

app = FastAPI()

# Funções úteis
def password_crypt(password):
    salt = bcrypt.gensalt()
    password = password.encode('utf-8')
    
    hash_password = bcrypt.hashpw(password,salt)
    return hash_password

def personagem_json():
    try:
        archive = open("personagem.json", 'r')
        personagem = json.load(archive)
        return personagem
    except FileNotFoundError:
        with open('personagem.json', 'w') as arquivo:
            arquivo.write("{\n\n}")
        archive = open("personagem.json", 'r')
        personagem = json.load(archive)
        return personagem

# API
@app.get('/')
def raiz ():
    return {"Status": "OK"}

@app.get('/status')
def status ():
    return {'API': 'OK',
            'Database': 'Em andamento...',
            'IA': 'Em andamento...'}

@app.get('/personagem', response_model=dict[str, show_character])
def listar_Personagens():
    personagem = personagem_json()
    return personagem

@app.get('/personagem/{personagem_id}', response_model=show_character)
def buscar_Personagem(personagem_id):
    personagem = personagem_json()

    if personagem_id not in personagem:
        raise HTTPException(
            status_code=404, 
            detail="Personagem não encontrado."
            )
    return personagem[f'{personagem_id}']

@app.post('/personagem/new')
def novo_Personagem(new_character: new_character):
    personagem = personagem_json()
    dados = {'nome': f'{new_character.nome}', 'Status': 'Ativo', 'Senha': f'{password_crypt(new_character.senha)}'}
    key = personagem.keys()
    if key:
        proximo_id = str(max([int(k) for k in key]) + 1)
    else: 
        proximo_id = '1' 
    personagem[proximo_id] = dados

    with open("personagem.json", "w", encoding="utf-8") as arquivo:
        json.dump(personagem, arquivo, ensure_ascii=False, indent=4)
    
    return personagem[proximo_id]

@app.patch('/personagem/update')
def atualizar_Personagem(personagem_id: str, alteration_field: str, alteration_value: str):
    user_old = personagem_json()
    user_old[personagem_id][f'{alteration_field}'] = alteration_value
    user_new = user_old
    
    if personagem_id not in user_old:
        raise HTTPException(
            status_code=404,
            detail="Usuario não encontrado"
        )
    with open("personagem.json", "w", encoding="utf-8") as arquivo:
        json.dump(user_new, arquivo, ensure_ascii=False, indent=4)
    
    return user_new[personagem_id]
    
@app.delete('/personagem/delete')
def deletar_Personagem(personagem_id):
    personagem = personagem_json()
    del personagem[personagem_id]
    atualized_personagem = personagem

    with open("personagem.json", "w", encoding="utf-8") as arquivo:
        json.dump(atualized_personagem, arquivo, ensure_ascii=False, indent=4)

    return {'Id apagado com sucesso' : personagem_id}