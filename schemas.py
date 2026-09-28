from pydantic import BaseModel, Field

class new_character (BaseModel):
    nome: str
    senha: str

class show_character (BaseModel):
    nome: str
    Status: str
    Senha: str = Field(exclude=True)

class update_character (BaseModel):
    nome: str | None = None
    Status: str | None = None
    Senha: str | None = None

