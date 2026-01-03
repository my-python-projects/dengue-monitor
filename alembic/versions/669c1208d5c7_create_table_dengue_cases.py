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

        # Identificação
        sa.Column("tp_not", sa.Integer, nullable=False),
        sa.Column("id_agravo", sa.String(5), nullable=False),

        # Datas
        sa.Column("dt_notific", sa.Date, nullable=False),
        sa.Column("dt_sin_pri", sa.Date),
        sa.Column("dt_invest", sa.Date),

        # Semana / Ano epidemiológico
        sa.Column("sem_not", sa.Integer),
        sa.Column("sem_pri", sa.Integer),
        sa.Column("nu_ano", sa.Integer, nullable=False),

        # Local da notificação
        sa.Column("sg_uf_not", sa.Integer, nullable=False),
        sa.Column("id_municip", sa.Integer, nullable=False),
        sa.Column("id_regiona", sa.Integer),
        sa.Column("id_unidade", sa.Integer),

        # Dados pessoais
        sa.Column("ano_nasc", sa.Integer),
        sa.Column("idade", sa.Integer),
        sa.Column("idade_unidade", sa.String(10)),
        sa.Column("cs_sexo", sa.String(1)),
        sa.Column("cs_gestant", sa.Integer),
        sa.Column("cs_raca", sa.Integer),
        sa.Column("cs_escol_n", sa.Integer),

        # Residência
        sa.Column("sg_uf", sa.Integer),
        sa.Column("id_mn_resi", sa.Integer),
        sa.Column("id_rg_resi", sa.Integer),
        sa.Column("id_pais", sa.Integer),
    )

    op.create_index(
        "ix_dengue_cases_ano_uf",
        "dengue_cases",
        ["nu_ano", "sg_uf_not"]
    )



def downgrade():
    op.drop_index("ix_dengue_cases_ano_uf", table_name="dengue_cases")
    op.drop_table("dengue_cases")