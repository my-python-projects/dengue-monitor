from alembic import op
import sqlalchemy as sa

revision = "xxxx"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "dengue_cases",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("ano", sa.Integer, nullable=False),
        sa.Column("mes", sa.Integer, nullable=False),
        sa.Column("estado", sa.String(length=2), nullable=False),
        sa.Column("municipio", sa.String(length=255)),
        sa.Column("casos", sa.Integer, nullable=False),
        sa.Column("obitos", sa.Integer),
    )

    op.create_index(
        "ix_dengue_cases_estado_ano",
        "dengue_cases",
        ["estado", "ano"]
    )


def downgrade():
    op.drop_index("ix_dengue_cases_estado_ano", table_name="dengue_cases")
    op.drop_table("dengue_cases")
