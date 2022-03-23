#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: demo_01.py
# 说明: 
# 时间: 2022/02/14 18:06:29
# 作者: Azure
# 版本: 1.0

'''
检测网页是否更改.
'''

from apscheduler.triggers.interval import IntervalTrigger
from typing import Dict, Union
from tools import info, debug, logexception


# 必须以 tr 命名, 具体规则自定
tr = IntervalTrigger(seconds=30)


'''
Your code here
'''

DATA_PATH = './temp/eheckhtml.json'

class Html(object):
    def __init__(self) -> None:
        self.data = None


# 必须以task命名, settings必须以此命名
def task(settings:dict):
    '''
    此tasks的入口\n
    settings来源于配置文件中的settings
    '''
    try:
        pass
        
    except Exception as e:
        logexception(e)
