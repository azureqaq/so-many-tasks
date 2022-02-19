#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: command.py
# 说明: 
# 时间: 2022/01/23 00:10:52
# 作者: Azure
# 版本: 1.0

'''command'''
from typing import Dict, Any

class Command(object):
    '''Command'''

class TasksConfigParserCommand(Command):
    '''配置文件解析器 Command'''
    # 配置文件格式
    JSON_FORM = Dict[str, Dict[str, Any]]
    # 配置文件地址
    JSON_FOLDER = './temp'
    JSONPATH = f'{JSON_FOLDER}/tasksconfig.json'

    # 任务配置属性
    NAME = 'name'
    ENABLE = 'enable'
    SETTINGS = 'settings'


class DownloaderCommand(Command):
    '''toos.下载器'''
    FAKE_UA = {
        "User-Agent":
	    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0"
    }