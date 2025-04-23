# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2025-04-21
# Desc  :
import json
import time

from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.connect_mysql import *
from utils.connect_redis import RedisPoolManager


def save_player_data(data_json):
    try:
        # 开始事务
        begin_transaction()  # 根据您的数据库连接方式实现

        # 1. 插入选手基本信息
        player_sql = """
        INSERT INTO lol.players (
            game_id, real_name, age, current_team, region, 
            last_position, birthplace, status, 
            international_appearances, world_championships, origin_json
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE real_name = VALUES(real_name)

        """

        if isinstance(data_json['other_info']['赛区'], list):
            data_json['other_info']['赛区'] = ','.join(data_json['other_info']['赛区'])
        player_params = (
            data_json['basic_info']['id'],
            data_json['basic_info']['name'],
            data_json['basic_info']['age'],
            data_json['basic_info']['current_team'],
            data_json['other_info']['赛区'],
            data_json['other_info']['最后担任职位'],
            data_json['other_info']['出生地'],
            data_json['other_info']['状态'],
            int(data_json['other_info']['国际赛次数']),
            int(data_json['other_info']['世界冠军次数']),
            json.dumps(data_json, ensure_ascii=False),
        )
        execute_one(player_sql, player_params)

        # 获取最后插入ID
        player_id = query_data("""SELECT player_id FROM lol.players WHERE game_id = '%s' """ % data_json['basic_info']['id'])[0][0]

        # 2. 插入历史战队
        if 'history_teams' in data_json and data_json['history_teams']:
            team_sql = """
            INSERT INTO lol.player_teams (
                player_id, team_name, join_order
            ) VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE team_name=VALUES(team_name), join_order=VALUES(join_order)
            """
            for idx, team in enumerate(data_json['history_teams'], 1):
                execute_one(team_sql, (player_id, team, idx))

        # 3. 插入擅长英雄
        if 'champion_pool' in data_json and data_json['champion_pool']:
            champion_sql = """
            INSERT INTO lol.player_champions (
                player_id, champion_name
            ) VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE champion_name=VALUES(champion_name)
            """
            for champion in data_json['champion_pool']:
                execute_one(champion_sql, (player_id, champion))

        # 提交事务
        commit()  # 根据您的数据库连接方式实现
        return True

    except Exception as e:
        # 回滚事务
        rollback()  # 根据您的数据库连接方式实现
        print(f"保存数据失败: {str(e)}, 原始结构: {data_json}")
        return False


def parse_player_modal(html_content):
    """解析HTML, 格式化成JSON"""
    try:
        # 解析HTML
        html_tree = etree.HTML(html_content)

        # 初始化结果字典
        player_data = {
            "basic_info": {},
            "history_teams": [],
            "champion_pool": [],
            "other_info": {}
        }

        # 提取选手ID/姓名
        player_id = html_tree.xpath("//h2[@class='answer-id']/text()")[0].strip()
        player_data["basic_info"]["id"] = player_id

        # 提取所有信息项
        items = html_tree.xpath("//ul[@class='answer-list']/li")

        for item in items:
            # 获取字段名和值
            field_name = item.xpath(".//strong/text()")[0].strip().replace("：", "")
            values = [span.text.strip() for span in item.xpath(".//span")]

            # 根据字段名分类存储
            if field_name == "ID/姓名":
                player_data["basic_info"]["name"] = values[1] if len(values) > 1 else ""
            elif field_name == "年龄":
                player_data["basic_info"]["age"] = int(values[0]) if values[0].isdigit() else -1
            elif field_name == "战队":
                player_data["basic_info"]["current_team"] = values[0]
            elif field_name == "选手身份的历史战队":
                player_data["history_teams"] = values
            elif field_name == "擅长英雄":
                player_data["champion_pool"] = values
            elif field_name in ["赛区", "最后担任职位", "出生地", "选手身份的状态", "国际赛次数", "世界冠军次数"]:
                key = field_name.replace("选手身份的", "").lower()
                player_data["other_info"][key] = values[0] if len(values) == 1 else values

        # print(json.dumps(player_data, indent=2, ensure_ascii=False))

        return player_data
    except Exception as e:
        print(f"解析数据异常: {str(e)}")
        return False


def html_parsing(driver):
    # 打开网页
    driver.get("https://guessassin.xyz/#/game")

    # 等待弹出显示
    modal = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-overlay"))
    )
    try:
        modal.find_element(By.XPATH, "//button[contains(text(), '原题库')]").click()  # 点击按钮

        modal.find_element(By.CSS_SELECTOR, ".btn-primary").click()  # 确认按钮
        name_set = set()
        error_list = ['Kid']
        redis_mgr = RedisPoolManager()

        for i in range(0, 1000):
            # 投降
            driver.find_element(By.CSS_SELECTOR, ".surrender-btn").click()
            pop_html = driver.find_element(By.CSS_SELECTOR, ".answer-modal").get_attribute('outerHTML')
            pop_id = pop_html.split('class="answer-id">')[1].split('</h2><button')[0]  # 获取到弹窗标题
            print(f"找到数据: {i} {pop_id}")
            redis_mgr.redis_conn.lpush("guessassin", pop_id)  # 写入redis
            if pop_id in error_list:
                continue
            player_modal = parse_player_modal(pop_html)

            if not player_modal:
                continue

            if player_modal['basic_info']['id'] in name_set:
                print(f"已存在: {player_modal['basic_info']['id']} =====")
            name_set.add(player_modal['basic_info']['id'])
            save_player_data(player_modal)

            # 点击再来一局
            driver.find_element(By.XPATH, "//button[contains(@class, 'btn-primary') and contains(text(), '再来一局')]").click()
            # 点击关闭弹窗, 可取消
            # driver.find_element(By.CSS_SELECTOR, ".close-btn").click()

            print(f"写入数据: {i} {player_modal['basic_info']['id']}")
            time.sleep(3)
    except Exception as e:
        print(f"解析页面异常: {e} \nHTML格式: \n{modal.get_attribute('outerHTML')}")
        html_parsing(driver)


if __name__ == '__main__':
    # 创建 Chrome 选项
    chrome_options = Options()

    # 设置无头模式
    chrome_options.add_argument('--headless')

    # 对于新版 Chrome (通常版本 >= 59)
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort问题
    chrome_options.add_argument('--disable-gpu')  # 早期版本需要，现在可选

    # 创建无头浏览器实例
    driver = webdriver.Chrome(options=chrome_options)

    html_parsing(driver)
    # 模拟输入
    # search_box = driver.find_element(By.CSS_SELECTOR, "input.form-control.search-input")  # 找到搜索框
    # search_box.send_keys("Uzi")  # 输入文本
    # search_box.send_keys(Keys.RETURN)  # 模拟回车
    # time.sleep(100)

    # 关闭浏览器
    driver.quit()
