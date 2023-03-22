#encoding=utf-8

import sys
import datetime
from clickhouse_driver import Client
import pandas as pd
from sklearn.cluster import KMeans

# 获取昨天对应的年份
#yesDate = datetime.date.today() + datetime.timedelta(-1)
yesDate = sys.argv[1]
yesDate = datetime.datetime.strptime(yesDate, '%Y-%m-%d').date()
startDate = yesDate + datetime.timedelta(-365)
year = yesDate.year

# 连接ck
# chClient = Client(host='192.168.0.104',database='bds_dw',user='default',password='aqEwHXHG')
chClient = Client(host='xxxx', database='bds_dw', user='default', password='default')

# 保存门店id，及聚类训练数据
idList = []
trainDataList = []

# 保存优惠敏感度类别
senLabelList = ["极度敏感", "较敏感", "一般敏感", "较不敏感", "极度不敏感"]

# 保存优惠敏感度类型所属聚类类别
senClusterDic = {}

# 保存用户优惠敏感度模型数据, user_sen_list = [[dt, senName, indexVal, indexRange], ...]
userSenList = []

# 获取昨天用户轻度汇总表数据，如该用户没有购买行为，则默认其为无价值
# user_dic[companyID] = [senName, indexVal, indexRange], 默认为“极度不敏感”，指数为0，且指数范围为最小的指数范围
defaultIndexRange = ""
userDic = {}
def userPreviousData():
    result = chClient.execute("select DISTINCT companyID \
                       from bds_dw.dws_user_details_1d_loc where dt = '%s'" % yesDate)
    if len(result) == 0:
        sys.exit("没有对应的数据!")
        
    for line in result:
        userDic[line[0]] = ["其他(未下单)", 0, ""]


"""
处理用户敏感度模型逻辑，优惠敏感度分为极度敏感、较敏感、一般敏感、较不敏感、极度不敏感等5类
计算逻辑:
抽取近一年销售订单数据
获取用户优惠订单占比: preOrderRate、用户平均每单优惠金额占比: preAvgPriceRate、总优惠订单金额占比: prePriceRate
输入参数：preOrderRate、(preAvgPriceRate + prePriceRate) / 2
输出标签：优惠敏感度、敏感指数
说明：
通过Calinski-Harabasz指数确定最佳聚类数目为5
"""
def userLogicProc():
    result = chClient.execute("select \
				companyID, \
				round(sum(if(userPreferentialPrice > 0, 1, 0)) / count(*), 4) as preCntRate, \
				round((sum(userPreferentialPrice / userOrderTotalPrice) / count(*) + sum(userPreferentialPrice) / sum(userOrderTotalPrice)) / 2, 4) as prePriceRate \
				from \
				( \
					select \
					max(companyID) as companyID, \
					sum(GMV) as userOrderTotalPrice, \
					sum(preferentialPayment) as userPreferentialPrice \
					from bds_dw.dws_order_details_1d_loc \
					where orderType not in (300, 301) \
					and dt > '%s' \
					and dt <= '%s' \
					and saleAmount > 0 \
					group by orderMainOID \
				) tmp \
				group by companyID;" % (startDate, yesDate))
    if len(result) == 0:
        sys.exit("没有对应的数据！")

    # 获取用户下单数据
    for res in result:
        idList.append(res[0])
        trainDataList.append((res[1], res[2]))

    data = pd.DataFrame(trainDataList, columns=["preCntRate", "prePriceRate"]) 
    #构建并训练模型
    kmeans_model = KMeans(n_clusters = 5, init='k-means++', random_state=11)
    # 进行聚类处理
    y_kmeans = kmeans_model.fit_predict(data)

    labelsList = list(kmeans_model.labels_)
    #print(len(userDic), len(idList), len(labelsList))
    
    # 保存每个聚类下面的用户id和指数
    labelDic = {}
    for i in range(len(idList)):
        label = labelsList[i]
        companyID = idList[i]
        indexVal = trainDataList[i][0]
        if label not in labelDic:
            labelDic[label] = []
        labelDic[label].append((companyID, indexVal))

    # 获取各个聚类的最大、最小值（目前只针对订单优惠数），然后按最大值排序，即值越大，越敏感
    tmpList = []
    for k, v in labelDic.items():
        maxVal = max([i[1] for i in v])
        minVal = min([i[1] for i in v])
        tmpList.append((k, minVal, maxVal))

    sortList = sorted(tmpList, key=lambda x: x[2], reverse=True)

    # 获取聚类下，对应的敏感度类别，以及对应的指数值
    minLabelVal = 0
    maxLabelVal = 0
    
    for idx, val in enumerate(sortList):
        if idx == 0:
            minLabelVal = round(val[1] * 100)
            maxLabelVal = 100
        else:
            maxLabelVal = minLabelVal
            if idx == (len(sortList) - 1):
                minLabelVal = 0
                defaultIndexRange = str(minLabelVal) + "-" + str(int(maxLabelVal))
            else:
                minLabelVal = round(val[1] * 100)
         
        senClusterDic[val[0]] = [senLabelList[idx], int(minLabelVal), int(maxLabelVal)]
        #print(str(idx) + "\t" + sen_label_list[idx] + "\t" + str(min_label_val) + "\t" + str(max_label_val))
    
    #print(defaultIndexRange)

    # 获取用户所属优惠敏感度类别，以及对应的指数和所属范围
    for k, v in labelDic.items():
        senName, minLabelVal, maxLabelVal = senClusterDic[k]
        indexRange = str(minLabelVal) + "-" + str(maxLabelVal)
        for subList in v:
            companyID = subList[0]
            indexVal = int(round(subList[1] * 100))
            if indexVal >= maxLabelVal and maxLabelVal != 100:
                indexVal = maxLabelVal - 1 

            userDic[companyID] = [senName, indexVal, indexRange]

     # 把最近一年没有下单的用户，设置默认优惠敏感度为“极度不敏感”
    for k, v in userDic.items():
        companyID = k
        senName = v[0]
        indexVal = v[1]
        indexRange = v[2]
        if indexRange == "":
            indexRange = "0" 
        userSenList.append([yesDate, year, companyID, senName, indexVal, indexRange])

def insert2CK(table, dataList):
    try:
        chClient.execute('insert into %s values' % table %(), dataList, types_check=True)
        print("插入%s表成功，条数为：%d" % (table, len(dataList)))
        return 1
    except Exception as e:
        print(e)
        return -1


if __name__ == "__main__":
    # 获取所有的用户
    userPreviousData()
    # 逻辑处理，实现用户价值模型，得到用户价值等级的数量
    userLogicProc()
    # 批量插入数据到clickhouse
    insert2CK("bds_dw.ads_user_sen_1y_loc", userSenList)
