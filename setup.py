#!/usr/bin/env python

try:
    from setuptools import setup
except:
    from distutils.core import setup


setup(name='eventparser',
      version='0.1.1',
      description='event parser',
      author='Unimap, Inc.',
      author_email='info@unimap.co.jp',
      packages=['eventparser'],
      scripts=['scripts/kyoto_u'],
      test_suite='tests',
      install_requires=[
          'beautifulsoup4==4.3.2',
          'nkf==0.1.1',
          'pytz==2014.4',
          'requests==2.3.0',
      ],
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7'
      ])
