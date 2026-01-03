import os
from collections import defaultdict
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError

# Importações locais
from core.database import SessionLocal
from core.models import DengueCase
from data.transformers.age import parse_idade

load_dotenv()

'''

# Quando utilizava a API 

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

'''

def load_csv_in_chunks(path: str, chunksize: int = 50_000):
    return pd.read_csv(path, chunksize=chunksize, low_memory=False)


def normalize_data(records: list[dict]) -> pd.DataFrame:

    """
    Normaliza os dados brutos da API do OpenDataSUS (dengue).
    Retorna DataFrame pronto para persistência e consumo.
    """

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)

    # Conversão de datas
    date_columns = ["dt_notific", "dt_sin_pri", "dt_invest"]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce").dt.date

    # Idade composta
    if "nu_idade_n" in df.columns:
        df[["idade", "idade_unidade"]] = df["nu_idade_n"].apply(
            lambda x: pd.Series(parse_idade(x))
        )

    # Conversão segura para Int64
    integer_columns = [
        "tp_not", "sem_not", "sem_pri", "nu_ano", "sg_uf_not",
        "id_municip", "id_regiona", "ano_nasc", "idade",
        "cs_gestant", "cs_raca", "cs_escol_n", "sg_uf",
        "id_mn_resi", "id_rg_resi", "id_pais"
    ]
    for col in integer_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    # Seleção final
    final_columns = [
        "tp_not", "id_agravo", "dt_notific", "sem_not", "nu_ano",
        "sg_uf_not", "id_municip", "id_regiona", "id_unidade",
        "dt_sin_pri", "sem_pri", "ano_nasc", "idade", "idade_unidade",
        "cs_sexo", "cs_gestant", "cs_raca", "cs_escol_n",
        "sg_uf", "id_mn_resi", "id_rg_resi", "id_pais", "dt_invest"
    ]
    
    final_columns = [c for c in final_columns if c in df.columns]
    
    return df[final_columns]


def save_to_database(df: pd.DataFrame) -> int:
    if df.empty:
        return 0

    session = SessionLocal()
    try:
        # Converter para lista de dicionários
        records = df.to_dict(orient="records")
        # Criar objetos DengueCase
        cases = [DengueCase(**r) for r in records]
        # Adicionar tudo de uma vez
        session.add_all(cases)
        session.commit()
        return len(cases)
    except IntegrityError:
        session.rollback()
        raise
    finally:
        session.close()


def run_pipeline(csv_path: str, max_per_group: int = 100):
    """
    Lê o CSV uma única vez, mantendo no máximo `max_per_group` registros
    por (sg_uf_not, nu_ano, mes).
    """
    
    # Buffer por grupo: (uf, ano, mes) → lista de registros (máx. 100)
    sampled_groups = defaultdict(list)
    total_read = 0

    print("Lendo CSV e aplicando amostragem estratificada...")
    for chunk in load_csv_in_chunks(csv_path):
        chunk.columns = chunk.columns.str.lower()
        chunk = chunk.dropna(subset=["dt_notific", "sg_uf_not", "nu_ano"])

        # Extrair mês
        chunk["mes"] = pd.to_datetime(chunk["dt_notific"], errors="coerce").dt.month
        chunk = chunk.dropna(subset=["mes"])

        # Converter tipos críticos
        chunk["sg_uf_not"] = pd.to_numeric(chunk["sg_uf_not"], errors="coerce").astype("Int64")
        chunk["nu_ano"] = pd.to_numeric(chunk["nu_ano"], errors="coerce").astype("Int64")
        chunk["mes"] = chunk["mes"].astype("Int64")

        # Iterar sobre registros como dicionários (mais rápido que iterrows)
        for record in chunk.to_dict(orient="records"):
            try:
                uf = int(record["sg_uf_not"])
                ano = int(record["nu_ano"])
                mes = int(record["mes"])
                key = (uf, ano, mes)
            except (TypeError, ValueError):
                continue

            if len(sampled_groups[key]) < max_per_group:
                sampled_groups[key].append(record)

        total_read += len(chunk)
        print(f"  Registros lidos: {total_read} | Grupos ativos: {len(sampled_groups)}")

    # Concatenar todos os registros selecionados
    all_selected = [rec for group in sampled_groups.values() for rec in group]
    print(f"\nTotal de registros após amostragem: {len(all_selected)}")

    # Normalizar e salvar
    df_final = normalize_data(all_selected)
    if df_final.empty:
        print("Nenhum registro válido para salvar.")
        return

    inserted = save_to_database(df_final)
    print(f"TOTAL inserido no banco: {inserted}")


if __name__ == "__main__":
    run_pipeline("data/raw/DENGBR25.csv")