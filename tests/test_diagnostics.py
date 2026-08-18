"""Tests for runtime health diagnostics."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from starter_kit.config import Settings
from starter_kit.diagnostics import CheckOutcome, collect_health


def test_collect_health_returns_application_metadata() -> None:
    timestamp = datetime(2026, 8, 18, 12, 0, tzinfo=UTC)
    settings = Settings(environment="production", build_commit="abc123")

    report = collect_health(settings, now=timestamp)

    assert report.status == "ok"
    assert report.environment == "production"
    assert report.build_commit == "abc123"
    assert report.timestamp == "2026-08-18T12:00:00Z"
    assert report.python_version
    assert "-" in report.platform
    assert report.as_dict()["app_name"] == "starter-kit-python"
    assert report.checks[0].name == "runtime"
    assert report.checks[0].status == "pass"


def test_collect_health_uses_current_time() -> None:
    assert collect_health(Settings()).timestamp.endswith("Z")


def test_collect_health_rejects_naive_timestamp() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        collect_health(Settings(), now=datetime(2026, 1, 1))  # noqa: DTZ001


def test_collect_health_aggregates_warning() -> None:
    report = collect_health(
        Settings(),
        checks=[lambda: CheckOutcome(name="cache", status="warn", detail="cold")],
        timer=iter([1.0, 1.025]).__next__,
    )

    assert report.status == "degraded"
    assert report.checks[0].duration_ms == 25.0


def test_collect_health_contains_failed_check_without_sensitive_detail() -> None:
    def broken_check() -> CheckOutcome:
        raise RuntimeError("secret connection string")

    report = collect_health(
        Settings(),
        checks=[broken_check],
        timer=iter([2.0, 2.125]).__next__,
    )

    assert report.status == "unhealthy"
    assert report.checks[0].detail == "Raised RuntimeError"
    assert "secret" not in report.checks[0].detail
