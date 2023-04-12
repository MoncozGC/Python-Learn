# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/4/12
# Desc  : 使用request
import requests

if __name__ == '__main__':
    url = 'https://www.baidu.com'
    # UA解析
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69"}
    # 发起get请求
    requests_get = requests.get(url=url, headers=headers)
    # 获取请求的文本
    get_text = requests_get.text
    print(get_text)
    # 写入文件
    with open('./baidu.html', 'w', encoding='utf-8') as fp:
        fp.write(get_text)
    print("end")
