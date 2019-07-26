from kueventparser import utils


def test_parse_time():
    case_in_1 = "12時10分～12時50分"
    case_in_2 = "17時30分～19時00分（17時00分受付開始）"
    case_in_3 = "15時00分～"
    import pytz
    import datetime as dt
    jst = pytz.timezone('Asia/Tokyo')

    case_out = {"start": dt.time(12, 10, tzinfo=jst),
                "end": dt.time(12, 50, tzinfo=jst)}
    assert utils.parse_str_to_time(case_in_1) == case_out

    case_out = {"start": dt.time(17, 30, tzinfo=jst),
                "end": dt.time(19, 0, tzinfo=jst)}
    assert utils.parse_str_to_time(case_in_2) == case_out

    case_out = {"start": dt.time(15, 0, tzinfo=jst),
                "end": dt.time(15, 0, tzinfo=jst)}
    assert utils.parse_str_to_time(case_in_3) == case_out


def test_parse_date():
    case_in_1 = "2019年08月08日 木曜日 〜 2019年08月09日 金曜日"
    case_in_2 = "2019年08月06日 火曜日"
    case_in_3 = "2019年07月31日 水曜日 〜 2019年11月03日 日曜日（祝日）"
    import datetime as dt

    case_out = {"start": dt.date(2019, 8, 8),
                "end": dt.date(2019, 8, 9)}
    assert utils.parse_str_to_date(case_in_1) == case_out

    case_out = {"start": dt.date(2019, 8, 6),
                "end": dt.date(2019, 8, 6)}
    assert utils.parse_str_to_date(case_in_2) == case_out

    case_out = {"start": dt.date(2019, 7, 31),
                "end": dt.date(2019, 11, 3)}
    assert utils.parse_str_to_date(case_in_3) == case_out


def test_url_to_soup():
    """url_to_soup のテスト

    今のところURLが取得できているかと, soupになるかしかみていない.
    (完全なものが取得できているかのテストはまだ)
    """
    from os import path

    from bs4 import BeautifulSoup
    url = "http://www.kyodaimap.net"
    uri = path.join(path.dirname(__file__), "data", "test_utils1.html")
    with open(uri, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    assert soup.title == utils.url_to_soup(url).title
