# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/12/27 19:56
# Desc  : 虎牙主播信息获取

import requests
from bs4 import BeautifulSoup


def getHTMLText(url):
    """
    定义获取页面内容的方法
    :param url:
    :return:
    """
    try:
        r = requests.get(url, timeout=30, verify=False)
        # #如果状态不是200，就会引发HTTPError异常
        r.raise_for_status()
        # r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


if __name__ == '__main__':
    url = 'https://www.huya.com/g/lol'
    html = getHTMLText(url)
    soup = BeautifulSoup(html, 'html.parser')

    # 提取目标值
    content_list = soup.find_all('span', class_='txt')
    # print(content_list)
    anchor_info = soup.find_all('i', class_='nick')
    heat_info = soup.find_all('i', class_='js-num')

    for info in content_list:
        tmp = info.get_text()
        print(tmp)
        # print(tmp.strip().split()[0])

