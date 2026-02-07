"""Tests for shikigami_dice2 dice rolling CLI."""

import subprocess
import sys

from shikigami_dice2 import roll_dice


def test_seed_produces_deterministic_results():
    """Test that using a seed produces deterministic results."""
    seed = 42
    sides = 6
    rolls = 5

    result1 = roll_dice(sides, rolls, seed)
    result2 = roll_dice(sides, rolls, seed)

    assert result1 == result2, "Same seed should produce identical results"
    assert len(result1) == rolls, f"Should have {rolls} results"

    # Verify results are within valid range
    for value in result1:
        assert 1 <= value <= sides, f"Result {value} not in range [1, {sides}]"


def test_default_behavior():
    """Test default behavior (6-sided die, 1 roll)."""
    result = roll_dice()

    assert len(result) == 1, "Default should roll once"
    assert 1 <= result[0] <= 6, "Default result should be in range [1, 6]"


def test_custom_sides_and_rolls():
    """Test custom number of sides and rolls."""
    sides = 20
    rolls = 3

    result = roll_dice(sides=sides, rolls=rolls)

    assert len(result) == rolls, f"Should have {rolls} results"
    for value in result:
        assert 1 <= value <= sides, f"Result {value} not in range [1, {sides}]"


def test_validation_sides_minimum():
    """Test that sides < 2 is rejected via CLI."""
    result = subprocess.run(
        [sys.executable, "-m", "shikigami_dice2", "--sides", "1"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 2, "Should exit with code 2 for invalid sides"
    assert "Error:" in result.stderr or "usage" in result.stderr.lower()


def test_validation_rolls_minimum():
    """Test that rolls < 1 is rejected via CLI."""
    result = subprocess.run(
        [sys.executable, "-m", "shikigami_dice2", "--rolls", "0"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 2, "Should exit with code 2 for invalid rolls"
    assert "Error:" in result.stderr or "usage" in result.stderr.lower()


def test_cli_basic_output():
    """Test basic CLI output format."""
    result = subprocess.run(
        [sys.executable, "-m", "shikigami_dice2", "--seed", "42", "--rolls", "3"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, "Should succeed"
    output = result.stdout.strip()
    values = output.split()

    assert len(values) == 3, "Should have 3 values"
    for v in values:
        assert v.isdigit(), "Output should be numeric"
        num = int(v)
        assert 1 <= num <= 6, "Values should be in range [1, 6]"


def test_cli_with_seed():
    """Test that CLI with seed produces consistent output."""
    seed = "123"
    rolls = "5"

    result1 = subprocess.run(
        [sys.executable, "-m", "shikigami_dice2", "--seed", seed, "--rolls", rolls],
        capture_output=True,
        text=True
    )

    result2 = subprocess.run(
        [sys.executable, "-m", "shikigami_dice2", "--seed", seed, "--rolls", rolls],
        capture_output=True,
        text=True
    )

    assert result1.stdout == result2.stdout, "Same seed should produce identical output"
