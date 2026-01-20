import streamlit as st
import pandas as pd
from sqlalchemy import text
from core.database import engine
from data.lookups.loader import load_municipios

@st.cache_data(ttl=600)
def cases_by_age_group_df(
    uf: int | None = None,
    ano: int | None = None,
    sexo: str | None = None
) -> pd.DataFrame:

    query = """
        SELECT
            faixa_inicio,
            casos
        FROM mv_cases_by_age_group
        WHERE 1=1
    """
    params = {}

    if uf is not None:
        query += " AND sg_uf_not = :uf"
        params["uf"] = uf

    if ano is not None:
        query += " AND nu_ano = :ano"
        params["ano"] = ano

    if sexo is not None:
        query += " AND sexo = :sexo"
        params["sexo"] = sexo

    query += " ORDER BY faixa_inicio"

    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn, params=params)

    df["faixa_etaria"] = df["faixa_inicio"].apply(
        lambda x: f"{int(x)}–{int(x)+9}" if x < 90 else "90+"
    )

    return df[["faixa_etaria", "casos"]]


@st.cache_data(ttl=600)
def cases_by_gender_df(
    uf: int | None = None,
    ano: int | None = None,
    idade_min: int | None = None,
    idade_max: int | None = None,
) -> pd.DataFrame:

    faixas_filtradas = None
    if idade_min is not None or idade_max is not None:
        idade_min = idade_min or 0
        idade_max = idade_max or 150

        faixas_possiveis = list(range(0, 100, 10))  # [0, 10, 20, ..., 90]
        faixas_filtradas = []
        for faixa in faixas_possiveis:
            faixa_fim = faixa + 9
            if not (faixa_fim < idade_min or faixa > idade_max):
                faixas_filtradas.append(faixa)
        if idade_max >= 90:
            faixas_filtradas.append(90)
        faixas_filtradas = sorted(set(faixas_filtradas))

    query = """
        SELECT
            sexo AS cs_sexo,
            SUM(casos) AS casos
        FROM mv_cases_by_gender_age_group
        WHERE 1=1
    """
    params = {}

    if uf is not None:
        query += " AND sg_uf_not = :uf"
        params["uf"] = uf

    if ano is not None:
        query += " AND nu_ano = :ano"
        params["ano"] = ano

    if faixas_filtradas is not None:
        query += " AND faixa_inicio = ANY(:faixas)"
        params["faixas"] = faixas_filtradas

    query += " GROUP BY sexo"

    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn, params=params)

    df["genero"] = df["cs_sexo"].map({
        "M": "Masculino",
        "F": "Feminino",
        "I": "Ignorado"
    }).fillna("Outros")

    return df[["genero", "casos"]]

@st.cache_data(ttl=600)
def cases_top_municipios_df(uf: int, ano: int, limit: int = 10) -> pd.DataFrame:
    query = """
        SELECT
            id_municip AS codigo_municipio,
            casos
        FROM mv_top_municipios
        WHERE sg_uf_not = :uf
          AND nu_ano = :ano
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
            mes,
            faixa_inicio,
            casos
        FROM mv_cases_heatmap_month_age
        WHERE 1=1
    """
    params = {}

    if uf is not None:
        query += " AND sg_uf_not = :uf"
        params["uf"] = uf

    if ano is not None:
        query += " AND nu_ano = :ano"
        params["ano"] = ano

    query += " ORDER BY mes, faixa_inicio"

    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn, params=params)

    df["faixa_etaria"] = df["faixa_inicio"].apply(
        lambda x: f"{int(x)}–{int(x)+9}" if x < 90 else "90+"
    )

    return df[["mes", "faixa_etaria", "casos"]]
