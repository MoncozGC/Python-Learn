# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/4/12 14:29
# Desc  : 条形码字段进行清洗匹配
"""
1. 获取数据
2. 根据spec(规格)字段进行转换, 以来提高匹配成功率
3. 根据各个字段进行匹配, 获取倒对应权重值, 其中gds_barc_df生产厂家字段只需和gds_bs_df字段的生产厂家或上市持有人匹配即可(一对多的情况)
4. 通用名和批准文号匹配上是基础, 在通过不同情况的匹配程度写入数据库中
5. 该案例没有写入数据库, 只打印了对应的更新语句, 如果要写入数据库, 更改update_records函数的mysql_conn参数即可.

权重值如下:
10000: 匹配通用名
11000: 匹配通用名 + 批准文号
111100: 匹配通用名 + 批准文号 + 生产厂家or上市持久人
111110: 匹配通用名 + 批准文号 + 生产厂家or上市持久人 + 商品名
111111: 匹配通用名(cmnzn) + 批准文号(adn) + 生产厂家or上市持久人(mftzn or mltzn) + 商品名(gdsn) + 包装规格(pckspec)
"""
import re

import numpy as np
import pandas as pd

from utils.comm_util import print_ts


def spec_clean(gds_df):
    """
    针对规格字段进行清洗
    """
    spec_list = np.array(gds_df["pckspec"]).tolist()
    # spec_list = ["80mg:5mg*10片", "1%:20ml", "1%30ml:0.3g", "100U:0.1mg*5支", "1ml:5mg:2mg", "香橙味1g*10片", "西林瓶100万IU/0.8ml", "草莓味3mg/ml*120ml"
    #              , "150丸(每100丸重60g)", "120丸*3盒(每丸重35mg)", "30粒*3板(每10丸重2g)", "72片(片芯重0.32g)", "30粒(每粒相当于原药材1g)", "10支(0.05%) -> 10支"
    #              , "8g*2袋(每100粒重10g)", "30g(每100粒重10g)*2瓶", "100ml*7.5%", "5％90ml"]

    # 保存【规格】括号里面的中文字符，如果匹配到，说明需要在括号里面去清洗出规格
    std_cn_list = ["每丸重", "每片芯重", "每粒相当于原药材"]

    # 保存清洗只有的规格
    clean_spec_list = []

    for spec in spec_list:
        # 1）对规则进行一些转换处理
        spec_res = spec.replace("万单位", "*10000") \
            .replace("万U", "#10000") \
            .replace("毫克", "mg") \
            .replace("万IU", "#10000") \
            .replace("毫升", "ml") \
            .replace("每丸重", "每1丸重") \
            .replace("片芯重", "每1片芯重") \
            .replace("每粒", "每1粒") \
            .replace("％", "%") \
            .replace("（", "(") \
            .replace("）", ")")

        # 2）如果规格存在":"字符，则需要特殊处理
        spec_res = spec_res.split(":")
        # 如1ml:5mg:2mg -> 1ml
        if len(spec_res) >= 3:
            spec_res = spec_res[0]
        # 如80mg:5mg*10片 -> 80mg*10片
        elif len(spec_res) == 2 and "*" in spec_res[1]:
            spec_res = spec_res[0] + "#" + spec_res[1].split("*")[-1]
        # 如1%30ml:0.3g -> 30ml; 1%:20ml -> 20ml
        elif len(spec_res) == 2 and "%" in spec_res[0]:
            if "ml" in spec_res[0]:
                spec_res = spec_res[0].split("%")[-1]
            else:
                spec_res = spec_res[1]
        else:
            spec_res = spec_res[0]

        # 3）把"g"转换为"mg"
        if len(re.findall("\\dg", spec_res)) != 0:
            spec_res = spec_res.replace("g", "#1000mg")

        # 4）去掉特殊字符"\"
        if "/" in spec_res:
            res = spec_res.split("/")
            # 如：草莓味3mg/ml*120ml -> 草莓味3mg*120ml
            if len(res) == 2 and "*" in res[1]:
                spec_res = res[0] + "#" + res[1].split("*")[-1]
            # 如：西林瓶100万IU/0.8ml -> 西林瓶100*10000
            else:
                spec_res = res[0]

        # 5）从括号里面获取包装规格， 如：150丸(每100丸重60*1000mg)
        if "(" in spec_res and ")" in spec_res:
            # 5.1 对字符串左括号进行切分
            split_spec_res = spec_res.split("(")

            # 5.2 获取括号里面的内容，如：(每100丸重60*1000mg)
            pattern_res = re.search("[(](.*)[)]", spec_res).group()
            # 5.3 匹配中文，如：每丸重
            cn_res_group = re.findall(".*?([\u4E00-\u9FA5]+)", pattern_res)
            cn_res = "".join(cn_res_group)
            if cn_res in std_cn_list:
                # 5.4 匹配所有数字和小数，【100,60,1000】
                num_res_group = re.findall("\\d+\.\\d+|\\d+", pattern_res)
                # 5.5 获取包装规格数值
                if len(num_res_group) >= 2:
                    divisor = int(num_res_group[0])
                    dividend = 1
                    for i in num_res_group[1:]:
                        dividend *= float(i)

                    if divisor == 0: divisor = 1
                    # 60 * 1000 / 100 = 600
                    num_res = round(dividend / divisor)
                    # 5.6 和之前的值进行拼接，如：150丸*600
                    spec_res = spec_res.split("(")[0] + "#" + str(num_res)
            # 如：30g(每100粒重10g)*2瓶 -> 30*1000mg*2瓶
            elif "*" in split_spec_res[1]:
                tmp_res = split_spec_res[1].split("*")[-1]
                spec_res = split_spec_res[0] + "#" + tmp_res
            else:
                spec_res = split_spec_res[0]

        # 6. 过滤包含【%】的数值
        if "%" in spec_res:
            # 如：100ml*7.5% -> 100ml
            if "*" in spec_res:
                spec_res = spec_res.split("*")[0]
            # 如：5％90ml -> 90ml
            else:
                spec_res = spec_res.split("%")[-1]

        # 7. 获取清洗之后规格的数值，同时把数值进行相乘
        num_res_list = re.findall("\\d+\.\\d+|\\d+", spec_res)
        spec_val = 1
        for i in num_res_list:
            spec_val *= float(i)

        clean_spec_list.append(int(spec_val))

    # 8. 把清洗之后的规格添加到dataframe中
    gds_df["spec"] = clean_spec_list
    return gds_df


