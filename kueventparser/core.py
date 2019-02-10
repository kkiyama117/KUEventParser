# -*- coding: utf-8 -*-
"""京大のイベント

京大の行事カレンダーから指定日のイベントを作成する.
"""
import datetime

from kueventparser.adapters.base import EventManagerMixin
from kueventparser.adapters.official import KUEventManager


def eventparser(manager: EventManagerMixin, *, date, year, month):
    """hook to call event list factory

    Args:
        manager: :obj:`kueventparser.events.EventManager` or :obj:`str`
        date(:obj:`datetime.date`): イベントを取得したい月.
        year (int): イベントを取得したい年.
            デフォルトは今年.(次の月でないことに注意)
        month (int): イベントを取得したい月.
            デフォルトは今月.

    Returns:
        list: list of event
    """
    if manager == 'official':
        _manager = KUEventManager
    elif isinstance(manager, EventManagerMixin):
        _manager = manager
    else:
        raise ValueError
    if date is not None:
        return event_list_factory(manager=_manager, date=date)
    elif year is not None:
        if month is not None:
            return event_list_factory(manager=_manager, year=year, month=month)
    return event_list_factory(manager=_manager)


def event_list_factory(*, manager: KUEventManager = None,
                       year: int = datetime.date.today().year,
                       month: int = datetime.date.today().month,
                       date: datetime.date = None, **kargs):
    """月ごとのイベントのリストを作る

    Args:
        manager(:obj:`kueventparser.events.KUEventManager`):
        date(:obj:`datetime.date`): イベントを取得したい月. 日付は無視される.
        year (int): イベントを取得したい年.
            デフォルトは今年.(次の月でないことに注意)

        month (int): イベントを取得したい月.
            デフォルトは今月.

    Returns:
        list: list of `Event` (HTML取得に失敗した時はStopIteration例外)
    """

    # datetimeを渡されたとき
    if date is not None:
        _date = date
    # 12月以外なら
    elif month is not None:
        _date = datetime.date(year, month, 1)
    else:
        raise ValueError
    # 月の全てのイベントを日ごとに取得
    events = manager.get_events(_date)
    return events
