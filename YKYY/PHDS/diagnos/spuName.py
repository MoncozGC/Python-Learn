# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/3/16 16:48
# Desc  :
import pandas as pd

if __name__ == '__main__':
    spuName_list = ['安宫牛黄丸', '一次性使用医用口罩', '人血白蛋白', '吸入用布地奈德混悬液', '硝苯地平缓释片', '舒筋健腰丸', '感冒灵颗粒', '丹参保心茶', '金嗓子喉片',
                    '藿香正气口服液', '阿奇霉素干混悬剂', '葡萄糖酸钙锌口服溶液', '钙维生素D3维生素K2软胶囊', '补肺丸', '养生堂蛋白粉', '益安宁丸', '清血八味片',
                    '硫酸特布他林雾化吸入用溶液', '维生素AD滴剂', '碳酸钙D3片', '磷酸奥司他韦颗粒', '艾申特牌维生素C维生素E蛋白粉', '天然时光氨糖软骨素钙片', '稳心颗粒', '阿卡波糖片',
                    '桂龙药膏', '祛湿颗粒', '苯磺酸氨氯地平片', '吸入用异丙托溴铵溶液', '四季抗病毒合剂', '阿司匹林肠溶片', '琥珀酸美托洛尔缓释片', '复方板蓝根颗粒', '小柴胡颗粒',
                    '苯磺酸左氨氯地平片', '维生素D滴剂', '夏桑菊颗粒', '云香祛风止痛酊', '医用外科口罩', '复方鱼腥草合剂', '抗病毒口服液', '川贝母', '天然维生素E软胶囊',
                    '复方扶芳藤合剂', '蒲公英颗粒', '氨糖软骨素维生素D钙片', '阿托伐他汀钙片', '枸橼酸西地那非片', '肠炎宁片', '欧姆龙电子血压计', '同仁牛黄清心丸', '大枣',
                    '复方金银花颗粒', '桂林西瓜霜', '蓝芩口服液', '消肿止痛酊', '小儿七星茶颗粒', '参苓健脾胃颗粒', '马来酸左氨氯地平分散片', '肺力咳合剂', '脑心通胶囊',
                    '玉叶解毒颗粒', '四物膏', '丹参茶', '厄贝沙坦片', '小儿氨酚黄那敏颗粒', '复方丹参滴丸', '脑脉泰胶囊', '炮山甲', '骨痛冷敷凝露', '迈之灵片',
                    '盐酸左氧氟沙星片', '强骨生血口服液', '复方金钱草颗粒', '益生元牌益生菌粉', '阿莫西林胶囊', '米格列醇片', '屈螺酮炔雌醇片', '扶芳参芪口服液', '金振口服液',
                    '京都念慈菴蜜炼川贝枇杷膏', '五松肿痛酊', '安宫牛黄丸', '益生菌冲剂', '复方黄松洗液', '云南白药粉', '天然时光维生素C咀嚼片', 'B族维生素片', '阿奇霉素片',
                    '氟哌噻吨美利曲辛片',
                    '硝苯地平控释片', '龟鹿补肾丸', '国公酒', '活络油', '六味地黄胶囊', '通脉颗粒', '强力枇杷露', '西洋参', '养生堂天然维生素E软胶囊+维生素C咀嚼片', '多维元素片',
                    '复方酮康唑发用洗剂']
# frame = pd.DataFrame(spuName_list)
# apply = frame.apply(pd.value_counts)
# print(apply)


counts = pd.value_counts(spuName_list, dropna=False)
print(counts)