import pandas as pd
from sqlalchemy import text
from core.database import engine


def cases_by_month_df(uf: int, ano: int) -> pd.DataFrame:
    query = """
        SELECT
            EXTRACT(MONTH FROM dt_notific) AS mes,
            COUNT(0) AS casos
        FROM dengue_cases
        WHERE sg_uf_not = :uf
          AND nu_ano = :ano
          AND dt_notific IS NOT NULL
        GROUP BY mes
        ORDER BY mes
    """

    with engine.connect() as conn:
        df = pd.read_sql(
            text(query),
            conn,
            params={"uf": uf, "ano": ano}
        )

    df["mes"] = df["mes"].astype(int)
    df["casos"] = df["casos"].astype(int)

    return df
