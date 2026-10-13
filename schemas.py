from pydantic import BaseModel, Field

class SchemaNovoPersonagem (BaseModel):
    nome: str
    raca: str
    classe: str

class SchemaMostrarPersonagem (BaseModel):
    nome: str
    nivel: str
    raca: str
    classe: str

class SchemaAtualizarPersonagem (BaseModel):
    nome: None | str
    raca: None | str
    classe: None | str

