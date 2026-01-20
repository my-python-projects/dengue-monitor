"""create_mv_cases_heatmap_month_age

Revision ID: 7a7e4cf08981
Revises: 3aff02595406
Create Date: 2026-01-13 14:27:28.743668

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a7e4cf08981'
down_revision: Union[str, Sequence[str], None] = '3aff02595406'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        CREATE MATERIALIZED VIEW mv_cases_heatmap_month_age AS
        SELECT
            nu_ano,
            sg_uf_not,
            EXTRACT(MONTH FROM dt_notific)::int AS mes,
            FLOOR(idade / 10) * 10 AS faixa_inicio,
            COUNT(0) AS casos
        FROM dengue_cases
        WHERE idade IS NOT NULL
        AND dt_notific IS NOT NULL
        GROUP BY nu_ano, sg_uf_not, mes, faixa_inicio;
    """)

    op.create_index(
        "ix_mv_heatmap_main",
        "mv_cases_heatmap_month_age",
        ["nu_ano", "sg_uf_not"]
    )

    op.create_index(
        "ix_mv_heatmap_mes_faixa",
        "mv_cases_heatmap_month_age",
        ["mes", "faixa_inicio"]
    )


def downgrade():
    op.drop_index("ix_mv_heatmap_main", table_name="mv_cases_heatmap_month_age")
    op.drop_index("ix_mv_heatmap_mes_faixa", table_name="mv_cases_heatmap_month_age")
    op.execute("DROP MATERIALIZED VIEW mv_cases_heatmap_month_age")
