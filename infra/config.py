import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME", "Dengue Monitor")
    ENV = os.getenv("ENV", "develop")

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    DATABASE_URL = (
        f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR = os.getenv("LOG_DIR", "logs")

    LOG_TO_CONSOLE = os.getenv("LOG_TO_CONSOLE", "true").lower() == "true"
    LOG_TO_FILE = os.getenv("LOG_TO_FILE", "false").lower() == "true"
    # LOG_FORMAT = os.getenv("LOG_FORMAT", "TEXT")

    SQLALCHEMY_LOG_LEVEL = os.getenv(
        "SQLALCHEMY_LOG_LEVEL",
        "WARNING",
    ).upper()

    UVICORN_LOG_LEVEL = os.getenv(
        "UVICORN_LOG_LEVEL",
        "INFO",
    ).upper()
