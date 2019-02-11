# -*- coding: utf-8 -*-
import datetime

import bs4

from kueventparser.adapters.base import EventFactoryMixin
from kueventparser.events import Event
from kueventparser.utils import url_to_soup, parse_str_to_time


class OfficialEventFactory(EventFactoryMixin):
    """イベントの管理クラス

    後ほど京大公式以外のHPからスクレイビングする時は,
    このクラスの関数にHP毎の処理を追加する.
    """

    @classmethod
    def get_events(cls, date):
        events = []
        for day, urls in cls._get_events_urls(date).items():
            for url in urls:
                # make event instance
                events.append(cls._get_event(url=url, date=datetime.date(date.year, date.month, day)))
        return events

    @staticmethod
    def _get_events_urls(date: datetime.date) -> dict:
        """京大の行事カレンダーから指定した月のイベントURLリストを作成する

        Args:
            date : 取得するイベントの日付

        Returns:
            指定のイベントURL (HTML取得に失敗した時はNoneが返ってくる)
        """
        # template of kyoto univ offical event calender
        template = "http://www.kyoto-u.ac.jp/ja/social/event/" \
                   "calendar/?year={0}&month={1}"
        url = template.format(date.year, date.month)
        # get beautifulsoup object from url
        soup = url_to_soup(url)
        urls = {}
        # get event data from table in HTML
        for td_day in soup.find_all("td", class_="event_of_day"):
            day = int(td_day.parent.find(class_="day").string.strip())
            urls[day] = []
            for e in td_day.find_all("a"):
                if e.get("href") is not None:
                    urls[day].append(e.get("href"))
        return urls

    @classmethod
    def _get_event(cls, url: str, date: datetime.date) -> Event:
        """日付とURLからイベントを作る.

        日付を引数に取るのは,HPの日付の表記がバラバラすぎるため.

        Args:
            url: URL
            date: 取得するイベントの日付

        Returns:
            Event: Event class

        """

        soup = url_to_soup(url)
        # リストに実際のイベントの情報を取り込む
        title = soup.find(
            "h1", class_="title").stripped_strings.__next__()
        location = cls.__find_location(soup)
        description = cls.__find_description(soup)
        time_data = parse_str_to_time(cls.__find_time(soup))
        start = time_data["start"]
        end = time_data["end"]

        # create event instance
        event = Event(title=title, url=url, location=location,
                      description=description, date=date, start=start, end=end)
        return event

    @staticmethod
    def __find_location(elem):
        """HTML要素から場所名を抽出する

        HTMLをBeautifulSoupでパースしてできたTagオブジェクトから
        場所名の記述を抽出し文字列で返す

        Args:
           elem(:obj:bs4.element.Tag): HTML要素

        Returns:
            str: 場所名
        """

        location = ""
        for string in elem.find(string="開催地") \
                .find_next("span").stripped_strings:
            # 構内マップが出てきたらそれ以降は除く
            if "マップ" in string:
                break
            # それ以外
            location += string
        return location

    @staticmethod
    def __find_description(elem):
        """HTML要素から場所名を抽出する

        HTMLをBeautifulSoupでパースしてできたTagオブジェクトから
        場所名の記述を抽出し文字列で返す

        Args:
            elem(:obj:bs4.element.Tag): HTML要素

        Returns:
            str: イベント詳細
        """
        description = ""
        for string in elem.find(string="要旨") \
                .find_next("span").stripped_strings:
            description += string
            description += "\n"
        return description

    @staticmethod
    def __find_time(elem: bs4.element.Tag):
        """HTML要素から時間を抽出する

        HTMLをBeautifulSoupでパースしてできたTagオブジェクトから
        時間の記述を抽出し文字列で返す

        Args:
            elem(:obj:`bs4.element.Tag`): HTML要素

        Returns:
            str: 開催時間
        """
        time = ""
        for string in elem.find(string="時間") \
                .find_next("span").stripped_strings:
            time += string
        return time
