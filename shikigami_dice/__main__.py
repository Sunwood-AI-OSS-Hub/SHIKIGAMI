#!/usr/bin/env python3
"""shikigami_dice - Simple dice rolling CLI.

Usage:
    python -m shikigami_dice [OPTIONS]

Options:
    --sides N    Number of sides on the dice (default: 6, must be >= 2)
    --rolls K    Number of rolls (default: 1, must be >= 1)
    --seed S     Random seed for reproducibility (optional)
"""

import argparse
import random
import sys


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Roll dice and display results.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python -m shikigami_dice           # Roll one 6-sided die
  python -m shikigami_dice --sides 20  # Roll one 20-sided die
  python -m shikigami_dice --rolls 3   # Roll 3 dice
  python -m shikigami_dice --sides 10 --rolls 5 --seed 42  # Reproducible roll"""
    )
    parser.add_argument(
        "--sides",
        type=int,
        default=6,
        help="Number of sides on the dice (default: 6, must be >= 2)"
    )
    parser.add_argument(
        "--rolls",
        type=int,
        default=1,
        help="Number of rolls (default: 1, must be >= 1)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility (optional)"
    )
    return parser.parse_args()


def validate_args(args):
    """Validate command line arguments.

    Returns:
        tuple: (is_valid, error_message)
    """
    if args.sides < 2:
        return False, f"Error: sides must be >= 2, got {args.sides}"
    if args.rolls < 1:
        return False, f"Error: rolls must be >= 1, got {args.rolls}"
    return True, None


def roll_dice(sides, rolls, seed=None):
    """Roll dice and return results.

    Args:
        sides: Number of sides on each die
        rolls: Number of times to roll
        seed: Optional random seed for reproducibility

    Returns:
        list: List of roll results
    """
    if seed is not None:
        random.seed(seed)
    return [random.randint(1, sides) for _ in range(rolls)]


def main():
    """Main entry point for the dice CLI."""
    args = parse_args()

    # Validate inputs
    is_valid, error_msg = validate_args(args)
    if not is_valid:
        print(error_msg, file=sys.stderr)
        print("\nUsage:", file=sys.stderr)
        print("  python -m shikigami_dice [--sides N] [--rolls K] [--seed S]", file=sys.stderr)
        sys.exit(2)

    # Roll dice
    results = roll_dice(args.sides, args.rolls, args.seed)

    # Output results (space-separated on one line)
    print(" ".join(map(str, results)))


if __name__ == "__main__":
    main()
