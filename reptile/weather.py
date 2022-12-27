# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/12/27
# Desc  : 天气数据爬取, 并且入库
# 导入相关的包
from datetime import datetime

import pymysql
import requests
import bs4
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings('ignore')


# 定义获取页面内容的方法
def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30, verify=False)
        # #如果状态不是200，就会引发HTTPError异常
        r.raise_for_status()
        # r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def insert_database(city_code, city_name, weather_day, weather_situation, temperature, air_quality, wind_situation,
                    create_date, create_time):
    conn = pymysql.connect(connect_timeout=5, write_timeout=5, host='localhost', port=3306, user='root',
                           password='hadoop',
                           database='world', charset="utf8")
    # 建库语句: CREATE DATABASE test;
    # 建表语句
    # CREATE TABLE IF NOT EXISTS `weather`
    # (
    #     `id`                INT UNSIGNED AUTO_INCREMENT COMMENT 'id',
    #     `city_name`         INT COMMENT '天气城市',
    #     `weather_day`       VARCHAR(100) NOT NULL COMMENT '天气日期',
    #     `weather_situation` VARCHAR(40)  NOT NULL COMMENT '天气情况',
    #     `temperature`         VARCHAR(40) COMMENT '天气温度',
    #     `air_quality`       VARCHAR(40) COMMENT '空气质量',
    #     `wind_situation`    VARCHAR(40) COMMENT '风向情况',
    #     create_time         datetime DEFAULT CURRENT_TIMESTAMP COMMENT '爬取时间',
    #     PRIMARY KEY (`id`)
    # ) ENGINE = InnoDB
    #   DEFAULT CHARSET = utf8;

    # 使用cursor()方法获取操作游标
    cursor = conn.cursor()
    info_sql = """INSERT INTO world.weather (`city_code`,`city_name`, `weather_day`, `weather_situation`, `temperature`, `air_quality`, `wind_situation`, `create_date`, `create_time`) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    # 执行SQL
    cursor.execute(info_sql,
                   (city_code, city_name, weather_day, weather_situation, temperature, air_quality,
                    wind_situation, create_date, create_time))

    # 4. 操作成功提交事务
    conn.commit()
    # 关闭游标
    cursor.close()


def date_conversion(date):
    """
    时间转换: 今天 -> 周二; 明天 -> 周三
    """
    week_list = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    if date == '今天':
        return week_list[datetime.today().isoweekday() - 1]
    elif date == '明天':
        return week_list[datetime.today().isoweekday()]
    else:
        return date


if __name__ == '__main__':
    today = datetime.today().date()
    create_time = datetime.today().strftime("%H:%M:%S")
    print(create_time)
    crawling_city = ['101250203?湘乡', '101250101?长沙']
    # 爬取 长沙的天气
    # url = 'https://tianqi.so.com/weather/'
    for i in crawling_city:
        url = 'https://tianqi.so.com/weather/' + i
        city_code = i.split('?')[0]
        city_name = i.split('?')[1]
        # print(city_code + "-" + city_name)
        html = getHTMLText(url)
        soup = BeautifulSoup(html, 'html.parser')
        url = ''

        # 提取目标值
        content_list = soup.find_all('ul', class_='weather-columns')
        city_list = soup.find_all('strong', class_='change-title')
        city = ''
        for c in city_list:
            city = c.get_text()

        # 格式化输出
        tplt = "{0:^8}\t{1:^8}\t{2:^8}\t{3:^8}\t{4:^8}\t{5:^8}"
        print(tplt.format('城市', '日期', '天气情况', '温度', '天气质量', '凤向情况'))
        for c in content_list:
            tmp = c.get_text()
            split_str = date_conversion(tmp.strip().split()[0])
            t0 = split_str + tmp.strip().split()[1]
            t1 = tmp.strip().split()[2]
            t2 = tmp.strip().split()[3].split('℃')[0] + '℃'
            t3 = tmp.strip().split()[3].split('℃')[1][0]
            t4 = tmp.strip().split()[3].split('℃')[1][1:] + " " + tmp.strip().split()[4]
            print(tplt.format(city, t0, t1, t2, t3, t4))
            insert_database(city_code, city, t0, t1, t2, t3, t4, today, create_time)