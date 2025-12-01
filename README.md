# 📚 Projeto Biblioteca --- FastAPI + Flask + PostgreSQL

Este projeto demonstra uma aplicação completa usando:

-   **FastAPI** → API REST responsável pelo CRUD de livros\
-   **Flask** → Aplicação web simples com HTML/Jinja2 interagindo com a
    API ou DB\
-   **SQLAlchemy + PostgreSQL** → Persistência dos dados\
-   **Uvicorn** → Servidor ASGI para rodar a API FastAPI

A FastAPI expõe endpoints para cadastro e consulta de livros, enquanto o
Flask fornece uma interface HTML que permite inserir e visualizar os
dados.

------------------------------------------------------------------------

## 🚀 Funcionalidades

### **API FastAPI**

A API realiza operações CRUD sobre livros:

-   **GET /livros** --- Lista todos os livros\
-   **GET /livros/{id}** --- Obtém um livro específico\
-   **POST /livros** --- Cria um novo livro\
-   **PUT /livros/{id}** --- Atualiza um livro existente\
-   **DELETE /livros/{id}** --- Remove um livro

Também inclui: - Validações Pydantic\
- Tratamento personalizado de erros\
- Documentação automática Swagger em `/docs`

------------------------------------------------------------------------

## 🖥️ Requisitos

Antes de rodar, garanta que possui:

-   Python 3.10+
-   PostgreSQL instalado e rodando\
-   Módulo `python3-venv`

Instale o módulo de virtualenv:

``` bash
sudo apt install python3-venv
```

------------------------------------------------------------------------

## 🔧 Como rodar o projeto

### 1️⃣ Criar e ativar o ambiente virtual

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ Instalar dependências

``` bash
pip install -r dependencies.txt
```

### 3️⃣ Subir a API FastAPI

``` bash
uvicorn api_fast:app --reload --port 8000
```

Documentação disponível:

-   http://localhost:8000/docs
-   http://localhost:8000/redoc

### 4️⃣ Subir a aplicação Flask

``` bash
python3 app_flask.py
```

A aplicação iniciará em:

👉 **http://localhost:5000**

------------------------------------------------------------------------

## 🌐 Endereços importantes

  Função                   URL
  ------------------------ -----------------------------
  API FastAPI (CRUD)       http://localhost:8000
  Interface HTML (Flask)   http://localhost:5000
  Swagger (FastAPI)        http://localhost:8000/docs
  ReDoc (FastAPI)          http://localhost:8000/redoc

------------------------------------------------------------------------

## 🗂️ Estrutura Principal do Projeto

    /project
     ├── api_fast.py           # API FastAPI com CRUD
     ├── app_flask.py          # Interface HTML Flask
     ├── db.py                 # Configuração SQLAlchemy + PostgreSQL
     ├── templates/            # Templates Jinja2 usados pelo Flask
     ├── dependencies.txt      # Lista de dependências
     └── README.md

------------------------------------------------------------------------

## 🏁 Pronto!

Após iniciar FastAPI e Flask, você pode:

-   Usar o **Flask (http://localhost:5000)** para cadastrar e visualizar
    livros\
-   Usar a **API FastAPI (http://localhost:8000)** via endpoints ou
    Postman\
-   Testar tudo pelo Swagger