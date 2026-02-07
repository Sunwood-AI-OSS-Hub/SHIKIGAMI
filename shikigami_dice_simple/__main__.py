"""SHIKIGAMI Dice Simple - Main CLI entry point."""

import argparse
import random
import sys


def roll_dice(num_rolls: int, seed: int | None = None) -> list[int]:
    """Roll the dice specified number of times.

    Args:
        num_rolls: Number of times to roll (1-6)
        seed: Optional seed for reproducibility

    Returns:
        List of dice roll results
    """
    if seed is not None:
        random.seed(seed)
    return [random.randint(1, 6) for _ in range(num_rolls)]


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        prog="shikigami_dice_simple",
        description="Simple dice roller CLI - Roll 1-6 sided dice.",
        epilog="Examples:\n  python -m shikigami_dice_simple\n  python -m shikigami_dice_simple --rolls 3\n  python -m shikigami_dice_simple --rolls 5 --seed 42",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--rolls",
        "-r",
        type=int,
        default=1,
        metavar="K",
        help="Number of times to roll the dice (default: 1)",
    )
    parser.add_argument(
        "--seed",
        "-s",
        type=int,
        default=None,
        metavar="S",
        help="Seed for random number generation (enables reproducibility)",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point for the dice CLI."""
    args = parse_args()

    # Validate rolls
    if args.rolls < 1:
        print(
            f"Error: --rolls must be >= 1, got {args.rolls}",
            file=sys.stderr,
        )
        print("\nUsage:", file=sys.stderr)
        parse_args().print_help()
        sys.exit(2)

    # Roll dice and output results
    results = roll_dice(args.rolls, args.seed)
    print(" ".join(map(str, results)))


if __name__ == "__main__":
    main()
