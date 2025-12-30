import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError

# Importa conexão e model
from api.database import SessionLocal
from api.models import DengueCase

from data.enums import (
    SEXO_MAP,
    RACA_MAP,
    GESTANTE_MAP,
    TIPO_NOT_MAP
)

from data.transformers.age import parse_idade

load_dotenv()

BASE_URL = os.getenv("OPENDATASUS_BASE_URL")
PAGE_SIZE = int(os.getenv("API_PAGE_SIZE", 1000))

HEADERS = {
    "accept": "application/json"
}


def fetch_dengue_data(nu_ano: int, limit: int, offset: int) -> list[dict]:
    params = {
        "nu_ano": nu_ano,
        "limit": limit,
        "offset": offset
    }

    response = requests.get(
        BASE_URL,
        params=params,
        headers=HEADERS,
        timeout=30
    )

    # response.raise_for_status()
    data = response.json()

    return data.get("parametros", [])


def normalize_data(records: list[dict], df_ibge: pd.DataFrame | None = None) -> pd.DataFrame:
    """
    Normaliza os dados brutos da API do OpenDataSUS (dengue).
    Retorna DataFrame pronto para persistência e consumo.
    """

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)

    # ============================
    # Datas
    # ============================
    date_columns = [
        "dt_notific",
        "dt_sin_pri",
        "dt_invest"
    ]

    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(
                df[col],
                format="%Y-%m-%d",
                errors="coerce"
            ).dt.date

    # =========================
    # Idade composta
    # =========================
    if "nu_idade_n" in df.columns:
        df[["idade", "idade_unidade"]] = df["nu_idade_n"].apply(
            lambda x: pd.Series(parse_idade(x))
        )

    # =========================
    # Seleção final (espelho do model)
    # =========================
    final_columns = [
        "tp_not",
        "id_agravo",
        "dt_notific",
        "sem_not",
        "nu_ano",
        "sg_uf_not",
        "id_municip",
        "id_regiona",
        "id_unidade",
        "dt_sin_pri",
        "sem_pri",
        "ano_nasc",
        "idade",
        "idade_unidade",
        "cs_sexo",
        "cs_gestant",
        "cs_raca",
        "cs_escol_n",
        "sg_uf",
        "id_mn_resi",
        "id_rg_resi",
        "id_pais",
        "dt_invest",
    ]

    final_columns = [c for c in final_columns if c in df.columns]

    return df[final_columns]


def save_to_database(df: pd.DataFrame) -> int:
    """
    Insere os dados no PostgreSQL usando SQLAlchemy.
    """
    session = SessionLocal()
    inserted = 0

    try:
        for _, row in df.iterrows():
            case = DengueCase(**row.to_dict())
            session.add(case)
            inserted += 1

        session.commit()

    except IntegrityError:
        session.rollback()
        raise

    finally:
        session.close()

    return inserted


# ======================================================
# Pipeline principal
# ======================================================

def run_pipeline(nu_ano: int, limit: int, offset: int):
    print(f"Buscando dados de dengue | Ano={nu_ano}")

    records = fetch_dengue_data(nu_ano, limit, offset)
    print(f"Registros brutos obtidos: {len(records)}")

    if not records:
        print("Nenhum dado encontrado.")
        return

    df = normalize_data(records)
    print(f"Dados normalizados: {len(df)} registros")

    inserted = save_to_database(df)
    print(f"Registros inseridos no banco: {inserted}")


# ======================================================
# Execução direta
# ======================================================

if __name__ == "__main__":
    run_pipeline(2025, limit=20, offset=0)


