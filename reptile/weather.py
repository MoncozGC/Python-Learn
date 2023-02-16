# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/12/27
# Desc  : 天气数据爬取, 并且入库
# 导入相关的包
import warnings
from datetime import datetime

import pymysql
import requests
from bs4 import BeautifulSoup

from utils.comm_util import chinese_conversion

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


def insert_database(city_code, city_name, week, weather_day, weather_situation, temperature_min, temperature_max,
                    air_quality,
                    wind_situation,
                    create_date, create_time):
    conn = pymysql.connect(connect_timeout=5, write_timeout=5, host='192.168.31.219', port=3306, user='root',
                           password='hadoop',
                           database='dev', charset="utf8")
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
    info_sql = """INSERT INTO dev.weather (`city_code`,`city_name`, `week`,`weather_day`, `weather_situation`, `temperature_min`, `temperature_max`, `air_quality`, `wind_situation`, `create_date`, `create_time`) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    # 执行SQL
    cursor.execute(info_sql,
                   (city_code, city_name, week, weather_day, weather_situation, temperature_min, temperature_max,
                    air_quality,
                    wind_situation, create_date, create_time))

    # 4. 操作成功提交事务
    conn.commit()
    # 关闭游标
    cursor.close()


def date_conversion(date):
    """
    时间转换: 今天 -> 星期二; 明天 -> 星期三
    """
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    if date == '今天':
        return week_list[datetime.today().isoweekday() - 1]
    elif date == '明天':
        return week_list[datetime.today().isoweekday()]
    else:
        # 将 周 替换成 星期
        return date.replace('周', '星期').replace('星期日', '星期天')


if __name__ == '__main__':
    today = datetime.today().date()
    create_time = datetime.today().strftime("%H:%M:%S")
    print(create_time)
    crawling_city = ['101250101?长沙']
    # crawling_city = ['101250203?湘乡', '101250101?长沙', '101010100?北京', '101020100?上海', '101280601?深圳', '101310101?海南', '101040100?重庆', '101240901?萍乡', '101050101?哈尔滨']
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
        tplt = "{0:^8}\t{1:^8}\t{2:^8}\t{3:^8}\t{4:^8}\t{5:^8}\t{6:^8}\t{7:^8}"
        print(tplt.format('城市', 'Week', '日期', '天气情况', '最低温度', '最高温度', '天气质量', '凤向情况'))
        insert_num = 0
        for c in content_list:
            tmp = c.get_text()
            split_str = date_conversion(tmp.strip().split()[0])
            week = split_str
            date_target = tmp.split()[1].strip("()")
            t1 = tmp.strip().split()[2]
            temperature_min = tmp.strip().split()[3].split('℃')[0].split('/')[0] + '℃'
            temperature_max = tmp.strip().split()[3].split('℃')[0].split('/')[1] + '℃'
            t3 = tmp.strip().split()[3].split('℃')[1][0]
            t4 = tmp.strip().split()[3].split('℃')[1][1:] + " " + tmp.strip().split()[4]
            print(tplt.format(city, week, date_target, t1, temperature_min, temperature_max, t3, t4))
            try:
                insert_database(city_code, city, week, date_target, t1, temperature_min, temperature_max, t3, t4, today,
                                create_time)
                insert_num = insert_num + 1
            except Exception as e:
                ""

        if insert_num > 0:
            # ljust右侧填充对齐字符串
            print(chinese_conversion(city_name).ljust(12) + "共插入数据: " + str(insert_num))
        else:
            print(chinese_conversion(city_name).ljust(12) + "数据未改动, 无需插入...")
