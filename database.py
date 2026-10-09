from sqlalchemy import create_engine, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column, relationship, Session
from typing import List, Optional

engine = create_engine("sqlite:///rpg.db", echo=True)
SessionMK = sessionmaker(bind=engine)

class Base (DeclarativeBase):
    pass

#===========================================
#              Banco de dados                                         
#===========================================

# Personagem
class personagem (Base):
    __tablename__ = "personagem"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)

    nome: Mapped[str]
    nivel: Mapped[int] = mapped_column(default=1)
    raca: Mapped[str]
    classe: Mapped[str]

    forca: Mapped[int] = mapped_column(default=5)
    magick: Mapped[int] = mapped_column(default=5)
    velocidade: Mapped[int] = mapped_column(default=5)

    inventario: Mapped[List["inventario"]] = relationship (
        "inventario",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

# Armas e Itens
class arsenal (Base):
    __tablename__ = "arsenal"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)

    nome: Mapped[str]
    durabilidade: Mapped[Optional[int]] 
    dano: Mapped[Optional[int]]
    descricao: Mapped[str]

# Npcs e Monstros
class bestiario (Base):
    __tablename__ = "bestiario"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)

    nome: Mapped[str]
    raca: Mapped[str]
    minLvl: Mapped[int]
    maxLvl: Mapped[int]
    descricao: Mapped[str]

# Inventario
class inventario (Base):
    __tablename__ = "inventario"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    ownerId: Mapped[int] = mapped_column(
        ForeignKey("personagem.id", ondelete="CASCADE"),
        nullable=False
        )

    itemId: Mapped[int]
    quantia: Mapped[int] = mapped_column(default=1)
    equipado: Mapped[bool] = mapped_column(default=False)
    durabilidade: Mapped[int]

    owner: Mapped["personagem"] = relationship("personagem", back_populates="inventario")


Base.metadata.create_all(bind=engine)

#===========================================
#              Banco de dados                       
#                 Funções
#===========================================

def novoPersonagem (nome, raca, classe):
    with Session(engine) as session:
        novoPersonagem = personagem(nome=nome, raca=raca, classe=classe)

        session.add(novoPersonagem)
        session.commit()

def mostrarPersonagens ():
    with Session(engine) as session:
        banco = select(personagem)
        saida = []
        for i in session.scalars(banco):
            pp = {"id": i.id,
                  "nome": i.nome,
                  "nivel": i.nivel,
                  "raca": i.raca,
                  "classe": i.classe}
            saida.append(pp)
        return saida
