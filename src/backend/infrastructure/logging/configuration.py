import logging
import sys

from backend.config.settings import LogFormat, Settings
from backend.infrastructure.logging.formatters import (
    ConsoleFormatter,
    JsonFormatter,
)


_BACKEND_LOGGER_NAME = "backend"


def configure_logging(settings: Settings) -> None:
    formatter: logging.Formatter

    if settings.log_format is LogFormat.JSON:
        formatter = JsonFormatter()
    else:
        formatter = ConsoleFormatter()

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(settings.log_level.value)
    handler.setFormatter(formatter)

    backend_logger = logging.getLogger(_BACKEND_LOGGER_NAME)
    backend_logger.handlers.clear()
    backend_logger.addHandler(handler)
    backend_logger.setLevel(settings.log_level.value)
    backend_logger.propagate = False