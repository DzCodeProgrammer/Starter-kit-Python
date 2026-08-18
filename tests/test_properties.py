"""Property-based tests for configuration normalization."""

from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st

from starter_kit.config import Settings


@given(st.sampled_from(["1", "true", "yes", "on"]), st.booleans(), st.booleans())
def test_true_boolean_values_are_case_and_whitespace_insensitive(
    value: str, uppercase: bool, padded: bool
) -> None:
    candidate = value.upper() if uppercase else value
    candidate = f"  {candidate}  " if padded else candidate

    assert Settings.from_env({"STARTER_KIT_DEBUG": candidate}).debug is True


@given(st.sampled_from(["0", "false", "no", "off"]), st.booleans(), st.booleans())
def test_false_boolean_values_are_case_and_whitespace_insensitive(
    value: str, uppercase: bool, padded: bool
) -> None:
    candidate = value.upper() if uppercase else value
    candidate = f"  {candidate}  " if padded else candidate

    assert Settings.from_env({"STARTER_KIT_DEBUG": candidate}).debug is False
