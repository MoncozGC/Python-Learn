# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/4/14 11:13
# Desc  : 调用bark接口, 推送消息
# Bark API: https://bark.day.app/#/tutorial
import configparser
import subprocess

import requests

from project.message_push.push_common import dir_info
from utils.comm_util import print_ts
from utils.config_util import get_root_path

config = configparser.ConfigParser()
config.read(get_root_path() + '/config.ini', encoding='utf-8')
deviceKey = config.get('message_push', 'deviceKey')


def send_bark(message, group_name, title='推送通知'):
    """
    使用python推送消息
    :param title: 推送标题
    :param message: 推送内容
    :param group_name: 消息分组
    :return:
    """
    url = f'https://api.day.app/{deviceKey}'
    param = {
        'title': title,
        'body': message,
        'level': 'active',
        'group': group_name
    }
    requests.post(url=url, params=param)


def bark_encr_push(message, group_name='', sound='birdsong', icon_name=''):
    """
    加密推送方式
    :param message: 推送内容
    :param group_name: 消息分组
    :param sound: 推送铃声
    :param icon_name: 推送图标
    :return:
    """

    """
    使用shell脚本加密推送消息

    subprocess.run函数参数解释：
    [shell_script_path, '传递参数']：将Shell脚本路径和传递参数作为一个列表传递给run()函数。
    stdout=subprocess.PIPE：将标准输出重定向到PIPE，以便在Python中捕获Shell脚本的输出。
    stderr=subprocess.PIPE：将标准错误输出重定向到PIPE，以便在Python中捕获Shell脚本的错误信息。
    text=True：将输出和错误信息转换为字符串类型。
    check=True：检查命令是否执行成功，如果命令返回非0，将抛出CalledProcessError异常。
    """
    shell_script_path = 'bark_encr_push.sh'

    print_ts("加密推送...")
    # 方式一:
    # subprocess.run(['cmd', '/c', 'bash', shell_script_path, '传递参数'],
    #                         stdout=subprocess.PIPE,
    #                         stderr=subprocess.PIPE,
    #                         text=True,
    #                         check=True)
    # 方式二: 调用shell脚本并禁止curl输出
    proc = subprocess.Popen(['cmd', '/c', 'bash', shell_script_path,
                             message, group_name, sound, icon_name, deviceKey],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()


if __name__ == '__main__':
    text = dir_info(__file__)
    group = '开发通知'
    send_bark(text, group)

    # bark_encr_push(text, '开发通知', 'birdsong', 'icon_dev.png')
