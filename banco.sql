CREATE DATABASE biblioteca_db;

\c biblioteca_db;

CREATE TABLE IF NOT EXISTS livros (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    autor TEXT,
    ano_publicacao INT,
    disponivel BOOLEAN DEFAULT false,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);