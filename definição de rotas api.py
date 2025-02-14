from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/empresas/", response_model=schemas.Empresa)
def criar_empresa(empresa: schemas.EmpresaCreate, db: Depends(get_db)):
    db_empresa = models.Empresa(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@app.get("/empresas/", response_model=list[schemas.Empresa])
def listar_empresas(db: Depends(get_db)):
    return db.query(models.Empresa).all()

@app.post("/obrigacoes/", response_model=schemas.Obrigacao)
def criar_obrigacao(obrigacao: schemas.ObrigacaoCreate, empresa_id: int, db: Depends(get_db)):
    db_obrigacao = models.Obrigacao(**obrigacao.dict(), empresa_id=empresa_id)
    db.add(db_obrigacao)
    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao

@app.get("/obrigacoes/", response_model=list[schemas.Obrigacao])
def listar_obrigacoes(db: Depends(get_db)):
    return db.query(models.Obrigacao).all()