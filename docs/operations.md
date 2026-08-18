# Operations

## Health metadata

Run `starter-kit health` to emit a machine-readable snapshot containing application version,
environment, build commit, Python version, platform, and UTC timestamp. It does not include
secrets or the full process environment. Each health check reports status and elapsed time;
unexpected errors are reduced to their exception type without exposing the exception message.

Set `STARTER_KIT_BUILD_COMMIT` to the deployed Git SHA so incidents can be mapped to source.

## Logging

Local development defaults to human-readable text logs. Set `STARTER_KIT_LOG_FORMAT=json` in
containers and hosted environments to emit one JSON object per line. Custom fields supplied via
the logging `extra` argument are stored under `context`. Use `log_context(request_id="...")` to
bind correlation fields for the duration of an operation without leaking state to other tasks.

## Containers

Build and run the non-root image with:

```bash
docker build -t starter-kit-python .
docker run --rm starter-kit-python health --pretty
```

Override the entrypoint arguments to run other commands. Inject configuration with `--env` or an
orchestrator's secret/config mechanism; never bake secrets into the image.

## Quality gate

Run all local checks using one cross-platform command:

```bash
uv run python scripts/check.py
uv build
```

CI repeats these checks and also builds and executes the container health command.
