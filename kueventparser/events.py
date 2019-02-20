# -*- coding: utf-8 -*-
import datetime


class Event:
    """イベント情報を含んだclass

    Attributes:
        title(:obj:`str`): イベント名
        url(:obj:`str`): イベント情報のURL
        location(:obj:`str`): 開催地
        description(:obj:`str`): 詳細説明文
        date (:obj:`datetime.date`): 開催日
        start (:obj:`datetime.time`): 開始時間
        end (:obj:`datetime.time`): 終了時間
    """

    def __init__(self, title: str, url: str, location: str, description: str,
                 date: datetime.date, start: datetime.time,
                 end: datetime.time):
        """イニシャライザー

        Args:
            title(str): イベント名
            url(str): イベント情報のURL
            location(str): 開催地
            description(str): 詳細説明文
            date: 開催日
            start: 開始時間
            end: 終了時間
        """
        self.title = title
        self.url = url
        self.location = location
        self.description = description
        self.date = date
        self.start = start
        self.end = end

    def __str__(self):
        """ to string

        Returns:
            str: `self.title`
        """
        return self.title

    def __eq__(self, other):
        if other is None or type(self) != type(other):
            return False
        # __dict__メソッドを使ってattributesを比較
        return self.__dict__ == other.__dict__

    def dict(self):
        """ to Dictionary

        event == Event(**event.dict())

        :return:
        """
        return self.__dict__.copy()
