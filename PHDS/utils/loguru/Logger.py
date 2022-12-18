# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/4/26 11:27
# Desc  :

from loguru import logger
from pathlib import Path


class Logger(object):

    def __init__(self):
        base_path = Path(__file__).parent.parent
        # 获得文件夹的绝对路径
        log_path = base_path.joinpath('./logs').resolve()
        # 日志文件夹不存在就新建
        if not log_path.exists():
            log_path.mkdir()
        logger.add(log_path.as_posix() + "./file_{time}.log", rotation="3 MB", enqueue=True)

    def log_error(self, info):
        logger.error(info)

    def log_info(self, info):
        logger.success(info)
