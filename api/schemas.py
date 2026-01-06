from pydantic import BaseModel

class UFOut(BaseModel):
    id: int
    sigla: str
    nome: str

class MunicipioOut(BaseModel):
    codigo: int
    nome: str

class DengueCaseOut(BaseModel):
    ano: int
    uf: UFOut
    municipio: MunicipioOut
    casos: int

class MonthlyCasesOut(BaseModel):
    mes: int
    casos: int

    class Config:
        from_attributes = True

class AgeGroupCasesOut(BaseModel):
    faixa_etaria: str
    casos: int

    class Config:
        from_attributes = True
