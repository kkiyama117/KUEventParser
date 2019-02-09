# content of conftest.py
from src import events


def make_test_event(uri: str, ) -> events.Event:
    """テスト用のEventクラス作成関数.

    Args:
        uri('str'): URI

    Returns:
        list: list for event
    """
    import datetime as dt
    import pytz
    from bs4 import BeautifulSoup

    # jst の設定
    jst = pytz.timezone('Asia/Tokyo')
    # soupでassertion用のデータを抜き出す.
    data_soup = BeautifulSoup(open(uri, encoding="utf-8"), "lxml-xml",
                              from_encoding="utf-8")
    title = data_soup.title.string
    url = data_soup.url.string
    location = data_soup.location.string
    date = dt.date(2018, 1, 1)
    start = dt.time(9, 0, tzinfo=jst)
    end = dt.time(21, 30, tzinfo=jst)
    description = ""
    for string in data_soup.description.stripped_strings:
        description += string
        description += "\n"
    # Eventの作成.
    event = events.Event(title=title, url=url, location=location,
                         description=description, date=date, start=start,
                         end=end)
    return event
