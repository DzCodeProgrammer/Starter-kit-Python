"""Run the full local quality gate consistently across operating systems."""

from __future__ import annotations

import shutil
import subprocess


def _tool(name: str) -> str:
    executable = shutil.which(name)
    if executable is None:
        raise RuntimeError(f"Required development tool is unavailable: {name}")
    return executable


def _commands() -> tuple[tuple[str, ...], ...]:
    return (
        (_tool("ruff"), "check", "."),
        (_tool("ruff"), "format", "--check", "."),
        (_tool("mypy"), "src", "tests", "scripts"),
        (_tool("pytest"),),
        (_tool("validate-pyproject"), "pyproject.toml"),
        (_tool("codespell"), "."),
        (_tool("deptry"), "src"),
        (_tool("vulture"), "src", "scripts", "--min-confidence", "90"),
        (_tool("mkdocs"), "build", "--strict"),
        (
            _tool("pip-audit"),
            "--local",
            "--skip-editable",
            "--cache-dir",
            ".pip-audit-cache",
        ),
        (_tool("zizmor"), "--pedantic", ".github/workflows"),
    )


def main() -> int:
    """Run each check in order and stop at the first failure."""
    for command in _commands():
        print(f"+ {' '.join(command)}", flush=True)
        result = subprocess.run(command, check=False)  # noqa: S603
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
