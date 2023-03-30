# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/3/28 10:55
# Desc  : 化学成分分析, 使用多线程的方式
# 化学名称与百度百科进行匹配, 打标记
# 在这个示例中，我们创建了一个名为 fetch_keyword_content 的函数，它接收一个关键词作为参数，然后发起请求并解析页面。main 函数中使用了 ThreadPoolExecutor 类来并发执行 fetch_keyword_content 函数。这将显著提高抓取速度。最后，我们将结果保存在一个Excel文件中。

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
        target_divs = soup.find_all('div', {'class': 'para', 'label-module': True})[0:6]

        # 遍历数据, 获取到其中的文本数据去除标签, 并且为空的不进入
        div_list = [div_para.text.strip() for div_para in target_divs if div_para.text]
        # 将数据拼接为字符串
        div_str = '\n'.join(div_list)

        if '化学' in str(div_str) or '分子' in str(div_str):
            return {'flag': 1, 'cmtn': keyword, 'content': div_str if div_str else 'None'}
        elif div_str is None:
            return {'flag': 0, 'cmtn': keyword, 'content': div_str if div_str else 'None'}
        elif '化学' not in str(div_str):
            return {'flag': 0, 'cmtn': keyword, 'content': div_str if div_str else 'None'}
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
