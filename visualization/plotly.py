import plotly.express as px

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


def plot_top_municipios_plotly(df):
    return px.bar(
        df,
        x="casos",
        y="codigo_municipio",
        orientation="h",
        title="Top Municípios por Casos",
        labels={"codigo_municipio": "Código do Município", "casos": "Casos"}
    )