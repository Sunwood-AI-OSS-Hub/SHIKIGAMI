"""Tests for shikigami_hello CLI."""

import subprocess

import pytest


def test_cli_default():
    """Test default greeting (no --name argument)."""
    result = subprocess.run(
        ["python", "-m", "shikigami_hello"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello, world"


def test_cli_with_name():
    """Test greeting with --name argument."""
    result = subprocess.run(
        ["python", "-m", "shikigami_hello", "--name", "Alice"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello, Alice"


def test_cli_with_short_flag():
    """Test greeting with -n short flag."""
    result = subprocess.run(
        ["python", "-m", "shikigami_hello", "-n", "Bob"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello, Bob"


def test_cli_help():
    """Test --help flag."""
    result = subprocess.run(
        ["python", "-m", "shikigami_hello", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Greet someone by name" in result.stdout
    assert "--name" in result.stdout
    assert "-n" in result.stdout


def test_cli_version():
    """Test --version flag."""
    result = subprocess.run(
        ["python", "-m", "shikigami_hello", "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "shikigami_hello" in result.stdout
    assert "0.1.0" in result.stdout


def test_cli_empty_name():
    """Test with empty string name."""
    result = subprocess.run(
        ["python", "-m", "shikigami_hello", "--name", ""],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello, world"


def test_cli_whitespace_name():
    """Test with whitespace-only name."""
    result = subprocess.run(
        ["python", "-m", "shikigami_hello", "--name", "   "],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello, world"
