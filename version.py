#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: version.py
# 说明: 
# 时间: 2022/01/23 00:15:14
# 作者: Azure
# 版本: 1.0

class Version(object):
    # 版本号，如果带有beta字符则为测试版
    VERSION = '0.1_beta'
    # 发布日期 年-月-日
    RELEASE = '2022-1-23'

    # 横幅
    BANNER = r"""
    _                         ___      _    ___  
   / \    _____   _ _ __ ___ / _ \    / \  / _ \ 
  / _ \  |_  / | | | '__/ _ \ | | |  / _ \| | | |
 / ___ \  / /| |_| | | |  __/ |_| | / ___ \ |_| |
/_/   \_\/___|\__,_|_|  \___|\__\_\/_/   \_\__\_\
                                                 
"""

    # 发布说明
    NOTE = r'''
    1. 发布最初版本；
    2. '''


def hello():
    '''say hello'''
    print(Version.BANNER)
    print(f'版本号：{Version.VERSION}', f'发布日期：{Version.RELEASE}')
    print()
    print(f'发布说明：{Version.NOTE}')
    print()
    if 'beta' in Version.VERSION:
        print('你正在使用的是测试版！')
        print('可能会经常出现BUG！')
        print('请及时回到正式版！')
    
    print('\n你好！欢迎使用本程序！\n')


class Helper(object):
    '''帮助文件'''

class TasksHelper(Helper):
    '''Tasks帮助'''
    # pass
    



if __name__ == '__main__':
    hello()
