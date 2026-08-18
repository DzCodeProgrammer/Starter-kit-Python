"""Environment-driven application configuration."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from typing import Final, Literal, TypeAlias, cast

Environment: TypeAlias = Literal["development", "test", "staging", "production"]

_ENVIRONMENTS: Final = {"development", "test", "staging", "production"}
_LOG_LEVELS: Final = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
_TRUE_VALUES: Final = {"1", "true", "yes", "on"}
_FALSE_VALUES: Final = {"0", "false", "no", "off"}
_DEFAULT_APP_NAME: Final = "starter-kit-python"
_DEFAULT_ENVIRONMENT: Final[Environment] = "development"
_DEFAULT_DEBUG: Final = False
_DEFAULT_LOG_LEVEL: Final = "INFO"


@dataclass(frozen=True, slots=True)
class Settings:
    """Validated settings used by the application."""

    app_name: str = _DEFAULT_APP_NAME
    environment: Environment = _DEFAULT_ENVIRONMENT
    debug: bool = _DEFAULT_DEBUG
    log_level: str = _DEFAULT_LOG_LEVEL

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> Settings:
        """Create settings from a mapping or the current process environment."""
        source = os.environ if environ is None else environ
        app_name = source.get("STARTER_KIT_APP_NAME", _DEFAULT_APP_NAME).strip()
        environment = source.get("STARTER_KIT_ENVIRONMENT", _DEFAULT_ENVIRONMENT).strip().lower()
        debug = _parse_bool(source.get("STARTER_KIT_DEBUG", str(_DEFAULT_DEBUG)))
        log_level = source.get("STARTER_KIT_LOG_LEVEL", _DEFAULT_LOG_LEVEL).strip().upper()

        if not app_name:
            raise ValueError("STARTER_KIT_APP_NAME must not be empty")
        if environment not in _ENVIRONMENTS:
            allowed = ", ".join(sorted(_ENVIRONMENTS))
            raise ValueError(f"STARTER_KIT_ENVIRONMENT must be one of: {allowed}")
        if log_level not in _LOG_LEVELS:
            allowed = ", ".join(sorted(_LOG_LEVELS))
            raise ValueError(f"STARTER_KIT_LOG_LEVEL must be one of: {allowed}")

        return cls(
            app_name=app_name,
            environment=cast(Environment, environment),
            debug=debug,
            log_level=log_level,
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
