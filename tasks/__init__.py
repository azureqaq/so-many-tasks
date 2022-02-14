#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: __init__.py
# 说明: 
# 时间: 2022/02/13 22:37:54
# 作者: Azure
# 版本: 1.0

from os import listdir
from typing import List

from apscheduler.schedulers.background import BackgroundScheduler
from tools import critical, debug, error, info, logexception, warn
from tools.tasksconfigparser import ConfigFile, TaskConfig
from apscheduler.job import Job

scheduler = BackgroundScheduler()

def get_all_tasks_name() -> List[str]:
    '''返回所有tasks的name list'''
    __dir = listdir(r'./tasks')
    res = []
    for i in __dir:
        if '.py' in i and '__init__.py' not in i:
            _i = i.replace('.py', '', 1)
            res.append(_i)
    return res


def configfile_refresh():
    '''根据tasks文件夹和configjson的情况，加入新放入的文件的配置'''
    # 当然是先刷新下文件names
    names = get_all_tasks_name()
    # 配置文件对象
    config_file = ConfigFile()
    # 如果配置文件中存在，那么就忽略
    need_add = []
    for name in names:
        if name not in config_file.alltasksconfig.keys():
            need_add.append(name)
    # 加入需要加入的配置
    for name in need_add:
        TaskConfig(name, False, {'default':'default'}).update_json()


def add_to_scheduler(name:str):
    '''加入任务到任务列表'''
    # 包名称
    im_name = f'tasks.{name}'
    # 读取配置参数
    configfile = ConfigFile().getconfig(name=name)
    # 导入
    task_m = __import__(im_name, fromlist=['task', 'tr'])
    scheduler.add_job(task_m.task, trigger=task_m.tr, kwargs=configfile.settings)



def refresh_scheduler():
    '''刷新任务列表'''
    # 当然是先刷新配置文件啊
    configfile_refresh()

    # 然后修改Job
    # 当前任务情况
    jobs:List[Job] = scheduler.get_jobs()
    # 配置文件
    config_file = ConfigFile().alltasksconfig
    # 开始修改
    for name, config in config_file.items():
        pass
