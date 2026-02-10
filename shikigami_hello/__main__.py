#!/usr/bin/env python3
"""
shikigami_hello - シンプルな挨拶CLIアプリケーション

使い方:
    python -m shikigami_hello
    python -m shikigami_hello --name Alice
    python -m shikigami_hello -n Bob
"""

import argparse


def main():
    """メインエントリーポイント"""
    parser = argparse.ArgumentParser(
        description='shikigami_hello - シンプルな挨拶CLIアプリケーション',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用例:
  python -m shikigami_hello           Hello, world と出力
  python -m shikigami_hello --name Alice    Hello, Alice と出力
  python -m shikigami_hello -n Bob          Hello, Bob と出力
        '''
    )

    parser.add_argument(
        '-n', '--name',
        dest='name',
        default='world',
        help='挨拶の対象となる名前（デフォルト: world）'
    )

    args = parser.parse_args()

    print(f'Hello, {args.name}')


if __name__ == '__main__':
    main()
