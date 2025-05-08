# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2025-05-08
# Desc  : 根据高德API获取经纬度获取两个地方驾车的等时线(15/30), 根据出发地点保存为excel文件
# 高德API: https://amap.apifox.cn/api-14580571
import math
import os
import time

import pandas as pd
import requests
import xlrd
from requests.adapters import HTTPAdapter

invoke = 0
keyid = 0


# 获取正确的 AMap API 密钥
def get_route(origin, destination, API_KEY):
    api = f'https://restapi.amap.com/v5/direction/driving?origin={origin}&destination={destination}&key={API_KEY}&show_fields=cost'
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))
    try:
        r = s.get(api, timeout=800)
        if r.status_code == 200:
            return r.json()
        else:
            print("请求失败，状态码：", r.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("请求异常：", e)
        return None


def get_route_info(o, ox, oy, endpt, endx, endy, keylist):
    routeplan = []
    lasttime = time.time()

    for j in range(0, len(endpt)):  # 假设第一行是标题或不需要的数据
        d = endpt[j]

        dx = endx[j]
        dy = endy[j]

        dist = math.sqrt((float(dx) - float(ox)) ** 2 + (float(dy) - float(oy)) ** 2)
        if dist > 2000000:
            duration = -1
        else:
            global invoke
            global keyid
            invoke += 1

            # 检查是否需要切换key
            if invoke > 4950:
                old_keyid = keyid
                keyid = (keyid + 1) % len(keylist)  # 循环使用keylist中的key
                print(f"API调用次数达到限制(count={invoke})，正在从key[{old_keyid}]切换到key[{keyid}]")
                invoke = 0  # 重置调用计数

            retry_count = 0
            max_retries = len(keylist)  # 最大重试次数等于密钥数量
            request_successful = False

            while not request_successful and retry_count < max_retries:
                key = keylist[keyid]
                print(f"使用key[{keyid}]: {key[:8]}...")  # 打印当前使用的key（只显示前8位）

                if (time.time() - lasttime < 1):
                    time.sleep(0.5)

                info = get_route(o, d, key)
                lasttime = time.time()

                # 检查是否返回了限额错误
                if info and info['status'] == '0' and 'USER_DAILY_QUERY_OVER_LIMIT' in info.get('info', ''):
                    print(f"请求错误: {info.get('info', '未知错误')}")
                    old_keyid = keyid
                    keyid = (keyid + 1) % len(keylist)  # 切换到下一个密钥
                    print(f"密钥超出每日限额，正在从key[{old_keyid}]切换到key[{keyid}]")
                    retry_count += 1
                    continue  # 使用新密钥重试

                request_successful = True  # 如果没有限额错误，跳出循环

                duration = 999999999999
                if info and info['status'] == '1' and info['info'] == 'OK':
                    min_duration = 999999999999  # 单位为秒，初始化最大值
                    # for transit in info['route']['transits']:
                    #     min_duration = min(min_duration, int(transit['cost']['duration']))
                    #     duration = min_duration
                    for transit in info['route']['paths']:
                        min_duration = min(min_duration, int(transit['distance']))
                        duration = min_duration
                else:
                    if info:
                        print(f"请求错误: {info.get('info', '未知错误')}")
                    else:
                        print("请求返回None，可能是网络问题")

                        # 如果所有密钥都超限，记录错误
            if retry_count >= max_retries:
                print("警告：所有密钥均已超出每日限额，无法完成请求")
                duration = 999999999999  # 使用默认值

        route = [o, d]
        route.append(duration)
        routeplan.append(route)

        if (j == 0 or (j + 1) % 10 == 0):
            print('%d:%s-%s-%d' % ((j + 1), o, d, duration))

    return routeplan


if __name__ == '__main__':


    data = xlrd.open_workbook(r'./get_map_isochron.xls')
    sheet0 = data.sheet_by_index(0)
    sheet1 = data.sheet_by_index(1)
    start = sheet0.col_values(1, 1, 51)
    end = sheet1.col_values(1, 1, 14811)

    startx = sheet0.col_values(2, 1, 51)
    starty = sheet0.col_values(3, 1, 51)
    endx = sheet1.col_values(2, 1, 14811)
    endy = sheet1.col_values(3, 1, 14811)

    print(f"起点数量: {len(start)}, 终点数量: {len(end)}")
    print(f"医院坐标: {start[0]}-{start[len(start) - 1]}")
    print(f"人口格网点: {end[0]}-{end[len(end) - 1]}")
    keylist = ['88bd535ed6901ca76dc3f907b4e190a8', '46648b0d46ed2fc868e3b10c9cf06fd7', 'abdfe9020d2934c6e323bfd44ab160d5', '30e2c24773b9e9481195b42c4e2c63dc', '834769133e3ef46189b74bf37cf33df6',
               '3091fab9b69fb0793b1c47bff694b92c']
    print(f"总共加载了{len(keylist)}个API密钥")
    # 自动检测上次运行到哪个索引
    start_index = 0
    desktop_path = r'./'
    output_files = [f for f in os.listdir(desktop_path) if f.startswith('输出') and f.endswith('.xls')]

    if output_files:
        max_index = 0
        for file in output_files:
            try:
                # 提取文件名中的索引数字
                index = int(file.replace('输出', '').replace('.xls', ''))
                max_index = max(max_index, index)
            except ValueError:
                continue

        if max_index > 0:
            start_index = max_index  # 从已完成的下一个索引开始
            print(f"检测到已处理到索引{max_index}，将从索引{start_index}继续")

    # 从确定的起始索引开始处理
    for i in range(start_index, len(start)):
        o = start[i]
        ox = startx[i]
        oy = starty[i]

        print(f"\n===== 正在处理索引 {i} ({i + 1}/{len(start)}) =====")
        routeplan = get_route_info(o, ox, oy, end, endx, endy, keylist)

        if not isinstance(routeplan, pd.DataFrame):
            result_df = pd.DataFrame(routeplan, columns=['起点', '终点', '最短耗时（秒）'])
        else:
            result_df = routeplan

        output_path = os.path.join(desktop_path, f'输出{i + 1}.xls')
        result_df.to_excel(output_path, index=False)
        print(f"已保存结果到 {output_path}")

    print("运行结束.")
