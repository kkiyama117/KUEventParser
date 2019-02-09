# -*- coding: utf-8 -*-
"""setup.py

    setuptoolsを使う.コードの通り.
"""

import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    """ PyTestを実行するコマンドの実装

    pytestのオプションを指定する際は--pytest-args='{options}'を使用する.
    """
    user_options = [
        ('pytest-args=', 'a', 'Arguments for pytest'),
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_target = []
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(cmdclass={'test': PyTest})
