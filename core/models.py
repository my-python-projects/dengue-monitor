from sqlalchemy import (
    Column,
    Integer,
    String,
    Date
)
from core.database import Base


class DengueCase(Base):
    __tablename__ = "dengue_cases"

    id = Column(Integer, primary_key=True)

    # =========================
    # Identificação da notificação
    # =========================
    tp_not = Column(Integer, nullable=False)          # Tipo de notificação
    id_agravo = Column(String(5), nullable=False)       # CID-10
    dt_notific = Column(Date, nullable=False)           # Data da notificação
    sem_not = Column(Integer)
    nu_ano = Column(Integer, nullable=False)

    # =========================
    # Local da notificação
    # =========================
    sg_uf_not = Column(Integer, nullable=False)
    id_municip = Column(Integer, nullable=False)
    id_regiona = Column(Integer)
    id_unidade = Column(Integer)

    # =========================
    # Dados clínicos
    # =========================
    dt_sin_pri = Column(Date, nullable=False)
    sem_pri = Column(Integer)

    # =========================
    # Dados do paciente
    # =========================
    ano_nasc = Column(Integer)
    idade = Column(Integer)
    idade_unidade = Column(String(10))  # hora, dia, mes, ano

    cs_sexo = Column(String(1), nullable=False)
    cs_gestant = Column(Integer)
    cs_raca = Column(Integer)
    cs_escol_n = Column(Integer)

    # =========================
    # Residência
    # =========================
    sg_uf = Column(Integer)
    id_mn_resi = Column(Integer)
    id_rg_resi = Column(Integer)
    id_pais = Column(Integer)

    # =========================
    # Investigação
    # =========================
    dt_invest = Column(Date)
