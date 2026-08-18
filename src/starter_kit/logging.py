"""Application logging setup."""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from starter_kit.context import get_context

if TYPE_CHECKING:
    from starter_kit.config import LogFormat

_STANDARD_RECORD_FIELDS = frozenset(logging.makeLogRecord({}).__dict__)


class ContextFilter(logging.Filter):
    """Attach context-local diagnostic fields to each log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Add fields without overwriting explicitly supplied record extras."""
        for key, value in get_context().items():
            record.__dict__.setdefault(key, value)
        return True


class JsonFormatter(logging.Formatter):
    """Format log records as single-line JSON for log aggregation systems."""

    def format(self, record: logging.LogRecord) -> str:
        """Serialize a log record and any custom context fields."""
        payload: dict[str, object] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC)
            .isoformat(timespec="milliseconds")
            .replace("+00:00", "Z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        context = {
            key: value
            for key, value in record.__dict__.items()
            if key not in _STANDARD_RECORD_FIELDS and not key.startswith("_")
        }
        if context:
            payload["context"] = context
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str, ensure_ascii=False, separators=(",", ":"))


def configure_logging(level: str = "INFO", log_format: LogFormat = "text") -> None:
    """Configure process-wide text or JSON logging."""
    formatter: logging.Formatter
    if log_format == "json":
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s %(name)s: %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z",
        )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.addFilter(ContextFilter())
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(level)
