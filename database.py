from sqlalchemy import create_engine, ForeignKey, select 
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column, relationship, Session
from typing import List, Optional

engine = create_engine("sqlite:///rpg.db")
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

    itemId: Mapped[int] = mapped_column(
        ForeignKey("arsenal.id"),
        nullable=False
)
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

def mostrarPersonagens (id = None):
    with Session(engine) as session:
        saida = {}

        if id != None:
            banco = select(personagem).where(personagem.id == id)
            for i in session.scalars(banco):
                saida = {
                    "id": f"{i.id}",
                    "nome": f"{i.nome}",
                    "nivel": f"{i.nivel}",
                    "raca": f"{i.raca}",
                    "classe": f"{i.classe}"
                }

        else:
            banco = select(personagem)
            lista = []
            for i in session.scalars(banco):
                pp = {
                    "id": f"{i.id}",
                    "nome": f"{i.nome}",
                    "nivel": f"{i.nivel}",
                    "raca": f"{ i.raca}",
                    "classe": f"{i.classe}"
                    }
                lista.append(pp)
                
                for j in lista:
                    id_personagem = j["id"]
        
                    saida[id_personagem] = {
                    "id": j["id"],
                    "nome": j["nome"],
                    "nivel": j["nivel"],
                    "raca": j["raca"],
                    "classe": j["classe"]
                    }
        return saida

def atualizarPersonagem (id: int, novoNome = None, novaRaca = None, novaClasse = None):
    script  = select(personagem).where(personagem.id == id)
    saida = {}
    with Session(engine) as session:
        pAntigo = session.scalars(script).first()

        if novoNome != None:
            pAntigo.nome = novoNome
        if novaRaca != None:
            pAntigo.raca = novaRaca
        if novaClasse != None:
            pAntigo.classe = novaClasse

        session.commit()

        for i in session.scalars(script):
                saida = {
                    "id": f"{i.id}",
                    "nome": f"{i.nome}",
                    "nivel": f"{i.nivel}",
                    "raca": f"{i.raca}",
                    "classe": f"{i.classe}"
                }

    return saida

def deletarPersonagem (id: int):
    script  = select(personagem).where(personagem.id == id)
    with Session(engine) as session:
        apagar = session.scalars(script).first()

        if apagar:
            session.delete(apagar)
            session.commit()
            mostrar = {"Resultado": f"Personagem {id} apagado com sucesso!"}
        else:
            mostrar = {"Resultado": f"Falha ao apagar o personagem {id}!"}

    return mostrar

def mostrarInventario (id = None):
    with Session(engine) as session:
        saida = {}

        if id != None:
            banco = select(inventario).where(inventario.ownerId == id)
            for i in session.scalars(banco):
                saida = {
                    "Dono": f"{i.owner.nome}",
                    "" : ""
                }

        print(saida)
    
def adicionarItem(ownerId, itemId, quantia, equipado, durabilidade):
        with Session(engine) as session:
            novoItem = inventario(ownerId=ownerId, itemId=itemId, quantia=quantia, equipado=equipado, durabilidade=durabilidade)

            session.add(novoItem)
            session.commit()

mostrarInventario(1)