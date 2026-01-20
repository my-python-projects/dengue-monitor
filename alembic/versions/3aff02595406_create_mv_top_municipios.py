"""create_mv_top_municipios

Revision ID: 3aff02595406
Revises: 20c8b9951934
Create Date: 2026-01-13 14:22:22.830556

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3aff02595406'
down_revision: Union[str, Sequence[str], None] = '20c8b9951934'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        CREATE MATERIALIZED VIEW mv_top_municipios AS
        SELECT
            nu_ano,
            sg_uf_not,
            id_municip,
            COUNT(0) AS casos
        FROM dengue_cases
        WHERE id_municip IS NOT NULL
        GROUP BY nu_ano, sg_uf_not, id_municip;
    """)

    op.create_index(
        "ix_mv_top_mun_uf_ano",
        "mv_top_municipios",
        ["nu_ano", "sg_uf_not"]
    )


def downgrade():
    op.drop_index("ix_mv_top_mun_uf_ano", table_name="mv_top_municipios")
    op.execute("DROP MATERIALIZED VIEW mv_top_municipios")