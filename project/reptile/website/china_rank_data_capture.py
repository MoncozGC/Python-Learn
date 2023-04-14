# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/12/27
# Desc  : 中国大学排名数据抓取
import json
import requests


def getHTMLText(url):
    '''从网络上获取大学排名网页内容'''
    try:
        r = requests.get(url, timeout=40)
        # #如果状态不是200，就会引发HTTPError异常
        r.raise_for_status()
        # r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def printUnivList(ulist, html, num):
    '''提取 html 网页内容中 前 num 名大学信息到 ulist列表中  '''
    data = json.loads(html)  # 对数据进行解码
    # 提取 数据 rankings 包含的内容
    content = data['data']['rankings']

    # 把 学校的相关信息放到  ulist 里面
    for i in range(num):
        index = content[i]['rankOverall']
        name = content[i]['univNameCn']
        score = content[i]['score']
        tage = content[i]['univTags']
        category = content[i]['univCategory']
        ulist.append([index, name, score, tage, category])

        # 打印前 num 名的大学
    tplt = "{0:^10}\t{1:{3}^10}\t{2:^10}\t{4:^15}\t{5:^10}"  # {1:{3}^10} 中的 {3} 代表取第三个参数
    print(tplt.format("排名 ", "学校名称", "总分", chr(12288), "标签", "类型"))  # chr(12288) 代表中文空格
    for i in range(num):
        u = ulist[i]
        # 将标签的数组类型转换为字符串
        tage_str = "/".join(u[3])
        print(tplt.format(u[0], u[1], u[2], chr(12288), tage_str, u[4]))  # chr(12288) 代表中文空格


def main():
    uinfo = []
    url = 'https://www.shanghairanking.cn/api/pub/v1/bcur?bcur_type=11&year=2022'
    html = getHTMLText(url)  # 获取大学排名内容
    printUnivList(uinfo, html, 30)  # 输出 排名前30 的大学内容


main()
