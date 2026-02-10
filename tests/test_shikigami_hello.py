"""
shikigami_hello CLI のテスト
"""

import subprocess
import sys


def test_cli_default_output():
    """デフォルトで 'Hello, world' と出力することをテスト"""
    result = subprocess.run(
        [sys.executable, '-m', 'shikigami_hello'],
        capture_output=True,
        text=True
    )
    assert result.stdout.strip() == 'Hello, world'
    assert result.returncode == 0


def test_cli_with_name_argument():
    """--name 引数で名前を指定できることをテスト"""
    result = subprocess.run(
        [sys.executable, '-m', 'shikigami_hello', '--name', 'Alice'],
        capture_output=True,
        text=True
    )
    assert result.stdout.strip() == 'Hello, Alice'
    assert result.returncode == 0


def test_cli_with_short_name_argument():
    """短縮形 -n 引数で名前を指定できることをテスト"""
    result = subprocess.run(
        [sys.executable, '-m', 'shikigami_hello', '-n', 'Bob'],
        capture_output=True,
        text=True
    )
    assert result.stdout.strip() == 'Hello, Bob'
    assert result.returncode == 0


def test_cli_with_japanese_name():
    """日本語の名前を指定できることをテスト"""
    result = subprocess.run(
        [sys.executable, '-m', 'shikigami_hello', '--name', '太郎'],
        capture_output=True,
        text=True
    )
    assert result.stdout.strip() == 'Hello, 太郎'
    assert result.returncode == 0


def test_cli_with_empty_name():
    """空文字列の名前を指定した場合のテスト"""
    result = subprocess.run(
        [sys.executable, '-m', 'shikigami_hello', '--name', ''],
        capture_output=True,
        text=True
    )
    assert result.stdout.strip() == 'Hello, '
    assert result.returncode == 0


def test_cli_help_option():
    """--help オプションでヘルプが表示されることをテスト"""
    result = subprocess.run(
        [sys.executable, '-m', 'shikigami_hello', '--help'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'shikigami_hello' in result.stdout
    assert '--name' in result.stdout or '-n' in result.stdout
