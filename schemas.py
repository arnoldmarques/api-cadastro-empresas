from pydantic import BaseModel

class ObrigacaoCreate(BaseModel):
    nome: str
    descricao: str
    prazo: str
    obrigatoria: bool

class Obrigacao(BaseModel):
    id: int
    nome: str
    descricao: str
    prazo: str
    obrigatoria: bool
    empresa_id: int

    class Config:
        orm_mode = True

class EmpresaCreate(BaseModel):
    nome: str
    cnpj: str

class Empresa(BaseModel):
    id: int
    nome: str
    cnpj: str
    obrigacoes: list[Obrigacao] = []

    class Config:
        orm_mode = True