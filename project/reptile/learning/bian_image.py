# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/4/19 10:06
# Desc  : 彼岸图网, 图片获取
# 1. 从首页获取到图片
# 2. 通过下钻页面获取到尺寸更大的图片
import os

import requests
from lxml import etree


def small_pic():
    """
    只能获取到小图片, 450*287
    :return:
    """
    # 获取图片名称和链接
    image_name = li.xpath('./a/img/@alt')[0] + '.jpg'
    image_url = url_prefix + li.xpath('./a/img/@src')[0]

    image_content = requests.get(url=image_url, headers=header).content
    # 写入数据
    with open('./data/' + image_name, 'wb') as fp:
        fp.write(image_content)


def big_pic():
    """
    获取到大图片, 1202*676
    :return:
    """
    # 通过首页图片中的a标签, 获取到下钻页面的子链接
    child_url = url_prefix + li.xpath('./a/@href')[0]

    child_response = requests.get(url=child_url, headers=header)
    child_response.encoding = 'gbk'
    child_tree = etree.HTML(child_response.text)

    # 获取子链接下的图片链接
    for div in child_tree.xpath("//div[@class='view']"):
        image_url = url_prefix + div.xpath("./div[@class='photo-pic']/a[@id='img']/img/@src")[0]
        image_name = div.xpath("./div[@class='photo-hd']/h1/text()")[0]
        print(image_url, image_name)

        child_content = requests.get(url=image_url, headers=header).content

        # 保持图片
        persistence(image_name, child_content)


def persistence(i_name, i_content):
    """
    持久化数据
    """
    i_name = './data/' + i_name + '.jpg'
    with open(i_name, 'wb') as fp:
        fp.write(i_content)


if __name__ == '__main__':
    url = 'http://pic.netbian.com/4kdongman/'
    url_prefix = 'http://pic.netbian.com/'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    # 发起请求
    response = requests.get(url=url, headers=header)
    response.encoding = 'gbk'
    index_text = response.text

    # 解析成HTML
    tree = etree.HTML(index_text)

    if not os.path.exists('./data'):
        os.mkdir('./data')

    for li in tree.xpath("//div[@class='slist']/ul[@class='clearfix']/li"):
        # small_pic()
        big_pic()
