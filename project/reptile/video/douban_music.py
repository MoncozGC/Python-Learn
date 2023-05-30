# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023-05-29
# Desc  : 爬取豆瓣音乐Top250数据, https://music.douban.com/top250

import pandas as pd
import requests
from lxml import etree
from pandas import DataFrame


def remove_special_characters(text):
    """
    去除特殊字符
    :param text:
    :return:
    """
    special_characters = ['!', '@', '\n', ' ']
    for char in special_characters:
        text = text.replace(char, '')
    return text


def df_transform(data_list):
    """
    读取list中的数据转换为df
    :param data_list:
    :return:
    """
    # 构建DataFrame
    origin_data = pd.DataFrame([data_list], columns=['title', 'singer', 'date', 'type', 'review', 'review_info'])
    # 对多个列同时应用 explode 函数
    """
    因为review, review_info的数据结构为数组, review是用户, review_info是对应用户的评论
    所以需要将这两个字段膨胀开
    """
    explode_data = origin_data.apply(lambda x: x.explode(ignore_index=True) if x.name in ['review', 'review_info'] else x)
    # 填充数据, 因为在对两个字段进行explode后会导致没有进行explode的数据变成nan
    # method=ffill, 代表向前填充数据, 即将非空值向下填充到空值所在的行
    # inplace=True, 代表在原始的df中进行操作
    explode_data['title'].fillna(method='ffill', inplace=True)
    explode_data['singer'].fillna(method='ffill', inplace=True)
    explode_data['date'].fillna(method='ffill', inplace=True)
    explode_data['type'].fillna(method='ffill', inplace=True)

    # 数据去噪
    for colum in explode_data.columns:
        if explode_data[colum].dtype == 'object':
            explode_data[colum] = explode_data[colum].astype(str).apply(remove_special_characters)

    return explode_data


if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    url = "https://music.douban.com/top250"
    file_name = "data/douban_music.csv"

    num = 0
    for num_item in range(0, 10):
        param = {
            'start': num
        }
        requests_get = requests.get(url=url, headers=headers, params=param)
        # requests_get.encoding = 'gbk'
        child_tree = etree.HTML(requests_get.text)

        dataset, reviews, reviews_info = [], '', ''
        i = 0
        for item in child_tree.xpath("//div[@class='pl2']"):
            # 音乐名称
            title = item.xpath("a/text()")[0]
            # 详情链接, 获取评论
            href = item.xpath("a/@href")[0]
            # 详情信息
            detail = item.xpath("p[@class='pl']/text()")[0]
            # 歌手, 发行时间, 专辑类型, 介质, 音乐类别
            details = detail.split(' / ')
            # 评论人数
            comments = item.xpath("div[@class='star clearfix']/span[@class='pl']/text()")[0]

            # 访问子链接, 获取评论信息
            child_get = requests.get(url=href, headers=headers)
            child = etree.HTML(child_get.text)

            # 获取评论信息
            for child_item in child.xpath("//div[@class='review-list  ']"):
                # 评论人员
                reviews = child_item.xpath("//div/div[@id]/header[@class='main-hd']/a[@class='name']/text()")
                # 评论具体信息
                reviews_info = child_item.xpath("//div/div[@id]/div[@class='main-bd']/div[@id]/div[@class='short-content']/text()")
                # 移除内容只有 ) 的数据
                reviews_info = [item.strip() for item in reviews_info if ')' not in item]

            dataset.append((title, details[0], details[1], details[4], reviews, reviews_info))
            i += 1
            # 控制查询的数据
            # if i > 3:
            #     break
            print(title)
            # time.sleep(3)
        num += 25
        print(num)

        # 将dataset转化为df, 并以追加的模式写入csv文件中
        for item in dataset:
            result_df: DataFrame = df_transform(item)
            result_df.to_csv(file_name, mode='a', header=False, index=False)
