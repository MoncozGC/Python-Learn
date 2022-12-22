
#! /usr/bin/env python3
# encoding=utf-8

import json
import sys
import time
import urllib.request
import requests

# 监控Flink实时任务
# 脚本使用： python3 FlinkMonitor.py DetailLayerDataRegroup[Flink中正在运行的类名称]

# 会从命令行输入的类名称读取
jobName = sys.argv[1]
jobUrl = 'http://172.16.0.2:8081/v1/jobs/overview'
url = 'https://oapi.dingtalk.com/robot/send?access_token=12374b447774556404b0b53c044126f2c3e4f6fec7b5cc41a039dfae7daa6edf'


def send_msg(msg):
    """
    发送消息的函数，这里使用阿里的钉钉
    :param msg: 要发送的消息
    :return: 200 or False
    """

    program = {"msgtype": "text", "text": {"content": msg},
               "at": {
                   "isAtAll": "false",
                   "atMobiles": ["18676383595", "18674858520"]
               }
               }
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json;charset=utf-8'}
    try:
        f = requests.post(url, data=json.dumps(program), headers=headers)
    except Exception as e:
        return False
    return f.status_code


# 定义一个数组用来保存同一jobName的end_time和state
matchJobState = ''

data = urllib.request.urlopen(jobUrl).read().decode('UTF-8')
data = json.loads(data)
# 获取任务信息
for jobInfo in data["jobs"]:

    name = jobInfo["name"]
    state = jobInfo["state"]
    if jobInfo["name"] == jobName and jobInfo["end-time"] == -1:
        matchJobState = state
        break
    elif jobInfo["name"] == jobName:
        matchJobState = state

# 获取当前时间
current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
if matchJobState != "RUNNING":
    send_msg("名称: %s，任务出现异常，请查看!" % jobName)
    print("时间: %s, 名称: %s，状态: %s, 任务出现异常！" % (current_time, jobName, matchJobState))
else:
    print("时间: %s, 名称: %s，状态: %s, 任务正常！" % (current_time, jobName, matchJobState))
    # send_msg("名称: %s，任务正常!" % jobName)
