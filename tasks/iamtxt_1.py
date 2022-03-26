#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: iamtxt_1.py
# 说明: 
# 时间: 2022/03/11 12:06:32
# 作者: Azure
# 版本: 1.0

'''
用requests
'''

from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from requests import Session
from tools.command import DownloaderCommand
from lxml import etree
from lxml.etree import _Element
from typing import List
from retry import retry

# logger
from tools import info, debug, logexception, error

# import time

# 必须以 tr 命名, 具体规则自定
tr = CronTrigger(hour=13)

class LoginError(Exception):...

class Iamtxt(object):
    def __init__(self) -> None:
        self.session = Session()
        self.session.headers.update(DownloaderCommand.FAKE_UA)
    
    @retry(tries=3)
    def login(self, name:str, pwd:str):
        '''登录'''
        try:
            self.session.headers.update(
                {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                    'Connection': 'Content-Length',
                    'Content-Length': '147',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Host': 'www.iamtxt.com',
                    'Origin': 'https://www.iamtxt.com',
                    'Sec-Fetch-Mode': 'document',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-User': r'?1',
                    'Upgrade-Insecure-Requests': '1'


                }
            )
            data = {
                'ecmsfrom': 'https://www.iamtxt.com/',
                'enews': 'login',
                'tobind': '0',
                'username': name,
                'password': pwd,
                'lifetime': '315360000',
                'Submit': '+登+录+'
            }
            req = self.session.post('https://www.iamtxt.com/e/member/doaction.php', data=data, timeout=5)
            text = req.text
            if req.ok and '' in text:
                info(f'{name}登录成功！')
                return
            else:
                raise LoginError(f'登录失败:{name}')

        except Exception as e:
            raise e

    @retry(tries=2)
    def logout(self):
        '''退出登录'''
        try:
            # ?enews=exit
            par = {'enews': 'exit'}
            req = self.session.get('https://www.iamtxt.com/e/member/doaction.php', timeout=5, params=par)
            print(req.status_code)
            if req.ok and '账号登录' in req.text:
                info(f'登出成功')
                return
            else:
                error(f'可能登出失败')
        except Exception as e:
            error(f'登出失败:{e}')
    
    def done(self):
        '''签到'''
        req = self.session.post('https://www.iamtxt.com/e/extend/signin.php', data={'userid': '0'}, timeout=5)
        if req.ok and '' in req.text:
            info(req.text.strip())
        else:
            error('发现错误，可能并未签到成功')

# 必须以task命名, settings必须以此命名
def task(settings:dict):
    '''
    此tasks的入口\n
    settings来源于配置文件中的settings
    '''
    try:
        info('开始 iamtxt 签到')
        for i, y in settings.items():
            txt = Iamtxt()
            txt.login(i, y)
            txt.done()
        
        
    except Exception as e:
        logexception(e)
    finally:
        info('iamtxt 今天的任务完成啦！')

def test():
    '''
    测试.
    '''
    try:
        info('iamtxt_1 测试...')
        from tools.tasksconfigparser import ConfigFile

        fil = ConfigFile().getconfig('iamtxt_1')
        sett = fil.settings
        return task(sett)
    except Exception as e:
        logexception(e)
    finally:
        info('iamtxt_1 测试 Done')

