"""Context-local metadata for correlated logs and diagnostics."""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator
    from contextvars import Token

_LOG_CONTEXT: ContextVar[dict[str, str] | None] = ContextVar(
    "starter_kit_log_context", default=None
)


def get_context() -> dict[str, str]:
    """Return a copy of the current context so callers cannot mutate shared state."""
    current = _LOG_CONTEXT.get()
    return current.copy() if current is not None else {}


def bind_context(**values: str) -> Token[dict[str, str] | None]:
    """Merge values into the current context and return a reset token."""
    current = get_context()
    current.update(values)
    return _LOG_CONTEXT.set(current)


def reset_context(token: Token[dict[str, str] | None]) -> None:
    """Restore the context associated with a previous bind operation."""
    _LOG_CONTEXT.reset(token)


@contextmanager
def log_context(**values: str) -> Iterator[None]:
    """Temporarily bind logging context and restore it on exit."""
    token = bind_context(**values)
    try:
        yield
    finally:
        reset_context(token)
