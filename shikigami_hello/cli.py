"""CLI interface for shikigami_hello."""

import argparse
import sys

from . import __version__
from .core import greet


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="shikigami_hello",
        description="Greet someone by name.",
    )
    parser.add_argument(
        "-n",
        "--name",
        default="world",
        help="Name to greet [default: world]",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"shikigami_hello {__version__}",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """
    Main CLI entry point.

    Args:
        argv: Command line arguments. If None, uses sys.argv[1:].

    Returns:
        Exit code (0 for success).
    """
    args = parse_args(argv)
    message = greet(args.name)
    print(message)
    return 0
