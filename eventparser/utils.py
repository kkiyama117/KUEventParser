#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime as dt
import re
import sys

import nkf
import pytz
import requests


def cleanup_html(html):
    """htmlから余計な要素を除去する

    BeautifulSoupオブジェクトを作る前にhtmlを綺麗にするのに用いる
    :param str html: HTML文字列
    :return: 整形済HTML文字列
    :rtype: str
    """
    LEFT_SPACE = re.compile(r'\s+<')
    RIGHT_SPACE = re.compile(r'>\s+')
    SCRIPT_TAG = re.compile(r'<script[^>]*>.*?</script>')
    COMMENT = re.compile(r'<!--[\s\S]*?-->')

    # 改行を除去
    html = html.replace('\n', '')
    # 変更 '<' -> '< '
    html = LEFT_SPACE.sub(lambda t: '<', html)
    # 変更 '>' -> '> '
    html = RIGHT_SPACE.sub(lambda t: '>', html)
    # scriptタグを除去
    html = SCRIPT_TAG.sub(lambda t: '', html)
    # コメントの除去
    html = COMMENT.sub(lambda t: '', html)

    return html


def get_html(url):
    """引数のURLのページのHTMLソースを取得して文字列として返す

    HTML取得失敗時にはrequests.exceptions.RequestExceptionを投げる
    :param str url: 対象ページのURL
    :return: 対象ページのHTML文字列
    :rtype: str
    """
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        raise

    # UTF-8に変換
    html = nkf.nkf("-w", r.content).decode('utf-8')
    # HTMLを整形
    html = cleanup_html(html)

    return html


def parse_datetime(date_text):
    """京大イベントページで見られる形式の日時文字列をdatetimeに変換する

    :param str date_text: 日時文字列
    :return: 開始, 終了日時のdatetimeを格納した辞書
             {"start": <開始日時>, "end": <終了日時>}
             パターンにマッチしなければNoneを返す
    :rtype: dict
    """
    pattern = (r'(平成)?(?P<year>\d+)年(?P<month>\d+)月(?P<day>\d+)日'
               r'(.*?(?P<hour_start>\d+)時(?P<minute_start>\d+)分'
               r'(.*?～.*?(?P<hour_end>\d+)時(?P<minute_end>\d+))?)?')

    match = re.match(pattern, date_text)
    if match is None:
        # パターンにマッチしなければNoneを返す
        return None

    jst = pytz.timezone('Asia/Tokyo')
    now = dt.now(tz=jst)

    if match.group('year') is not None:
        year = int(match.group('year'))
        if len(match.group('year')) == 2:
            # 年号が二桁(平成表記)であれば西暦に変換
            year = year + 1988
    else:
        # マッチしなければ現在時刻で代替
        year = now.year

    if match.group('month') is not None:
        month = int(match.group('month'))
    else:
        # マッチしなければ現在時刻で代替
        month = now.month

    if match.group('day') is not None:
        day = int(match.group('day'))
    else:
        # マッチしなければ現在時刻で代替
        day = now.day

    if match.group('hour_start') is not None:
        hour_start = int(match.group('hour_start'))
    else:
        # マッチしなければ現在時刻で代替
        hour_start = now.hour

    if match.group('minute_start') is not None:
        minute_start = int(match.group('minute_start'))
    else:
        # マッチしなければ現在時刻で代替
        minute_start = now.hour

    if match.group('hour_end') is not None:
        hour_end = int(match.group('hour_end'))
    elif match.group('hour_start') is not None:
        # マッチしなければ開始時刻で代替
        hour_end = hour_start
    else:
        # 開始時刻も無ければ現在時刻で代替
        hour_end = now.hour

    if match.group('minute_end') is not None:
        minute_end = int(match.group('minute_end'))
    elif match.group('minute_start') is not None:
        # マッチしなければ開始時刻で代替
        minute_end = minute_start
    else:
        # 開始時刻も無ければ現在時刻で代替
        minute_end = now.hour

    # 抽出結果からそれぞれのdatetimeオブジェクトを生成
    # タイムゾーンは'Asia/Tokyo'を用いる
    start = dt(year, month, day, hour_start, minute_start, tzinfo=jst)
    end = dt(year, month, day, hour_end, minute_end, tzinfo=jst)

    # 辞書に格納して返す
    return {'start': start, 'end': end}


def print_event(event, stream=sys.stdout):
    """イベント情報の入った dict を綺麗に出力する

    :param dict event: イベント情報
    """
    def recursive(obj, level=0, indent=2):
        if isinstance(obj, dict):
            stream.write('\n')
            for key, value in obj.iteritems():
                stream.write(' ' * indent * level + '"' + key + '": ')
                recursive(value, level=level + 1, indent=indent)
        elif isinstance(obj, (str, unicode,)):
            stream.write(('"' + obj + '"').encode('utf-8'))
        elif isinstance(obj, dt):
            stream.write(str(obj).encode('utf-8'))
        stream.write('\n')

    recursive(event)