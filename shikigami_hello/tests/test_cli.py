"""Tests for shikigami_hello CLI application."""

import pytest
from shikigami_hello.cli import parse_args, main
from unittest.mock import patch
import sys


class TestParseArgs:
    """Tests for parse_args function."""

    def test_default_name(self):
        """Test that default name is 'world' when no arguments provided."""
        # Simulate no command line arguments
        with patch.object(sys, 'argv', ['shikigami_hello']):
            args = parse_args()
            assert args.name == "world"

    def test_custom_name(self):
        """Test that custom name is used when --name argument provided."""
        with patch.object(sys, 'argv', ['shikigami_hello', '--name', 'Alice']):
            args = parse_args()
            assert args.name == "Alice"

    def test_name_with_spaces(self):
        """Test that names with spaces work correctly."""
        with patch.object(sys, 'argv', ['shikigami_hello', '--name', 'Claude AI']):
            args = parse_args()
            assert args.name == "Claude AI"


class TestMain:
    """Tests for main function."""

    def test_main_default_output(self, capsys):
        """Test that main prints 'Hello, world' by default."""
        with patch.object(sys, 'argv', ['shikigami_hello']):
            main()
            captured = capsys.readouterr()
            assert captured.out == "Hello, world\n"

    def test_main_custom_name_output(self, capsys):
        """Test that main prints 'Hello, <name>' with custom name."""
        with patch.object(sys, 'argv', ['shikigami_hello', '--name', 'Alice']):
            main()
            captured = capsys.readouterr()
            assert captured.out == "Hello, Alice\n"

    def test_main_japanese_name(self, capsys):
        """Test that main works with Japanese characters."""
        with patch.object(sys, 'argv', ['shikigami_hello', '--name', '式神']):
            main()
            captured = capsys.readouterr()
            assert captured.out == "Hello, 式神\n"
