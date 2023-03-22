#encoding=utf-8

import sys
import datetime
from clickhouse_driver import Client

# 获取昨天对应的年份
#yesDate = datetime.date.today() + datetime.timedelta(-1)
yesDate = sys.argv[1]
yesDate = datetime.datetime.strptime(yesDate, '%Y-%m-%d').date()
#startDate = yesDate + datetime.timedelta(-365)
startDate = '2020-02-04'
year = yesDate.year

# 连接ck
# chClient = Client(host='192.168.0.104',database='bds_dw',user='default',password='aqEwHXHG')
chClient = Client(host='xxxx', database='bds_dw', user='default', password='default')

# 保存用户订单数量、订单销售额、订单毛利额，获取其中位值
orderCountList = []
saleAmountList = []

# 保存用户价值模型数据, user_value_list = [[dt, valueName, valueCount], ...]
userValueList = []

# 获取昨天用户轻度汇总表数据，如该用户没有购买行为，则默认其为无价值
# userDic[companyID] = "无价值"
userDic = {}
def userPreviousData():
    result = chClient.execute("select DISTINCT companyID \
                       from bds_dw.dws_user_details_1d_loc where dt = '%s'" % yesDate)
    if len(result) == 0:
        sys.exit("没有对应的数据!")

    for line in result:
        userDic[line[0]] = "其他(未下单)"

# 获取对应数据的中位数
def getMedian(data):
   data = sorted(data)
   size = len(data)
   if size % 2 == 0: # 判断列表长度为偶数
    median = (data[size//2]+data[size//2-1])/2
    data[0] = median
   if size % 2 == 1: # 判断列表长度为奇数
    median = data[(size-1)//2]
    data[0] = median
   return data[0]


"""
处理用户价值逻辑，其中分为高价值、中价值、低价值、无价值
计算逻辑:
抽取近一年销售订单数据
说明：毛利润暂时不用
选取三个参数维度（购买频率R、购买金额F、毛利润M） 
计算R比较值=（所有用户R的中位值）、F比较值=（所有用户金额的中位值）、M比较值=600
当用户购买频率R >= R比较值时，值为1，否则为0
当用户购买金额F >= F比较值时，值为1，否则为0
当用户购买毛利润M >= M比较值时，值为1，否则为0
应用RFM模型，如下图：
价值等级数值	价值等级
111		高价值
110		中价值
101		中价值
100		低价值
011		中价值
010		低价值
001		低价值
000		无价值
"""
def userLogicProc():
    #result = chClient.execute("select companyID, count(distinct orderMainOID), sum(saleAmount) / 100 from \
    #                             dws_order_details_1d_loc where dt >= '%s' group by companyID" % startDate)

    result = chClient.execute("select a.companyID, a.orderCount, a.saleAmount, a.saleAmount - if(b.originalAmount is null, 0, b.originalAmount) as grossAmount from \
	                       ( \
		                   select companyID, count(distinct orderMainOID) as orderCount, sum(saleAmount) / 100 as saleAmount from \
                                   dws_order_details_1d_loc where dt >= '%s' and dt <= '%s' group by companyID	\
	                       ) a \
	                       left join	\
	                       (	\
		                   select companyID, sum(originalAmount) / 100 as originalAmount from \
                                   dws_order_details_1d_loc where actuaDeliveryDT >= '%s' group by companyID	\
	                       ) b	\
	                       on a.companyID = b.companyID" % (startDate, yesDate, startDate))
    
    if len(result) == 0:
        sys.exit("没有对应的数据！")

    # 获取用户访问数据，及用户下单数据
    for line in result:
        orderCountList.append(line[1])
        saleAmountList.append(line[2])
        #gross_amount_list.append(line[3])

    medianOrderCount = getMedian(orderCountList)
    medianSaleAmount = getMedian(saleAmountList)
    #median_gross_amount = get_median(gross_amount_list)


    # 获取用户RFM模型
    for line in result:
        companyID = line[0]
        orderCount = line[1]
        saleAmount = line[2]
        grossAmount = line[3]
        
        valueLevel = ""
        if orderCount >= medianOrderCount:
            valueLevel += "1"
        else:
            valueLevel += "0"
        if saleAmount >= medianSaleAmount:
            valueLevel += "1"
        else:
            valueLevel += "0"
        if grossAmount >= 600:
            valueLevel += "1"
        else:
            valueLevel += "0"
            

        if valueLevel == "111":
            userDic[companyID] = "高价值"
        elif valueLevel in ("110", "101", "011"):
            userDic[companyID] = "中价值"
        elif valueLevel in ("100", "010", "001"):
            userDic[companyID] = "低价值"
        else:
            userDic[companyID] = "无价值"

    
    for k, v in userDic.items():
        companyID = k
        valueName = userDic[k]
        userValueList.append([yesDate, year, companyID, valueName])


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
    insert2CK("bds_dw.ads_user_value_1y_loc", userValueList)

