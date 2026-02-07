"""pytest tests for shikigami_dice_verify2"""

import subprocess
import sys


def test_seed_deterministic():
    """seed指定時に決定的な結果が得られることをテスト"""
    # 同じシードで2回実行して結果が一致するか確認
    result1 = subprocess.run(
        [sys.executable, "-m", "shikigami_dice_verify2", "--seed", "42", "--rolls", "10"],
        capture_output=True,
        text=True
    )
    result2 = subprocess.run(
        [sys.executable, "-m", "shikigami_dice_verify2", "--seed", "42", "--rolls", "10"],
        capture_output=True,
        text=True
    )

    assert result1.returncode == 0
    assert result2.returncode == 0
    assert result1.stdout.strip() == result2.stdout.strip()

    # 出力が10個の数値であることを確認
    values = result1.stdout.strip().split()
    assert len(values) == 10
    assert all(v.isdigit() and 1 <= int(v) <= 6 for v in values)


def test_rolls_validation():
    """rollsのバリデーションをテスト（不正値はエラー）"""
    # 0はエラー
    result = subprocess.run(
        [sys.executable, "-m", "shikigami_dice_verify2", "--rolls", "0"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 2
    assert "エラー" in result.stderr or "error" in result.stderr.lower()

    # 負の値はエラー
    result = subprocess.run(
        [sys.executable, "-m", "shikigami_dice_verify2", "--rolls", "-1"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 2


def test_default_behavior():
    """デフォルトの挙動をテスト（引数なしで1回振る）"""
    result = subprocess.run(
        [sys.executable, "-m", "shikigami_dice_verify2"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    output = result.stdout.strip()

    # 出力は1つの数値
    values = output.split()
    assert len(values) == 1
    assert values[0].isdigit()
    assert 1 <= int(values[0]) <= 6


def test_multiple_rolls():
    """複数回振る場合のテスト"""
    result = subprocess.run(
        [sys.executable, "-m", "shikigami_dice_verify2", "--rolls", "5"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    values = result.stdout.strip().split()
    assert len(values) == 5
    assert all(v.isdigit() and 1 <= int(v) <= 6 for v in values)


def test_output_format():
    """出力形式のテスト（スペース区切り）"""
    result = subprocess.run(
        [sys.executable, "-m", "shikigami_dice_verify2", "--seed", "123", "--rolls", "3"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    output = result.stdout.strip()

    # スペースで区切られている
    assert " " in output or len(output.split()) == 3

    # 余計な空白や改行がない
    assert output == output.strip()
    assert "\n" not in output
