#!python3
# -*- coding: utf-8 -*-

"""京大のイベント

京大の行事カレンダーから指定日のイベントを作成する.
"""
import datetime

from kueventparser.adapters.base import EventFactoryMixin
from kueventparser.adapters.official import OfficialEventFactory


def prepare(factory, method, **kwargs):
    _factory = select_factory(factory)
    _kwargs = select_date(**kwargs)
    return _factory, method, _kwargs


def event_parser(factory, method: str, **kwargs):
    """hook to call event list factory

    call any function

    Args:
        factory: :obj:`kueventparser.events.EventManager` or :obj:`str`
        method (str): 取得の仕方. 'get' or 'get_all'
        kwargs (dict): kwargs for method selected by args
            date or (year and month) ... get_all method
            url ... get

    Returns:
        method selected by args
    """
    _factory, _method, _kwargs = prepare(factory, method, **kwargs)
    return getattr(_factory, _method)(_kwargs)


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
    date = kwargs.get('date', None)
    year = kwargs.get('year', None)
    month = kwargs.get('month', None)
    if (date is not None) and type(date) is datetime.date:
        return date
    elif year is not None and month is not None:
        return datetime.date(year, month, 1)
    else:
        return datetime.date.today()


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
    parser.add_argument('method', default='get_all', nargs='?',
                        const="get_all", type=str, choices=None,
                        action='store',
                        help="method for parsing Event. 'get', 'get_all' etc",
                        metavar=None)
    args = parser.parse_args()
    # call event_parser
    for event in event_parser(factory=args.manager, method=args.method):
        print(event)


if __name__ == '__main__':
    main()
