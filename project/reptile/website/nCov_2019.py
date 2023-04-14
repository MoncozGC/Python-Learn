# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/12/27
# Desc  : nCov-2019 CN
# nCov-2019 CN 发布地址: https://www.chinacdc.cn/jkzt/crb/zl/szkb_11803/jszl_11809/
import re
from datetime import datetime

import pymysql
import requests
from bs4 import BeautifulSoup

from utils.connect_databases import getDatabaseOperation, load_config, load_database_config
from utils.time_util import time_cn_trans


def getHTMLText(url):
    """
    定义获取页面内容的方法
    :param url:
    :return:
    """
    try:
        # 设置浏览器访问头
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30'}
        r = requests.get(url, headers=headers)
        # #如果状态不是200，就会引发HTTPError异常
        r.raise_for_status()
        # r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def get_detailed_info(url_info):
    """
    获取具体链接数据
    :param url_info: 具体的链接信息
    :return: 详细文本信息数据
    """
    detailed_html = getHTMLText(url_info)
    detailed_soup = BeautifulSoup(detailed_html, 'html.parser')
    return detailed_soup.find_all('div', 'cn-main-detail')


def save_info(link_info, date, text):
    """
    保存文本数据至本地
    :param link_info: 链接地址及标题
    :param date: 时间
    :param text: 详细文本信息
    """
    file = open("../datas/nCov_2019_info.txt", 'a', encoding='utf-8')
    file.write(date + "\n" + link_info + "\n" + text + "\n\n")
    file.close()


def insert_database(ncov_date, ncov_title, ncov_info, ncov_link, create_date, create_time):
    """
    保存数据至mysql中
    """
    conn = pymysql.connect(connect_timeout=5, write_timeout=5, host='localhost', port=3306, user='root',
                           password='hadoop',
                           database='world', charset="utf8")
    # 建库语句: CREATE DATABASE world;
    # 建表语句
    # CREATE TABLE IF NOT EXISTS `ncov_2019`
    # (
    #     `ncov_date`   VARCHAR(24) COMMENT '新冠情况时间',
    #     `ncov_title`  VARCHAR(100) COMMENT '新冠情况详细标题',
    #     `ncov_info`   text COMMENT '新冠情况详细信息',
    #     `ncov_link`   VARCHAR(100) COMMENT '新冠情况详细地址',
    #     `create_date` VARCHAR(10) COMMENT '爬取日期',
    #     `create_time` VARCHAR(10) COMMENT '爬取时间',
    #     PRIMARY KEY (`ncov_date`)
    # ) ENGINE = InnoDB
    #   DEFAULT CHARSET = utf8
    # ;

    # 使用cursor()方法获取操作游标
    cursor = conn.cursor()
    info_sql = """INSERT INTO world.ncov_2019 (`ncov_date`, `ncov_title`, `ncov_info`, `ncov_link`,`create_date`, `create_time`) 
    VALUES (%s, %s, %s, %s, %s, %s)"""

    # 执行SQL
    cursor.execute(info_sql,
                   (ncov_date, ncov_title, ncov_info, ncov_link, create_date, create_time))

    # 4. 操作成功提交事务
    conn.commit()
    # 关闭游标
    cursor.close()


def insert_config(ncov_date, ncov_title, ncov_info, ncov_link, create_date, create_time):
    """
    利用配置文件的形式写入数据库中
    """
    sql = "INSERT INTO world.ncov_2019 (`ncov_date`, `ncov_title`, `ncov_info`, `ncov_link`,`create_date`, `create_time`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" \
          % (ncov_date, ncov_title, ncov_info, ncov_link, create_date, create_time)
    execute = getDatabaseOperation('world').execute(sql)
    return execute


def reptile_handle(content_list, insert_num, is_first):
    """
    爬虫逻辑处理
    """
    flag_num = 0
    for info in content_list:
        # 正则模糊匹配, 当满足时查询数据
        line_text = info.get_text()
        match_score = re.findall('.*疫情最新情况.*', line_text)
        if len(match_score) > 0:
            detailed_url = 'https://www.chinacdc.cn/jkzt/crb/zl/szkb_11803/jszl_11809/'
            detailed_href = info.get('href')
            href_url = detailed_url + info.get('href').strip('./')
            href_title = info.get_text()
            flag_num = flag_num + 1
            # 跳过动态首页第一条数据, 因为每页第一条数据为重复数据(展示的当天的疫情动态数据);
            if flag and flag_num == 1: continue
            # 拼接详细的链接地址及标题
            href_info = "详细的链接地址: " + href_url + " - " + href_title
            # 根据链接地址获取时间
            href_date = href_info.split('jszl_11809/')[1].split('/t')[0][0:4] + '年' + href_info.split('截至')[1].split('24时')[0]
            trans_date = time_cn_trans(href_date)
            print(trans_date + " - " + href_info)
            # 根据具体链接数据获取文本信息
            detailed_info = get_detailed_info(href_url)
            for detailed_date in detailed_info:
                detailed_text = detailed_date.get_text().strip()
                # print("信息获取\n\n " + detailed_text)
                # 将获取的文本信息保存到本地及数据库中
                try:
                    # insert_database(trans_date, href_title, detailed_text, href_url, n_create_date, n_create_time)
                    execute = insert_config(trans_date, href_title, detailed_text, href_url, n_create_date, n_create_time)
                    if execute > 0:
                        insert_num = insert_num + 1
                    save_info(href_info, trans_date, detailed_text)
                except Exception as e:
                    ""

                # 为False则表示仅爬取网页的最新数据, 爬取完后跳出
                if not is_first: return

        # 置空url, 避免url拼接时重复
        url = ''

    return insert_num


if __name__ == '__main__':
    # 填写项目名称, 需要根据项目名称去获取配置文件路径
    appRootDir, config = load_config('Python-Learn', ' ')
    load_database_config(config)

    # 解决Unverified HTTPS request is being made
    # requests.packages.urllib3.disable_warnings()
    n_create_date = datetime.today().date()
    n_create_time = datetime.today().strftime("%H:%M:%S")

    # 控制爬取分页条数, (1,50]
    reptile_num = 3
    # 控制是否只爬取最新的一条数据, 如果为False则 reptile_num必需等于 1, 否则会爬取旧数据
    is_first = True

    # flag/flag_num控制跳过网页的第一条数据, 避免在全量爬取时爬取重复数据
    flag = False

    # 记录条数
    insert_num = 0
    # 循环遍历数据
    for i in range(0, reptile_num):
        url = 'https://www.chinacdc.cn/jkzt/crb/zl/szkb_11803/jszl_11809/'
        if i == 0:
            url = url + "index" + ".html"
        else:
            url = url + "index_" + str(i) + ".html"
            flag = True
        print("获取疫情动态首页地址: " + url)
        html = getHTMLText(url)
        soup = BeautifulSoup(html, 'html.parser')

        # 提取目标值
        # content_list = soup.find_all('ul', class_='jal-item-list')
        content_list = soup.find_all('a')

        # 爬虫逻辑处理
        insert_num = reptile_handle(content_list, insert_num, is_first)

    if insert_num is not None and insert_num > 0:
        print("\n\n数据保存至本地及数据库中完成, 条数: " + str(insert_num))
    else:
        print("\n\n数据未改动, 未插入...")
