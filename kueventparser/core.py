#!python3
# -*- coding: utf-8 -*-

"""京大のイベント

京大の行事カレンダーから指定日のイベントを作成する.
"""
import datetime

from kueventparser.adapters.base import EventFactoryMixin
from kueventparser.adapters.official import OfficialEventFactory


def select_factory(factory):
    """Choose EventFactory class

    param: factory: str or Class of EventFactory
    return: Class of EventFactory
    """
    if type(factory) is str:
        if factory == 'official':
            return OfficialEventFactory
    elif isinstance(factory, EventFactoryMixin):
        return factory
    else:
        raise ValueError


def select_date(**kwargs):
    """select date from kwargs

    Args:
        date (:obj:`datetime`, optional): 欲しいイベントのdatetime.
            `month` , `year` とどちらかを選択.両方指定した場合,こちらが優先される.
        year (int, optional): イベントを取得する年.
            両方指定した場合, `date` が優先される.
        month (int, optional): イベントを取得する月.
            両方指定した場合, `date` が優先される

    Returns:
        list: list of event (HTML取得に失敗した時はStopIteration例外)
    """
    date = kwargs.get('data', None)
    year = kwargs.get('year', None)
    month = kwargs.get('month', None)
    if (date is not None) and type(date) is datetime.date:
        return date
    elif year is not None and month is not None:
        return datetime.date(year, month, 1)
    else:
        return datetime.date.today()


def event_parser(factory, **kwargs):
    """hook to call event list factory
    月ごとのイベントのリストを作る

    Args:
        factory: :obj:`kueventparser.events.EventManager` or :obj:`str`
        date (:obj:`datetime`, optional): 欲しいイベントのdatetime.
            `month` , `year` とどちらかを選択.両方指定した場合,こちらが優先される.
        year (int, optional): イベントを取得する年.
            両方指定した場合, `date` が優先される.
        month (int, optional): イベントを取得する月.
            両方指定した場合, `date` が優先される

    Returns:
        list: list of event (HTML取得に失敗した時はStopIteration例外)
    """
    _factory = select_factory(factory)
    _date = select_date(**kwargs)
    return _factory.get_all(_date)


def main():
    """スクリプトとして実行したとき,実際に実行される関数

    `argparse` を用いた.
    `get` を呼び出すだけ.
    """
    import argparse

    parser = argparse.ArgumentParser(description='event parser of kyoto Univ.')
    parser.add_argument('manager', default='official', nargs='?',
                        const="official", type=str, choices=None,
                        action='store',
                        help="Manager for parsing Events from any homepages 'official' etc",
                        metavar=None)
    args = parser.parse_args()
    for event in event_parser(factory=args.manager):
        print(event)


if __name__ == '__main__':
    main()
