# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023-08-15
# Desc  : 企名片破解加密: https://www.qimingpian.com/finosda/project/ainvestment
import execjs
import requests

if __name__ == '__main__':
    # F12 bash格式复制, 使用 https://curlconverter.com/ 生成代码
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.qimingpian.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'time_interval': '',
        'industry': '',
        'page': '1',
        'num': '20',
        'unionid': '',
    }

    response = requests.post('https://vipapi.qimingpian.cn/DataList/investmentTotalVip', headers=headers, data=data).json()
    # print(response['encrypt_data'])
    # 读取js文件, 指定编码 r: 读取模式
    with open("./qimingpian.js", 'r', encoding='utf-8') as f:
        js_file = f.read()

    # 执行jscode, 主方法为: s
    ctx = execjs.compile(js_file).call('s', response['encrypt_data'])
    # print(ctx)