def update_records(mysql_conn, sql_template, record, matching_weight):
    """
    根据权重获取sql模板
    """
    update_sql = sql_template.format(*record)
    # mysql_conn.execute_sql(update_sql)
    print_ts(matching_weight + "--" + update_sql)


def barc_matching(gds_barc_df, gds_bs_df):
    """
    核心数据处理
    """
    merge_barc_df = gds_barc_df.merge(gds_bs_df, how='left', on='cmnzn', suffixes=('_barc', '_bs'))

    # 获取匹配字段的权重
    # 111111: 匹配 -> 通用名 + 批准文号 + 生产厂家or上市持久人 + 商品名 + 包装规格
    merge_barc_df['matching_weight'] = (merge_barc_df['cmnzn'] == merge_barc_df['cmnzn']).astype(int).astype(str).str.cat(
        [np.where(merge_barc_df['adn_barc'] == merge_barc_df['adn_bs'], 1, 0).astype(str),
         np.where(merge_barc_df['mftzn_barc'] == merge_barc_df['mftzn_bs'], 1, 0).astype(str),
         np.where(merge_barc_df['mftzn_barc'] == merge_barc_df['mltzn'], 1, 0).astype(str),
         np.where(merge_barc_df['gdsn_barc'] == merge_barc_df['gdsn_bs'], 1, 0).astype(str),
         np.where(merge_barc_df['spec_barc'] == merge_barc_df['spec_bs'], 1, 0).astype(str)], sep='')

    # 获取1占位最多的数据, 再获取值最大的权重值
    # 如果值等于1, 则再此基础上进行累加
    merge_barc_df['max_weight'] = merge_barc_df['matching_weight'].apply(lambda x: sum(1 for char in x if char == '1'))
    # 根据两个字段进行降序排序
    sort_barc_df = merge_barc_df.sort_values(by=['max_weight', 'matching_weight'], ascending=[False, False])
    # 根据两个字段分组, 获取到最大的值
    pro_barc_df = sort_barc_df.groupby(['cmnzn', 'max_weight']).first().reset_index()

    # 获取所有数据
    all_barc_df = pro_barc_df[['cmnzn', 'gdsn_bs', 'adn_bs', 'pckspec_bs', 'mftzn_bs', 'mft_oid', 'mlf_oid', 'barc', 'matching_weight']] \
        .rename(columns={'gdsn_bs': 'gdsn', 'adn_bs': 'adn', 'pckspec_bs': 'pckspec', 'mftzn_bs': 'mftzn'})

    # 获取11开头的数据, 因为通用名和批准文号匹配上为基础
    other_barc_df = all_barc_df[all_barc_df['matching_weight'].str.startswith('11')]
    other_barc_df = other_barc_df[['barc', 'cmnzn', 'adn', 'mft_oid', 'mlf_oid', 'gdsn', 'pckspec', 'matching_weight']]
    barc_list = np.array(other_barc_df).tolist()

    # 记录每一个权重执行的次数
    update_num = {}
    # sql模板, 根据权重值, sql语句, 索引下标 -> 构造成一个UPDATE更新语句
    sql_templates = {
        # 2
        '110000': ("UPDATE bdcp_stg.stg_spr_gdsbs SET barc = '{}' WHERE cmnzn = '{}' AND adn = '{}'", (0, 1, 2)),

        # 3
        '110001': ("UPDATE bdcp_stg.stg_spr_gdsbs SET barc = '{}' WHERE cmnzn = '{}' AND adn = '{}' AND (pckspec = '{}' OR pckspec IS NULL)", (0, 1, 2, 6)),
        '110010': ("UPDATE bdcp_stg.stg_spr_gdsbs SET barc = '{}' WHERE cmnzn = '{}' AND adn = '{}' AND gdsn = '{}'", (0, 1, 2, 5)),
        '110100': ("UPDATE bdcp_stg.stg_spr_gdsbs SET barc = '{}' WHERE cmnzn = '{}' AND adn = '{}' AND mlf_oid = '{}'", (0, 1, 2, 4)),
        '111000': ("UPDATE bdcp_stg.stg_spr_gdsbs SET barc = '{}' WHERE cmnzn = '{}' AND adn = '{}' AND mft_oid = '{}'", (0, 1, 2, 3)),

        # 4
        '110011': ("UPDATE bdcp_stg.stg_spr_gdsbs SET barc = '{}' WHERE cmnzn = '{}' AND adn = '{}' AND gdsn = '{}' AND (pckspec = '{}' OR pckspec IS NULL)", (0, 1, 2, 5, 6)),
        '110101': ("UPDATE bdcp_stg.stg_spr_gdsbs SET barc = '{}' WHERE cmnzn = '{}' AND adn = '{}' AND mlf_oid = '{}' AND (pckspec = '{}' OR pckspec IS NULL)", (0, 1, 2, 4, 6)),
        '110110': ("UPDATE bdcp_stg.stg_spr_gdsbs SET barc = '{}' WHERE cmnzn = '{}' AND adn = '{}' AND mlf_oid = '{}' AND gdsn = '{}'", (0, 1, 2, 4, 5)),
        '111001': ("UPDATE bdcp_stg.stg_spr_gdsbs SET barc = '{}' WHERE cmnzn = '{}' AND adn = '{}' AND mft_oid = '{}' AND (pckspec = '{}' OR pckspec IS NULL)", (0, 1, 2, 3, 6)),
        '111010': ("UPDATE bdcp_stg.stg_spr_gdsbs SET barc = '{}' WHERE cmnzn = '{}' AND adn = '{}' AND mft_oid = '{}' AND gdsn = '{}'", (0, 1, 2, 3, 5)),
        '111100': ("UPDATE bdcp_stg.stg_spr_gdsbs SET barc = '{}' WHERE cmnzn = '{}' AND adn = '{}' AND mft_oid = '{}'", (0, 1, 2, 3)),

        # 5
        '110111': ("UPDATE bdcp_stg.stg_spr_gdsbs SET barc = '{}' WHERE cmnzn = '{}' AND adn = '{}' AND mlf_oid = '{}' AND gdsn = '{}' AND (pckspec = '{}' OR pckspec IS NULL)", (0, 1, 2, 4, 5, 6)),
        '111011': ("UPDATE bdcp_stg.stg_spr_gdsbs SET barc = '{}' WHERE cmnzn = '{}' AND adn = '{}' AND mft_oid = '{}' AND gdsn = '{}' AND (pckspec = '{}' OR pckspec IS NULL)", (0, 1, 2, 3, 5, 6)),
        '111101': ("UPDATE bdcp_stg.stg_spr_gdsbs SET barc = '{}' WHERE cmnzn = '{}' AND adn = '{}' AND mft_oid = '{}' AND (pckspec = '{}' OR pckspec IS NULL)", (0, 1, 2, 3, 6)),
        '111110': ("UPDATE bdcp_stg.stg_spr_gdsbs SET barc = '{}' WHERE cmnzn = '{}' AND adn = '{}' AND mft_oid = '{}' AND gdsn = '{}'", (0, 1, 2, 3, 5)),

        # 6
        '111111': ("UPDATE bdcp_stg.stg_spr_gdsbs SET barc = '{}' WHERE cmnzn = '{}' AND adn = '{}' AND mft_oid = '{}' AND gdsn = '{}' AND (pckspec = '{}' OR pckspec IS NULL)", (0, 1, 2, 3, 5, 6))
    }

    for i in barc_list:
        # 获取权重值
        matching_weight = i[7]
        # 如果某权重值为第一次执行, 则创建一个新值并且记录
        if matching_weight not in update_num:
            update_num.update({matching_weight: 0})
        if matching_weight in sql_templates:
            # 获取到sql语句及索引下标值
            sql_template, indices = sql_templates[matching_weight]
            # 列表推导式根据indices列表中的索引值从i列表中提取元素，然后将其转换为元组。
            # i是一个包含多个字段值的列表，而indices是一个包含我们需要的字段在i列表中的索引的列
            record = tuple(i[idx] or '' for idx in indices)
            # update_records(mysql_conn, sql_template, record, matching_weight)
            # 数据更新
            update_records('mysql_conn', sql_template, record, matching_weight)
            # 更新记录条数 +1
            update_num[matching_weight] += 1

    print_ts("【商品基础信息表-条形码】, bdcp_stg.stg_spr_gdsbs 更新数据条数: %d \n数据详细更新情况: %s" % (len(barc_list), update_num))


