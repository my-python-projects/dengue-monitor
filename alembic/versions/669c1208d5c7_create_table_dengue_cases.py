"""create_table_dengue_cases

Revision ID: 669c1208d5c7
Revises: 
Create Date: 2025-12-30 16:21:18.568807

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '669c1208d5c7'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "dengue_cases",
        sa.Column("id", sa.Integer, primary_key=True),

        # Identificação do registro
        sa.Column("tp_not", sa.String(5)),
        sa.Column("id_agravo", sa.String(10)),

        # Datas
        sa.Column("dt_notific", sa.Date),
        sa.Column("dt_sin_pri", sa.Date),
        sa.Column("dt_invest", sa.Date),

        # Semana / Ano
        sa.Column("sem_not", sa.String(6)),
        sa.Column("sem_pri", sa.String(6)),
        sa.Column("nu_ano", sa.String(4)),

        # Localização notificação
        sa.Column("sg_uf_not", sa.String(2)),
        sa.Column("id_municip", sa.String(10)),
        sa.Column("id_regiona", sa.String(10)),
        sa.Column("id_unidade", sa.String(15)),

        # Dados pessoais
        sa.Column("ano_nasc", sa.String(4)),
        sa.Column("idade", sa.Integer),
        sa.Column("idade_unidade", sa.String(10)),
        sa.Column("cs_sexo", sa.String(1)),
        sa.Column("cs_gestant", sa.String(2)),
        sa.Column("cs_raca", sa.String(2)),
        sa.Column("cs_escol_n", sa.String(2)),

        # Residência
        sa.Column("sg_uf", sa.String(2)),
        sa.Column("id_mn_resi", sa.String(10)),
        sa.Column("id_rg_resi", sa.String(10)),
        sa.Column("id_pais", sa.String(3))
    )

    op.create_index(
        "ix_dengue_cases_ano_uf",
        "dengue_cases",
        ["nu_ano", "sg_uf_not"]
    )


def downgrade():
    op.drop_index("ix_dengue_cases_ano_uf", table_name="dengue_cases")
    op.drop_table("dengue_cases")