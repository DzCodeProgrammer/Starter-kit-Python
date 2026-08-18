"""Tests for the command-line interface."""

from __future__ import annotations

import json
from datetime import UTC, datetime

import pytest

from starter_kit.cli import build_parser, entrypoint, main
from starter_kit.config import Settings
from starter_kit.diagnostics import HealthReport


def test_hello_uses_provided_name(capsys: pytest.CaptureFixture[str]) -> None:
    result = main(["hello", "--name", "Team"], settings=Settings())

    assert result == 0
    assert capsys.readouterr().out == "Hello, Team!\n"


def test_hello_defaults_to_world(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["hello"], settings=Settings()) == 0
    assert capsys.readouterr().out == "Hello, World!\n"


def test_show_config_returns_json(capsys: pytest.CaptureFixture[str]) -> None:
    settings = Settings(app_name="example", environment="test", debug=True, log_level="DEBUG")

    assert main(["show-config"], settings=settings) == 0

    assert json.loads(capsys.readouterr().out) == {
        "app_name": "example",
        "build_commit": "unknown",
        "debug": True,
        "environment": "test",
        "log_level": "DEBUG",
        "log_format": "text",
    }


def test_parser_reports_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit, match="0"):
        build_parser().parse_args(["--version"])

    assert capsys.readouterr().out == "starter-kit 0.1.0\n"


def test_parser_requires_a_command() -> None:
    with pytest.raises(SystemExit, match="2"):
        build_parser().parse_args([])


def test_entrypoint_exits_with_main_result(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr("sys.argv", ["starter-kit", "hello"])

    with pytest.raises(SystemExit, match="0"):
        entrypoint()

    assert capsys.readouterr().out == "Hello, World!\n"


def test_health_returns_runtime_metadata(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        "starter_kit.cli.collect_health",
        lambda settings: HealthReport(
            status="ok",
            app_name=settings.app_name,
            version="0.1.0",
            environment=settings.environment,
            build_commit=settings.build_commit,
            python_version="3.11.0",
            platform="test-machine",
            timestamp=datetime(2026, 1, 1, tzinfo=UTC).isoformat(),
            checks=(),
        ),
    )

    assert main(["health", "--pretty"], settings=Settings()) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "ok"
    assert report["app_name"] == "starter-kit-python"
    assert report["platform"] == "test-machine"


def test_entrypoint_reports_invalid_configuration(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("STARTER_KIT_LOG_FORMAT", "invalid")
    monkeypatch.setattr("sys.argv", ["starter-kit", "health"])

    with pytest.raises(SystemExit, match="2"):
        entrypoint()

    assert "Configuration error: STARTER_KIT_LOG_FORMAT" in capsys.readouterr().err
