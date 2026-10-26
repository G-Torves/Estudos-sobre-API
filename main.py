from fastapi import FastAPI, HTTPException
import bcrypt
from schemas import SchemaNovoPersonagem, SchemaMostrarPersonagem, SchemaAtualizarPersonagem, SchemaAdicionarItem
from database import novoPersonagem, mostrarPersonagens, atualizarPersonagem, deletarPersonagem, adicionarItem, mostrarInventario, apagarItem, deletarItem, criarItem, apagarItem, criarCriatura, apagarCriatura

app = FastAPI()


@app.get('/')
def raiz ():
    return {"Rota inicial": "OK"}

@app.get('/status')
def status ():
    return {'API': 'OK',
            'Database': 'Em andamento...',
            'IA': 'Em andamento...'}

#===========================================
#                   API                       
#                Personagem
#===========================================
@app.get('/personagem', response_model=dict[str, SchemaMostrarPersonagem])
def listar_Personagens():
    saida = mostrarPersonagens()
    return saida

@app.get('/personagem/{personagem_id}', response_model=SchemaMostrarPersonagem)
def buscar_Personagem(personagem_id: int):
    personagem = mostrarPersonagens(personagem_id)

    if personagem == {}:
        raise HTTPException(
            status_code=404, 
            detail="Personagem não encontrado."
            )

    return personagem

@app.post('/personagem/novo')
def novo_Personagem(personagem: SchemaNovoPersonagem):
    novoPersonagem(personagem.nome, personagem.raca, personagem.classe)
    return {"Concluido": "Personagem criado"}

@app.patch('/personagem/{personagem_id}/atualizar')
def atualizar_Personagem(personagem_id: int, alteracao: SchemaAtualizarPersonagem):
    saida = atualizarPersonagem(personagem_id, alteracao.nome, alteracao.raca, alteracao.classe)
    return saida
    
@app.delete('/personagem/{personagem_id}/apagar')
def apagar_Personagem(personagem_id: int):
    saida = deletarPersonagem(personagem_id)

    return saida

#===========================================
#                   API                       
#               Inventario
#===========================================

@app.get('/inventario')
def listar_inventarios():
    saida = mostrarInventario()

    return saida

@app.get('/inventario/{personagem_id}')
def visualizar_inventario(personagem_id: int):
    saida = mostrarInventario(personagem_id)

    return saida

@app.post('/inventario/{personagem_id}/adicionar_item')
def adicionar_item(personagem_id: int, item: SchemaAdicionarItem):
    saida = adicionarItem(personagem_id, item.itemId, item.quantia, item.equipado, item.durabilidade)
    
    return saida

@app.delete('/inventario/{personagem_id}/apagar_item')
def apagar_item(personagem_id: int):
    saida = apagarItem(personagem_id)

    return saida

@app.patch('/inventario/{personagem_id}/alterar_item')
def alterar_item(personagem_id: int):
    pass