#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re
from urlparse import urljoin

from bs4 import BeautifulSoup

from eventparser.utils import get_html, parse_datetime


def _element2text(elem, url):
    """HTML要素を文字列に変換する

    HTMLをBeautifulSoupでパースしてできたTagオブジェクトを
    京大イベントページの構造に従って文字列に変換する
    :param bs4.element.Tag elem: HTML要素
    :param str url: ソースのURL (aタグの変換に用いる)
    :return: 結果文字列
    :rtype: str
    """
    def rec(e):
        """再帰呼出により階層構造のHTML要素を文字列に変換する

        引数のHTML要素をそのタグに応じて文字列に変換する. 子要素を持つ場合は
        それを引数に自身を再帰的に呼び出し, 子要素の変換結果を親要素のものに
        連結して返す. DOMツリーを深さ優先探索しながら文字列を生成している.
        :param bs4.element.Tag e: HTML要素
        :return: 結果文字列
        :rtype: str
        """
        # 結果文字列を初期化
        res = ""

        # タグ名を取得
        tag = e.name

        # タグの種類に応じて文字列への変換を行う
        if tag in ["p", "div", "tr"]:
            # p, div, tr タグ
            # 改行を結果に追加
            res += "\n"
            text = e.find(text=True, recursive=False)
            if text is not None:
                # テキストがあれば結果に追加
                res += text
            children = e.findChildren(recursive=False)
            if len(children) > 0:
                # 子要素を持つならば
                for child in children:
                    # 子要素の変換結果を追加
                    res += rec(child)
            return res
        elif tag[0] == "h":
            # h1~6 の見出しタグ
            res += "\n\n"
            text = e.find(text=True, recursive=False)
            if text is not None:
                # テキストがあれば整形して結果に追加
                if tag == "h2":
                    # h2 タグの時には見易さのために括弧を付加
                    # 京大ページでは日時, 場所等の項目名が h2 で書かれている
                    res += "【" + text + "】"
                else:
                    res += text
            children = e.findChildren(recursive=False)
            if len(children) > 0:
                # 子要素を持つならば
                for child in children:
                    # 子要素の変換結果を追加
                    res += rec(child)
            return res
        elif tag == "a":
            # a タグ
            text = e.find(text=True, recursive=False)
            if text is not None:
                # テキストがあれば結果に追加
                res += text
            children = e.findChildren(recursive=False)
            if len(children) > 0:
                # 子要素を持つならば
                for child in children:
                    # 子要素の変換結果を追加
                    res += rec(child)
            if e.get("href") is not None:
                href = urljoin(url, e.get("href"))
                if res == href:
                    # aタグで囲われたテキストがhrefの内容と同じURLの場合
                    res = href + " "
                else:
                    # aタグで囲われたテキストがURLでない場合
                    # hrefのURLを括弧で囲ってテキスト直後に追加
                    res += " (" + href + ")"
            return res
        elif tag in ["td", "th"]:
            # td, th タグ
            text = e.find(text=True, recursive=False)
            if text is not None:
                # テキストがあれば結果に追加
                res += text
            children = e.findChildren(recursive=False)
            if len(children) > 0:
                # 子要素を持つならば
                for child in children:
                    # 子要素の変換結果を追加
                    res += rec(child)
            # テーブルの列要素なので区切りの半角スペースを追加
            res += " "
            return res
        elif tag == "ul":
            # ul タグ
            # 改行を結果に追加
            res += "\n"
            children = e.findChildren(recursive=False)
            if len(children) > 0:
                # 子要素を持つならば
                for child in children:
                    # 子要素の変換結果をリスト項目の形で追加
                    res += "・" + rec(child) + "\n"
            return res
        elif tag == "img":
            # img タグ
            # 画像要素は変換をスキップしm 半角スペースとして返す
            res += " "
            return res
        else:
            # 上記以外のタグ
            text = e.find(text=True, recursive=False)
            if text is not None:
                # テキストがあれば結果に追加
                res += text
            children = e.findChildren(recursive=False)
            if len(children) > 0:
                # 子要素を持つならば
                for child in children:
                    # 子要素の変換結果を追加
                    res += rec(child)
            return res

    # HTML要素をテキストに変換
    text = rec(elem)
    # 末尾の空白文字を削除
    text = text.rstrip()
    # ソースへのリンクを追加
    text += '\n\n詳細: ' + url

    return text


