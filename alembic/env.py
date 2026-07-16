from logging.config import fileConfig
from urllib.parse import quote_plus

from sqlalchemy import engine_from_config, pool

from alembic import context
from infra.config import Settings

# ======================================================
# Import the Base class from the application models
# ======================================================
from infra.database import Base  # noqa

# ======================================================
# Main Alembic configuration
# ======================================================
config = context.config

# ======================================================
# Logging
# ======================================================
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ======================================================
# Metadata autogenerate
# ======================================================
target_metadata = Base.metadata

# ======================================================
# Build DATABASE_URL from environment variables
# ======================================================
DB_USER = quote_plus(Settings.DB_USER)
DB_PASSWORD = quote_plus(Settings.DB_PASSWORD)

# Override alembic.ini configuration
config.set_main_option("sqlalchemy.url", Settings.DATABASE_URL)


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
# Select the execution mode
# ======================================================
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
