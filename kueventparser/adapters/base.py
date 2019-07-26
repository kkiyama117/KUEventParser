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
