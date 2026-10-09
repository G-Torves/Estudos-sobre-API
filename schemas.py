from pydantic import BaseModel, Field

class SchemaNovoPersonagem (BaseModel):
    nome: str
    raca: str
    classe: str

class SchemaMostrarPersonagem (BaseModel):
    nome: str
    Status: str
    Senha: str = Field(exclude=True)

class SchemaAtualizarPersonagem (BaseModel):
    nome: str | None = None
    Status: str | None = None
    Senha: str | None = None

