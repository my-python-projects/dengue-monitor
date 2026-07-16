import sys
from pathlib import Path as FilePath

ROOT_DIR = FilePath(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import streamlit as st

from dashboard.utils import load_ufs_for_select
from data.analysis import (
    cases_by_age_group_df,
    cases_by_gender_df,
    cases_heatmap_month_age_df,
    cases_top_municipios_df,
)
from visualization.plotly import (
    plot_cases_by_age_group_plotly,
    plot_cases_by_gender_plotly,
    plot_heatmap_month_age,
    plot_top_municipios_plotly,
    prepare_heatmap_df,
)

st.title("Dengue Monitor")


def bordered_container():
    return st.container(border=True)


uf_options = load_ufs_for_select()

# Split names for display and IDs for values
uf_names, uf_ids = zip(*uf_options, strict=True)

# Selectbox with dynamic options
selected_index = st.selectbox(
    "UF", range(len(uf_names)), format_func=lambda x: uf_names[x]
)
uf = uf_ids[selected_index]  # Integer value of the state ID

ano = st.slider("Ano", 2024, 2025)

# Load data
df_top_municipios = cases_top_municipios_df(uf=uf, ano=ano)

col1, col2 = st.columns(2)

# Chart 1: Age group
with col1:
    with bordered_container():

        # Selectbox for gender filtering
        sexo_opcoes = {
            "Todos": None,
            "Masculino": "M",
            "Feminino": "F",
            "Ignorado": "I",
        }
        sexo_selecionado = st.selectbox(
            "Filtrar por sexo",
            options=list(sexo_opcoes.keys()),
            key="faixa_etaria_sexo",
        )
        sexo_valor = sexo_opcoes[sexo_selecionado]

        df_age = cases_by_age_group_df(uf=uf, ano=ano, sexo=sexo_valor)

        fig_age = plot_cases_by_age_group_plotly(df_age)
        fig_age.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_age, width="stretch")

# Chart 2: Gender
with col2:
    with bordered_container():
        # Define pre-grouped age ranges
        faixas_etarias = [
            "0–9",
            "10–19",
            "20–29",
            "30–39",
            "40–49",
            "50–59",
            "60–69",
            "70–79",
            "80–89",
            "90+",
        ]

        faixa_selecionada = st.selectbox(
            "Selecione a faixa etária",
            options=faixas_etarias,
            key="faixa_etaria_genero",
        )

        # Convert the selected age range into idade_min and idade_max
        if faixa_selecionada == "90+":
            idade_min, idade_max = 90, 150  # High enough upper bound
        else:
            inicio = int(faixa_selecionada.split("–")[0])
            fim = int(faixa_selecionada.split("–")[1])
            idade_min, idade_max = inicio, fim

        df_gender_filtered = cases_by_gender_df(
            uf=uf,
            ano=ano,
            idade_min=idade_min,
            idade_max=idade_max,
        )

        fig_gender = plot_cases_by_gender_plotly(df_gender_filtered)
        fig_gender.update_layout(
            margin=dict(l=20, r=20, t=40, b=5),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_gender, width="stretch")


col3, col4 = st.columns(2)

with col3:
    with bordered_container():
        fig_top = plot_top_municipios_plotly(df_top_municipios)
        st.plotly_chart(fig_top, width="stretch")

with col4:
    with bordered_container():
        df_heat = cases_heatmap_month_age_df(uf=uf, ano=ano)
        df_pivot = prepare_heatmap_df(df_heat)

        fig_heat = plot_heatmap_month_age(df_pivot)
        st.plotly_chart(fig_heat, width="stretch")
