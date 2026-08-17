import json
import logging
from datetime import UTC, datetime


class ConsoleFormatter(logging.Formatter):
    def __init__(self) -> None:
        super().__init__(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z",
        )


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "timestamp": datetime.fromtimestamp(
                record.created,
                tz=UTC,
            ).isoformat(timespec="milliseconds"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if record.exc_info is not None:
            payload["exception"] = self.formatException(record.exc_info)

        for attribute in (
            "request_id",
            "method",
            "path",
            "environment",
        ):
            value = getattr(record, attribute, None)

            if value is not None:
                payload[attribute] = value

        return json.dumps(payload, ensure_ascii=False)