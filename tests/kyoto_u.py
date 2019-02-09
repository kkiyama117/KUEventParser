#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from os import path
import unittest

from eventparser.kyoto_u import _extract_event_urls


class UtilsTestCase(unittest.TestCase):
    def test_extract_event_urls(self):
        file_path = path.join(path.dirname(__file__), 'case_in_extract_event_urls.txt')
        with open(file_path, 'r') as f:
            case_in = f.read()
        file_path = path.join(path.dirname(__file__), 'case_out_extract_event_urls.txt')
        with open(file_path, 'r') as f:
            case_out = f.read().splitlines()

        self.assertEqual(_extract_event_urls(case_in), case_out)


if __name__ == "__main__":
    unittest.main()