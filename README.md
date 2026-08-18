# Python Starter Kit

A small, production-friendly foundation for Python 3.11+ applications. It uses a
`src` package layout, has no runtime dependencies, and includes a tested command-line
entry point, typed environment configuration, structured logging, packaging, and CI.

## Included

- Modern packaging through `pyproject.toml` and `uv.lock`
- `src` layout with an installable `starter-kit` command
- Environment-driven, validated application settings
- Ruff formatting and linting, strict mypy checks, and pytest coverage
- Local pre-commit and pre-push hooks
- GitHub Actions across Python 3.11-3.14
- Dependabot updates for Python and GitHub Actions dependencies

## Quick start

Install [uv](https://docs.astral.sh/uv/), then run:

```bash
uv sync --all-groups
uv run starter-kit hello --name Developer
uv run starter-kit show-config
```

The package can also be executed as a module:

```bash
uv run python -m starter_kit hello
```

## Configuration

Application settings use the `STARTER_KIT_` prefix:

| Variable | Default | Allowed values |
| --- | --- | --- |
| `STARTER_KIT_APP_NAME` | `starter-kit-python` | Any non-empty string |
| `STARTER_KIT_ENVIRONMENT` | `development` | `development`, `test`, `staging`, `production` |
| `STARTER_KIT_DEBUG` | `false` | `true/false`, `1/0`, `yes/no`, `on/off` |
| `STARTER_KIT_LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |

Copy `.env.example` to `.env` as a reference. This starter deliberately does not
auto-load `.env`; deployment platforms should provide environment variables directly,
while local tooling can use any dotenv loader.

## Development

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src tests
uv run pytest
uv build
```

Install the optional Git hooks with:

```bash
uv run pre-commit install
uv run pre-commit install --hook-type pre-push
```

## Use this as a template

1. Rename `src/starter_kit` and update the package/script names in `pyproject.toml`.
2. Replace the sample CLI commands with the application's entry points.
3. Add runtime dependencies with `uv add <package>`.
4. Replace this README with product-specific setup and operational notes.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution workflow.
