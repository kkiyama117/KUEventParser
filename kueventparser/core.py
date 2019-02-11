#!python3
# -*- coding: utf-8 -*-

"""京大のイベント

京大の行事カレンダーから指定日のイベントを作成する.
"""
import datetime

from kueventparser.adapters.base import EventFactoryMixin
from kueventparser.adapters.official import OfficialEventFactory

def selectparser(manager):
    pass

def eventparser(manager, **kwargs):
    """hook to call event list factory
    月ごとのイベントのリストを作る

    Args:
        manager: :obj:`kueventparser.events.EventManager` or :obj:`str`
        date (:obj:`datetime`, optional): 欲しいイベントのdatetime.
            `month` , `year` とどちらかを選択.両方指定した場合,こちらが優先される.
        year (int, optional): イベントを取得する年.
            両方指定した場合, `date` が優先される.
        month (int, optional): イベントを取得する月.
            両方指定した場合, `date` が優先される

    Returns:
        list: list of event (HTML取得に失敗した時はStopIteration例外)
    """
    date = kwargs.get('data', datetime.date.today())
    year = kwargs.get('year', None)
    month = kwargs.get('month', None)
    if manager == 'official':
        _manager = OfficialEventFactory
    elif isinstance(manager, EventFactoryMixin):
        _manager = manager
    else:
        raise ValueError

    if (year is not None) and (month is not None):
        _date = datetime.date(year, month, 1)
    else:
        _date = date
    return _manager.get_events(_date)


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
    for event in eventparser(manager=args.manager):
        print(event)


if __name__ == '__main__':
    main()
