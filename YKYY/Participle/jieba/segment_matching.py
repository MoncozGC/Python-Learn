# Author: MoncozGC
# Date  : 2021/12/16 15:04
# Desc  : 切词匹配功能实现
# encoding: utf-8
import functools
import operator
import re
import pandas as pd
from collections import Counter

import jieba
from clickhouse_driver import Client

# 输入输出文件信息
origanword_file = "../datas/spuName.txt"
stopword_file = "../datas/stopwords.dat"
outputword_file = "../sorted_words.json"
ckClient = Client(host='xxxx', database='bds_dw', user='default', password='default')


def connect_ck():
    spuName = ckClient.execute(
        "SELECT DISTINCT(spuName) as spuName  FROM bds_dw.dws_sku_details_1d_loc dsddl WHERE spuName LIKE '%维生素%' ")
    strSource = functools.reduce(operator.add, spuName)
    # 将查询的数据以udf-8编码保存到文件
    # f = open('spuName.txt', mode='w',encoding='utf-8')
    # f.write(strSource.__str__())
    # f.close()

    return strSource


# 按行读取文件，返回文件的行字符串列表
def read_file(file_name):
    fp = open(file_name, "r", encoding="utf-8")
    content_lines = fp.readlines()
    fp.close()
    # 去除行末的换行符，否则会在停用词匹配的过程中产生干扰
    for i in range(len(content_lines)):
        content_lines[i] = content_lines[i].rstrip("\n")
    return content_lines


# 对短信中的用户名前缀和内部的url链接进行过滤删除
def regex_change(line):
    # 前缀的正则
    username_regex = re.compile(r"^\d+::")
    # URL，为了防止对中文的过滤，所以使用[a-zA-Z0-9]而不是\w
    url_regex = re.compile(r"""
        (https?://)?
        ([a-zA-Z0-9]+)
        (\.[a-zA-Z0-9]+)
        (\.[a-zA-Z0-9]+)*
        (/[a-zA-Z0-9]+)*
    """, re.VERBOSE | re.IGNORECASE)
    # 剔除日期
    data_regex = re.compile(u"""        #utf-8编码
        年 |
        月 |
        日 |
        (周一) |
        (周二) | 
        (周三) | 
        (周四) | 
        (周五) | 
        (周六)
    """, re.VERBOSE)
    # 剔除所有数字
    decimal_regex = re.compile(r"[^a-zA-Z]\d+")
    # 剔除空格
    space_regex = re.compile(r"\s+")

    line = username_regex.sub(r"", line)
    line = url_regex.sub(r"", line)
    line = data_regex.sub(r"", line)
    line = decimal_regex.sub(r"", line)
    line = space_regex.sub(r"", line)

    return line


def delete_stopwords(words):
    stopwords = connect_ck()
    all_words = []

    for line in words:
        all_words += [word for word in jieba.cut(line) if word not in stopwords]

    dict_words = dict(Counter(all_words))
    return dict_words


if __name__ == '__main__':
    # 获取ClickHouse商品名信息
    # words = connect_ck()
    # print(words)
    # 按行读取文件
    lines = read_file(origanword_file)
    # print(lines)

    for i in range(len(lines)):
        lines[i] = regex_change(lines[i])
        print(lines)
    #
    # # 去除停用词, 并返回词袋字典
    # # print(delete_stopwords(words))
    # bow_words = delete_stopwords(words)
    #
    # sorted_bow = sorted(bow_words.items(), key=lambda d: d[1], reverse=True)
    #
    # for words in sorted_bow:
    #     print(words)

    print(connect_ck)