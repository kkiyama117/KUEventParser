#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""setup.py

    setuptoolsを使う.コードの通り.
"""
import os
import sys
from codecs import open
from setuptools import setup
from setuptools.command.test import test as TestCommand

here = os.path.abspath(os.path.dirname(__file__))


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
        self.test_suite = 'tests'

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('rm -rf dist/*')
    os.system('python setup.py sdist')
    os.system('twine upload dist/*')
    sys.exit()

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish_test':
    os.system('rm -rf dist/*')
    os.system('python setup.py sdist')
    os.system('twine upload --repository pypitest dist/*')
    sys.exit()

packages = ['kueventparser', 'kueventparser.adapters']

requires = [
    'beautifulsoup4',
    'lxml',
    'pytz',
    'requests'
]

test_requirements = [
    'pytest',
    'pytest-cov',
    'tox'
]

about = {}
with open(os.path.join(here, 'kueventparser', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()
with open('HISTORY.md', 'r', 'utf-8') as f:
    history = f.read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    maintainer=about['__maintainer__'],
    maintainer_email=about['__maintainer_email__'],
    url=about['__url__'],
    packages=packages,
    package_data={'': ['LICENSE', 'NOTICE']},
    package_dir={'kueventparser': 'kueventparser'},
    include_package_data=True,
    python_requires=">=3.4",
    setup_requires=['setuptools >= 30.3'],
    install_requires=requires,
    license=about['__license__'],
    zip_safe=False,
    classifiers=[
        # 'Development Status :: 4 - Beta',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: Japanese',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Utilities'
    ],
    entry_points={
        'console_scripts': ['parse_event= kueventparser.core:main']
    },
    cmdclass={'test': PyTest},
    tests_require=test_requirements,
    extras_require={
        'test': ['pytest', 'tox'],
    },

)
