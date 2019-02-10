#! /usr/bin/python
# -*- coding: utf-8 -*-

from . import api


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
    for event in api.get_events(manager=args.manager):
        print(event)


if __name__ == '__main__':
    main()
