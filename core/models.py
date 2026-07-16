from sqlalchemy import Column, Date, Integer, String

from infra.database import Base


class DengueCase(Base):
    __tablename__ = "dengue_cases"

    id = Column(Integer, primary_key=True)

    # =========================
    # Notification identification
    # =========================
    tp_not = Column(Integer, nullable=False)  # Notification type
    id_agravo = Column(String(5), nullable=False)  # CID-10
    dt_notific = Column(Date, nullable=False)  # Notification date
    sem_not = Column(Integer)
    nu_ano = Column(Integer, nullable=False)

    # =========================
    # Notification location
    # =========================
    sg_uf_not = Column(Integer, nullable=False)
    id_municip = Column(Integer, nullable=False)
    id_regiona = Column(Integer)
    id_unidade = Column(Integer)

    # =========================
    # Clinical data
    # =========================
    dt_sin_pri = Column(Date, nullable=False)
    sem_pri = Column(Integer)

    # =========================
    # Patient data
    # =========================
    ano_nasc = Column(Integer)
    idade = Column(Integer)
    idade_unidade = Column(String(10))  # hour, day, month, year

    cs_sexo = Column(String(1), nullable=False)
    cs_gestant = Column(Integer)
    cs_raca = Column(Integer)
    cs_escol_n = Column(Integer)

    # =========================
    # Residence
    # =========================
    sg_uf = Column(Integer)
    id_mn_resi = Column(Integer)
    id_rg_resi = Column(Integer)
    id_pais = Column(Integer)

    # =========================
    # Investigation
    # =========================
    dt_invest = Column(Date)
