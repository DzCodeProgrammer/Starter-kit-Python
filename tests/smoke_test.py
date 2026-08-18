"""Smoke test executed against isolated wheel and source-distribution installs."""

from __future__ import annotations

import json
import subprocess
import sys

from starter_kit import __version__


def main() -> int:
    """Verify package metadata and the installed console entry point."""
    completed = subprocess.run(
        [sys.executable, "-m", "starter_kit", "health"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)
    if payload["status"] != "ok" or payload["version"] != __version__:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
