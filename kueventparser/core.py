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
    """
    import argparse

    # templates
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('manager', default='official', nargs='?',
                               const="official", type=str, choices=None,
                               action='store',
                               help="Manager for parsing Events from any homepages 'official' etc",
                               metavar=None)

    # args for get_all
    get_all_parser_mixin = argparse.ArgumentParser(add_help=False)
    get_all_parser_mixin.add_argument('--year', '-y', type=int, action='store',
                                      help="year for get_events (only used in `get_all`)")
    get_all_parser_mixin.add_argument('--month', '-m', type=int, action='store',
                                      help="month for get_events (only used in `get_all`)")

    # main parser
    parser = argparse.ArgumentParser(
        description='event parser of kyoto Univ.',
        epilog="For detail, see github, sphinx and source code",
        parents=[parent_parser, get_all_parser_mixin]
    )

    # main parser args
    parser.add_argument('method', default='get_all', nargs='?',
                        const="get_all", type=str, choices=None,
                        action='store',
                        help="method for parsing Event. 'get', 'get_all' etc",
                        metavar=None)
    # args for get
    parser.add_argument('--url', '-u', type=str, action='store',
                        help="url for event (only used in `get`, required if `method` is 'get')")

    # sub commands
    # `get` or `get_all`
    subparsers = parser.add_subparsers(dest="commands", help='sub-commands. for detail, see "subcommand -h".',
                                       title='commands')

    # GET
    get_parser = subparsers.add_parser("get", parents=[parent_parser])
    get_parser.set_defaults(method="get")
    get_parser.add_argument('url', type=str, action='store',
                            help="url for event")

    get_all_parser = subparsers.add_parser("get_all", parents=[parent_parser, get_all_parser_mixin])
    get_all_parser.set_defaults(method="get_all")

    args = parser.parse_args()

    kwargs = {}
    # call event_parser
    # for event in event_parser(factory=args.manager, method=args.method, kwargs=kwargs):
    #     print(event)
    print(args)


if __name__ == '__main__':
    main()
