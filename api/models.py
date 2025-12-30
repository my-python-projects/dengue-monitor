from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    SmallInteger
)
from api.database import Base


class DengueCase(Base):
    __tablename__ = "dengue_cases"

    id = Column(Integer, primary_key=True)

    # =========================
    # Identificação da notificação
    # =========================
    tp_not = Column(String(1), nullable=False)          # Tipo de notificação
    id_agravo = Column(String(5), nullable=False)       # CID-10
    dt_notific = Column(Date, nullable=False)           # Data da notificação
    sem_not = Column(String(6))
    nu_ano = Column(String(4), nullable=False)

    # =========================
    # Local da notificação
    # =========================
    sg_uf_not = Column(String(2), nullable=False)
    id_municip = Column(String(6), nullable=False)
    id_regiona = Column(String(8))
    id_unidade = Column(String(7), nullable=False)

    # =========================
    # Dados clínicos
    # =========================
    dt_sin_pri = Column(Date, nullable=False)
    sem_pri = Column(String(6))

    # =========================
    # Dados do paciente
    # =========================
    ano_nasc = Column(String(4))
    idade = Column(SmallInteger)
    idade_unidade = Column(String(10))  # hora, dia, mes, ano

    cs_sexo = Column(String(1), nullable=False)
    cs_gestant = Column(String(1))
    cs_raca = Column(String(1))
    cs_escol_n = Column(String(2))

    # =========================
    # Residência
    # =========================
    sg_uf = Column(String(2))
    id_mn_resi = Column(String(6))
    id_rg_resi = Column(String(8))
    id_pais = Column(String(4))

    # =========================
    # Investigação
    # =========================
    dt_invest = Column(Date)
