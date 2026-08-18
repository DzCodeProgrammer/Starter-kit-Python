# Python Starter Kit

A small, production-friendly foundation for Python 3.11+ applications. It uses a
`src` package layout, has no runtime dependencies, and includes a tested command-line
entry point, typed environment configuration, structured logging, packaging, and CI.

## Included

- Modern packaging through `pyproject.toml` and `uv.lock`
- `src` layout with an installable `starter-kit` command
- Environment-driven, validated application settings
- Text or single-line JSON logging with contextual fields
- Context-local correlation metadata safe for threads and async tasks
- Machine-readable health/build diagnostics with pluggable checks and latency measurements
- Ruff formatting and linting, strict mypy checks, and pytest coverage
- Property-based tests, strict warnings, and 95% minimum branch coverage
- Dependency vulnerability/SBOM auditing, dead-code detection, spelling, and metadata validation
- Local pre-commit and pre-push hooks
- GitHub Actions across Python 3.11-3.14, Linux, Windows, and macOS
- Strict MkDocs Material documentation with generated API reference
- Non-root multi-stage Docker image with a CI smoke test
- Isolated wheel and source-distribution smoke tests plus verified release artifacts
- Dependabot updates for Python and GitHub Actions dependencies
- Immutable action pins, minimal token permissions, Zizmor workflow analysis, and CI concurrency
- Dev container, issue forms, PR template, CODEOWNERS, changelog, support, conduct, and security policies

## Quick start

Install [uv](https://docs.astral.sh/uv/), then run:

```bash
uv sync --all-groups
uv run starter-kit hello --name Developer
uv run starter-kit show-config
uv run starter-kit health --pretty
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
| `STARTER_KIT_LOG_FORMAT` | `text` | `text`, `json` |
| `STARTER_KIT_BUILD_COMMIT` | `unknown` | A non-empty build or Git identifier |

Copy `.env.example` to `.env` as a reference. This starter deliberately does not
auto-load `.env`; deployment platforms should provide environment variables directly,
while local tooling can use any dotenv loader.

## Development

Run the complete local quality gate:

```bash
uv run python scripts/check.py
uv build
```

The quality gate runs Ruff, format verification, strict mypy checks, pytest with branch
coverage, project metadata validation, spelling, dependency hygiene, dead-code detection,
strict documentation builds, a dependency vulnerability audit, and GitHub Actions security
analysis. Each command can also be run separately.

Install the optional Git hooks with:

```bash
uv run pre-commit install
uv run pre-commit install --hook-type pre-push
```

## Container

The multi-stage image installs only the built application wheel, runs as an unprivileged
user, and defaults to the health command:

```bash
docker build -t starter-kit-python .
docker run --rm starter-kit-python health --pretty
```

See [operations](docs/operations.md) for logging, build metadata, and deployment notes.

## Project structure

```text
.
|-- src/starter_kit/     # Installable application package
|-- tests/               # Unit and CLI behavior tests
|-- scripts/check.py     # Cross-platform local quality gate
|-- docs/                # Architecture and operations guidance
|-- .github/             # CI, ownership, and contribution templates
|-- .devcontainer/       # Reproducible editor development environment
|-- Dockerfile           # Non-root production image
|-- pyproject.toml       # Package and tool configuration
`-- uv.lock              # Reproducible dependency lock
```

## Use this as a template

1. Rename `src/starter_kit` and update the package/script names in `pyproject.toml`.
2. Replace the sample CLI commands with the application's entry points.
3. Add runtime dependencies with `uv add <package>`.
4. Replace this README with product-specific setup and operational notes.

See [architecture](docs/architecture.md), [open-source references](docs/references.md),
[CONTRIBUTING.md](CONTRIBUTING.md),
[SECURITY.md](SECURITY.md), and [CHANGELOG.md](CHANGELOG.md) for project conventions.
