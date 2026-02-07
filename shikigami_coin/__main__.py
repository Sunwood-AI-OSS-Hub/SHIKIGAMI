"""
shikigami_coin CLIエントリーポイント

`python -m shikigami_coin` で実行されます。
"""

import argparse
import json
import random
import sys


def flip_coin() -> str:
    """コインを1回投げて 'heads' または 'tails' を返す"""
    return "heads" if random.random() < 0.5 else "tails"


def flip_coins(count: int, seed: int | None = None) -> list[str]:
    """
    指定回数コイントスを行う

    Args:
        count: 投げる回数
        seed: 乱数シード（再現性のため）

    Returns:
        コイントス結果のリスト
    """
    if seed is not None:
        random.seed(seed)
    return [flip_coin() for _ in range(count)]


def parse_args() -> argparse.Namespace:
    """コマンドライン引数をパースする"""
    parser = argparse.ArgumentParser(
        description="シンプルなコイントスCLIアプリケーション",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  python -m shikigami_coin              # 1回だけトス
  python -m shikigami_coin --flips 5    # 5回トス
  python -m shikigami_coin --seed 42    # シードを指定（再現可能）
  python -m shikigami_coin --format json --flips 3  # JSON形式で出力
        """,
    )
    parser.add_argument(
        "--flips",
        type=int,
        default=1,
        help="トスする回数（デフォルト: 1）",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="乱数シード（指定時は結果が再現可能）",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="出力フォーマット（デフォルト: text）",
    )
    return parser.parse_args()


def output_text(results: list[str]) -> None:
    """テキスト形式で出力する"""
    print(" ".join(results))


def output_json(results: list[str]) -> None:
    """JSON形式で出力する"""
    print(json.dumps({"results": results}, indent=2))


def main() -> int:
    """メイン関数"""
    args = parse_args()

    # 入力値バリデーション
    if args.flips < 1:
        print(
            f"エラー: --flips は1以上の整数を指定してください（指定値: {args.flips}）",
            file=sys.stderr,
        )
        print("使い方: python -m shikigami_coin [--flips N] [--seed S] [--format FORMAT]", file=sys.stderr)
        return 2

    # コイントス実行
    results = flip_coins(args.flips, args.seed)

    # 出力
    if args.format == "json":
        output_json(results)
    else:
        output_text(results)

    return 0


if __name__ == "__main__":
    sys.exit(main())
