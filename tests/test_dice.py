"""
shikigami_dice_ci のテスト
"""

import subprocess
import sys


def test_seed_determinism():
    """
    テスト1: seedを指定すると同じ結果になること
    """
    # seed=42, rolls=3 で2回実行して結果が一致することを確認
    result1 = subprocess.run(
        [sys.executable, "-m", "shikigami_dice_ci", "--rolls", "3", "--seed", "42"],
        capture_output=True,
        text=True,
    )
    result2 = subprocess.run(
        [sys.executable, "-m", "shikigami_dice_ci", "--rolls", "3", "--seed", "42"],
        capture_output=True,
        text=True,
    )

    assert result1.returncode == 0
    assert result2.returncode == 0
    assert result1.stdout.strip() == result2.stdout.strip()


def test_rolls_validation():
    """
    テスト2: rollsに0や負数を指定するとエラーになること
    """
    # rolls=0 でエラー
    result0 = subprocess.run(
        [sys.executable, "-m", "shikigami_dice_ci", "--rolls", "0"],
        capture_output=True,
        text=True,
    )
    assert result0.returncode == 2
    assert "エラー" in result0.stderr or "error" in result0.stderr.lower()

    # rolls=-1 でエラー
    result_neg = subprocess.run(
        [sys.executable, "-m", "shikigami_dice_ci", "--rolls", "-1"],
        capture_output=True,
        text=True,
    )
    assert result_neg.returncode == 2


def test_default_behavior():
    """
    テスト3: オプションなしで1回振って1つの値が出力されること
    """
    result = subprocess.run(
        [sys.executable, "-m", "shikigami_dice_ci"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    output = result.stdout.strip()

    # 1つの整数（1-6）が出力されていること
    parts = output.split()
    assert len(parts) == 1
    value = int(parts[0])
    assert 1 <= value <= 6


def test_multiple_rolls():
    """
    テスト4: 複数回振ると指定数の値が出力されること
    """
    result = subprocess.run(
        [sys.executable, "-m", "shikigami_dice_ci", "--rolls", "5", "--seed", "123"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    output = result.stdout.strip()

    # 5つの整数が出力されていること
    parts = output.split()
    assert len(parts) == 5

    # 全ての値が1-6の範囲であること
    for part in parts:
        value = int(part)
        assert 1 <= value <= 6
