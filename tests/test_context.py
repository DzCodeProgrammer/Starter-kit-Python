"""Tests for context-local logging metadata."""

from __future__ import annotations

from starter_kit.context import bind_context, get_context, log_context, reset_context


def test_bind_and_reset_context() -> None:
    token = bind_context(request_id="req-123")
    try:
        assert get_context() == {"request_id": "req-123"}
    finally:
        reset_context(token)

    assert get_context() == {}


def test_context_manager_merges_and_restores_nested_values() -> None:
    with log_context(environment="test"):
        with log_context(request_id="req-456"):
            assert get_context() == {"environment": "test", "request_id": "req-456"}
        assert get_context() == {"environment": "test"}

    assert get_context() == {}


def test_get_context_returns_a_copy() -> None:
    token = bind_context(component="worker")
    try:
        copy = get_context()
        copy["component"] = "changed"
        assert get_context()["component"] == "worker"
    finally:
        reset_context(token)
