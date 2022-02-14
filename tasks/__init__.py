#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: __init__.py
# 说明:
# 时间: 2022/02/14 19:47:50
# 作者: Azure
# 版本: 1.0

from os import listdir
from typing import List

from apscheduler.job import Job
from apscheduler.schedulers.background import BackgroundScheduler
from tools import critical, debug, error, info, logexception, warn
from tools.command import TasksConfigParserCommand as Tcpc
from tools.tasksconfigparser import ConfigFile, TaskConfig
from version import TasksHelper
from tools.exception import *

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
    debug('刷新配置文件...')
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
        TaskConfig(name, True, {'default':'default'}).update_json()
    # 如果没有对应的文件那么就删除对应配置文件
    for name in config_file.alltasksconfig.keys():
        if name not in names:
            config_file.rmconfig(TaskConfig(name, False, {}))
            info(f'从配置文件中删除不存在对应任务文件：{name}')


def add_to_scheduler(name:str):
    '''加入任务到任务列表-无视 enable '''
    # 包名称
    im_name = f'tasks.{name}'
    # 读取配置参数
    configfile = ConfigFile().getconfig(name=name)
    # 导入
    try:
        task_m = __import__(im_name, fromlist=['task', 'tr'])
        scheduler.add_job(
            task_m.task,
            trigger=task_m.tr,
            kwargs={Tcpc.SETTINGS:configfile.settings},
            name=name,
            id=im_name
        )
        info(f'加入任务：{im_name}')
    except Exception as e:
        logexception(e)
        error(TasksHelper.TASK_FORM)


def refresh_scheduler():
    '''刷新任务列表'''
    debug('刷新任务列表...')
    # 当然是先刷新配置文件啊
    configfile_refresh()

    # 然后修改Job
    # 当前任务情况
    jobs:List[Job] = scheduler.get_jobs()
    # 当前任务的name
    job_names = set()
    for job in jobs:
        job_names.add(job.name)
    # 配置文件
    config_file = ConfigFile().alltasksconfig
    # 开始对比
    for name, config in config_file.items():
        '''配置文件中的每个'''
        # 如果配置文件中存在的正在运行
        if name in job_names:
            # 如果配置文件开启了
            if config.enable:
                pass
            # 如果配置文件没开启，就关闭
            else:
                scheduler.pause_job(job_id=f'tasks.{name}')
                info(f'暂停任务：tasks.{name}')
        # 如果配置文件中的没在运行
        else:
            # 如果配置文件开启了
            if config.enable:
                add_to_scheduler(name)
            # 如果没开启
            else:
                pass

