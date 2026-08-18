"""Tests for application logging setup."""

from __future__ import annotations

import json
import logging

from starter_kit.context import log_context
from starter_kit.logging import ContextFilter, JsonFormatter, configure_logging


def test_configure_logging_sets_root_level() -> None:
    configure_logging("WARNING")

    assert logging.getLogger().level == logging.WARNING


def test_configure_json_logging_installs_json_formatter() -> None:
    configure_logging("INFO", "json")

    root_logger = logging.getLogger()
    assert len(root_logger.handlers) == 1
    assert isinstance(root_logger.handlers[0].formatter, JsonFormatter)


def test_json_formatter_includes_custom_context() -> None:
    record = logging.LogRecord(
        name="starter_kit.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="Ready %s",
        args=("now",),
        exc_info=None,
    )
    record.__dict__["environment"] = "test"

    payload = json.loads(JsonFormatter().format(record))

    assert payload["level"] == "INFO"
    assert payload["message"] == "Ready now"
    assert payload["context"] == {"environment": "test"}


def test_json_formatter_serializes_exceptions() -> None:
    try:
        raise RuntimeError("example")
    except RuntimeError:
        record = logging.LogRecord(
            name="starter_kit.test",
            level=logging.ERROR,
            pathname=__file__,
            lineno=1,
            msg="Failed",
            args=(),
            exc_info=__import__("sys").exc_info(),
        )

    payload = json.loads(JsonFormatter().format(record))
    assert "RuntimeError: example" in payload["exception"]


def test_context_filter_attaches_bound_values() -> None:
    configure_logging("INFO", "json")
    record = logging.LogRecord(
        name="starter_kit.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="Ready",
        args=(),
        exc_info=None,
    )

    context_filter = logging.getLogger().handlers[0].filters[0]
    assert isinstance(context_filter, ContextFilter)
    with log_context(request_id="req-789"):
        assert context_filter.filter(record)

    assert record.__dict__["request_id"] == "req-789"
