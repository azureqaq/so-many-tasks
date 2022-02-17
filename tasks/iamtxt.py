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
from time import sleep
from re import findall

class IamTxtError(Exception):...

class LoginError(IamTxtError):...
class LogoutError(IamTxtError):...


# 每天2点
tr = CronTrigger(hour=2)

class Command(object):
    '''command'''
    LOGIN_URL = r'https://www.iamtxt.com/e/member/login/log.html'
    HOME_URL = r'https://www.iamtxt.com/'
    SETTINGS_URL = r'https://www.iamtxt.com/e/member/cp/'

    # 账号输入框
    NAME_XPATH = r'/html/body/div[1]/div[1]/div/form/div[2]/input'
    # 密码输入框
    PWD_XPATH = r'/html/body/div[1]/div[1]/div/form/div[3]/input'
    # 登录按钮
    SUBMIT_XPATH = r'/html/body/div[1]/div[1]/div/form/div[5]/input'
    # 设置界面中，用户名位置
    NAME_STR_XPATH = r'/html/body/div[1]/div[1]/div[1]/div[2]'
    # 设置界面，注销登录按钮
    LOGOUT_XPATH = r'/html/body/div[1]/div[2]/div/div[6]/a'
    # 签到按钮
    SIGNIN_XPATH = r'//*[@id="signin"]'
    # 设置页面，积分信息
    POINTS_XPATH = r'/html/body/div[1]/div[1]/div[2]'


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
        debug('打开登录网页')
        self.driver.get(Command.LOGIN_URL)
        # 等一会儿，可能别的地方没退出
        sleep(3)
        self.driver.refresh()
        self.driver.get(Command.LOGIN_URL)
        # 输入name pwd
        name_bt:WebElement = self.driver.find_element_by_xpath(Command.NAME_XPATH)
        name_bt.clear()
        debug(f'输入账户:{name}')
        name_bt.send_keys(name)
        # 输入密码
        pwd_bt:WebElement = self.driver.find_element_by_xpath(Command.PWD_XPATH)
        pwd_bt.clear()
        debug('输入对应密码')
        pwd_bt.send_keys(pwd)
        # 点击登录按钮
        submit_bt:WebElement = self.driver.find_element_by_xpath(Command.SUBMIT_XPATH)
        submit_bt.click()
        debug('点击登录按钮')
        # 检查是否登录成功
        # 打开设置网址
        self.driver.get(Command.SETTINGS_URL)
        name_e:WebElement = self.driver.find_element_by_xpath(Command.NAME_STR_XPATH)
        if name.lower() in name_e.text.lower():
            info(f'{name} 登录成功')
        else:
            error(f'{name} 登录失败')
            raise LoginError('登录失败')
    
    @retry(tries=3)
    def logout(self):
        '''登出'''
        debug('注销登录')
        # 打开设置页面
        self.driver.get(Command.SETTINGS_URL)
        sleep(2)
        self.driver.refresh()
        sleep(2)
        if self.driver.current_url == Command.LOGIN_URL:
            info('未登录账号！')
            return
        else:
            info('登出账号')
            name_e:WebElement = self.driver.find_element_by_xpath(Command.NAME_STR_XPATH)
            name_es:str = name_e.text
            name_es = name_es.replace('修改头像', '').strip()
            # 点击退出按钮
            logout_bt:WebElement = self.driver.find_element_by_xpath(Command.LOGOUT_XPATH)
            logout_bt.click()
            info(f'注销登录的账号：{name_es}')
            raise LogoutError('登出失败')
    
    def get_points(self):
        '''获取积分'''
        # 打开设置页面
        self.driver.get(Command.SETTINGS_URL)
        self.driver.refresh()
        point_e:WebElement = self.driver.find_element_by_xpath(Command.POINTS_XPATH)
        point_es:str = point_e.text
        point_es = findall(r'分(.*)?点', point_es)[0]
        point_es = point_es.strip()
        return findall(r'\d+', point_es)[0]


    def signin(self):
        '''给他们都签到上！'''
        # 遍历每一个账号
        for name, pwd in self.users.items():
            # 登录
            self.login(name, pwd)
            p_ = self.get_points()
            debug(f'签到前积分：{p_}')
            # 签到
            signin_bt:WebElement = self.driver.find_element_by_xpath(Command.SIGNIN_XPATH)
            debug('点击签到按钮')
            signin_bt.click()
            e_ = self.get_points()
            info(f'签到后积分：{e_}')
            if p_ == e_:
                info(f'{name} 签到失败')
            else:
                info(f'{name} 签到成功')
            # 登出
            self.logout()
            # 清楚cooikes
            self.driver.delete_all_cookies()
        info('本轮iamtxt签到完成')



def task(settings:Dict[str, str]):
    '''task'''
    try:
        IamTxt(settings).signin()

    except Exception as e:
        logexception(e)

def test():
    '''test'''
    from tools.tasksconfigparser import ConfigFile
    configs = ConfigFile().getconfig('iamtxt').settings
    IamTxt(configs).signin()
