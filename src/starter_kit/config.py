"""Environment-driven application configuration."""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, Final, Literal, TypeAlias, cast

if TYPE_CHECKING:
    from collections.abc import Mapping

Environment: TypeAlias = Literal["development", "test", "staging", "production"]
LogFormat: TypeAlias = Literal["text", "json"]

_ENVIRONMENTS: Final = {"development", "test", "staging", "production"}
_LOG_LEVELS: Final = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
_LOG_FORMATS: Final = {"text", "json"}
_TRUE_VALUES: Final = {"1", "true", "yes", "on"}
_FALSE_VALUES: Final = {"0", "false", "no", "off"}
_DEFAULT_APP_NAME: Final = "starter-kit-python"
_DEFAULT_ENVIRONMENT: Final[Environment] = "development"
_DEFAULT_DEBUG: Final = False
_DEFAULT_LOG_LEVEL: Final = "INFO"
_DEFAULT_LOG_FORMAT: Final[LogFormat] = "text"
_DEFAULT_BUILD_COMMIT: Final = "unknown"


@dataclass(frozen=True, slots=True)
class Settings:
    """Validated settings used by the application."""

    app_name: str = _DEFAULT_APP_NAME
    environment: Environment = _DEFAULT_ENVIRONMENT
    debug: bool = _DEFAULT_DEBUG
    log_level: str = _DEFAULT_LOG_LEVEL
    log_format: LogFormat = _DEFAULT_LOG_FORMAT
    build_commit: str = _DEFAULT_BUILD_COMMIT

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> Settings:
        """Create settings from a mapping or the current process environment."""
        source = os.environ if environ is None else environ
        app_name = source.get("STARTER_KIT_APP_NAME", _DEFAULT_APP_NAME).strip()
        environment = source.get("STARTER_KIT_ENVIRONMENT", _DEFAULT_ENVIRONMENT).strip().lower()
        debug = _parse_bool(source.get("STARTER_KIT_DEBUG", str(_DEFAULT_DEBUG)))
        log_level = source.get("STARTER_KIT_LOG_LEVEL", _DEFAULT_LOG_LEVEL).strip().upper()
        log_format = source.get("STARTER_KIT_LOG_FORMAT", _DEFAULT_LOG_FORMAT).strip().lower()
        build_commit = source.get("STARTER_KIT_BUILD_COMMIT", _DEFAULT_BUILD_COMMIT).strip()

        if not app_name:
            raise ValueError("STARTER_KIT_APP_NAME must not be empty")
        if environment not in _ENVIRONMENTS:
            allowed = ", ".join(sorted(_ENVIRONMENTS))
            raise ValueError(f"STARTER_KIT_ENVIRONMENT must be one of: {allowed}")
        if log_level not in _LOG_LEVELS:
            allowed = ", ".join(sorted(_LOG_LEVELS))
            raise ValueError(f"STARTER_KIT_LOG_LEVEL must be one of: {allowed}")
        if log_format not in _LOG_FORMATS:
            allowed = ", ".join(sorted(_LOG_FORMATS))
            raise ValueError(f"STARTER_KIT_LOG_FORMAT must be one of: {allowed}")
        if not build_commit:
            raise ValueError("STARTER_KIT_BUILD_COMMIT must not be empty")

        return cls(
            app_name=app_name,
            environment=cast("Environment", environment),
            debug=debug,
            log_level=log_level,
            log_format=cast("LogFormat", log_format),
            build_commit=build_commit,
        )

    def as_dict(self) -> dict[str, str | bool]:
        """Return settings that are safe to print in diagnostics."""
        return asdict(self)


def _parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in _TRUE_VALUES:
        return True
    if normalized in _FALSE_VALUES:
        return False
    raise ValueError("STARTER_KIT_DEBUG must be a boolean (true/false, 1/0, yes/no, on/off)")
