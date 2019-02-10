""" 'obj:kueventparser.events' のテスト
"""
from os import path

from kueventparser import events
from tests import conftest


class Test_KUEventManager:
    """ 'obj:kueventparser.events.KUEventManager' のテスト
    """

    def test_get_events_urls(self):
        from datetime import date
        # uri
        uri = path.join(path.dirname(__file__), "data",
                        "test_eventsmanager1.txt")
        # 予想結果
        assert_urls = []
        # 予想結果の準備
        with open(uri, encoding="utf-8") as f:
            data = f.read()
        lines = data.split('\n')
        for line in lines:
            assert_urls.append(line)
        # assertion
        foo = date(2018, 1, 1)
        eve = events.KUEventManager._get_events_urls(foo)
        assert assert_urls == eve[1]

    def test_get_event(self):
        from datetime import date
        # assert の準備
        uri = path.join(path.dirname(__file__),
                        "data",
                        "test_event1.xml")
        assert_event = conftest.make_test_event(uri)
        # event
        event = events.KUEventManager._get_event(url=
                                                 "http://www.kyoto-u.ac.jp/ja/"
                                                 "social/events_news/department"
                                                 "/yasei/events/2017/"
                                                 "171030_2140.html",
                                                 date=date(2018, 1, 1))
        # 何故か is が使えないのでクラスの定義から直接判別する.
        assert assert_event.__eq__(event)
