import os
import re
import sys
import time

from setuptools import find_packages, setup

setup(
    name="requestmax",
    version="1.0",
    description="A stronger requests in the aspect of response.",
    author="trent",
    author_email="fango8888@163.com",
    url="https://gitee.com/trentfzq/requestmax",
    packages=find_packages(),

    install_requires=[
        'requests',
        'parsel',
        'bs4',
        'user-agent',
    ],

    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
