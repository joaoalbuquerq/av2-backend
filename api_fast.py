# api_fast.py
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

from db import SessionLocal, init_db, Livro

app = FastAPI(title="API Biblioteca - FastAPI")

# Inicializa a tabela caso não exista
init_db()

# Pydantic schemas
class LivroBase(BaseModel):
    titulo: str = Field(..., title="Título do livro")
    autor: Optional[str] = Field(None, title="Autor")
    ano_publicacao: Optional[int] = Field(None, title="Ano de publicação")
    disponivel: Optional[bool] = Field(False, title="Disponível")

    @validator("titulo")
    def titulo_nao_vazio(cls, v):
        if isinstance(v, str) and not v.strip():
            raise ValueError("titulo não pode ser vazio")
        return v

class LivroCreate(LivroBase):
    pass

class LivroUpdate(BaseModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    ano_publicacao: Optional[int] = None
    disponivel: Optional[bool] = None

    @validator("titulo")
    def titulo_nao_vazio(cls, v):
        if v is not None and not v.strip():
            raise ValueError("titulo não pode ser vazio")
        return v

class LivroOut(LivroBase):
    id: int
    criado_em: Optional[datetime]

    class Config:
        orm_mode = True

# Tratamento de erros de validação para retornar 400 e listar campos faltantes
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # extrair campos faltantes/erros
    errors = exc.errors()
    campos = []
    mensagens = []
    for err in errors:
        loc = ".".join([str(l) for l in err.get("loc", []) if l != "body"])
        msg = err.get("msg")
        # se for 'field required' pega o nome do campo
        campos.append(loc or err.get("loc")[-1])
        mensagens.append(f"{loc or err.get('loc')[-1]}: {msg}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": mensagens, "fields": campos}
    )

# CRUD endpoints
@app.get("/livros", response_model=List[LivroOut], status_code=status.HTTP_200_OK)
def listar_livros():
    db = SessionLocal()
    try:
        livros = db.query(Livro).order_by(Livro.id).all()
        return livros
    finally:
        db.close()

@app.get("/livros/{livro_id}", response_model=LivroOut)
def obter_livro(livro_id: int):
    db = SessionLocal()
    try:
        livro = db.query(Livro).filter(Livro.id == livro_id).first()
        if not livro:
            raise HTTPException(status_code=404, detail="Livro não encontrado")
        return livro
    finally:
        db.close()

@app.post("/livros", response_model=LivroOut, status_code=status.HTTP_201_CREATED)
def criar_livro(payload: LivroCreate):
    db = SessionLocal()
    try:
        livro = Livro(
            titulo=payload.titulo.strip(),
            autor=payload.autor,
            ano_publicacao=payload.ano_publicacao,
            disponivel=payload.disponivel or False
        )
        db.add(livro)
        db.commit()
        db.refresh(livro)
        return {
            "id": livro.id,
            "titulo": livro.titulo,
            "autor": livro.autor,
            "ano_publicacao": livro.ano_publicacao,
            "disponivel": livro.disponivel,
            "criado_em": livro.criado_em.isoformat() if livro.criado_em else None
        }
    finally:
        db.close()

@app.put("/livros/{livro_id}", response_model=LivroOut)
def atualizar_livro(livro_id: int, payload: LivroUpdate):
    db = SessionLocal()
    try:
        livro = db.query(Livro).filter(Livro.id == livro_id).first()
        if not livro:
            raise HTTPException(status_code=404, detail="Livro não encontrado")
        # atualiza apenas campos fornecidos
        for field, value in payload.dict(exclude_unset=True).items():
            setattr(livro, field, value)
        db.commit()
        db.refresh(livro)
        return livro
    finally:
        db.close()

@app.delete("/livros/{livro_id}", status_code=status.HTTP_200_OK)
def deletar_livro(livro_id: int):
    db = SessionLocal()
    try:
        livro = db.query(Livro).filter(Livro.id == livro_id).first()
        if not livro:
            raise HTTPException(status_code=404, detail="Livro não encontrado")
        db.delete(livro)
        db.commit()
        return {"detail": f"Livro {livro_id} deletado com sucesso"}
    finally:
        db.close()

# Se rodar diretamente: uvicorn api_fast:app --reload --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_fast:app", host="0.0.0.0", port=8000, reload=True)
