"""
shikigami_coin のテスト
"""

import json
import subprocess
import sys


def run_shikigami_coin(*args: str) -> subprocess.CompletedProcess[str]:
    """shikigami_coin CLIを実行するヘルパー関数"""
    return subprocess.run(
        [sys.executable, "-m", "shikigami_coin", *args],
        capture_output=True,
        text=True,
    )


def test_default_single_flip():
    """デフォルト挙動：1回だけトスして heads/tails のどちらかを出力"""
    result = run_shikigami_coin()
    assert result.returncode == 0
    assert result.stdout.strip() in ("heads", "tails")


def test_flips_option():
    """--flips オプション：指定回数分の結果をスペース区切りで出力"""
    result = run_shikigami_coin("--flips", "3")
    assert result.returncode == 0
    outputs = result.stdout.strip().split()
    assert len(outputs) == 3
    for output in outputs:
        assert output in ("heads", "tails")


def test_seed_deterministic():
    """seed 指定で決定的になる：同じシードなら同じ結果"""
    result1 = run_shikigami_coin("--flips", "10", "--seed", "42")
    result2 = run_shikigami_coin("--flips", "10", "--seed", "42")
    assert result1.returncode == 0
    assert result2.returncode == 0
    assert result1.stdout == result2.stdout


def test_seed_different_results():
    """異なるシードでは異なる結果になる"""
    result1 = run_shikigami_coin("--flips", "10", "--seed", "42")
    result2 = run_shikigami_coin("--flips", "10", "--seed", "123")
    assert result1.returncode == 0
    assert result2.returncode == 0
    assert result1.stdout != result2.stdout


def test_flips_validation():
    """flips のバリデーション：0以下の値ではエラー（終了コード2）"""
    result = run_shikigami_coin("--flips", "0")
    assert result.returncode == 2
    assert "エラー" in result.stderr or "error" in result.stderr.lower()

    result = run_shikigami_coin("--flips", "-1")
    assert result.returncode == 2


def test_json_output():
    """JSON 出力：正しいJSON形式で results 配列を含む"""
    result = run_shikigami_coin("--flips", "3", "--format", "json")
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert "results" in data
    assert len(data["results"]) == 3
    for item in data["results"]:
        assert item in ("heads", "tails")


def test_json_with_seed():
    """JSON + seed の組み合わせ：正しいJSONで結果が再現可能"""
    result1 = run_shikigami_coin("--flips", "5", "--seed", "999", "--format", "json")
    result2 = run_shikigami_coin("--flips", "5", "--seed", "999", "--format", "json")
    assert result1.returncode == 0
    assert result2.returncode == 0
    data1 = json.loads(result1.stdout)
    data2 = json.loads(result2.stdout)
    assert data1 == data2
