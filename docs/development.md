# Development workflow

## Prerequisites

- Git
- Python 3.11 or newer
- [uv](https://docs.astral.sh/uv/)
- Docker when changing container behavior

Install every dependency group and Git hook:

```bash
uv sync --all-groups
uv run pre-commit install
uv run pre-commit install --hook-type pre-push
```

## Quality gate

```bash
uv run python scripts/check.py
uv build
```

The script runs formatting/linting, strict typing, tests and coverage, metadata validation,
spelling, dependency hygiene, dead-code detection, documentation builds, vulnerability auditing,
and GitHub Actions security analysis. It stops at the first failure.

## Adding dependencies

Use `uv add <package>` for runtime packages. Add tools to the narrowest PEP 735 dependency group:

```bash
uv add --group dev <test-tool>
uv add --group quality <quality-tool>
uv add --group docs <documentation-tool>
```

Commit `pyproject.toml` and `uv.lock` together. Explain any new runtime dependency in the PR.

## Tests

Unit tests mirror the source package under `tests/`. Add regression coverage for bug fixes and
property-based tests for behavior with a large input space. Keep tests deterministic and avoid
network access unless an integration test explicitly owns that boundary.
