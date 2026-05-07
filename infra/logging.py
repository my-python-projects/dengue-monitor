import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from infra.config import Settings
from infra.formatter import SafeFormatter

LOG_DIR = Path(Settings.LOG_DIR)
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

def setup_logging():

    formatter = SafeFormatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s | uf=%(uf)s ano=%(ano)s mes=%(mes)s | total_registros=%(total_registros)s"
    )

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5_000_000,
        backupCount=5,
        encoding="utf-8",
        errors="replace"
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(Settings.LOG_LEVEL)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
