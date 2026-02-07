"""CLI module for shikigami_dice2 dice rolling application."""

import argparse
import random
import sys


def roll_dice(sides: int = 6, rolls: int = 1, seed: int | None = None) -> list[int]:
    """
    Roll a dice multiple times.

    Args:
        sides: Number of sides on the dice (must be >= 2)
        rolls: Number of times to roll (must be >= 1)
        seed: Random seed for reproducibility (optional)

    Returns:
        List of roll results
    """
    if seed is not None:
        random.seed(seed)

    return [random.randint(1, sides) for _ in range(rolls)]


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="python -m shikigami_dice2",
        description="A simple dice rolling CLI application."
    )
    parser.add_argument(
        "--sides",
        type=int,
        default=6,
        metavar="N",
        help="Number of sides on the dice (default: 6, must be >= 2)"
    )
    parser.add_argument(
        "--rolls",
        type=int,
        default=1,
        metavar="K",
        help="Number of times to roll (default: 1, must be >= 1)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        metavar="S",
        help="Random seed for reproducibility (optional)"
    )

    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> bool:
    """
    Validate command line arguments.

    Args:
        args: Parsed arguments

    Returns:
        True if valid, False otherwise
    """
    if args.sides < 2:
        print(f"Error: --sides must be >= 2, got {args.sides}", file=sys.stderr)
        return False

    if args.rolls < 1:
        print(f"Error: --rolls must be >= 1, got {args.rolls}", file=sys.stderr)
        return False

    return True


def main() -> None:
    """Main entry point for the CLI."""
    args = parse_args()

    if not validate_args(args):
        parser = parse_args.__wrapped__
        print("\nUsage:", file=sys.stderr)
        print("  python -m shikigami_dice2 [--sides N] [--rolls K] [--seed S]", file=sys.stderr)
        print("\nOptions:", file=sys.stderr)
        print("  --sides N     Number of sides on the dice (default: 6, must be >= 2)", file=sys.stderr)
        print("  --rolls K     Number of times to roll (default: 1, must be >= 1)", file=sys.stderr)
        print("  --seed S      Random seed for reproducibility (optional)", file=sys.stderr)
        sys.exit(2)

    results = roll_dice(args.sides, args.rolls, args.seed)
    print(" ".join(map(str, results)))


if __name__ == "__main__":
    main()
