# -*- coding: utf-8 -*-
import datetime
from abc import ABCMeta, abstractmethod

from kueventparser.events import Event


class EventFactoryMixin(metaclass=ABCMeta):
    """イベントの管理クラス

    後ほど京大公式以外のHPからスクレイビングする時は,
    このクラスの関数にHP毎の処理を追加する.
    """

    @classmethod
    @abstractmethod
    def get_all(cls, date) -> list:
        return []

    @classmethod
    @abstractmethod
    def get(cls, url) -> list:
        return []

    @staticmethod
    @abstractmethod
    def _get_events_urls(date: datetime.date) -> dict:
        """京大の行事カレンダーから指定した月のイベントURLリストを作成する

        Args:
            date : 取得するイベントの日付

        Returns:
            指定のイベントURL (HTML取得に失敗した時はNoneが返ってくる)
        """
        return {}

    @classmethod
    @abstractmethod
    def _get_event(cls, url: str, date: datetime.date) -> Event:
        """日付とURLからイベントを作る.

        日付を引数に取るのは,HPの日付の表記がバラバラすぎるため.

        Args:
            url: URL
            date: 取得するイベントの日付

        Returns:
            Event: Event class

        """
        return Event(title="", url=url, location="", description="",
                     date=date, start=datetime.time(0, 0, 0), end=datetime.time(0, 0, 1))
