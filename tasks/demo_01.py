#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: demo_01.py
# 说明: 
# 时间: 2022/02/14 18:06:29
# 作者: Azure
# 版本: 1.0

'''示例task'''

from apscheduler.triggers.interval import IntervalTrigger

# logger
from tools import info, debug, logexception

import time

# 必须以 tr 命名, 具体规则自定
tr = IntervalTrigger(seconds=30)


'''
Your code here
'''


# 必须以task命名, settings必须以此命名
def task(settings:dict):
    '''
    此tasks的入口\n
    settings来源于配置文件中的settings
    '''
    try:
        _time = time.strftime(r'%H:%M:%S', time.localtime())
        info(f'{_time}\t参数：{settings}')
        
    except Exception as e:
        logexception(e)
