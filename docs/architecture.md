# Architecture

The starter intentionally keeps runtime concerns small and explicit. Product repositories can
replace individual modules without adopting a framework or dependency injection container.

## Package boundaries

- `config.py` reads and validates process-level configuration.
- `context.py` propagates correlation metadata through context-local state.
- `logging.py` owns process-wide text and JSON log formatting.
- `diagnostics.py` aggregates non-secret build/runtime metadata and pluggable health checks.
- `cli.py` performs input/output orchestration and delegates reusable behavior.

The `src` layout prevents tests from accidentally importing an uninstalled package from the
repository root. Public functions are typed, and `py.typed` tells downstream type checkers that
the package ships type information.

## Dependency policy

The base application has no third-party runtime dependencies. Development tools are isolated in
the `dev` dependency group and locked by `uv.lock`. Add a runtime package only when it provides
clear product value that would be costly or risky to maintain locally.

## Extension points

For a service, add transport-specific adapters such as HTTP or queue consumers beside the CLI.
Keep domain behavior independent from those adapters. For a library, remove the sample CLI and
expose a deliberately small public API from `__init__.py`.

## Health-check contract

Health checks return a named `CheckOutcome` with `pass`, `warn`, or `fail` status. The collector
measures each check, converts unexpected exceptions into sanitized failures, and derives the
overall state as `ok`, `degraded`, or `unhealthy`. Exception messages are deliberately excluded
from output to reduce the risk of leaking credentials or connection details.

## Context propagation

Logging context uses `contextvars`, so correlation fields remain isolated between threads and
async tasks. The context manager always restores prior state, including when an operation raises.
Explicit log-record extras win over context defaults.
