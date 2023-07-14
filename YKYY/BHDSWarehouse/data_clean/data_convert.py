# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/4/6 22:47
# Desc  : 根据匹配规则转换数据, 并且获取同一段文本中的最小指标数据
import re

if __name__ == '__main__':
    import pandas as pd

    data = {
        'vod': ['非PVC软袋：24个月；聚丙烯塑料瓶：48个月', '六个月', '六月', '五年']
    }

    vod_df = pd.DataFrame(data)


    def chinese_to_arabic(cn):
        """
        将中文量词转换为数字
        :param cn:
        :return:
        """
        cn_num = {
            '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
            '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
            '十': 10
        }
        arabic = 0
        temp = 0
        for c in cn:
            if c == '十':
                if temp == 0:
                    temp = 1
                arabic += temp * cn_num[c]
                temp = 0
            else:
                temp = cn_num[c]
        arabic += temp
        return arabic


    def convert_to_days(text):
        """
        数据转换, 并且获取同文本中的最小值
        :param text:
        :return:
        """
        results = re.findall(r'(\d+|[一二三四五六七八九十]+)([个]*月|年|天)', text)
        # 正无穷
        min_days = float('inf')

        if results:
            for result in results:
                if result[0].isdigit():
                    number = int(result[0])
                else:
                    number = chinese_to_arabic(result[0])

                unit = result[1]

                if unit == '年':
                    days = number * 365
                elif unit == '个月' or unit == '月':
                    days = number * 30
                elif unit == '天':
                    days = number

                if days < min_days:
                    min_days = days

            return min_days
        return None


    vod_df['days'] = vod_df['vod'].apply(convert_to_days)

    print(vod_df)
