"""Tests for application logging setup."""

from __future__ import annotations

import logging

from starter_kit.logging import configure_logging


def test_configure_logging_sets_root_level() -> None:
    configure_logging("WARNING")

    assert logging.getLogger().level == logging.WARNING
