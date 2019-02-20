# -*- coding: utf-8 -*-
"""event-parser api

APIを規定.
各APIは他のAPIまたは `core` の関数を呼び出す.
api.pyをスクリプトとして利用すると今月のイベント名一覧が得られる.
eventそのものを得たい場合,以下の関数を利用する.

Example:

    >>> from kueventparser import api
    >>> api.get_all()
    []

詳細は各関数のdocstringを参照.
"""

from .core import event_parser


def kueventparser(factory, method, **kwargs):
    return event_parser(factory, method, **kwargs)


def get_all(factory='official', **kwargs):
    """Construct and return an list of Class `Event`.

    hookを呼び出す.

    Args:
        factory: `Event` の取得用マネージャ 今のところ,京大公式HP用のみ.
            EventFactoryMixin classを継承したクラスか 'official' に対応
        date (:obj:`datetime`, optional): 欲しいイベントのdatetime.
            `month` , `year` とどちらかを選択.両方指定した場合,こちらが優先される.
        year (int, optional): イベントを取得する年.
            両方指定した場合, `date` が優先される.
        month (int, optional): イベントを取得する月.
            両方指定した場合, `date` が優先される.

    Returns:
        generator of Events
    """
    return kueventparser(factory=factory, method='get_all', **kwargs)


def get(factory='official', **kwargs):
    """Construct and return an list of Class `Event`.

    hookを呼び出す.

    Args:
        factory: `Event` の取得用マネージャ 今のところ,京大公式HP用のみ.
            EventFactoryMixin classを継承したクラスか 'official' に対応
        url: url of event

    Returns:
        :obj:`kueventparser.events.Event`: Event
    """
    return kueventparser(factory=factory, method='get', **kwargs)
