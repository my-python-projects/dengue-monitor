import streamlit as st
import pandas as pd
from sqlalchemy import text
from core.database import engine
from data.lookups.loader import load_municipios

@st.cache_data(ttl=300) # cache por 5 minutos
def cases_by_age_group_df(uf: int | None = None, ano: int | None = None, sexo: str | None = None ) -> pd.DataFrame:
    query = """
        SELECT
            FLOOR(idade / 10) * 10 AS faixa_inicio,
            COUNT(*) AS casos
        FROM dengue_cases
        WHERE idade IS NOT NULL AND idade >= 0
    """
    params = {}
    if uf is not None:
        query += " AND sg_uf_not = :uf"
        params["uf"] = uf
    if ano is not None:
        query += " AND nu_ano = :ano"
        params["ano"] = ano

    if sexo is not None: 
        params["sexo"] = sexo
        # Filtro por sexo
        match sexo:
            case "M":
                query += " AND cs_sexo = 'M'"
            case "F":
                query += " AND cs_sexo = 'F'"
            case "I":
                query += " AND (cs_sexo IS NULL OR cs_sexo NOT IN ('M', 'F'))"

    query += """
        GROUP BY faixa_inicio
        ORDER BY faixa_inicio
    """

    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn, params=params)

    df["faixa_etaria"] = df["faixa_inicio"].apply(
        lambda x: f"{int(x)}–{int(x)+9}" if x < 90 else "90+"
    )
    return df[["faixa_etaria", "casos"]]


def cases_by_gender_df(
    uf: int | None = None,
    ano: int | None = None,
    idade_min: int | None = None,
    idade_max: int | None = None,
) -> pd.DataFrame:

    query = """
        SELECT
            cs_sexo,
            COUNT(*) AS casos
        FROM dengue_cases
        WHERE cs_sexo IS NOT NULL
    """

    params = {}

    if uf is not None:
        query += " AND sg_uf_not = :uf"
        params["uf"] = uf

    if ano is not None:
        query += " AND nu_ano = :ano"
        params["ano"] = ano

    if idade_min is not None:
        query += " AND idade >= :idade_min"
        params["idade_min"] = idade_min

    if idade_max is not None:
        query += " AND idade <= :idade_max"
        params["idade_max"] = idade_max

    query += " GROUP BY cs_sexo"

    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn, params=params)

    df["genero"] = df["cs_sexo"].map({
        "M": "Masculino",
        "F": "Feminino"
    }).fillna("Outros")

    return df[["genero", "casos"]]


@st.cache_data(ttl=600)
def cases_top_municipios_df(uf: int, ano: int, limit: int = 10) -> pd.DataFrame:
    query = """
        SELECT
            id_municip AS codigo_municipio,
            COUNT(*) AS casos
        FROM dengue_cases
        WHERE sg_uf_not = :uf
          AND nu_ano = :ano
          AND id_municip IS NOT NULL
        GROUP BY id_municip
        ORDER BY casos DESC
        LIMIT :limit
    """

    with engine.connect() as conn:
        df = pd.read_sql(
            text(query),
            conn,
            params={"uf": uf, "ano": ano, "limit": limit}
        )

    municipios_lookup = load_municipios()

    df["codigo_municipio"] = df["codigo_municipio"].astype(str).str[:6]

    df["municipio"] = df["codigo_municipio"].map(
        lambda x: municipios_lookup.get(x, {}).get("nome", "Desconhecido")
    )

    return df[["municipio", "casos"]]


@st.cache_data(ttl=600)
def cases_heatmap_month_age_df(
    uf: int | None = None,
    ano: int | None = None
) -> pd.DataFrame:

    query = """
        SELECT
            EXTRACT(MONTH FROM dt_notific)::int AS mes,
            FLOOR(idade / 10) * 10 AS faixa_inicio,
            COUNT(*) AS casos
        FROM dengue_cases
        WHERE idade IS NOT NULL
          AND idade >= 0
          AND dt_notific IS NOT NULL
    """

    params = {}

    if uf is not None:
        query += " AND sg_uf_not = :uf"
        params["uf"] = uf

    if ano is not None:
        query += " AND nu_ano = :ano"
        params["ano"] = ano

    query += """
        GROUP BY mes, faixa_inicio
        ORDER BY mes, faixa_inicio
    """

    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn, params=params)

    df["faixa_etaria"] = df["faixa_inicio"].apply(
        lambda x: f"{int(x)}–{int(x)+9}" if x < 90 else "90+"
    )

    return df[["mes", "faixa_etaria", "casos"]]
