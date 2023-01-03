# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/12/27
# Desc  : nCov-2019 CN
# 导入相关的包
import re
from datetime import datetime

import pymysql
import requests
import bs4
from bs4 import BeautifulSoup
import warnings

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
    # 解决Unverified HTTPS request is being made
    requests.packages.urllib3.disable_warnings()
    url = 'https://www.chinacdc.cn/jkzt/crb/zl/szkb_11803/jszl_11809/'

    html = getHTMLText(url)
    soup = BeautifulSoup(html, 'html.parser')

    # 提取目标值
    # content_list = soup.find_all('ul', class_='jal-item-list')
    content_list = soup.find_all('a')

    for info in content_list:
        # 正则模糊匹配, 当满足时查询数据
        line_text = info.get_text()
        match_score = re.findall('.*疫情最新情况.*', line_text)
        if len(match_score) > 0:
            detailed_href = url + info.get('href').strip('./')
            tmp = info.get_text()
            print(detailed_href + " - " + tmp)
            # print(tmp.strip().split()[0])