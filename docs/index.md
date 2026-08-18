# Python Starter Kit

This repository provides a typed, packaged, tested, documented, and container-ready baseline for
Python 3.11+ applications. It is deliberately framework-neutral and has no third-party runtime
dependencies.

## Start here

```bash
uv sync --all-groups
uv run starter-kit hello --name Developer
uv run starter-kit health --pretty
uv run python scripts/check.py
```

Use the navigation to understand the architecture, local workflow, operational contracts, and
release process. The [README](https://github.com/DzCodeProgrammer/Starter-kit-Python#readme) remains
the concise onboarding path.

## Core guarantees

- configuration is validated before command execution
- structured logs can carry context-local correlation fields
- health output contains non-secret runtime/build data and pluggable check results
- wheels and source distributions are smoke-tested in isolated environments
- CI tests supported Python versions and major operating systems
- development, documentation, security, and packaging checks are reproducible from the lockfile
