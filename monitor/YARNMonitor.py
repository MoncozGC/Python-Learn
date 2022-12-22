import datetime
import json
import time
import urllib.request

import requests

if __name__ == '__main__':

    # jobUrl = 'http://node01:8088/ws/v1/cluster/apps/'
    jobUrl = 'http://106.55.243.16:8088/ws/v1/cluster/apps/'
    url = 'https://oapi.dingtalk.com/robot/send?access_token=be05aa39498020bd894b34d63e398f2cfcd2d74a9c20dfc8ef38bdbdbec1c022'
    data = urllib.request.urlopen(jobUrl).read().decode('UTF-8')
    data = json.loads(data)


    def send_msg(yarn_job_id, yarn_job_state, yarn_job_name, nowDate):
        """
        发送消息的函数，这里使用阿里的钉钉
        :param msg: 要发送的消息
        :return: 200 or False
        """

        msg = '"YARN TASK Error Alarm \n YARN_JOB_ID:  %s \n TASK_STATUS: %s  \n YARN_JOB_NAME:  %s \n CREATE_TIME: %s' % (
            yarn_job_id, yarn_job_state, yarn_job_name, nowDate)
        program = {"msgtype": "text", "text": {"content": msg},
                   "at": {
                       "isAtAll": "false",
                       "atMobiles": []
                   }
                   }
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json;charset=utf-8'}
        try:
            f = requests.post(url, data=json.dumps(program), headers=headers)
        except Exception as e:
            return False
        return f.status_code


    # print(datas['apps']['app'])
    for jobInfo in data['apps']['app']:
        yarn_job_id = jobInfo['id']
        yarn_job_name = jobInfo['name']
        yarn_job_state = jobInfo['finalStatus']
        finishedTime = jobInfo['finishedTime']

        # id = datas['apps']['app'][0]['id']
        # name = datas['apps']['app'][0]['name']
        # finalStatus = datas['apps']['app'][0]['finalStatus']
        # finishedTime = datas['apps']['app'][0]['finishedTime']

        # # 获取当前时间
        # current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # print(current_time)
        # #
        # print(finishedTime)

        # 根据任务时间戳转换为时间
        timeArray = time.localtime(finishedTime / 1000)
        nowDate = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        # print("now " + nowDate)
        # 获取五分钟前的时间
        Timestamp = int(time.time() - 300)
        now = datetime.datetime.now()
        timeArray = time.localtime(Timestamp)
        nowDate_5 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        # 打印
        # print(nowDate + " " + nowDate_5)
        # 时间比较
        result = nowDate > nowDate_5
        # result = compare_time(nowDate_5, nowDate)
        # min_5 = Timestamp - 300000
        # print(min_5)
        # print(otherStyleTime)

        # 任务状态为成功 并且 任务时间戳 大于 当前五分钟前的时间戳时执行逻辑
        if yarn_job_state != "SUCCEEDED" and result:
            send_msg(yarn_job_id, yarn_job_state, yarn_job_name, nowDate)
            print("时间: %s, id: %s ,名称: %s，状态: %s, 任务出现异常！" % (nowDate, yarn_job_id, yarn_job_name, yarn_job_state))
        else:
            print(result)
            print("时间: %s, id: %s ,名称: %s，状态: %s, 任务正常！" % (nowDate, yarn_job_id, yarn_job_name, yarn_job_state))
        #     # send_msg(yarn_job_id, yarn_job_state, yarn_job_name, nowDate)
