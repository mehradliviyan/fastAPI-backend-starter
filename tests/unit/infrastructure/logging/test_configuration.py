import logging

import pytest

from backend.config.settings import LogFormat, LogLevel, Settings
from backend.infrastructure.logging.configuration import configure_logging
from backend.infrastructure.logging.formatters import (
    ConsoleFormatter,
    JsonFormatter,
)


@pytest.mark.parametrize(
    ("log_format", "formatter_type"),
    [
        (LogFormat.CONSOLE, ConsoleFormatter),
        (LogFormat.JSON, JsonFormatter),
    ],
)
def test_configure_logging_selects_requested_formatter(
    log_format: LogFormat,
    formatter_type: type[logging.Formatter],
) -> None:
    backend_logger = logging.getLogger("backend")
    original_handlers = backend_logger.handlers.copy()
    original_level = backend_logger.level
    original_propagate = backend_logger.propagate

    try:
        settings = Settings(
            _env_file=None,
            log_level=LogLevel.INFO,
            log_format=log_format,
        )

        configure_logging(settings)

        assert backend_logger.level == logging.INFO
        assert backend_logger.propagate is False
        assert len(backend_logger.handlers) == 1
        assert isinstance(
            backend_logger.handlers[0].formatter,
            formatter_type,
        )
    finally:
        new_handlers = [
            handler
            for handler in backend_logger.handlers
            if handler not in original_handlers
        ]

        for handler in new_handlers:
            handler.close()

        backend_logger.handlers = original_handlers
        backend_logger.setLevel(original_level)
        backend_logger.propagate = original_propagate