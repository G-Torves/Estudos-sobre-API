from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column, relationship
from typing import List, Optional

engine = create_engine("sqlite:///rpg.db", echo=True)
Session = sessionmaker(bind=engine)

class Base (DeclarativeBase):
    pass

#===========================================
#              Banco de dados                       
#                  Base
#===========================================

# Personagem
class character (Base):
    __tablename__ = "character"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)

    name: Mapped[str]
    level: Mapped[int]
    raca: Mapped[str]
    classe: Mapped[str]

    strength: Mapped[int]
    magic: Mapped[int]
    speed: Mapped[int]

    inventory: Mapped[List["inventory"]] = relationship (
        "inventory",
        back_populates="Owner",
        cascade="all, delete-orphan"
    )

# Armas e Itens
class dictionary (Base):
    __tablename__ = "dictionary"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)

    name: Mapped[str]
    durability: Mapped[Optional[int]] 
    damage: Mapped[Optional[int]]
    desc: Mapped[str]

# Npcs e Monstros
class bestiary (Base):
    __tablename__ = "bestiary"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)

    name: Mapped[str]
    race: Mapped[str]
    minLvl: Mapped[int]
    maxLvl: Mapped[int]
    desc: Mapped[str]

#===========================================
#               Banco de dados                         
#                     FK
#===========================================

# Inventario
class inventory (Base):
    __tablename__ = "inventory"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    ownerId: Mapped[int] = mapped_column(
        ForeignKey("character.id", ondelete="CASCADE"),
        nullable=False
        )

    itemId: Mapped[int]
    amount: Mapped[int] = mapped_column(default=1)
    isEquiped: Mapped[bool] = mapped_column(default=False)
    durability: Mapped[int]

    owner: Mapped["character"] = relationship("character", back_populates="inventory")

Base.metadata.create_all(bind=engine)