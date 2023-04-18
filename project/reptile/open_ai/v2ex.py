# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/4/18 11:41
# Desc  : 使用xpath获取v2ex中的内容数据
import datetime

import requests
from lxml import etree

if __name__ == '__main__':
    proxies = {
        'http': 'http://127.0.0.1:10809',
        'https': 'http://127.0.0.1:10809',
    }

    response = requests.get('https://www.v2ex.com/?tab=hot', proxies=proxies)
    content = response.text

    tree = etree.HTML(content)

    """
    xpath
    //: 代表所有位置
    []: 筛选条件
    @ : 标签属性, @class="cell item" 表示这个class为cell item
    contains(): 检查指定的字符串出现在指定的属性中
    text(): 获取文本信息
    """
    # 获取最大宽带用来进行文本对齐
    max_user_width = 0
    max_title_width = 0

    results = []
    for item in tree.xpath('//div[@class="cell item"]'):
        user = item.xpath('.//a[contains(@href,"/member/")]/text()')[0]
        title = item.xpath('.//a[contains(@href,"/t/")]/text()')[0]
        url = item.xpath('.//a[contains(@href, "/t/")]/@href')[0]
        url = 'https://www.v2ex.com/' + url
        reply_num = item.xpath('.//a[@class="count_livid"]/text()')[0]
        max_user_width = max(max_user_width, len(user))
        max_title_width = max(max_title_width, len(title))

        results.append({"user": user, "title": title, "url": url, "reply_num": reply_num})

    now_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('v2ex.text', 'a', encoding='utf-8') as fp:
        fp.write("\n\n数据获取时间: {}\n".format(now_date))
        for result in results:
            # :<{width_variable}}表示左对齐, 变量可改变仅是占位符
            text = "用户: {user:<{user_width}}\t标题: {title:<{title_width}}\t链接: {url}\t回复数: {reply_num}\r".format(user_width=max_user_width, title_width=max_title_width, **result)
            fp.write(text)

    print("文件追加完成")
