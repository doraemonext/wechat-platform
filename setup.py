# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import wechat_platform
version = wechat_platform.__version__

setup(
    name='wechat_platform',
    version=version,
    author='',
    author_email='doraemonext@gmail.com',
    packages=[
        'wechat_platform',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.6.5',
    ],
    zip_safe=False,
    scripts=['wechat_platform/manage.py'],
)