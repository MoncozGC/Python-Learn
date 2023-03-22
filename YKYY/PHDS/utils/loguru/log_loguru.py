# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/4/26 10:46
# Desc  : loguru日志模块使用
# Fix: 日志不是实时写入, 需要程序执行完毕才会写入

from pathlib import Path

from loguru import logger

if __name__ == '__main__':
    base_path = Path(__file__).parent.parent
    # 获得文件夹的绝对路径
    log_path = base_path.joinpath('./logs').resolve()
    # 日志文件夹不存在就新建
    if not log_path.exists():
        log_path.mkdir()

    # 通过as_posix转换成str类型可与字符串相加并且将windows路径中的的 \转成unix的/
    # logger.add(logpath.as_posix() + './test1.log',
    #            format="<green>{time:HH:mm:ss}</green> | {module} line:{line} {function} |{level} | {message}",
    #            level="INFO", encoding='utf-8')
    # logger.info('test message')
    # rotation控制日志大小超过则新增日志.
    logger.add(log_path.as_posix() + "./file_{time}.log", rotation="3 MB", enqueue=True)

    logger.debug("this is a Debug log")
    logger.info("this is a Info log")

    logger.info("this is a modify info log")
    logger.error("this is a error log")

    for i in range(1000):
        logger.info(i)

    # 通过{} %的格式添加字符, 等同于str.format()
    logger.info("If you're using Python {version}, prefer {feature} of course!", version=3.6, feature="f-strings")
