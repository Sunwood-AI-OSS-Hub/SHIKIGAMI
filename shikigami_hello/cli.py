"""CLI module for shikigami_hello greeting application."""

import argparse


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed arguments with 'name' attribute
    """
    parser = argparse.ArgumentParser(
        description="A simple greeting CLI application"
    )
    parser.add_argument(
        "--name",
        type=str,
        default="world",
        help="Name to greet (default: world)"
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point for the CLI application."""
    args = parse_args()
    print(f"Hello, {args.name}")


if __name__ == "__main__":
    main()
