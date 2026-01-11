"""create_materialized_view_dengue_by_age_gender

Revision ID: 078c9590e748
Revises: 669c1208d5c7
Create Date: 2026-01-10 21:14:24.856723

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '078c9590e748'
down_revision: Union[str, Sequence[str], None] = '669c1208d5c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        CREATE MATERIALIZED VIEW dengue_by_age_gender AS
        SELECT
            sg_uf_not,
            nu_ano,
            FLOOR(idade / 10) * 10 AS faixa_inicio,
            cs_sexo,
            COUNT(*) AS casos
        FROM dengue_cases
        WHERE idade IS NOT NULL
          AND idade >= 0
        GROUP BY sg_uf_not, nu_ano, faixa_inicio, cs_sexo;
    """)

    op.execute("""
        CREATE INDEX ix_mv_dengue_uf_ano
        ON dengue_by_age_gender (sg_uf_not, nu_ano);
    """)


def downgrade():
    op.execute("DROP MATERIALIZED VIEW IF EXISTS dengue_by_age_gender")