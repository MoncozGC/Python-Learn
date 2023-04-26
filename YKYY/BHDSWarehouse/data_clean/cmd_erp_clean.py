# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/4/26
# Desc  : 解析json字段
# 将json的键做为数据库的字段名, value为字段名数据内容.
# 在json的键作为字段名的时候, 会根据映射表转换为数据库的字段名
import json

if __name__ == '__main__':

    gdsexp = '{"beCareful": "不宜与藜芦同用。", "component": "丹参", "indications": "祛瘀止痛，活血通经，清心除烦。用于月经不调，经闭痛经，症瘕积聚，胸腹刺痛，热痹疼痛，疮疡肿痛，心烦不眠；肝脾肿大，心绞痛。", "relatredGoods": "三七粉、西洋参粉、天麻粉、山楂粉", "talkingSkills": "1、主根打粉，低温萃取，保留药效；2、祛瘀止痛，活血通经。", "relatedReasons": "活血祛瘀，降三高，改善心脑血管疾病。"}'
    # 字典中的键是JSON数据中的键（例如relatedReasons、components等），值是将要为每个键创建的变量名（例如reladrugs、cpt等）。
    file_mapping = {'components': 'cpt', 'usage': 'usg', 'relatedReasons': 'reladisc', 'beCareful': 'atten', 'taboo': 'taboo', 'talkingSkills': 'proc', 'indications': 'susx'}

    gdsexp_json = json.loads(gdsexp) if gdsexp else {}
    # 用于存储从gdsexp_json提取的值。
    variables = {}
    # 使用for循环遍历keys字典. 在循环内部，使用get()方法从gdsexp_json中获取值，并将其存储在variables字典中.
    # 如果键不存在，get()方法将返回指定的默认值（在这种情况下是空字符串''）
    for key, var_name in file_mapping.items():
        variables[var_name] = gdsexp_json.get(key, '')
    # 将variables字典中的值分配给对应的变量
    # 主要成分, 用法用量, 相关论述, 注意事项, 禁忌, 适应症状
    cpt, usg, reladisc, atten, taboo, proc, susx = variables.values()

    print(variables.values())
