"""Tests for shikigami_dice_simple dice CLI."""

import subprocess
import sys

from shikigami_dice_simple import __version__
from shikigami_dice_simple.__main__ import roll_dice


def test_version():
    """Test that version is defined."""
    assert __version__ == "0.1.0"


def test_roll_dice_default():
    """Test default behavior: single roll."""
    results = roll_dice(1)
    assert len(results) == 1
    assert 1 <= results[0] <= 6


def test_roll_dice_multiple():
    """Test multiple rolls."""
    results = roll_dice(5)
    assert len(results) == 5
    for result in results:
        assert 1 <= result <= 6


def test_seed_determinism():
    """Test that seed produces deterministic results."""
    seed = 42
    results1 = roll_dice(10, seed)
    results2 = roll_dice(10, seed)
    assert results1 == results2


def test_seed_different_values():
    """Test that different seeds produce different results."""
    results1 = roll_dice(100, seed=1)
    results2 = roll_dice(100, seed=2)
    # With 100 rolls, they should almost certainly differ
    assert results1 != results2


def test_cli_rolls_validation():
    """Test CLI validates rolls >= 1 and exits with code 2."""
    result = subprocess.run(
        [sys.executable, "-m", "shikigami_dice_simple", "--rolls", "0"],
        capture_output=True,
    )
    assert result.returncode == 2
    assert b"Error:" in result.stderr


def test_cli_negative_rolls():
    """Test CLI rejects negative rolls."""
    result = subprocess.run(
        [sys.executable, "-m", "shikigami_dice_simple", "--rolls", "-1"],
        capture_output=True,
    )
    assert result.returncode == 2


def test_cli_default_behavior():
    """Test CLI default output (single roll)."""
    result = subprocess.run(
        [sys.executable, "-m", "shikigami_dice_simple"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    output = result.stdout.strip()
    values = output.split()
    assert len(values) == 1
    assert 1 <= int(values[0]) <= 6


def test_cli_multiple_rolls():
    """Test CLI with multiple rolls."""
    result = subprocess.run(
        [sys.executable, "-m", "shikigami_dice_simple", "--rolls", "3"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    output = result.stdout.strip()
    values = output.split()
    assert len(values) == 3
    for val in values:
        assert 1 <= int(val) <= 6


def test_cli_seed_reproducibility():
    """Test CLI with seed produces reproducible output."""
    seed = "123"
    result1 = subprocess.run(
        [sys.executable, "-m", "shikigami_dice_simple", "--seed", seed, "--rolls", "5"],
        capture_output=True,
        text=True,
    )
    result2 = subprocess.run(
        [sys.executable, "-m", "shikigami_dice_simple", "--seed", seed, "--rolls", "5"],
        capture_output=True,
        text=True,
    )
    assert result1.stdout == result2.stdout
