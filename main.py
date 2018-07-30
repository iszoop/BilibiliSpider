# _*_ coding:utf-8 _*_
__author__ = 'iszoop'
__date__ = '2018/7/26 19:36'
from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy","crawl","bilibili"])