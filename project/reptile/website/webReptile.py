# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/8/17 19:31
# Desc  : 中国湘乡网数据爬取
import re
from urllib import request

from utils.comm_util import print_ts


def write_file(name):
    file = 'guest3.txt'
    with open(file, 'a', encoding='utf-8') as fileobj:
        fileobj.write(name + '\n')

    # with open(file, 'r', encoding='utf-8') as fileobj:
    #     for line in fileobj:
    #         print(line.rstrip())


def get_reply(year, day):
    # 定义url

    # url = 'https://xiangxiang.rednet.cn/channel/8060_10.html'
    # https://xiangxiang.rednet.cn/channel/2021/0101/8060.html
    # 拼接时间
    url = f'https://xiangxiang.rednet.cn/channel/{year}/{day}/8060.html'

    print_ts("%s, %s, 访问地址: %s" % (year, day, url))

    write_file(day)
    write_file(f"访问地址: {url}")

    try:
        # time.sleep(3)
        # 定义请求头
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39'}
        # 定义请求，传入请求头
        req = request.Request(url, headers=headers)
        # 打开网页
        resp = request.urlopen(req)
        # 打印响应，解码
        # print(resp.read().decode('utf-8'))
        content = resp.read().decode('utf-8')
        # 正则表达式获取需要的网页信息
        # pattern=re.compile(r'<a.*>title=(.*?)\s{1}.?>(.*?)</a>')
        # pattern = re.compile(r'<font size=(.*?)>(.*?)</font>')
        # pattern = re.compile(r'<div class="newsmod">(.*?)</div>')
        # pattern = re.compile(r'<h3><a href="(.*?)"(.*?)</h3>')
        pattern = re.compile(r'title="(.*?)"(.*?)</a></h3>')
        # 匹配html
        items = re.findall(pattern, content)
        # 打印解析内容
        for i in items:
            # print('标题:' + i[0] + " " + '内容' + i[1])
            # 写入文件
            write_file(str(i))
            # 输出控制台
            print_ts(i)

    except request as e:
        # 打印响应码
        if hasattr(e, 'code'):
            print(e.code)
        # 打印异常
        if hasattr(e, 'reason'):
            print(e.reason)


if __name__ == '__main__':
    year, day = '2022', '0127'

    # get_reply(year, day)

    import datetime

    # 循环时间, 拼接至url中爬取数据
    begin = datetime.date(2022, 1, 1)
    end = datetime.date(2022, 1, 17)
    d = begin
    delta = datetime.timedelta(days=1)
    while d <= end:
        year = d.strftime("%Y")
        day = d.strftime("%m%d")
        print_ts(year, day)
        get_reply(year, day)
        d += delta
