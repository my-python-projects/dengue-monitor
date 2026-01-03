from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# ======================================================
# Carrega variáveis de ambiente
# ======================================================
load_dotenv()

# ======================================================
# Importa Base dos models da aplicação
# ======================================================
from core.database import Base  # noqa

# ======================================================
# Configuração principal do Alembic
# ======================================================
config = context.config

# ======================================================
# Logging
# ======================================================
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ======================================================
# Metadata para autogenerate
# ======================================================
target_metadata = Base.metadata

# ======================================================
# Monta DATABASE_URL a partir do .env (BLINDADO)
# ======================================================
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DB_USER = quote_plus(os.getenv("DB_USER"))
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))

DATABASE_URL = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Sobrescreve alembic.ini
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# print("DATABASE_URL:", DATABASE_URL)


# ======================================================
# Migrations OFFLINE
# ======================================================
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ======================================================
# Migrations ONLINE
# ======================================================
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# ======================================================
# Seleção do modo de execução
# ======================================================
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
