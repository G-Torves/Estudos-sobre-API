from pydantic import BaseModel, EmailStr, Field

class new_character (BaseModel):
    nome: str
    senha: str

class show_character (BaseModel):
    nome: str
    Status: str
    Senha: str = Field(exclude=True)
