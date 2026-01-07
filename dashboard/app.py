import sys
from pathlib import Path as FilePath

ROOT_DIR = FilePath(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))



import streamlit as st
from data.analysis import cases_by_month_df
from visualization.plotly import plot_cases_by_month_plotly


st.title("Dengue Monitor")

uf = st.selectbox("UF", [31, 33, 35])
ano = st.slider("Ano", 2015, 2025)

df = cases_by_month_df(uf, ano)
fig = plot_cases_by_month_plotly(df)

st.plotly_chart(fig, use_container_width=True)
