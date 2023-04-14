# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/4/14 14:57
# Desc  : 推送通用类
import datetime
import os.path

now_time = datetime.datetime.now().strftime("%Y-%m-%d%H:%M:%S")


def dir_info(__file__):
    """
    输出当前文件名
    """
    return "SUCCESS " + os.path.basename(__file__)


if __name__ == '__main__':
    print(dir_info(__file__))
