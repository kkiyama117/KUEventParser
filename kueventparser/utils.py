# -*- coding: utf-8 -*-
"""雑多な流用可能な関数群

主にbeautifulsoup4周りの物が多い.
"""

import datetime
import re

import pytz
import requests
from bs4 import BeautifulSoup


def url_to_soup(url: str) -> BeautifulSoup:
    """URLからBeautifulSoupのオブジェクトを作る

    Args:
        url(str): 変換したいURL

    Returns:
        :obj:`bs4.BeautifulSoup` : BeautifulSoupのオブジェクト

    """
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    return soup


def parse_str_to_time(time_text: str):
    """京大イベントページで見られる形式の時刻文字列をdatetimeに変換する

    'n時m分～k時l分' の形をとるものを処理する.

    Args:
        time_text(str): 時刻文字列

    Returns:
        dict: 開始, 終了時刻の `datetime.time` を格納した辞書

    {"start": :obj:`datetime.time` , "end": :obj:`datetime.time` }

    Raises:
        ValueError: `time_text` が正規表現にマッチしない場合.
    """
    pattern = (r'.*?(?P<hour_start>\d+)時(?P<minute_start>\d+)分～'
               r'.*?(?P<hour_end>\d+)時(?P<minute_end>\d+)分'
               )
    pattern2 = (r'.*?(?P<hour_start>\d+)時(?P<minute_start>\d+)分'
                )

    match = re.match(pattern, time_text)
    match2 = re.match(pattern2, time_text)
    if match is None:
        # パターン1に合わなかったらパターン2を使う
        match = match2
    elif match2 is None:
        # パターンにマッチしなければ例外を返す
        raise ValueError
    jst = pytz.timezone('Asia/Tokyo')
    hour_start = int(match.group('hour_start'))
    minute_start = int(match.group('minute_start'))
    if match is match2:
        hour_end = hour_start
        minute_end = minute_start
    else:
        hour_end = int(match.group('hour_end'))
        minute_end = int(match.group('minute_end'))
    # 抽出結果からそれぞれのdatetimeオブジェクトを生成
    # タイムゾーンは'Asia/Tokyo'を用いる
    start = datetime.time(hour_start, minute_start, tzinfo=jst)
    end = datetime.time(hour_end, minute_end, tzinfo=jst)
    # 辞書に格納して返す
    return {'start': start, 'end': end}


def parse_str_to_date(date_text: str):
    """京大イベントページで見られる形式の文字列をdatetimeに変換する

    'n時m分～k時l分' の形をとるものを処理する.

    Args:
        date_text(str): 時刻文字列

    Returns:
        dict: 開始, 終了時刻の `datetime.time` を格納した辞書

    {"start": :obj:`datetime.time` , "end": :obj:`datetime.time` }

    Raises:
        ValueError: `time_text` が正規表現にマッチしない場合.
    """
    # 2019年06月04日 火曜日 〜 2019年07月16日 火曜日
    pattern = (r'.*?(?P<year_start>\d+)年(?P<month_start>\d+)月(?P<day_start>\d+)日.*?〜'
               r'.*?(?P<year_end>\d+)年(?P<month_end>\d+)月(?P<day_end>\d+)日.*?'
               )
    pattern2 = (r'.*?(?P<year_start>\d+)年(?P<month_start>\d+)月(?P<day_start>\d+)日 *?'
                )

    match = re.match(pattern, date_text)
    match2 = re.match(pattern2, date_text)
    if match is None:
        # パターン1に合わなかったらパターン2を使う
        match = match2
    elif match2 is None:
        # パターンにマッチしなければ例外を返す
        raise ValueError
    year_start = int(match.group('year_start'))
    month_start = int(match.group('month_start'))
    day_start = int(match.group('day_start'))
    if match is match2:
        year_end = year_start
        month_end = month_start
        day_end = day_start
    else:
        year_end = int(match.group('year_end'))
        month_end = int(match.group('month_end'))
        day_end = int(match.group('day_end'))
    # 抽出結果からそれぞれのdatetimeオブジェクトを生成
    # タイムゾーンは'Asia/Tokyo'を用いる
    start = datetime.date(year=year_start, month=month_start, day=day_start)
    end = datetime.date(year_end, month_end, day_end)
    # 辞書に格納して返す
    return {'start': start, 'end': end}
