# -*- coding: utf-8 -*-
"""event-parser api

APIを規定.
各APIは他のAPIまたは `core` の関数を呼び出す.
api.pyをスクリプトとして利用すると今月のイベント名一覧が得られる.
eventそのものを得たい場合,以下の関数を利用する.

Example:

    >>> get_events()
    []

詳細は各関数のdocstringを参照.
"""
from . import core


def get_events(manager='official', *, date=None, year: int = None,
               month: int = None) -> list:
    """Construscts and return an list of Class `Event`.

    hookを呼び出す.

    Args:
        manager : `Event` の取得用マネージャ 今のところ,京大公式HP用のみ.
            "official" のみ使用可能.
        date (:obj:`datetime`, optional): 欲しいイベントのdatetime.
            `month` , `year` とどちらかを選択.両方指定した場合,こちらが優先される.
        year (int, optional): イベントを取得する年.
            両方指定した場合, `date` が優先される.
        month (int, optional): イベントを取得する月.
            両方指定した場合, `date` が優先される.

    Returns:
        list: list of :obj:`kueventparser.events.Event`
    """
    return core.eventparser(manager=manager, date=date, year=year, month=month)
