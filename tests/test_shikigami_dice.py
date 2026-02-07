"""Tests for shikigami_dice package."""

import subprocess
import sys


def test_seed_determinism():
    """Test that using the same seed produces the same results."""
    # Test with seed=42, sides=6, rolls=5
    result1 = subprocess.run(
        [sys.executable, "-m", "shikigami_dice", "--sides", "6", "--rolls", "5", "--seed", "42"],
        capture_output=True,
        text=True
    )
    result2 = subprocess.run(
        [sys.executable, "-m", "shikigami_dice", "--sides", "6", "--rolls", "5", "--seed", "42"],
        capture_output=True,
        text=True
    )

    assert result1.returncode == 0
    assert result2.returncode == 0
    assert result1.stdout == result2.stdout
    # Verify we got 5 numbers
    assert len(result1.stdout.strip().split()) == 5


def test_sides_validation():
    """Test that sides < 2 is rejected with exit code 2."""
    result = subprocess.run(
        [sys.executable, "-m", "shikigami_dice", "--sides", "1"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 2
    assert "Error" in result.stderr
    assert "sides must be >= 2" in result.stderr


def test_rolls_validation():
    """Test that rolls < 1 is rejected with exit code 2."""
    result = subprocess.run(
        [sys.executable, "-m", "shikigami_dice", "--rolls", "0"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 2
    assert "Error" in result.stderr
    assert "rolls must be >= 1" in result.stderr


def test_default_behavior():
    """Test default behavior (6 sides, 1 roll)."""
    result = subprocess.run(
        [sys.executable, "-m", "shikigami_dice"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    output = result.stdout.strip()
    # Should be a single number between 1 and 6
    values = output.split()
    assert len(values) == 1
    value = int(values[0])
    assert 1 <= value <= 6


def test_multiple_rolls():
    """Test multiple rolls output format."""
    result = subprocess.run(
        [sys.executable, "-m", "shikigami_dice", "--sides", "10", "--rolls", "3", "--seed", "123"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    values = result.stdout.strip().split()
    assert len(values) == 3
    # All values should be between 1 and 10
    for v in values:
        value = int(v)
        assert 1 <= value <= 10
