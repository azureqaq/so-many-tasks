#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: tractor.py
# 说明:
# 时间: 2022/02/14 20:40:13
# 作者: Azure
# 版本: 1.0

from time import localtime, sleep, strftime

from apscheduler.job import Job

from tasks import (add_to_scheduler, configfile_refresh, get_all_tasks_name,
                   refresh_scheduler, scheduler)
from tools import critical, debug, error, info, logexception, warn


def main():
    '''main'''
    # 任务初始化
    refresh_scheduler()
    # 开启任务
    scheduler.start()
    # 指令集合
    COMMANDS = [
        '任务列表状态',
        '刷新任务列表',
        '暂停任务',
        '强制加入任务',
        '暂停任务',
        '恢复任务',
        '退出',
        '删除任务',
        '删除所有任务'
    ]
    # 保持一直运行主程序
    while True:
        # 休息一秒钟
        sleep(1)
        # 输入指令
        for i in range(len(COMMANDS)):
            print(f'{i}:{COMMANDS[i]}', end=' ')
        print()
        command = input('请输入对应序号:')
        try:
            command = int(command)
            if command not in range(len(COMMANDS)):
                raise
        except:
            continue

        info(f'{COMMANDS[command]} ...')

        # 当前任务 names
        job_names = set()
        for _job in scheduler.get_jobs():
            _job:Job
            job_names.add(_job.name)

        # 任务列表状态
        if command == 0:
            scheduler.print_jobs()
        # 刷新任务列表
        elif command == 1:
            refresh_scheduler()
        # 暂停某一个任务
        elif command == 2:
            __input_name = input('请输入要暂停的任务的 name :')
            if __input_name not in job_names:
                warn(f'任务 {__input_name} 未运行')
                continue
            else:
                _job:Job = scheduler.get_job(f'tasks.{__input_name}')
                _job.pause()
                info(f'暂停任务：{__input_name}')
        # 强制加入任务
        elif command == 3:
            configfile_refresh()
            __all_tasks_names = get_all_tasks_name()
            debug(f'所有可选任务：{__all_tasks_names}')
            __input_name = input('请输入要加入的任务 name :')
            if __input_name not in __all_tasks_names:
                error(f'未找到任务文件：{__input_name}')
            else:
                add_to_scheduler(__input_name)
        # 暂停任务
        elif command == 4:
            __input_name = input('请输入要暂停任务 name :')
            _job = scheduler.get_job(f'tasks.{__input_name}')
            if _job != None:
                info(f'任务:{__input_name}已经暂停')
                _job.pause()
            else:
                warn(f'任务：{__input_name} 并未运行')
        # 恢复任务
        elif command == 5:
            __input_name = input('请输入要恢复的任务 name :')
            if __input_name not in job_names:
                warn(f'不存在任务{__input_name}')
                continue
            _job = scheduler.resume_job(f'tasks.{__input_name}')
            if _job != None:
                info(f'任务:{__input_name} 已经恢复，下次运行时间：{_job.next_run_time}')
            else:
                warn(f'任务:{__input_name}并不存在')
        # 退出
        elif command == 6:
            break
        # 删除任务
        elif command == 7:
            __input_name = input('请输入要删除的任务 name :')
            if __input_name in job_names:
                scheduler.remove_job(f'tasks.{__input_name}')
                info(f'删除任务:{__input_name}')
            else:
                warn(f'{__input_name}并不存在')
        # 删除所有任务
        elif command == 8:
            scheduler.remove_all_jobs()


if __name__ == '__main__':
    '''main'''
    info(' S T A R T ')
    try:
        main()
    except Exception as e:
        logexception(e)
    finally:
        scheduler.pause()
        scheduler.shutdown()
        info(' E N D ')
