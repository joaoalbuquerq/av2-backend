# db.py
import os
import time
import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3030")
DB_NAME = os.getenv("DB_NAME", "biblioteca_db")

Base = declarative_base()

class Livro(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    autor = Column(Text, nullable=True)
    ano_publicacao = Column(Integer, nullable=True)
    disponivel = Column(Boolean, default=False)
    criado_em = Column(TIMESTAMP, server_default=func.now())

# ------------------------------------------------------------------
# 1 - Criar banco se não existir
# ------------------------------------------------------------------
def criar_banco():
    print("🔍 Verificando existência do banco...")

    conn = None
    while not conn:
        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user=DB_USER,
                password=DB_PASS,
                host=DB_HOST,
                port=DB_PORT
            )
        except Exception:
            print("⏳ Aguardando Postgres iniciar...")
            time.sleep(2)

    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (DB_NAME,))
    exists = cur.fetchone()

    if not exists:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
        print(f"📌 Banco '{DB_NAME}' criado!")
    else:
        print(f"✔️ Banco '{DB_NAME}' já existe.")

    cur.close()
    conn.close()


# ------------------------------------------------------------------
# 2 - Criar tabelas específicas da aplicação
# ------------------------------------------------------------------
def criar_tabelas():
    print("🔧 Criando tabelas (se necessário)...")

    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        pool_pre_ping=True
    )
    Base.metadata.create_all(bind=engine)
    print("✔️ Tabelas prontas.")

# ------------------------------------------------------------------
# 3 - Inicialização completa
# ------------------------------------------------------------------
def inicializar_banco():
    criar_banco()
    criar_tabelas()


# ------------------------------------------------------------------
# 4 - SQLAlchemy engine e sessão
# ------------------------------------------------------------------
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    