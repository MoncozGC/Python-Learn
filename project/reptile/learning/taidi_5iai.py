# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/4/13 14:16
# Desc  : 泰迪招聘
import requests


def recruit_5iai():
    url = 'https://www.5iai.com/api/resume/baseInfo/public/es'
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    param = {
        'pageSize': 10,
        'pageNumber': 1
    }
    requests_get = requests.get(url=url, headers=header, params=param)

    get_json = requests_get.json()
    print(get_json)


def job_5iai():
    url = 'https://www.5iai.com/api/enterprise/public/page'
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    param = {
        'pageSize': 10,
        'pageNumber': 1
    }
    requests_get = requests.get(url=url, headers=header, params=param)

    get_json = requests_get.json()


if __name__ == '__main__':
    recruit_5iai()
