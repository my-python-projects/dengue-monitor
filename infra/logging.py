import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from infra.config import Settings
from infra.formatter import SafeFormatter

CONSOLE_HANDLER_NAME = "dengue_monitor_console"
FILE_HANDLER_NAME = "dengue_monitor_file"


def _get_handler(
    logger: logging.Logger,
    name: str,
) -> logging.Handler | None:
    return next(
        (handler for handler in logger.handlers if handler.get_name() == name),
        None,
    )


def _configure_external_loggers() -> None:
    logging.getLogger("sqlalchemy.engine").setLevel(Settings.SQLALCHEMY_LOG_LEVEL)
    logging.getLogger("sqlalchemy.pool").setLevel(Settings.SQLALCHEMY_LOG_LEVEL)

    logging.getLogger("uvicorn").setLevel(Settings.UVICORN_LOG_LEVEL)
    logging.getLogger("uvicorn.error").setLevel(Settings.UVICORN_LOG_LEVEL)
    logging.getLogger("uvicorn.access").setLevel(Settings.UVICORN_LOG_LEVEL)


def setup_logging() -> None:
    formatter = SafeFormatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s | "
        "uf=%(uf)s ano=%(ano)s mes=%(mes)s | "
        "total_registros=%(total_registros)s"
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(Settings.LOG_LEVEL.upper())

    console_handler = _get_handler(
        root_logger,
        CONSOLE_HANDLER_NAME,
    )

    if Settings.LOG_TO_CONSOLE:
        if console_handler is None:
            console_handler = logging.StreamHandler()
            console_handler.set_name(CONSOLE_HANDLER_NAME)
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)

    elif console_handler is not None:
        root_logger.removeHandler(console_handler)
        console_handler.close()

    file_handler = _get_handler(
        root_logger,
        FILE_HANDLER_NAME,
    )

    if Settings.LOG_TO_FILE:
        log_dir = Path(Settings.LOG_DIR)
        log_dir.mkdir(parents=True, exist_ok=True)

        if file_handler is None:
            file_handler = RotatingFileHandler(
                log_dir / "app.log",
                maxBytes=5_000_000,
                backupCount=5,
                encoding="utf-8",
                errors="replace",
            )
            file_handler.set_name(FILE_HANDLER_NAME)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

    elif file_handler is not None:
        root_logger.removeHandler(file_handler)
        file_handler.close()

    _configure_external_loggers()
