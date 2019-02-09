# -*- coding: utf-8 -*-

from src.api import get_events


def main():
    """スクリプトとして実行したとき,実際に実行される関数

    `argparse` を用いた.
    `get_events` を呼び出すだけ.
    """
    import argparse

    parser = argparse.ArgumentParser(description='event parser of kyoto Univ.')
    parser.add_argument('manager', default='official', nargs='?',
                        const="official", type=str, choices=None,
                        action='store',
                        help="Manager for parsing Events from any homepages ",
                        metavar=None)
    args = parser.parse_args()
    for event in get_events(manager=args.manager):
        print(event)


if __name__ == '__main__':
    main()
