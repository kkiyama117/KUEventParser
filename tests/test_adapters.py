""" 'obj:kueventparser.events' のテスト
"""
from os import path

from kueventparser.adapters.official import OfficialEventFactory
from tests import conftest


class TestKUEventManager:
    """ 'obj:kueventparser.events.OfficialEventFactory' のテスト
    """

    def test_get_event(self):
        from datetime import date
        # assert の準備
        uri = path.join(path.dirname(__file__),
                        "data",
                        "test_event1.xml")
        assert_event = conftest.make_test_event(uri)
        # event
        event = OfficialEventFactory._get_event(url="http://www.kyoto-u.ac.jp/ja/"
                                                "social/events_news/department"
                                                "/yasei/events/2017/"
                                                "171030_2140.html",
                                                date=date(2018, 1, 1))
        # 何故か is が使えないのでクラスの定義から直接判別する.
        assert assert_event.__eq__(event)
