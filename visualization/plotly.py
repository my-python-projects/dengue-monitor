import plotly.express as px

def plot_cases_by_month_plotly(df):
    return px.line(
        df,
        x="mes",
        y="casos",
        markers=True,
        title="Casos de Dengue por Mês"
    )
