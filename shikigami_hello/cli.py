"""CLI implementation for shikigami_hello."""

import argparse
import sys
import unicodedata

MAX_NAME_LENGTH = 1000


def sanitize_name(name: str) -> str:
    """
    Strip whitespace, normalize to NFC, remove control/format characters.

    Args:
        name: The raw name input

    Returns:
        Sanitized name

    Raises:
        ValueError: If name is empty after sanitization or exceeds max length
    """
    # Strip whitespace from ends
    name = name.strip()

    # Normalize to NFC
    name = unicodedata.normalize('NFC', name)

    # Remove ALL control characters (C*) and line/paragraph separators (Zl, Zp)
    result = []
    for char in name:
        cat = unicodedata.category(char)
        if cat[0] not in ('C', 'Z'):  # Excludes all C* and Z* categories
            result.append(char)

    sanitized = ''.join(result)

    # Check if empty after sanitization
    if not sanitized:
        raise ValueError("Name cannot be empty or whitespace only.")

    # Check max length
    if len(sanitized) > MAX_NAME_LENGTH:
        raise ValueError(f"Name exceeds maximum length of {MAX_NAME_LENGTH} characters.")

    return sanitized


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="A simple greeting CLI tool.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '--name', '-n',
        type=str,
        default='world',
        help='The name to greet (default: "world")'
    )

    parser.add_argument(
        '--version',
        action='store_true',
        help='Show version information and exit'
    )

    args = parser.parse_args()

    # Handle --version
    if args.version:
        from . import __version__
        print(f"shikigami-hello {__version__}")
        sys.exit(0)

    # Handle --name
    try:
        sanitized_name = sanitize_name(args.name)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("\nRun 'python -m shikigami_hello --help' for usage.", file=sys.stderr)
        sys.exit(1)

    print(f"Hello, {sanitized_name}")
    sys.exit(0)


if __name__ == "__main__":
    main()
