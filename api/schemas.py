from pydantic import BaseModel

class MunicipioOut(BaseModel):
    codigo: str
    nome: str


class DengueCaseOut(BaseModel):
    ano: int
    uf: str
    uf_nome: str
    municipio: MunicipioOut
    casos: int
