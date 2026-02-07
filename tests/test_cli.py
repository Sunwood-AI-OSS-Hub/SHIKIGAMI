"""Tests for shikigami_hello CLI."""

import subprocess
import sys


def test_default_greeting():
    """Test default greeting without arguments."""
    result = subprocess.run(
        [sys.executable, '-m', 'shikigami_hello'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello, world"


def test_custom_name():
    """Test greeting with custom name."""
    result = subprocess.run(
        [sys.executable, '-m', 'shikigami_hello', '--name', 'Alice'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello, Alice"


def test_short_flag():
    """Test greeting with short flag."""
    result = subprocess.run(
        [sys.executable, '-m', 'shikigami_hello', '-n', 'Bob'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello, Bob"


def test_empty_string():
    """Test that empty string returns error."""
    result = subprocess.run(
        [sys.executable, '-m', 'shikigami_hello', '--name', ''],
        capture_output=True,
        text=True
    )
    assert result.returncode == 1
    assert "Error:" in result.stderr


def test_whitespace_only():
    """Test that whitespace-only name returns error."""
    result = subprocess.run(
        [sys.executable, '-m', 'shikigami_hello', '--name', '   '],
        capture_output=True,
        text=True
    )
    assert result.returncode == 1
    assert "Error:" in result.stderr


def test_whitespace_trim():
    """Test that leading/trailing whitespace is trimmed."""
    result = subprocess.run(
        [sys.executable, '-m', 'shikigami_hello', '--name', '  Alice  '],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello, Alice"


def test_newlines_stripped():
    """Test that newlines are removed from name."""
    result = subprocess.run(
        [sys.executable, '-m', 'shikigami_hello', '--name', 'A\nB'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello, AB"


def test_unicode_emoji():
    """Test that emoji are supported."""
    result = subprocess.run(
        [sys.executable, '-m', 'shikigami_hello', '--name', '👻'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello, 👻"


def test_unicode_japanese():
    """Test that Japanese characters are supported."""
    result = subprocess.run(
        [sys.executable, '-m', 'shikigami_hello', '--name', '日本語'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello, 日本語"


def test_version_flag():
    """Test --version flag."""
    result = subprocess.run(
        [sys.executable, '-m', 'shikigami_hello', '--version'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "shikigami-hello" in result.stdout
    assert "0.1.0" in result.stdout
