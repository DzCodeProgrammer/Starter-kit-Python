# Releasing

## GitHub release artifacts

1. Update `CHANGELOG.md` and the version in `pyproject.toml` and `src/starter_kit/__init__.py`.
2. Run `uv run python scripts/check.py` and `uv build`.
3. Open and merge a release PR.
4. Create and push an annotated tag such as `v0.2.0`.

The release workflow rebuilds the distributions from the tag, verifies their metadata and
contents, smoke-tests both formats in isolated environments, and creates a GitHub release with
the artifacts attached.

## Optional PyPI publication

PyPI publication is intentionally not active in this starter because the final distribution
name and owner must be chosen first. When ready, configure a protected `pypi` GitHub environment
and a PyPI trusted publisher, then add a dedicated publish job with only `id-token: write`.

Keep building and publishing in separate jobs, never store a long-lived PyPI token, and keep the
publishing job free of repository-controlled build commands.
