from fastapi import FastAPI, HTTPException
import bcrypt
from schemas import SchemaNovoPersonagem, SchemaMostrarPersonagem, SchemaAtualizarPersonagem
from database import novoPersonagem, mostrarPersonagens
app = FastAPI()


# Funções úteis
def password_crypt(senha):
    salt = bcrypt.gensalt()
    senha = senha.encode('utf-8')
    
    hash_password = bcrypt.hashpw(senha, salt)
    return hash_password

# API
@app.get('/')
def raiz ():
    return {"Status": "OK"}

@app.get('/status')
def status ():
    return {'API': 'OK',
            'Database': 'Em andamento...',
            'IA': 'Em andamento...'}

@app.get('/personagem', response_model=dict[str, SchemaMostrarPersonagem])
def listar_Personagens():
    mostrar = mostrarPersonagens()
    return mostrar

@app.get('/personagem/{personagem_id}', response_model=SchemaMostrarPersonagem)
def buscar_Personagem(personagem_id):
    personagem = personagem_json()

    if personagem_id not in personagem:
        raise HTTPException(
            status_code=404, 
            detail="Personagem não encontrado."
            )
    return personagem[f'{personagem_id}']

@app.post('/personagem/novo')
def novo_Personagem(SchemaNovoPersonagem: SchemaNovoPersonagem):
    novoPersonagem(SchemaNovoPersonagem.nome, SchemaNovoPersonagem.raca, SchemaNovoPersonagem.classe)
    return {"Concluido": "Personagem criado"}

@app.patch('/personagem/atualizar')
def atualizar_Personagem(personagem_id: str, alteracao: SchemaAtualizarPersonagem):
    user_old = personagem_json()

    if personagem_id not in user_old:
        raise HTTPException(
            status_code=404,
            detail="Usuario não encontrado"
        )

    user = user_old[personagem_id]
    update = alteracao.model_dump(exclude_unset=True)

    for chave, valor in update.items():
        if chave == "Senha":
            user[chave] = password_crypt(valor)
        else:
            user[chave] = valor
    return user

    
@app.delete('/personagem/apagar')
def apagar_Personagem(personagem_id):
    personagem = personagem_json()
    del personagem[personagem_id]
    atualized_personagem = personagem

    with open("personagem.json", "w", encoding="utf-8") as arquivo:
        json.dump(atualized_personagem, arquivo, ensure_ascii=False, indent=4)

    return {'Id apagado com sucesso' : personagem_id}