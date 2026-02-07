#!/usr/bin/env python3
"""shikigami_dice_verify2 - メインエントリーポイント

シンプルなサイコロCLIアプリケーション。
ランダムな1-6の値を指定回数分出力します。
"""

import argparse
import random
import sys


def roll_dice(num_rolls: int, seed: int | None = None) -> list[int]:
    """サイコロを振る

    Args:
        num_rolls: 振る回数
        seed: 乱数シード（省略時はランダム）

    Returns:
        サイコロの結果リスト（各要素は1-6）
    """
    if seed is not None:
        random.seed(seed)
    return [random.randint(1, 6) for _ in range(num_rolls)]


def parse_args() -> argparse.Namespace:
    """コマンドライン引数をパース

    Returns:
        パースされた引数
    """
    parser = argparse.ArgumentParser(
        description="シンプルなサイコロCLIアプリケーション",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python -m shikigami_dice_verify2           # 1回振る
  python -m shikigami_dice_verify2 --rolls 3 # 3回振る
  python -m shikigami_dice_verify2 --seed 42 --rolls 2  # シード付きで2回
        """
    )
    parser.add_argument(
        "--rolls",
        type=int,
        default=1,
        help="振る回数（デフォルト: 1）"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="乱数シード（指定すると再現性があります）"
    )
    return parser.parse_args()


def main() -> int:
    """メイン関数

    Returns:
        終了コード（0: 成功, 2: エラー）
    """
    args = parse_args()

    # バリデーション: rolls は 1 以上
    if args.rolls < 1:
        print(f"エラー: --rolls は1以上の整数を指定してください（指定値: {args.rolls}）", file=sys.stderr)
        print("\n使い方:", file=sys.stderr)
        parse_args().print_help(file=sys.stderr)
        return 2

    # サイコロを振る
    results = roll_dice(args.rolls, args.seed)

    # 出力: スペース区切り
    print(" ".join(map(str, results)))

    return 0


if __name__ == "__main__":
    sys.exit(main())
