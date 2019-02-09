#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime as dt
import unittest

import pytz

from eventparser.utils import parse_datetime


class UtilsTestCase(unittest.TestCase):
    def test_parse_datetime(self):
        case_in_1 = "2014年7月11日（金曜日） 12時10分～12時50分"
        case_in_2 = "平成26年7月8日（火曜日） 18時30分～20時00分"
        case_in_3 = "2014年7月4日（金曜日） 17時30分～19時00分（17時00分受付開始）"
        case_in_4 = "2014年7月26日（土曜日）・27日（日曜日） 10時00分～15時20分"
        case_in_5 = "2014年7月12日（土曜日） 15時00分～"

        utc = pytz.timezone('UTC')

        case_out = {"start": dt(2014, 7, 11, 3, 10, tzinfo=utc),
                    "end": dt(2014, 7, 11, 3, 50, tzinfo=utc)}
        self.assertEqual(parse_datetime(case_in_1), case_out)

        case_out = {"start": dt(2014, 7, 8, 9, 30, tzinfo=utc),
                    "end": dt(2014, 7, 8, 11, 0, tzinfo=utc)}
        self.assertEqual(parse_datetime(case_in_2), case_out)

        case_out = {"start": dt(2014, 7, 4, 8, 30, tzinfo=utc),
                    "end": dt(2014, 7, 4, 10, 0, tzinfo=utc)}
        self.assertEqual(parse_datetime(case_in_3), case_out)

        case_out = {"start": dt(2014, 7, 26, 1, 0, tzinfo=utc),
                    "end": dt(2014, 7, 26, 6, 20, tzinfo=utc)}
        self.assertEqual(parse_datetime(case_in_4), case_out)

        case_out = {"start": dt(2014, 7, 12, 6, 0, tzinfo=utc),
                    "end": dt(2014, 7, 12, 6, 0, tzinfo=utc)}
        self.assertEqual(parse_datetime(case_in_5), case_out)


if __name__ == "__main__":
    unittest.main()