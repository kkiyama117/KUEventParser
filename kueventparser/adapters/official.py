import calendar
import datetime
import re
from itertools import chain
from typing import Optional

import bs4

from kueventparser.adapters.base import EventFactoryMixin
from kueventparser.events import Event
from kueventparser.utils import url_to_soup, parse_str_to_time, parse_str_to_date


class OfficialEventFactory(EventFactoryMixin):
    """イベントの管理クラス
    """
    # template of kyoto univ official event calender
    _template = "http://www.kyoto-u.ac.jp/ja/social/event/" \
                "calendar/?year={0}&month={1}"
    _event_urls = []

    @classmethod
    def get(cls, url: str):
        date = datetime.date.today()
        return cls._get_event(url=url)

    @classmethod
    def get_all(cls, start_date: datetime.date, end_date: datetime.date):
        """ get events in month containing date

        Args:
            start_date (datetime.date): date to get events including year and month
            end_date (datetime.date): date to get events including year and month

        Returns:
            list: `events.Event'
        """
        return list(cls.generate_all(start_date, end_date))

    @classmethod
    def generate_all(cls, start_date: datetime.date, end_date: datetime.date):
        url = cls._template.format(start_date.year, start_date.month)
        # get beautifulsoup object from url
        session = url_to_soup(url)
        # return values
        answer = []
        # TODO: python3.8 PEP572
        for _url in cls._get_events_urls(start_date, end_date, session):
            event = cls._get_event(url=_url)
            if event is not None:
                answer.append(event)
        return answer

    @classmethod
    def _get_events_urls(cls, start, end: datetime.date, session=None):
        urls = None
        for n in range((end - start).days):
            day = start + datetime.timedelta(n)
            _url = cls._get_events_url_daily(day, session=session)
            if urls is None:
                urls = _url
            else:
                urls = chain(urls, _url)
        yield from tuple(urls)

    @classmethod
    def _get_events_url_daily(cls, date: datetime.date, session=None):
        """京大の行事カレンダーから指定した月のイベントURLリストを作成する

        Args:
            date : 取得するイベントの月(日付は参照されない)

        Returns:
            指定のイベントURL (HTML取得に失敗した時はNoneが返ってくる)
        """
        url = cls._template.format(date.year, date.month)
        # get beautifulsoup object from url or given args
        soup = url_to_soup(url) if session is None else session
        # get event data from table in HTML
        td_day = soup.find('td', class_='day', text=re.compile(str(date.day)))
        for e in td_day.parent.find(class_='event_of_day').find_all('a'):
            url = e.get('href')
            if url is not None:
                yield url

    @classmethod
    def _get_event(cls, url: str) -> Optional[Event]:
        """日付とURLからイベントを作る.

        日付を引数に取るのは,HPの日付の表記がバラバラすぎるため.

        Args:
            url: URL

        Returns:
            Event: Event class

        """

        soup = url_to_soup(url)
        # リストに実際のイベントの情報を取り込む
        title = soup.find(
            "h1", class_="title").stripped_strings.__next__()
        try:
            location = cls.__find_location(soup)
            description = cls.__find_description(soup)
            date_data = parse_str_to_date(cls.__find_date(soup))
            time_data = parse_str_to_time(cls.__find_time(soup))
            start_ = date_data.get('start')
            end_ = date_data.get('end')
            start = time_data.get('start')
            end = time_data.get('end')
        except AttributeError:
            return None

        # create event instance
        event = Event(title=title, url=url, location=location,
                      description=description, start_date=start_, end_date=end_, start=start, end=end)
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

    @staticmethod
    def __find_date(elem: bs4.element.Tag):
        """HTML要素から時間を抽出する

        HTMLをBeautifulSoupでパースしてできたTagオブジェクトから
        時間の記述を抽出し文字列で返す

        Args:
            elem(:obj:`bs4.element.Tag`): HTML要素

        Returns:
            str: 開催時間
        """
        item = None
        for item in elem.find(string="開催日").parent.parent.parent.stripped_strings:
            pass
        return item
