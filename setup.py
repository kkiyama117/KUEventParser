# -*- coding: utf-8 -*-
"""setup.py

    setuptoolsを使う.コードの通り.
"""

import os
import sys

import sphinx.apidoc
from setuptools import setup
from setuptools.command.test import test as TestCommand
from sphinx.setup_command import BuildDoc


class BuildDocApiDoc(BuildDoc, object):
    """Document を `setuptools` で実行する時に, 自動でdocstringsを読み込ませるためのclass.

    """
    # inherit from object to enable 'super'
    user_options = []
    description = 'sphinx'

    def run(self):
        # metadata contains information supplied in setup()
        metadata = self.distribution.metadata
        # package_dir may be None, in that case use the current directory.
        # Run sphinx by calling the main method, '--full' also adds a conf.py
        sphinx.apidoc.main(
            ['', '-f', '-o', os.path.join('docs', 'source'), os.path.join('src')])
        super(BuildDocApiDoc, self).run()


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


setup(cmdclass={'build_sphinx': BuildDocApiDoc, 'test': PyTest})
