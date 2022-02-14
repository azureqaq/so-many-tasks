#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: tasksconfigparser.py
# 说明:
# 时间: 2022/02/13 22:41:06
# 作者: Azure
# 版本: 1.0

from json import dump, load
from os import makedirs
from os.path import exists
from .exception import *
from typing import Any, Dict

from tools import critical, debug, error, info, logexception, warn

from .command import TasksConfigParserCommand as Tcpc


class TaskConfig(object):
    '''任务配置对象'''
    def __init__(self, name:str, enable:bool, settings:Dict[str, Any]) -> None:
        '''解析为taskconfig对象'''
        self.name = name
        self.settings = settings
        self.enable = enable

        # 如果json文件夹不存在则创建
        if not exists(Tcpc.JSON_FOLDER):
            debug(f'json文件夹：{Tcpc.JSON_FOLDER}不存在，创建')
            makedirs(Tcpc.JSON_FOLDER)

    @property
    def realconfig(self):
        '''除了name'''
        __config = {
            Tcpc.ENABLE:self.enable,
            Tcpc.SETTINGS:self.settings
        }
        return __config

    @staticmethod
    def read_json():
        '''读取配置文件json的完整数据'''
        settings = None
        try:
            with open(Tcpc.JSONPATH, 'r', encoding='utf-8') as fr:
                settings:Tcpc.JSON_FORM = load(fr)
            if not isinstance(settings, dict):
                debug('配置文件格式不太对，无法读取！')
                raise TypeError(f'配置文件:{Tcpc.JSONPATH}非法格式')
        except:
            # 重置json
            with open(Tcpc.JSONPATH, 'w', encoding='utf-8') as fr:
                dump({}, fr, indent=4, ensure_ascii=False)
            warn(f'重置配置文件:{Tcpc.JSONPATH}')
            settings = {}
        return settings

    @staticmethod
    def write_to_json(con:Dict[str, Any]):
        '''将完整数据写入json'''
        with open(Tcpc.JSONPATH, 'w', encoding='utf-8') as fr:
            dump(con, fr, indent=4, ensure_ascii=False)

    def __str__(self):
        return f'{self.name} enable:{self.enable}'

    def update_json(self):
        '''将这个写入json'''
        settings = self.read_json()
        settings.update(
            {
                self.name: self.realconfig
            }
        )
        self.write_to_json(settings)

    def rm_from_json(self):
        '''将这个从json移除'''
        settings = self.read_json()
        try:
            settings.pop(self.name)
            self.write_to_json(settings)
        except:
            debug(f'配置文件中本来就没:{self.name}')


class ConfigFile(object):
    def __init__(self) -> None:
        # 读取json文件
        self.con = TaskConfig.read_json()
        json_con = {}
        for name, values in self.con.items():
            task_config = TaskConfig(name=name, enable=values[Tcpc.ENABLE], settings=values[Tcpc.SETTINGS])
            json_con.update({name:task_config})
        # 所有任务配置文件的字典 { taskname : TaskConfig }
        self.alltasksconfig:Dict[str, TaskConfig] = json_con
    

    def read_json(self):
        '''读取json数据'''
        self.con = TaskConfig.read_json()
        return self.con

    def addconfig(self, taskconfig:TaskConfig):
        '''配置文件中加入taskconfig'''
        return taskconfig.update_json()
    
    def rmconfig(self, taskconfig:TaskConfig):
        '''配置文件中移除这个taskconfig'''
        return taskconfig.rm_from_json()
    
    def getconfig(self, name:str):
        '''从文件中获取taskconfig'''
        if name not in self.alltasksconfig.keys():
            raise TaskConfigNotFoundError(f'配置文件未找到：{name}')
        else:
            return self.alltasksconfig[name]
    
