"""create_mv_cases_by_age_group.py

Revision ID: 16aa33840134
Revises: 669c1208d5c7
Create Date: 2026-01-13 14:05:37.376821

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16aa33840134'
down_revision: Union[str, Sequence[str], None] = '669c1208d5c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        CREATE MATERIALIZED VIEW mv_cases_by_age_group AS
        SELECT
            nu_ano,
            sg_uf_not,
            CASE
                WHEN cs_sexo IN ('M', 'F') THEN cs_sexo
                ELSE 'I'
            END AS sexo,
            FLOOR(idade / 10) * 10 AS faixa_inicio,
            COUNT(0) AS casos
        FROM dengue_cases
        WHERE idade IS NOT NULL
          AND idade >= 0
        GROUP BY
            nu_ano,
            sg_uf_not,
            sexo,
            faixa_inicio;
    """)

    op.create_index(
        "ix_mv_age_group_main",
        "mv_cases_by_age_group",
        ["nu_ano", "sg_uf_not", "sexo"]
    )

    op.create_index(
        "ix_mv_age_group_faixa",
        "mv_cases_by_age_group",
        ["faixa_inicio"]
    )


def downgrade():
    op.drop_index("ix_mv_age_group_faixa", table_name="mv_cases_by_age_group")
    op.drop_index("ix_mv_age_group_main", table_name="mv_cases_by_age_group")
    op.execute("DROP MATERIALIZED VIEW mv_cases_by_age_group")

