from sqlalchemy import Column, Integer, String
from api.database import Base

class DengueCase(Base):
    __tablename__ = "dengue_cases"

    id = Column(Integer, primary_key=True, index=True)
    ano = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    estado = Column(String(2), nullable=False)
    municipio = Column(String)
    casos = Column(Integer, nullable=False)
    obitos = Column(Integer)
