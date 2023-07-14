# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/4/12
# Desc  : 监控湖南高考网发布消息, 如果有最新消息则通过bark发送消息通知
import time

import requests
from lxml import etree

from project.message_push.bark_push import send_bark
from utils.comm_util import print_ts, getNowTimeStr


def request_():
    url = 'http://jyt.hunan.gov.cn/jyt/sjyt/hnsjyksy/web/ksyzkzx/index.html'
    # UA解析
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    # 发起get请求
    requests_get = requests.get(url=url, headers=headers)
    requests_get.encoding = requests_get.apparent_encoding
    # 获取请求的文本
    get_text = requests_get.text
    tree = etree.HTML(get_text)
    # 使用 XPath 查询获取目标数据
    data = tree.xpath('//table[@class="table_list"]//tr/td/a/text()')

    with open('./data/gaokao.txt', 'r', encoding='utf-8') as file:
        file_content = file.read().strip()

    # 打印文件内容

    url_content = ''
    # 输出结果
    for item in data:
        url_content = item.strip()
        break

    # print(file_content)
    # print("=======================")
    # print(url_content)
    if file_content == url_content:
        print_ts("高考标题-相等")
    else:
        print_ts("高考最新标题", url_content)
        send_bark(url_content, '其余通知', '高考查分')

        # 重新写入数据文件
        with open('./data/gaokao.txt', 'w', encoding='utf-8') as f:
            f.write(url_content)
            print_ts("已重写 高考标题 文件, 内容为: ", url_content)


if __name__ == '__main__':

    flag = True
    while flag:
        request_()
        time.sleep(10)
        if getNowTimeStr() > '2023-06-26 00:00:00':
            flag = False
            print_ts("运行结束")
