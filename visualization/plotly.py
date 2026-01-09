import plotly.express as px
import pandas as pd

def plot_cases_by_age_group_plotly(df):
    return px.bar(
        df,
        x="faixa_etaria",
        y="casos",
        title="Casos por Faixa Etária",
        labels={"faixa_etaria": "Faixa Etária", "casos": "Número de Casos"}
    )

def plot_cases_by_gender_plotly(df):
    return px.pie(
        df,
        names="genero",
        values="casos",
        title="Distribuição por Gênero",
        hole=0.4 
    )

def plot_top_municipios_plotly(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="casos",
        y="municipio",
        orientation="h",
        title="Top municípios com mais casos",
        text="casos",
        labels={"municipio": "Município", "casos": "Número de Casos"}
    )

    fig.update_layout(
        yaxis=dict(categoryorder="total ascending"),
        height=400
    )

    return fig


def prepare_heatmap_df(df: pd.DataFrame) -> pd.DataFrame:
    # garante mês inteiro
    df["mes"] = df["mes"].astype(int)

    pivot = (
        df.pivot_table(
            index="faixa_etaria",
            columns="mes",
            values="casos",
            aggfunc="sum"
        )
        .fillna(0)
        .sort_index(axis=1)
    )

    return pivot



def plot_heatmap_month_age(df_pivot: pd.DataFrame):
    meses = df_pivot.columns.tolist()
    
    fig = px.imshow(
        df_pivot,
        aspect="auto",
        color_continuous_scale="Blues",
        labels=dict(
            x="Mês",
            y="Faixa etária",
            color="Casos"
        ),
        title="Distribuição mensal de casos por faixa etária"
    )

    fig.update_layout(
        height=450,
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis=dict(
            type="category",
            tickmode="array",
            tickvals=meses,
            ticktext=[str(m) for m in meses]
        )
    )

    return fig


