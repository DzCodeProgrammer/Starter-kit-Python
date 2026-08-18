"""Command-line interface for the starter application."""

from __future__ import annotations

import argparse
import json
import logging
from collections.abc import Sequence

from starter_kit import __version__
from starter_kit.config import Settings
from starter_kit.logging import configure_logging

LOGGER = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Build and return the command-line parser."""
    parser = argparse.ArgumentParser(
        prog="starter-kit",
        description="A production-friendly Python starter application.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", required=True)

    hello_parser = subparsers.add_parser("hello", help="Print a greeting.")
    hello_parser.add_argument("--name", default="World", help="Name to greet.")

    subparsers.add_parser("show-config", help="Print the active non-secret settings as JSON.")
    return parser


def main(argv: Sequence[str] | None = None, *, settings: Settings | None = None) -> int:
    """Run the CLI and return a process exit code."""
    active_settings = settings or Settings.from_env()
    configure_logging(active_settings.log_level)
    args = build_parser().parse_args(argv)

    if args.command == "hello":
        LOGGER.info("Greeting requested", extra={"environment": active_settings.environment})
        print(f"Hello, {args.name}!")
        return 0

    if args.command == "show-config":
        print(json.dumps(active_settings.as_dict(), indent=2, sort_keys=True))
        return 0

    raise AssertionError(f"Unhandled command: {args.command}")  # pragma: no cover


def entrypoint() -> None:
    """Console script entry point."""
    raise SystemExit(main())
