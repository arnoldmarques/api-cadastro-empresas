from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    cnpj = Column(String, unique=True, index=True)
    obrigacoes = relationship("Obrigacao", back_populates="empresa")

class Obrigacao(Base):
    __tablename__ = "obrigacoes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String)
    prazo = Column(String)
    obrigatoria = Column(Boolean)
    empresa_id = Column(Integer, ForeignKey("empresas.id"))
    empresa = relationship("Empresa", back_populates="obrigacoes")