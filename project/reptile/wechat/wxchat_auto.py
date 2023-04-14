# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/2/8 10:20
# Desc  : 微信自动发送聊天
import pyautogui as pg
import pyperclip as pc
from apscheduler.schedulers.blocking import BlockingScheduler

pg.PAUSE = 1

# 微信的备注
name = '文件传输助手'
# 发送的消息
msg = '...wxchat'


def auto():
    # 打开微信
    pg.hotkey('ctrl', 'alt', 'w')
    pg.hotkey('ctrl', 'f')

    pc.copy(name)
    pg.hotkey('ctrl', 'v')
    pg.press('enter')

    pc.copy(msg)
    pg.hotkey('ctrl', 'v')
    pg.hotkey('ctrl', 'enter')

    pg.hotkey('ctrl', 'alt', 'w')


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(auto)
    # 定时每天十二点执行
    # scheduler.add_job(auto, 'cron', hour=0, minute=0)
    scheduler.start()
