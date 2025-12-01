
from flask import Flask, render_template, request, redirect, url_for
from db import SessionLocal, inicializar_banco, Livro
import os

import requests

app = Flask(__name__)

# garante que tabela exista
inicializar_banco()

USE_API = os.getenv("FLASK_USE_API", "false").lower() == "true"
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")

def listar_livros_db():
    db = SessionLocal()
    try:
        return db.query(Livro).order_by(Livro.id).all()
    finally:
        db.close()

@app.route("/", methods=["GET", "POST"])
def index():
    mensagem = None
    if request.method == "POST":

        # validação: titulo é obrigatório
        titulo = request.form.get("titulo", "").strip()
        autor = request.form.get("autor", "").strip() or None
        ano = request.form.get("ano_publicacao", "").strip()
        disponivel = request.form.get("disponivel") == "true"

        missing = []
        if not titulo:
            missing.append("titulo")

        # valida ano se informado
        ano_int = None
        if ano:
            try:
                ano_int = int(ano)
            except ValueError:
                mensagem = "Campo 'ano_publicacao' inválido. Deve ser um número."
                # mantém a listagem e mostra erro
                if USE_API:
                    try:
                        livros = requests.get(f"{FASTAPI_URL}/livros").json()
                    except Exception:
                        livros = []
                else:
                    livros = listar_livros_db()
                return render_template("index.html", livros=livros, mensagem=mensagem)

        if missing:
            mensagem = f"Campos obrigatórios faltando: {', '.join(missing)}"
        else:
            # inserir via DB local
            if USE_API:
                # usa a API FastAPI
                payload = {
                    "titulo": titulo,
                    "autor": autor,
                    "ano_publicacao": ano_int,
                    "disponivel": disponivel
                }
                r = requests.post(f"{FASTAPI_URL}/livros", json=payload)
                if r.status_code not in (200, 201):
                    mensagem = f"Erro ao criar via API: {r.status_code} {r.text}"
            else:
                db = SessionLocal()
                try:
                    novo = Livro(titulo=titulo, autor=autor, ano_publicacao=ano_int, disponivel=disponivel)
                    db.add(novo)
                    db.commit()
                finally:
                    db.close()

    # GET ou após POST
    if USE_API:
        try:
            resp = requests.get(f"{FASTAPI_URL}/livros")
            livros = resp.json() if resp.status_code == 200 else []
        except Exception as e:
            livros = []
            if mensagem is None:
                mensagem = f"Erro ao consultar API FastAPI: {e}"
    else:
        livros = listar_livros_db()

    return render_template("index.html", livros=livros, mensagem=mensagem)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
