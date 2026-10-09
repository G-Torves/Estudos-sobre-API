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
    nome: str | None = None
    Status: str | None = None
    Senha: str | None = None

