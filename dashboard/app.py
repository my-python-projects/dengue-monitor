import sys
from pathlib import Path as FilePath

ROOT_DIR = FilePath(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from dashboard.utils import load_ufs_for_select

from data.analysis import (
    cases_by_age_group_df, 
    cases_by_gender_df, 
    cases_top_municipios_df
)

from visualization.plotly import (
    plot_cases_by_age_group_plotly, 
    plot_cases_by_gender_plotly, 
    plot_top_municipios_plotly
)

from data.analysis import cases_heatmap_month_age_df
from visualization.plotly import plot_heatmap_month_age, prepare_heatmap_df


st.title("Dengue Monitor")

def bordered_container():
    return st.container(border=True)


# Carrega UFs dinamicamente
uf_options = load_ufs_for_select()
uf_names, uf_ids = zip(*uf_options)  # separa nomes (exibição) e IDs (valor)

# Selectbox com opções dinâmicas
selected_index = st.selectbox("UF", range(len(uf_names)), format_func=lambda x: uf_names[x])
uf = uf_ids[selected_index]  # ← valor inteiro do ID da UF

ano = st.slider("Ano", 2024, 2025)

# Carregar dados
df_top_municipios = cases_top_municipios_df(uf=uf, ano=ano)

# Criar duas colunas
col1, col2 = st.columns(2)

# Gráfico 1: Faixa etária (na coluna 1)
with col1:
    with bordered_container():

        # Selectbox para filtrar por sexo
        sexo_opcoes = {
            "Todos": None,
            "Masculino": "M",
            "Feminino": "F",
            "Ignorado": "I"
        }
        sexo_selecionado = st.selectbox(
            "Filtrar por sexo",
            options=list(sexo_opcoes.keys()),
            key="faixa_etaria_sexo"
        )
        sexo_valor = sexo_opcoes[sexo_selecionado]

        df_age = cases_by_age_group_df(uf=uf, ano=ano, sexo=sexo_valor)


        fig_age = plot_cases_by_age_group_plotly(df_age)
        fig_age.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_age, use_container_width=True)

# Gráfico 2: Gênero (na coluna 2)
with col2:
    with bordered_container():
        # Definir as faixas etárias pré-agrupadas
        faixas_etarias = [
            "0–9", "10–19", "20–29", "30–39", "40–49",
            "50–59", "60–69", "70–79", "80–89", "90+"
        ]
        
        faixa_selecionada = st.selectbox(
            "Selecione a faixa etária",
            options=faixas_etarias,
            key="faixa_etaria_genero"
        )

        # Converter a faixa selecionada em idade_min e idade_max
        if faixa_selecionada == "90+":
            idade_min, idade_max = 90, 150  # valor alto o suficiente
        else:
            inicio = int(faixa_selecionada.split("–")[0])
            fim = int(faixa_selecionada.split("–")[1])
            idade_min, idade_max = inicio, fim

        df_gender_filtered = cases_by_gender_df(
            uf=uf,
            ano=ano,
            idade_min=idade_min,
            idade_max=idade_max
        )

        fig_gender = plot_cases_by_gender_plotly(df_gender_filtered)
        fig_gender.update_layout(
            margin=dict(l=20, r=20, t=40, b=5),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_gender, use_container_width=True)


col3, col4 = st.columns(2)

with col3:
    with bordered_container():
        fig_top = plot_top_municipios_plotly(df_top_municipios)
        st.plotly_chart(fig_top, use_container_width=True)

with col4:
    with bordered_container():
        df_heat = cases_heatmap_month_age_df(uf=uf, ano=ano)
        df_pivot = prepare_heatmap_df(df_heat)

        fig_heat = plot_heatmap_month_age(df_pivot)
        st.plotly_chart(fig_heat, use_container_width=True)