def _find_location(elem):
    """HTML要素から場所名を抽出する

    HTMLをBeautifulSoupでパースしてできたTagオブジェクトから
    場所名の記述を抽出し文字列で返す
    :param bs4.element.Tag elem: HTML要素
    :return: 場所名
    :rtype: str
    """
    location = ""
    # h2タグ要素を全て列挙
    h2_elems = elem.find_all('h2')
    for e in h2_elems:
        text = e.find(text=True, recursive=False)
        if '場所' in text or '会場' in text:
            # テキストに'場所'か'会場'が含まれていれば
            if e.next_sibling.name == "p":
                # 隣接するpタグを場所名として取得
                location = e.next_sibling.find(text=True, recursive=False)
            break
    return location


def _find_date(elem):
    """HTML要素から日時を表す記述を抽出する

    HTMLをBeautifulSoupでパースしてできたTagオブジェクトから
    日時を表す記述を抽出し文字列で返す
    :param bs4.element.Tag elem: HTML要素
    :return: 日時の記述
    :rtype: str
    """
    date = ""
    # h2タグ要素を全て列挙
    h2_elems = elem.find_all('h2')
    for e in h2_elems:
        text = e.find(text=True, recursive=False)
        if '日時' in text:
            # テキストに'日時'が含まれていれば
            if e.next_sibling.name == "p":
                # 隣接するpタグを日時として取得
                date = e.next_sibling.find(text=True, recursive=False)
            break
    return date


def get_event(url):
    """イベントページのURLから情報を抽出・整形し辞書に格納して返す

    :param str url: イベントページのURL
    :return: 抽出したイベントデータ (HTML取得に失敗した時はNone)
    :rtype: dict
    """
    try:
        html = get_html(url)
    except:
        # HTMLの取得に失敗
        return None

    # 改行タグをマーカーに置換
    BR_MARKER = "{#BR#}"
    br = re.compile(r'<br\s*/?>')
    html = br.sub(lambda t: BR_MARKER, html)

    # パース
    soup = BeautifulSoup(html)

    # イベントを初期化
    event = {"name": "",
             "location": "",
             "start": None,
             "end": None,
             "description": "",
             "url": ""}

    # イベント内容全体の要素を取得
    content_elem = soup.find(id="region-content").contents[2]

    # イベント名を取得
    title_elem = content_elem.find("h1", class_="documentFirstHeading")
    if title_elem is not None:
        event["name"] = title_elem.string

    # イベント内容要素を京大マップイベントページの構造に従って文字列化
    content_text = _element2text(content_elem, url)
    content_text = content_text.replace(BR_MARKER, '\n')

    # 場所名を抽出
    location = _find_location(content_elem)
    # 改行マーカーが含まれていれば除去
    event["location"] = location.replace(BR_MARKER, '')

    # 開始/終了日時を抽出
    date = _find_date(content_elem)
    # 改行マーカーが含まれていれば除去
    date = date.replace(BR_MARKER, '')
    # 日時の記述をdatetimeに変換
    datetime = parse_datetime(date)
    if datetime is not None:
        event["start"] = datetime["start"]
        event["end"] = datetime["end"]

    # イベント内容全体を詳細文として格納
    event["description"] = content_text

    # urlはイベントページのものを使用
    event["url"] = url

    # ソースを生成
    source = {"url": url, "body": content_text}

    # イベントとソースを辞書に格納して返す
    result = {"event": event, "source": source}

    return result


def _extract_event_urls(html):
    """行事カレンダーページのHTML文字列からイベントURLを抽出する

    :param str html: 行事カレンダーページのHTML文字列
    :return: イベントURLのリスト
    :rtype: list
    """
    # リストを初期化
    urls = []

    # パースしてイベントへのリンク要素を取得
    soup = BeautifulSoup(html)
    links = soup.select(".event_calender li > a")

    # リストに追加
    for l in links:
        urls.append(l.get("href"))

    return urls


def get_event_list(date):
    """京大の行事カレンダーから指定年月のイベントURLリストを作成する

    :param datetime.date date: 取得するイベントの年月
    :return: 指定年月のイベントURLリスト (HTML取得に失敗した時はNone)
    :rtype: list
    """
    template = "http://www.kyoto-u.ac.jp/ja?type=calendar&y={0}&m={1}"
    url = template.format(date.year, date.month)
    try:
        html = get_html(url)
    except:
        # HTMLの取得に失敗
        return None

    result = _extract_event_urls(html)
    return result