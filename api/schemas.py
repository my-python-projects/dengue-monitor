from pydantic import BaseModel

class DengueCaseSchema(BaseModel):
    ano: int
    mes: int
    estado: str
    municipio: str | None
    casos: int
    obitos: int | None

    class Config:
        from_attributes = True
