#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: run.py
# 说明: 
# 时间: 2022/03/20 10:25:34
# 作者: Azure
# 版本: 1.0

'''
在Linux系统中启动。
'''

import subprocess
from tools import info, warn
import re
import os
import sys

if os.name not in ['posix']:
    info('不支持的系统, 请手动操作')
    exit(1)

def linux_command(command:str):
    '''
    运行Linux命令.
    "param command: 命令.
    '''
    tre = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, encoding='utf-8', timeout=3
    )
    return tre

# screen 名称
SCREEN_NAME = r'somanytasks'
# 用户名
WHO = linux_command('echo $USER').stdout.strip()

# 检查是否开启，如果开启则跳过
_allscreen = linux_command('screen -ls')
if _allscreen.returncode != 0:
    _allscreen = _allscreen.stdout.strip()
    if re.match(f'(.*)?{SCREEN_NAME}', _allscreen):
        info('已经存在无需重复开启')
        exit(0)
    else:
        # 开启
        # 位置
        os.chdir(sys.path[0])
        # 开启虚拟环境
        # 如果没有虚拟环境那么就创建
        if not os.path.isdir('./venv'):
            info('未找到虚拟环境，创建...')
            os.system('python3 -m venv venv')
            info('激活虚拟环境')
            os.system('source ./venv/bin/activate')
            info('安装依赖')
            os.system('pip install -r ./requirements.txt')
        else:
            info('存在虚拟环境，直接开启')
            os.system('source ./venv/bin/activate')
        # 开启
        os.system(f'screen -dmS {SCREEN_NAME} python ./tractor.py')
        info('关闭虚拟环境')
        os.system('deactivate')

else:
    info('无法得知screen情况')
    exit(1)

