# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/4/21
# Desc  : 模拟客户端爬取JD数据
import time

import pandas as pd
from pyecharts.charts import Pie
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

if __name__ == "__main__":
    word = input("请输入要爬取的商品名称")
    page_size = int(input("请输入要爬取的页数"))
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # 设置无界面模式
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # 创建一个浏览器驱动器的对象
    # driver = webdriver.Edge()
    # 通过驱动器去打开京东的首页
    driver.get("https://www.jd.com")
    time.sleep(2)
    # 找到搜索框
    input_box = driver.find_element(By.ID, "key")
    input_box.send_keys(word)
    input_box.send_keys(Keys.ENTER)
    # html = driver.page_source
    # df = pd.read_html(html)[0]
    names, prices, commits, shops = [], [], [], []
    for i in range(page_size):
        # 将滚动条拖到最下面
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')

        # 停顿3秒，等待数据刷新
        time.sleep(3)
        good_list = driver.find_elements(By.XPATH, '//*[@id="J_goodsList"]/ul/li')

        # 便利每页所需爬取的内容
        for good in good_list:
            price = good.find_element(By.CLASS_NAME, "p-price").text,
            name = good.find_element(By.CLASS_NAME, "p-name").text,
            commit = good.find_element(By.CLASS_NAME, "p-commit").text,
            shop = good.find_element(By.CLASS_NAME, "p-shop").text
            # 将爬取的数据赋值给空列表中
            names.append(name[0])
            prices.append(price[0])
            commits.append(commit[0])
            shops.append(shop)

        driver.find_element(By.CLASS_NAME, "pn-prev").click()
        # 停顿3秒，等待数据刷新
        time.sleep(3)
        print("执行一次")
    df = pd.DataFrame(
        {
            "价格": prices,
            "标题": names,
            "评论数": commits,
            "出版社": shops
        })
    df.to_excel("./data/jd_data.xlsx")

    # 按数量统计出前10名的数据
    sort_data = df.groupby("出版社").size().sort_values(ascending=True).head(10)

    # 进行数据治理。将数据按图表所需要的数据进行融合，重要！！！变为这种格式：[‘xx_xx’，1]
    data = [list(z) for z in zip(sort_data.index.tolist(),
                                 sort_data.values.tolist())]
    # print(data)
    # 绘制饼图
    pip = Pie()
    pip.add(series_name="排名",
            data_pair=data)

    pip.render(path="./data/jd_pie.html")
