#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: downloader.py
# 说明: 
# 时间: 2022/02/18 21:43:07
# 作者: Azure
# 版本: 1.0

'''简单的下载器'''

from tools import debug
from .command import *
from .exception import *

from requests import Session
from os.path import exists
from os import makedirs
from retry import retry
from PIL import Image
from typing import List
from os import remove


class PicStatus(object):
    # 已下载
    DOWNLOADED = 'downloaded'
    # 已经验证
    VERIFIED = 'verified'
    # 正在下载
    DOWNLOADING = 'downloading'
    # 下载失败
    FAILED = 'failed'
    # 跳过下载
    SKIP = 'skip'
    # 未下载
    NOT_DOWNLOADED = 'not_downloaded'


class Reason(object):
    '''未正常下载的原因'''
    SKIP_DOWNLOAD = '跳过下载'
    CHECK_ERROR = '下载的图片损坏，打不开'
    NETWORK_ERROR = '网络错误'


class Picture(object):
    '''需要下载的文件类'''
    def __init__(self, name:str, folder:str, url:str) -> None:
        self.name = name
        self.folder = folder
        self.url = url
        # 状态
        self.status = None
        # 原因
        self.reason = None

    @property
    def path(self):
        return f'{self.folder}/{self.name}'
    
    def __str__(self) -> str:
        return f'{self.path} - {self.status}'

    def check_path(self):
        '''检查是否存在需要的文件夹'''
        if not exists(self.folder):
            makedirs(self.folder)
    
    def check_jpg(self):
        '''检查图片是否可以打开，如果不行就删除'''
        if exists(self.path):
            self.status = PicStatus.DOWNLOADED
            try:
                img = Image.open(self.path)
                img.verify()
            except:
                remove(self.path)
            finally:
                self.status = PicStatus.FAILED
                self.reason = Reason.CHECK_ERROR
                img.close()
        else:
            self.status = PicStatus.NOT_DOWNLOADED
    

class Downloader(object):
    ''''图片下载器'''
    def __init__(self, pics:List[Picture]) -> None:
        self.pictures = pics

        # session初始化
        self.session = Session()
        self.session.headers.update(DownloaderCommand.FAKE_UA)

    