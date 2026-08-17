import json
import logging

from backend.infrastructure.logging.formatters import (
    ConsoleFormatter,
    JsonFormatter,
)


def create_log_record() -> logging.LogRecord:
    return logging.LogRecord(
        name="backend.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="Application started",
        args=(),
        exc_info=None,
    )


def test_console_formatter_creates_readable_log() -> None:
    output = ConsoleFormatter().format(create_log_record())

    assert "INFO" in output
    assert "backend.test" in output
    assert "Application started" in output


def test_json_formatter_creates_structured_log() -> None:
    record = create_log_record()
    record.__dict__["request_id"] = "request-123"

    output = JsonFormatter().format(record)
    payload = json.loads(output)

    assert payload["level"] == "INFO"
    assert payload["logger"] == "backend.test"
    assert payload["message"] == "Application started"
    assert payload["request_id"] == "request-123"
    assert payload["timestamp"].endswith("+00:00")