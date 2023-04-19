# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/4/19 10:06
# Desc  : 彼岸图网, 图片获取
import requests
from lxml import etree

if __name__ == '__main__':
    url = 'http://pic.netbian.com/4kdongman/'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    # 发起请求
    response = requests.get(url=url, headers=header)
    response.encoding = 'gbk'
    index_text = response.text

    # 解析成HTML
    tree = etree.HTML(index_text)

    for li in tree.xpath("//div[@class='slist']/ul[@class='clearfix']/li"):
        # 获取图片名称和链接
        image_name = li.xpath('./a/img/@alt')[0] + '.jpg'
        image_url = 'http://pic.netbian.com/' + li.xpath('./a/img/@src')[0]

        image_content = requests.get(url=image_url, headers=header).content
        # 写入数据
        with open('./data/' + image_name, 'wb') as fp:
            fp.write(image_content)