def test_data():
    """
    构建测试数据
    :return:
    """
    barc_list = {
        'cmnzn': {0: '维生素C泡腾片', 1: '维生素C泡腾片', 2: '维生素C泡腾片', 3: '维生素C泡腾片', 4: '维生素C泡腾片', 5: '维生素C泡腾片', 6: '维生素C泡腾片', 7: '维生素C泡腾片', 8: '维生素C泡腾片', 9: '维生素C泡腾片', 10: '维生素C泡腾片', 11: '维生素C泡腾片', 12: '维生素C泡腾片', 13: '维生素C泡腾片',
                  14: '维生素C泡腾片'},
        'gdsn': {0: '力度伸', 1: '力度伸', 2: '力度伸', 3: 'gdsn_barc', 4: '百维', 5: '百维', 6: '维诺健', 7: '葵花康宝', 8: 'gdsn_barc', 9: 'gdsn_barc', 10: '百维/国药C', 11: '汉维/百维/汉光', 12: '维口佳', 13: '果维康', 14: '果维康'},
        'adn': {0: '国药准字H20056946', 1: '国药准字H20056946', 2: '国药准字H20056946', 3: '国药准字H20074169', 4: 'adn_barc', 5: 'adn_barc', 6: 'adn_barc', 7: 'adn_barc', 8: '国药准字H20074169', 9: '国药准字H20074169', 10: '国药准字H20093616',
                11: '国药准字H20093616', 12: '国药准字H61022373', 13: '国药准字H20044780', 14: '国药准字H20044780'},
        'pckspec': {0: '香橙味1g*10片', 1: '1g*10片(柠檬味)', 2: '橙味1g*15片*2支', 3: '500mg*10片', 4: '15片/瓶x6瓶/盒', 5: '1.0克x15片/盒', 6: '16片/瓶/盒', 7: '0.5克', 8: '500mg*10片*2瓶', 9: '500mg*15片*2瓶', 10: '1.0g*15片', 11: '1.0g*10片',
                    12: '1g*18片', 13: '12片*2瓶(橙味)', 14: '12片(橙味)'},
        'mftzn': {0: '拜耳医药保健有限公司', 1: '拜耳医药保健有限公司', 2: '拜耳医药保健有限公司', 3: '南京亿华药业有限公司', 4: '华夏国药(菏泽)制药有限公司', 5: '华夏国药(菏泽)制药有限公司', 6: '华夏国药(菏泽)制药有限公司', 7: '黑龙江省地纳制药有限公司', 8: '南京亿华药业有限公司', 9: '南京亿华药业有限公司',
                  10: '华夏国药(菏泽)制药有限公司', 11: '华夏国药(菏泽)制药有限公司', 12: '西安利君制药有限责任公司', 13: '石药集团欧意药业有限公司', 14: '石药集团欧意药业有限公司'},
        'barc': {0: '6924147604027', 1: '6924147604010', 2: '6924147604065', 3: '6933519801186', 4: '6927373561263', 5: '6927373560860', 6: '6927373561201', 7: '6931511400444', 8: '6933519800882', 9: '6933519800325',
                 10: '6927373560860', 11: '6927373560792', 12: '6909563306489', 13: '6936292110391', 14: '6916119070190'},
        'spec': {0: 10000, 1: 10000, 2: 30000, 3: 5000, 4: 15, 5: 15, 6: 16, 7: 0, 8: 10000, 9: 15000, 10: 15000, 11: 10000, 12: 18000, 13: 24, 14: 12}}
    bs_list = {
        'cmnzn': {0: '维生素C泡腾片', 1: '维生素C泡腾片', 2: '维生素C泡腾片', 3: '维生素C泡腾片', 4: '维生素C泡腾片', 5: '维生素C泡腾片', 6: '维生素C泡腾片', 7: '维生素C泡腾片', 8: '维生素C泡腾片', 9: '维生素C泡腾片', 10: '维生素C泡腾片', 11: '维生素C泡腾片', 12: '维生素C泡腾片', 13: '维生素C泡腾片',
                  14: '维生素C泡腾片', 15: '维生素C泡腾片', 16: '维生素C泡腾片', 17: '维生素C泡腾片', 18: '维生素C泡腾片', 19: '维生素C泡腾片', 20: '维生素C泡腾片', 21: '维生素C泡腾片', 22: '维生素C泡腾片', 23: '维生素C泡腾片', 24: '维生素C泡腾片', 25: '维生素C泡腾片', 26: '维生素C泡腾片',
                  27: '维生素C泡腾片', 28: '维生素C泡腾片', 29: '维生素C泡腾片', 30: '维生素C泡腾片', 31: '维生素C泡腾片', 32: '维生素C泡腾片', 33: '维生素C泡腾片', 34: '维生素C泡腾片'},
        'gdsn': {0: '力度伸', 1: '力度伸', 2: 'gdsn_bs', 3: 'gdsn_bs', 4: 'gdsn_bs', 5: 'gdsn_bs', 6: 'gdsn_bs', 7: 'gdsn_bs', 8: 'gdsn_bs', 9: 'gdsn_bs', 10: 'gdsn_bs', 11: 'gdsn_bs', 12: 'gdsn_bs', 13: 'gdsn_bs',
                 14: 'gdsn_bs', 15: 'gdsn_bs', 16: 'gdsn_bs', 17: 'gdsn_bs', 18: 'gdsn_bs', 19: 'gdsn_bs', 20: 'gdsn_bs', 21: 'gdsn_bs', 22: 'gdsn_bs', 23: 'gdsn_bs', 24: 'gdsn_bs', 25: 'gdsn_bs', 26: 'gdsn_bs',
                 27: 'gdsn_bs', 28: 'gdsn_bs', 29: 'gdsn_bs', 30: 'gdsn_bs', 31: 'gdsn_bs', 32: 'gdsn_bs', 33: 'gdsn_bs', 34: 'gdsn_bs'},
        'adn': {0: '国药准字H20056946', 1: '国药准字H20056946', 2: '国药准字H11021195', 3: '国药准字H11021350', 4: '国药准字H20074169', 5: '国药准字H20074169', 6: '国药准字H20074169', 7: '国药准字H20043080', 8: '国药准字H61022373', 9: '国药准字H61022373',
                10: '国药准字H20093616', 11: '国药准字H20093616', 12: '国药准字H20093616', 13: '国药准字H20093616', 14: '国药准字H20093616', 15: '国药准字H20093616', 16: '国药准字H20093616', 17: '国药准字H20093616', 18: '国药准字H20044780',
                19: '国药准字H20044780', 20: '国药准字H20093585', 21: '国药准字H20093600', 22: '国药准字H20063336', 23: '国药准字H20063336', 24: '国药准字H20063336', 25: '国药准字H20067540', 26: '国药准字H20067540', 27: '国药准字H20067546',
                28: '国药准字H20067546', 29: '国药准字H20054888', 30: '国药准字H20054888', 31: '国药准字H20044176', 32: '国药准字H20044176', 33: '国药准字H34022063', 34: '国药准字H34022064'},
        'pckspec': {0: '1g*10片每盒', 1: '1g*30片每盒', 2: '0.3g', 3: '1g', 4: '500mg*10片每盒', 5: '500mg*20片每盒', 6: '500mg*30片每盒', 7: '0.5g', 8: '1g*12片每盒', 9: '1g*18片每盒', 10: '1.0g*10片每盒', 11: '1.0g*12片每盒', 12: '1.0g*15片每盒',
                    13: '1.0g*20片每盒', 14: '1.0g*24片每盒', 15: '1.0g*30片每盒', 16: '1.0g*16片每盒', 17: '1.0g*18片每盒', 18: '1.0g*12片每盒', 19: '1.0g*24片每盒', 20: '0.5g', 21: '1g', 22: '1.0g*15片每支', 23: '1.0g*30片每盒',
                    24: '1.0g*150片每盒', 25: '1g*12片每盒', 26: '1g*18片每盒', 27: '0.5g*10片每盒', 28: '0.5g*18片每盒', 29: '0.5g*15片每盒', 30: '0.5g*30片每盒', 31: '0.5g*15片每盒', 32: '0.5g*15片每管', 33: '1g', 34: '0.5g'},
        'mftzn': {0: '山东新华制药股份有限公司', 1: '山东新华制药股份有限公司', 2: '华润双鹤药业股份有限公司', 3: '北京万辉双鹤药业有限责任公司', 4: '南京亿华药业有限公司', 5: '南京亿华药业有限公司', 6: '南京亿华药业有限公司', 7: '西安利君制药有限责任公司', 8: '西安利君制药有限责任公司', 9: '西安利君制药有限责任公司',
                  10: '华夏国药(菏泽)制药有限公司', 11: '华夏国药(菏泽)制药有限公司', 12: '华夏国药(菏泽)制药有限公司', 13: '华夏国药(菏泽)制药有限公司', 14: '华夏国药(菏泽)制药有限公司', 15: '华夏国药(菏泽)制药有限公司', 16: '华夏国药(菏泽)制药有限公司', 17: '华夏国药(菏泽)制药有限公司', 18: '石药集团欧意药业有限公司',
                  19: '石药集团欧意药业有限公司', 20: '华润三九(唐山)药业有限公司', 21: '华润三九(唐山)药业有限公司', 22: '亚宝药业集团股份有限公司', 23: '亚宝药业集团股份有限公司', 24: '亚宝药业集团股份有限公司', 25: '吉林敖东延边药业股份有限公司', 26: '吉林敖东延边药业股份有限公司', 27: '吉林敖东延边药业股份有限公司',
                  28: '吉林敖东延边药业股份有限公司', 29: '黑龙江省地纳制药有限公司', 30: '黑龙江省地纳制药有限公司', 31: '正大制药(青岛)有限公司', 32: '正大制药(青岛)有限公司', 33: '安徽城市药业股份有限公司', 34: '安徽城市药业股份有限公司'},
        'mltzn': {0: '拜耳医药保健有限公司广州分公司', 1: '拜耳医药保健有限公司广州分公司', 2: '华润双鹤药业股份有限公司', 3: '华润双鹤药业股份有限公司', 4: '南京亿华药业有限公司', 5: '南京亿华药业有限公司', 6: '南京亿华药业有限公司', 7: '西安利君制药有限责任公司', 8: 'mltn_bs', 9: 'mltn_bs', 10: 'mltn_bs',
                  11: 'mltn_bs', 12: 'mltn_bs', 13: 'mltn_bs', 14: 'mltn_bs', 15: 'mltn_bs', 16: 'mltn_bs', 17: 'mltn_bs', 18: 'mltn_bs', 19: 'mltn_bs', 20: 'mltn_bs', 21: 'mltn_bs', 22: 'mltn_bs', 23: 'mltn_bs',
                  24: 'mltn_bs', 25: 'mltn_bs', 26: 'mltn_bs', 27: 'mltn_bs', 28: 'mltn_bs', 29: 'mltn_bs', 30: 'mltn_bs', 31: 'mltn_bs', 32: 'mltn_bs', 33: '安徽城市药业股份有限公司', 34: '安徽城市药业股份有限公司'},
        'mft_oid': {0: 398957306384495, 1: 398957306384495, 2: 398957305995354, 3: 398957305876549, 4: 398957306208362, 5: 398957306208362, 6: 398957306208362, 7: 398957305946203, 8: 398957305946203, 9: 398957305946203,
                    10: 398957306175559, 11: 398957306175559, 12: 398957306175559, 13: 398957306175559, 14: 398957306175559, 15: 398957306175559, 16: 398957306175559, 17: 398957306175559, 18: 398957306384457,
                    19: 398957306384457, 20: 398957305942143, 21: 398957305942143, 22: 398957306298493, 23: 398957306298493, 24: 398957306298493, 25: 398957306138721, 26: 398957306138721, 27: 398957306138721,
                    28: 398957306138721, 29: 398957306286195, 30: 398957306286195, 31: 398957306081395, 32: 398957306081395, 33: 398957306105956, 34: 398957306105956},
        'mlf_oid': {0: 398957305847889, 1: 398957305847889, 2: 398957305995354, 3: 398957305995354, 4: 398957306208362, 5: 398957306208362, 6: 398957306208362, 7: 398957305946203, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0,
                    14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0, 31: 0, 32: 0, 33: 398957306105956, 34: 398957306105956},
        'spec': {0: 10000, 1: 30000, 2: 300, 3: 1000, 4: 5000, 5: 10000, 6: 15000, 7: 500, 8: 12000, 9: 18000, 10: 10000, 11: 12000, 12: 15000, 13: 20000, 14: 24000, 15: 30000, 16: 16000, 17: 18000, 18: 12000, 19: 24000,
                 20: 500, 21: 1000, 22: 15000, 23: 30000, 24: 150000, 25: 12000, 26: 18000, 27: 5000, 28: 9000, 29: 7500, 30: 15000, 31: 7500, 32: 7500, 33: 1000, 34: 500}}

    return pd.DataFrame(barc_list), pd.DataFrame(bs_list)


if __name__ == '__main__':
    barc_df, bs_df = test_data()
    barc_matching(barc_df, bs_df)
