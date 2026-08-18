"""Command-line interface for the starter application."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from typing import TYPE_CHECKING

from starter_kit import __version__
from starter_kit.config import Settings
from starter_kit.context import log_context
from starter_kit.diagnostics import collect_health
from starter_kit.logging import configure_logging

if TYPE_CHECKING:
    from collections.abc import Sequence

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

    health_parser = subparsers.add_parser("health", help="Print runtime health metadata as JSON.")
    health_parser.add_argument(
        "--pretty", action="store_true", help="Pretty-print the JSON output."
    )
    return parser


def main(argv: Sequence[str] | None = None, *, settings: Settings | None = None) -> int:
    """Run the CLI and return a process exit code."""
    active_settings = settings or Settings.from_env()
    configure_logging(active_settings.log_level, active_settings.log_format)
    args = build_parser().parse_args(argv)

    with log_context(command=args.command, environment=active_settings.environment):
        return _dispatch(args, active_settings)


def _dispatch(args: argparse.Namespace, settings: Settings) -> int:
    """Execute a parsed command using validated settings."""

    if args.command == "hello":
        LOGGER.info("Greeting requested")
        print(f"Hello, {args.name}!")
        return 0

    if args.command == "show-config":
        print(json.dumps(settings.as_dict(), indent=2, sort_keys=True))
        return 0

    if args.command == "health":
        indent = 2 if args.pretty else None
        print(json.dumps(collect_health(settings).as_dict(), indent=indent, sort_keys=True))
        return 0

    raise AssertionError(f"Unhandled command: {args.command}")  # pragma: no cover


def entrypoint() -> None:
    """Console script entry point."""
    try:
        exit_code = main()
    except ValueError as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        exit_code = 2
    raise SystemExit(exit_code)
