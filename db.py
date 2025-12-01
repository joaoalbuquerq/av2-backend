# db.py
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os


DB_USER = os.getenv("DB_USER", "pedro")
DB_PASS = os.getenv("DB_USER","pp4040%4010")
DB_HOST = os.getenv("DB_HOST", "10.2.1.52")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "biblioteca_db")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

class Livro(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    autor = Column(Text, nullable=True)
    ano_publicacao = Column(Integer, nullable=True)
    disponivel = Column(Boolean, default=False)
    criado_em = Column(TIMESTAMP, server_default=func.now())

def init_db():
    Base.metadata.create_all(bind=engine)
