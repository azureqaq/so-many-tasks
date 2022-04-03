#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: demo_01.py
# 说明: 
# 时间: 2022/02/14 18:06:29
# 作者: Azure
# 版本: 1.0

'''示例task'''

from re import compile, findall
from typing import List, Union

from apscheduler.triggers.cron import CronTrigger
from random import randint
from lxml import etree
from lxml.etree import _Element
from pypinyin import lazy_pinyin
import china_idiom as idiom
from requests import Session
from retry import retry
from tools import debug, info, logexception, warn
from tools.command import SpiderCommand as Command
from time import sleep


class TjuptError(Exception):...
class AskurlError(TjuptError):...
class TopicError(TjuptError):...

# 必须以 tr 命名, 具体规则自定
tr = CronTrigger(hour=13, minute=31)


class TjuPt(object):
    VIEW = 'https://tjupt.org/forums.php?action=viewtopic&topicid=15223&page=last#last'
    HEAD_LOGIN = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Alt-Used': 'tjupt.org',
            'Connection': 'keep-alive',
            'Content-Length': '52',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'tjupt.org',
            'Origin': 'https://tjupt.org',
            'Referer': 'https://tjupt.org/login.php',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'TE': 'trailers',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0'
        }
    def __init__(self, name:str, pwd:str) -> None:
        '''
        tjupt对象.
        :param name: 登陆用户名.
        :param pwd: 登陆密码.
        '''
        self.name = name
        self.pwd = pwd
        self.session = Session()
        self.session.headers.update(Command.FAKE_UA)
    
    def __askurl(self, url:str, par:dict={}, head:dict={}):
        '''
        获取网页内容.
        :param url: 网页链接.
        :param par: 参数.
        :param head: 临时head.
        '''
        _head = self.session.headers
        _head.update(head)
        req = self.session.get(url=url, params=par, headers=_head)
        if req.ok:
            return req.content
        else:
            raise AskurlError(f'访问{url}失败')
    
    def login(self):
        '''登陆'''
        loginurl = 'https://tjupt.org/takelogin.php'
        data = {
            'username': self.name,
            'password': self.pwd,
            'logout': '7days'
        }
        req = self.session.post(loginurl, data, headers=Command.FAKE_UA)
        req.encoding = 'utf-8'
        if req.ok and self.name in req.text:
            info(f'{self.name}登陆成功')
        else:
            warn(f'{self.name}登陆失败')
            raise AskurlError(f'{self.name}登陆失败')
    

    def viewtopic(self, topicid:str, page:str):
        '''
        查看所发内容.
        :param topicid: 地址代码.
        :param page: 页码 last 是最新.
        '''
        res = []
        urlcon = self.__askurl(f'https://tjupt.org/forums.php?action=viewtopic&topicid={topicid}&page={page}')
        html:_Element = etree.HTML(urlcon)
        items:List[_Element] = html.xpath('//div[contains(@id, "pid")]')
        if not len(items):
            raise TopicError(f'无法获取有效信息:{topicid}')
        for i in items:
            res.append(i.text)
        
        return res
    
    def reply(self, topicid:str, content:str):
        '''
        回复消息.
        :param topicid: 地址代码.
        :param content: 回复内容.
        '''
        data = {
            'id': topicid,
            'type': 'reply',
            'body': content.strip()
        }
        req = self.session.post('https://tjupt.org/forums.php?action=post', data=data)
        if req.ok and content.strip() in req.text:
            info(f'评论成功{topicid} {content}')
        else:
            warn(f'评论失败{topicid} {content}')
            raise TopicError(f'评论失败{topicid} {content}')
        

    def chengyujielong(self, chengyulist:Union[List[str], None]):
        '''
        成语接龙.
        :param chengyulist: 成语列表.
        '''
        p = compile(r'[\u4e00-\u9fa5]')
        chengyus = []
        # 先对列表进行处理
        for i in chengyulist.copy():
            if i is None:
                chengyus.append(i)
            else:
                res:List[str] = findall(p, i.strip())
                chengyus.append(''.join(res))
        
        if len(chengyus) == 0:
            warn('未找到可用列表')
            return
        elif chengyus[-1] is None:
            warn('最后一个是None')
            return
        else:
            # 找到最后一个成语的第一个的字的拼音
            _l = chengyus[-1][-1]
            _l_py = lazy_pinyin(chengyus[-1][0])[0]
            # 新的成语
            ido = idiom.search_idiom(_l, 1, 5)
            if len(ido) == 0:
                raise TopicError('接不出来')
            # 如果新的成语列表最后一个字的pinyin和第一个相同跳过，如果不是4跳过
            res = []
            for i in ido:
                if len(i) != 4:
                    continue
                if lazy_pinyin(chengyus[-1][0])[0] == lazy_pinyin(i[-1])[0]:
                    continue
                else:
                    res.append(i)
            if len(ido) == 1:
                ne = ido[0]
            elif not len(res):
                # 如果没有合格的
                ne = ido[randint(0, len(ido)-1)]
            elif len(res) == 1:
                ne = res[0]
            else:
                ne = res[randint(0, len(res)-1)]
            # 开始接龙
            self.reply('15223', ne)





# 必须以task命名, settings必须以此命名
def task(settings:dict):
    '''
    此tasks的入口\n
    settings来源于配置文件中的settings
    '''
    def _in():
        tju = TjuPt(settings.get('name'), settings.get('pwd'))
        tju.login()
        s = tju.viewtopic('15223', 'last')
        tju.chengyujielong(s)
    try:
        for i in range(3):
            debug(f'第{i+1}次')
            _in()
            sleep(3)
            
    except Exception as e:
        logexception(e)

def test():
    '''测试'''
    try:
        from tools.tasksconfigparser import ConfigFile
        sett = ConfigFile().getconfig('tju').settings
        return task(sett)
        
    except Exception as e:
        raise e
