"""Tests for environment-driven settings."""

from __future__ import annotations

import pytest

from starter_kit.config import Settings


def test_defaults() -> None:
    assert Settings.from_env({}) == Settings()


def test_process_environment_is_used(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("STARTER_KIT_ENVIRONMENT", "test")

    assert Settings.from_env().environment == "test"


def test_values_are_normalized() -> None:
    settings = Settings.from_env(
        {
            "STARTER_KIT_APP_NAME": "  API worker  ",
            "STARTER_KIT_ENVIRONMENT": " PRODUCTION ",
            "STARTER_KIT_DEBUG": "YeS",
            "STARTER_KIT_LOG_LEVEL": "warning",
        }
    )

    assert settings == Settings(
        app_name="API worker",
        environment="production",
        debug=True,
        log_level="WARNING",
    )


@pytest.mark.parametrize("value", ["0", "false", "NO", "off"])
def test_false_boolean_values(value: str) -> None:
    assert Settings.from_env({"STARTER_KIT_DEBUG": value}).debug is False


@pytest.mark.parametrize(
    ("variable", "value", "message"),
    [
        ("STARTER_KIT_APP_NAME", "  ", "APP_NAME"),
        ("STARTER_KIT_ENVIRONMENT", "local", "ENVIRONMENT"),
        ("STARTER_KIT_DEBUG", "sometimes", "DEBUG"),
        ("STARTER_KIT_LOG_LEVEL", "TRACE", "LOG_LEVEL"),
    ],
)
def test_invalid_values(variable: str, value: str, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        Settings.from_env({variable: value})


def test_as_dict_contains_public_settings() -> None:
    assert Settings().as_dict() == {
        "app_name": "starter-kit-python",
        "environment": "development",
        "debug": False,
        "log_level": "INFO",
    }
