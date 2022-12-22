#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: yu.jiang
Email:  safemonitor@outlook.com
Time:   2018/09/04
Describe：钉钉告警机器人，支持@多个用户， 传递参数$1为信息内容、$2表示要通知的钉钉用户
Usage:  python dingding.py  这是一条测试信息  "152055xxxx","15088xxxx","187551xxxx"
"""

import requests
import json
import sys
import os
import datetime


# 告警通知用户列表, 多个用户以逗号分隔. 此规则为固定列表、不支持zabbix自定义通知用户
Alarm_User_List = '15205xxxx', '15088xxxxx'

headers = {'Content-Type': 'application/json;charset=utf-8'}

# 个人群组： 监控报警
api_url = 'https://oapi.dingtalk.com/robot/send?access_token=be05aa39498020bd894b34d63e398f2cfcd2d74a9c20dfc8ef38bdbdbec1c022'


def msg(text):
    json_text = {
        "msgtype": "text",
        "at": {
            "atMobiles":
                at_user,
            "isAtAll": False  # 为True表示@所有人
        },

        "text": {
            "content": text
        }
    }
    notice = requests.post(api_url, json.dumps(json_text), headers=headers).content
    print(json.loads(notice))

    # 增加日志打点功能
    if os.path.exists("/var/log/dingding.log"):
        f = open("/var/log/dingding.log", "a+")
    else:
        f = open("/var/log/dingding.log", "w+")
        f.write("\n" + "--" * 60)

    if json.loads(notice)["errcode"] == 0:
        f.write("\n" + str(datetime.datetime.now()) + "    " + str(at_user) + "    " + "发送成功" + "\n" + str(
            text) + "\n" + "--" * 60)
        f.close()
    else:
        f.write("\n" + str(datetime.datetime.now()) + "    " + str(at_user) + "    " + "发送失败" + "\n" + str(
            text) + "\n" + "--" * 60)
        f.close()


if __name__ == '__main__':
    text = "test"
    # text = sys.argv[1]
    # 固定列表通知用户选项
    #    try:
    #        at_user = (Alarm_User_List).split(',')
    #    except IndexError as e:
    #        at_user = []

    # 此处支持zabbix自定义脚本参数, $1 {ALERT.MESSAGE}, $2 {ALERT.SENDTO}
    try:
        at_user = sys.argv[2].split(',')
    except IndexError as e:
        at_user = []
    msg(text)
