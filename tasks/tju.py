#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: demo_01.py
# 说明: 
# 时间: 2022/02/14 18:06:29
# 作者: Azure
# 版本: 1.0

'''示例task'''

from apscheduler.triggers.cron import CronTrigger

import china_idiom as idiom
from lxml import etree
from lxml.etree import _Element
from tools import info, debug, logexception
from requests import Session
from tools.command import DownloaderCommand
from retry import retry

class TjuPtError(Exception):...
class LoginError(TjuPtError):...


# 必须以 tr 命名, 具体规则自定
tr = CronTrigger(hour=10)

class Tjupt(object):
    def __init__(self, name:str, pwd:str) -> None:
        self.session = Session()
        self.session.headers.update(DownloaderCommand.FAKE_UA)
        self.name = name
        self.pwd = pwd

    
    @retry(tries=3)
    def login(self):
        '''登录'''
        data = {
            'username': self.name,
            'password': self.pwd,
            'logout': '7days'
        }
        self.session.headers.update(
            {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Alt-Used': 'tjupt.org',
                'Connection': 'keep-alive',
                'Content-Length': '52',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'tjupt.org',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1'
            }
        )
        req = self.session.post(url='https://tjupt.org/takelogin.php', timeout=5, data=data)
        if req.ok and self.name not in req.text:
            info(f'{self.name} 登录成功')
        else:
            raise LoginError(f'{self.name} 登录失败')

    @retry(tries=3)
    def comm(self, con:str):
        '''评论帖子'''
        data = {
            'id': '15223',
            'type': 'reply',
            'body': con
        }
        req = self.session.post('https://tjupt.org/forums.php?action=post', data=data, timeout=5)
        if req.ok:
            info(f'评论成功: {con}')
        else:
            raise TjuPtError(f'评论 {con} 失败')
    
    def find_list(self):
        '''找出已经存在的list'''
        # 先查找页码
        def page(p:int):
            return f'https://tjupt.org/forums.php?action=viewtopic&topicid=15223&page={p-1}'
        html = self.session.get(page(1), timeout=5).text
        tree:_Element = etree.HTML(html)
        page_all:str = tree.xpath('//p[@class="pagertop"]/a[6]/b/text()')[0].strip()
        page_all = int(page_all)
        # 获取最新一页的
        html = self.session.get(page(page_all), timeout=5).text
        tree:_Element = etree.HTML(html)
        # 查找这一页所有的成语

        print(html)
        
    

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
