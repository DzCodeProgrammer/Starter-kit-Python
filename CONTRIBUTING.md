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
uv run python scripts/check.py
uv build
```

Keep pull requests focused, add tests for behavioral changes, and update the
documentation and changelog when public behavior changes. Report suspected vulnerabilities
through the private process in [SECURITY.md](SECURITY.md), not in a public issue.
