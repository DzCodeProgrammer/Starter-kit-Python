# Contributing

## Local setup

1. Install [uv](https://docs.astral.sh/uv/).
2. Install the project and development tools:

   ```bash
   uv sync --all-groups
   ```

3. Enable the Git hooks:

   ```bash
   uv run pre-commit install
   uv run pre-commit install --hook-type pre-push
   ```

## Before opening a pull request

Run the same checks used by CI:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src tests
uv run pytest
uv build
```

Keep pull requests focused, add tests for behavioral changes, and update the
documentation when public behavior changes.
