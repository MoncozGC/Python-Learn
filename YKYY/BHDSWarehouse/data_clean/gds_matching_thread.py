# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/3/28 10:55
# Desc  : 化学成分分析, 使用多线程的方式
# 化学名称与百度百科进行匹配, 打标记

import urllib.parse
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests
from bs4 import BeautifulSoup

from utils.comm_util import print_ts


def fetch_keyword_content(keyword):
    base_url = 'https://baike.baidu.com/item/'
    encoded_keyword = urllib.parse.quote(keyword)
    url = base_url + encoded_keyword

    response = requests.get(url)
    print_ts("查询数据: " + keyword + " - " + url)
    if response.status_code == 200:
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        target_divs = soup.find('div', {'class': 'para', 'label-module': True})

        if '化学' in str(target_divs) or '分子' in str(target_divs):
            return {'flag': 1, 'cmtn': keyword, 'content': target_divs.text if target_divs else 'None'}
        elif target_divs is None:
            return {'flag': 0, 'cmtn': keyword, 'content': target_divs.text if target_divs else 'None'}
        elif '化学' not in str(target_divs):
            return {'flag': 0, 'cmtn': keyword, 'content': target_divs.text if target_divs else 'None'}
    else:
        return {'cmtn': keyword, 'content': 'Request failed'}


def main():
    with open('../data/化学名称字典.txt', 'r', encoding='utf-8') as file:
        keywords = [line.strip() for line in file]

    results = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fetch_keyword_content, keyword): keyword for keyword in keywords}
        for future in futures:
            results.append(future.result())

    df = pd.DataFrame(results)
    writer = pd.ExcelWriter('../data/化学名称与百度百科匹配v2.xlsx')
    df.to_excel(writer, sheet_name='匹配数据', index=False)
    writer.save()
    print("数据写入完成")


if __name__ == '__main__':
    main()
