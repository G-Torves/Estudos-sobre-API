from pydantic import BaseModel, Field

# Personagem
class SchemaNovoPersonagem (BaseModel):
    nome: str
    raca: str
    classe: str

class SchemaMostrarPersonagem (BaseModel):
    nome: str
    nivel: int
    raca: str
    classe: str

class SchemaAtualizarPersonagem (BaseModel):
    nome: None | str
    raca: None | str
    classe: None | str

# Inventario
class SchemaAdicionarItem (BaseModel):
    itemId: int
    quantia: int
    equipado: bool
    durabilidade: int

class SchemaAlterarItem (BaseModel):
    quantia: int
    equipado: bool
    durabilidade: int

class SchemaMostrarInventario (BaseModel):
    pass

# Arsenal


# Bestiario

