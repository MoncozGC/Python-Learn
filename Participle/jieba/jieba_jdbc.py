# Author: MoncozGC
# Date  : 2021/12/8 16:41
# Desc  : 连接CK, 根据spuName字段进行分词处理
# encoding: utf-8

import jieba
import re
import functools
import operator
from clickhouse_driver import Client

ckClient = Client(host='xxxx', database='bds_dw', user='default', password='default')


def find_SourceData():
    """
    查找全量数据
    :return:
    """
    sql = "SELECT DISTINCT spuName FROM bds_dw.dws_sku_details_1d_loc WHERE spuName LIKE '%维生素%' "
    execute = ckClient.execute(sql)
    strSource = functools.reduce(operator.add, execute)
    for str in strSource:
        print(str)
    return strSource


def find_onwerOIDByName(spu_Name):
    """
    进入CK查询数据
    :param spu_Name: 匹配的词
    :return: 查询的语句
    https://www.yisu.com/zixun/447521.html
    """
    print(spu_Name)
    # print(continent)
    sql = "SELECT COUNT(ownerOID) FROM bds_dw.dws_sku_details_1d_loc WHERE 1=1"
    if spu_Name is not None:
        sql = sql + "AND ( spuName LIKE '%" + spu_Name + "%' )"

    execute = ckClient.execute(sql)
    # list = []
    # for i in res:
    #     # print(i)
    #     list.append(i)
    return execute


def cut_words(words):
    """
    实现切词功能
    :param words: 需要切词的字段
    :return: 切词完的字段
    """
    strSource = re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', str(words), re.S)
    # jieba.load_userdict("dict.txt")

    # 搜索引擎模式
    for strDict in strSource:
        seg_list = jieba.cut_for_search(strDict)
        # print(' '.join(seg_list))
        # 精准模式
        search = jieba.cut(strDict, cut_all=False)
        print(", ".join(search))


if __name__ == '__main__':
    spuName = ckClient.execute(
        "SELECT DISTINCT(spuName) as spuName  FROM bds_dw.dws_sku_details_1d_loc dsddl WHERE spuName LIKE '%维生素%' ")

    # strSource = functools.reduce(operator.add, spuName)
    # 利用正则匹配 去除特殊字符
    strSource = re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', str(spuName), re.S)
    # print(strSource)

    # jieba.load_userdict("dict.txt")

    # 使用paddle模式
    # for strDict in strSource:
    #     seg_list = jieba.cut(strDict, use_paddle=True)
    #     print(' '.join(seg_list))

    # 搜索引擎模式
    for strDict in strSource:
        seg_list = jieba.cut_for_search(strDict)
        # print(' '.join(seg_list))cut_for_search
        # 精准模式
        search = jieba.cut(strDict, cut_all=False)
        print(", ".join(search))

    # 查询全量数据

    # print(find_SourceData)

    sql = "SELECT DISTINCT spuName FROM bds_dw.dws_sku_details_1d_loc WHERE spuName LIKE '%维生素%' "
    execute = ckClient.execute(sql)
    strSource = functools.reduce(operator.add, execute)
    print(strSource)
    # 查找对应的ownerOID
    # world_by_name = find_worldByName("维生素")
    # world_by_name = find_onwerOIDByName("维生素")
    # print(world_by_name)

    # 进行切词
    # words = cut_words("")
    # print(words)
