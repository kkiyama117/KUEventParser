#!python3
# -*- coding: utf-8 -*-

"""京大のイベント

京大の行事カレンダーから指定日のイベントを作成する.
"""
import datetime

from kueventparser.adapters.base import EventFactoryMixin
from kueventparser.adapters.official import OfficialEventFactory


def prepare(factory, method, **kwargs):
    """ select kwargs

    Args:
        factory:
        method:
        **kwargs:

    Returns:

    """
    _factory = select_factory(factory)
    if method is 'get_all':
        _kwargs: dict = select_date(**kwargs)
    elif method is 'get':
        _kwargs: dict = {'url': kwargs.get('url')}

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
    return getattr(_factory, _method)(**_kwargs)


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
        dict:  (HTML取得に失敗した時はStopIteration例外)
    """
    year = kwargs.get('year', None)
    month = kwargs.get('month', None)
    if year is not None and month is not None:
        kwargs.setdefault("date", datetime.date(year, month, 1))
    else:
        kwargs.setdefault("date", datetime.date.today())
    _kwargs = {"date": kwargs.get("date")}
    return _kwargs


def main():
    """スクリプトとして実行したとき,実際に実行される関数

    `argparse` を用いた.
    """
    import argparse

    # templates
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('factory', default='official', nargs='?',
                               const="official", type=str, choices=None,
                               action='store',
                               help="Manager for parsing Events from any homepages 'official' etc",
                               metavar=None)
    # main parser
    parser = argparse.ArgumentParser(
        description='event parser of kyoto Univ.',
        epilog="For detail, see github, sphinx and source code",
        parents=[parent_parser]
    )
    # sub commands
    # `get` or `get_all`
    subparsers = parser.add_subparsers(dest="method", help='sub-commands. for detail, see "subcommand -h".',
                                       title='commands')
    # GET
    get_parser = subparsers.add_parser("get")
    get_parser.set_defaults(method="get")
    get_parser.add_argument('--url', '-u', type=str, action='store', required=True,
                            help="url for event", metavar='url')
    # GET_ALL
    get_all_parser = subparsers.add_parser("get_all")
    get_all_parser.set_defaults(method="get_all")
    get_all_parser.add_argument('--year', '-y', type=int, action='store', dest="year",
                                help="year for get_events")
    get_all_parser.add_argument('--month', '-m', type=int, action='store', dest="month",
                                help="month for get_events")

    args = parser.parse_args()
    kwargs = vars(args)
    # call event_parser
    # print(kwargs)
    if args.method is 'get':
        print(event_parser(**kwargs))
    else:
        for event in event_parser(**kwargs):
            print(event)


if __name__ == '__main__':
    main()
