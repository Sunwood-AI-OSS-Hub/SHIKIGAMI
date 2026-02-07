"""
shikigami_dice_ci CLI メインモジュール

サイコロを振るCLIツールのエントリーポイント。
"""

import argparse
import random
import sys


def roll_dice(num_rolls: int, seed: int | None = None) -> list[int]:
    """
    サイコロを振る

    Args:
        num_rolls: 振る回数
        seed: 乱数シード（指定時は再現性あり）

    Returns:
        サイコロの結果リスト（1-6の整数）
    """
    if seed is not None:
        random.seed(seed)

    results = [random.randint(1, 6) for _ in range(num_rolls)]
    return results


def parse_args() -> argparse.Namespace:
    """
    コマンドライン引数を解析する

    Returns:
        解析済みの引数
    """
    parser = argparse.ArgumentParser(
        description="シンプルなサイコロCLIツール",
        epilog="使用例:\n  python -m shikigami_dice_ci\n  python -m shikigami_dice_ci --rolls 3\n  python -m shikigami_dice_ci --rolls 5 --seed 42",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--rolls",
        type=int,
        default=1,
        help="サイコロを振る回数（デフォルト: 1）",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="乱数シード（指定時は再現性あり）",
    )
    return parser.parse_args()


def main() -> None:
    """
    メイン関数
    """
    args = parse_args()

    # バリデーション: rolls >= 1
    if args.rolls < 1:
        print(
            f"エラー: --rolls は1以上の整数を指定してください（指定された値: {args.rolls}）",
            file=sys.stderr,
        )
        print("\n使用方法:", file=sys.stderr)
        print("  python -m shikigami_dice_ci [--rolls K] [--seed S]", file=sys.stderr)
        print("\nオプション:", file=sys.stderr)
        print("  --rolls K   サイコロを振る回数（デフォルト: 1）", file=sys.stderr)
        print("  --seed S    乱数シード（指定時は再現性あり）", file=sys.stderr)
        sys.exit(2)

    # サイコロを振る
    results = roll_dice(args.rolls, args.seed)

    # 結果を出力（スペース区切り）
    print(" ".join(map(str, results)))


if __name__ == "__main__":
    main()
