#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: iamtxt.py
# 说明: 
# 时间: 2022/02/15 17:35:37
# 作者: Azure
# 版本: 1.0

from apscheduler.triggers.cron import CronTrigger
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.remote.webelement import WebElement
from tools import info, debug, warn, error, logexception, critical
from typing import Dict
from retry import retry

# 每天2点
tr = CronTrigger(hour=2)

class Command(object):
    '''command'''
    LOGIN_URL = r'https://www.iamtxt.com/e/member/login/log.html'
    HOME_URL = r'https://www.iamtxt.com/'


class IamTxt(object):
    '''iamtxt每日签到'''
    def __init__(self, users:Dict[str, str]) -> None:
        self.users = users
        op = ChromeOptions()
        op.headless = True
        # 设置无图
        prefs = {"profile.managed_default_content_settings.images": 2}
        # op.add_experimental_option("prefs", prefs)
        self.driver = Chrome(options=op)
        debug('浏览器已打开')
        # 设置等待时间
        self.driver.implicitly_wait(5)
    
    @retry(tries=3)
    def login(self, name:str, pwd:str):
        '''登录iamtxt'''
        info(f'登录iamtxt {name}')
        self.driver.get(Command.LOGIN_URL)
    
    def check_login(self):
        '''检查登录状态'''
        self.driver.get(Command.HOME_URL)



def task(settings:Dict[str, str]):
    '''task'''
    try:
        pass

    except Exception as e:
        logexception(e)

def test():
    '''test'''
