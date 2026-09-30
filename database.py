from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column, relationship
from typing import List, Optional

engine = create_engine("sqlite:///rpg.db", echo=True)
Session = sessionmaker(bind=engine)

class Base (DeclarativeBase):
    pass

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

class dictionary (Base):
    __tablename__ = "dictionary"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)

    name: Mapped[str]
    durability: Mapped[Optional[int]] 
    damage: Mapped[Optional[int]]
    desc: Mapped[str]


Base.metadata.create_all(bind=engine)