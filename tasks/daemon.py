#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: daemon.py
# 说明: 
# 时间: 2022/03/11 13:03:43
# 作者: Azure
# 版本: 1.0

#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: demo_01.py
# 说明: 
# 时间: 2022/02/14 18:06:29
# 作者: Azure
# 版本: 1.0

'''示例task'''

from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from tasks import refresh_scheduler

# logger
from tools import info, debug, logexception

import time

# 必须以 tr 命名, 具体规则自定
tr = CronTrigger(minute=0)


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
        '''每小时更新一次表'''
        info('每小时刷新一次任务列表')
        refresh_scheduler()
        info('刷新完成')
        
        
    except Exception as e:
        logexception(e)
