from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException
from dotenv import load_dotenv
import os

Base = declarative_base()

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    cnpj = Column(String, unique=True)
    endereco = Column(String)
    email = Column(String)
    telefone = Column(String)

    obrigacoes = relationship("ObrigacaoAcessoria", back_populates="empresa")

class ObrigacaoAcessoria(Base):
    __tablename__ = "obrigacoes_acessorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    periodicidade = Column(String)
    empresa_id = Column(Integer, ForeignKey("empresas.id"))

    empresa = relationship("Empresa", back_populates="obrigacoes")

class EmpresaCreate(BaseModel):
    nome: str
    cnpj: str
    endereco: str
    email: str
    telefone: str

class Empresa(EmpresaCreate):
    id: int
    obrigacoes: list["ObrigacaoAcessoria"] = []

    class Config:
        orm_mode = True

class ObrigacaoAcessoriaCreate(BaseModel):
    nome: str
    periodicidade: str

class ObrigacaoAcessoria(ObrigacaoAcessoriaCreate):
    id: int
    empresa_id: int

    class Config:
        orm_mode = True

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/empresas/", response_model=Empresa)
def criar_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    db_empresa = Empresa(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@app.get("/empresas/", response_model=list[Empresa])
def listar_empresas(db: Session = Depends(get_db)):
    return db.query(Empresa).all()

@app.post("/obrigacoes/", response_model=ObrigacaoAcessoria)
def criar_obrigacao(obrigacao: ObrigacaoAcessoriaCreate, empresa_id: int, db: Session = Depends(get_db)):
    db_obrigacao = ObrigacaoAcessoria(**obrigacao.dict(), empresa_id=empresa_id)
    db.add(db_obrigacao)
    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao

@app.get("/obrigacoes/", response_model=list[ObrigacaoAcessoria])
def listar_obrigacoes(db: Session = Depends(get_db)):
    return db.query(ObrigacaoAcessoria).all()
