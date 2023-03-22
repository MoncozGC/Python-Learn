# encoding=utf-8

import sys
import datetime
from clickhouse_driver import Client
import numpy as np
from sklearn.linear_model import LinearRegression

# 获取昨天对应的年份
# yesDate = datetime.date.today() + datetime.timedelta(-1)
yesDate = '2021-12-13'
yesDate = datetime.datetime.strptime(yesDate, '%Y-%m-%d').date()
beforeYesDate = yesDate + datetime.timedelta(-1)
# startDate = yesDate + datetime.timedelta(-365)
startDate = yesDate + datetime.timedelta(-365)
# 获取近X个月的日期
before180Date = yesDate + datetime.timedelta(-180)
before90Date = yesDate + datetime.timedelta(-90)
before60Date = yesDate + datetime.timedelta(-60)
before30Date = yesDate + datetime.timedelta(-30)

# 连接ck
# chClient = Client(host='192.168.0.104',database='bds_dw',user='default',password='aqEwHXHG')
chClient = Client(host='xxx', database='bds_dw', user='default', password='default')

# 保存用户行为数据(访问及订单数据)
userAccessDic = {}
userOrderDic = {}

# 获取昨天用户轻度汇总表数据，
'''
对于用户生命周期模型：
userType: 默认全部为新生用户
userType: 1：潜在用户，2：新生用户，4：潜力用户，8：活跃用户，16：忠实用户，32：风险用户，64：沉睡用户，128：流失用户
riskLevel: 默认风险级别为正常
riskLevel: 0: 正常, 1: 中风险, 2: 高风险

对于用户忠诚度模型
loyalType: 默认全部都为不忠诚用户
loyalType: 1：不忠诚，2：潜在忠诚，4：雇佣型忠诚，8：坚定型忠诚，16：狂热型忠诚

数据格式：
user_dic[companyID] = [userType, riskLevel, loyalType]
'''
userDic = {}


def userPreviousData():
    # 获取所有用户
    result = chClient.execute("select DISTINCT companyID \
                       from bds_dw.dws_user_details_1d_loc where dt = '%s'" % yesDate)
    if len(result) == 0:
        sys.exit("没有对应的数据！")
    for line in result:
        userDic[line[0]] = [2, 0, 1]

    # 获取用户当年访问及订单数据
    result = chClient.execute("select dt, companyID, accessCount, orderCount, firstOrderDT, lastOrderDT, preOrderCount, shoppingCartCount, clickCount from \
                            bds_dw.dws_user_details_1d_loc where dt >= '%s' and dt<= '%s' and companyID != 0 and (accessCount > 0 or shoppingCartCount>0 or clickCount > 0 or orderCount > 0)" % (
    startDate, yesDate))
    # print(result)
    if len(result) == 0:
        sys.exit("没有对应的数据！")

    # 获取用户访问数据，及用户下单数据
    for line in result:
        # 将字段数据放入数组中
        dt = line[0]
        companyID = line[1]
        accessCount = line[2]
        orderCount = line[3]
        firstOrderDT = line[4]
        lastOrderDT = line[5]
        preOrderCount = line[6]
        shoppingCartCount = line[7]
        clickCount = line[8]
        # 不存在的companyID 保存到用户访问数据数组中
        if companyID not in userAccessDic:
            userAccessDic[companyID] = []
        userAccessDic[companyID].append(
            [dt, accessCount, orderCount, firstOrderDT, lastOrderDT, preOrderCount, shoppingCartCount, clickCount])

        if orderCount == 0:
            continue
        # 不存在的companyID 保存到用户访问数据数组中
        if companyID not in userOrderDic:
            userOrderDic[companyID] = []
        userOrderDic[companyID].append([dt, orderCount, firstOrderDT, lastOrderDT])


# 处理用户生命周期逻辑
def userLogicProc():
    print(yesDate)
    # 处理逻辑
    for k, v in userAccessDic.items():
        if k == 536891915:
            print(v)
        # cnt统计近3月总访问频率，cnt_x统计近1/2/3月份是否有访问
        cnt, cnt_1, cnt_2, cnt_3 = 0, 0, 0, 0
        # 近3月访问数、加购日频、点击日频、下单数
        accCnt, shopCnt, clickCnt, odrCnt = 0, 0, 0, 0

        # 如果近3月有2个月以上都访问
        # 或近3月总访问频率>=6次，
        # 或近3月总访问次数>=8次，或近3个月加购sku日频>=2个，或近3个月点击sku日频>=3个, 或近3个月下单数>=2次
        # 则该用户为"潜力用户"

        for userList in v:
            if userList[0] < before90Date:
                continue
            cnt += 1
            accCnt += userList[1]
            shopCnt += 1
            clickCnt += 1
            odrCnt += userList[2]
            if userList[0] >= before30Date:
                cnt_1 = 1
            elif userList[0] >= before60Date:
                cnt_2 = 1
            elif userList[0] >= before90Date:
                cnt_3 = 1
        if (cnt_1 + cnt_2 + cnt_3) >= 2 or cnt >= 4 or accCnt >= 6 or shopCnt >= 2 or clickCnt >= 3 or odrCnt >= 2:
            userDic[k][0] = 4
            # print(userDic[k][0])

    # 判断该用户是否为"活跃用户"
    for k, v in userAccessDic.items():
        # 近3月购买日频率>=3次, 或近1个月访问日频率>=6次，或近3个月加购sku日频>=5个，或近3月点击sku日频>=7个
        odrCntFreq, accCntFreq, shopCntFreq, clickCntFreq = 0, 0, 0, 0
        for userList in v:
            # 首单时间等于最后下单时间（即为首单）
            # if userList[3] == userList[4]:
            #    continue
            if userList[0] >= before90Date and userList[2] > 0:
                odrCntFreq += 1
            if userList[0] >= before30Date:
                accCntFreq += 1
            if userList[0] >= before90Date and userList[6] > 0:
                shopCntFreq += 1
            if userList[0] >= before90Date and userList[7] > 0:
                clickCntFreq += 1

        if odrCntFreq >= 3 or accCntFreq >= 4 or shopCntFreq >= 3 or clickCntFreq >= 5:
            userDic[k][0] = 8

    # 判断该用户是否为"忠诚用户"
    for k, v in userOrderDic.items():
        if userDic[k][0] != 8:
            continue
        # print(userOrderDic)

        # print(userDic)
        # cnt统计近6月的下单频率；cnt_x统计近1/2/3月份是否有购买
        cnt, cnt_1, cnt_2, cnt_3 = 0, 0, 0, 0

        # 如果近3月连续下单，或近6月购买频率>=7,则该用户为"忠诚用户"
        for userList in v:
            if userList[0] < before180Date:
                continue
            cnt += 1

            if userList[0] > before30Date:
                cnt_1 = 1
                continue
            if userList[0] > before60Date:
                cnt_2 = 1
                continue
            if userList[0] > before90Date:
                cnt_3 = 1
        if (cnt_1 + cnt_2 + cnt_3) == 3 or cnt >= 7:
            userDic[k][0] = 16


    # 判断该用户是否为"风险用户"
    for k, v in userAccessDic.items():
        # 在新生用户下，近3月访问日频>2次或完成首单，且最后登录时间>30天为中风险，最后登录时间>60天为高风险
        if userDic[k][0] == 2:
             #continue
             # 定义访问日频
             acc3mCnt, acc2mCnt, acc1mCnt, firstOrderFlag = 0, 0, 0, False
             for userList in v:
                 if userList[0] > before90Date:
                     acc3mCnt += 1
                 # 首单时间等于最后下单时间（即为首单）
                 if userList[3] == userList[4] and (userList[3].strftime("%Y-%m-%d")) != '1970-01-01':
                     firstOrderFlag = True
                 if userList[0] > before30Date:
                     acc1mCnt += 1
                     continue
                 if userList[0] > before60Date:
                     acc2mCnt += 1
             if acc3mCnt > 2 or firstOrderFlag == True:
                 if acc1mCnt == 0:
                     userDic[k][0] = 32
                     userDic[k][1] = 1
                 if acc2mCnt == 0:
                     userDic[k][0] = 32
                     userDic[k][1] = 2


        elif userDic[k][0] in (8, 16):
            # 按dt升序，用于计算该用户第几次消费、及消费间隔
            res = sorted(v, key = lambda x: x[0], reverse=False)
            # 保存风险评估模型的训练数据
            x = []
            y = []
            initValue = res[0][0]
            cnt = 1
            x.append(cnt), y.append(0)
            # 同一天用户多次访问只算一次
            for userList in res[1:]:
                if initValue == userList[0]:
                    continue
                cnt += 1
                y.append((userList[0] - initValue).days)
                x.append(cnt)
                initValue = userList[0]

            # 获取最后访问距昨天的天数
            label_y = (yesDate - initValue).days
            # 通过模型来预测下一次访问的间隔天数
            pre_x = cnt + 1
            pre_y = riskModelTrain(x, y, pre_x)

            # 近一年最大一次访问间隔
            max_y = max(y)
            # 如果最后访问距昨天数 > max(近一年最大一次访问间隔, 预测下一次访问的间隔天数)，则为高风险用户；在两者之间为中风险用户；否则为正常用户
            if label_y >= max(max_y, pre_y):
                userDic[k][0] = 32
                userDic[k][1] = 2
            elif label_y <= min(max_y, pre_y):
                userDic[k][1] = 0
            else:
                userDic[k][0] = 32
                userDic[k][1] = 1


    # 判断该用户是否为"沉睡用户"，在"新生用户" "潜力用户" "风险用户"下，最后登录时间距昨天>=90天
    for k, v in userAccessDic.items():
         #if userDic[k][0] != 32:
         #   continue
         if userDic[k][0] in (8, 16):
            continue

         maxDate = max([i[0] for i in v])
         if maxDate <= before90Date:
            userDic[k][0] = 64
            userDic[k][1] = 0


    #  # 判断该用户是否为"流失用户"，在"风险用户"下，最后登录时间距昨天>=180天
    for k, v in userAccessDic.items():
        if userDic[k][0] != 64:
            continue
        #if k != 536879177:
        #    continue
        maxDate = max([i[0] for i in v])
        if maxDate <= before180Date:
            userDic[k][0] = 128


# 针对每一个用户，基于其历史访问数据，来训练其风险评估模型
def riskModelTrain(x, y, pre_x):
    x = np.array(x).reshape((-1,1))
    y = np.array(y)
    model = LinearRegression()
    model = model.fit(x, y)
    pre_x = np.array([pre_x]).reshape((-1, 1))

    pre_y = model.predict(pre_x)
    return pre_y



# 用户忠诚度模型处理，获取对应用户所属忠诚度模型（不忠诚/潜在忠诚/雇佣型忠诚/坚定性忠诚/狂热型忠诚）
def loyaltyLogicProc():
    # acc_cnt/or_cnt/pre_cnt分别统计近3月访问/下单/优惠下单频率
    acc_cnt, or_cnt, pre_cnt = 0, 0, 0
    # cnt_x统计近1/2/3月份是否有下单
    cnt_1, cnt_2, cnt_3 = 0, 0, 0
    for k, v in userAccessDic.items():
        for userList in v:
            dt = userList[0]
            accessCount = userList[1]
            orderCount = userList[2]
            preOrderCount = userList[5]
            if dt < before90Date:
                continue
            acc_cnt += 1
            if orderCount > 0:
                or_cnt += 1
                if dt >= before30Date:
                    cnt_1 = 1
                elif dt>= before60Date:
                    cnt_2 = 1
                elif dt >= before90Date:
                    cnt_3 = 1
            if preOrderCount > 0:
                pre_cnt += 1

        # 判断是否为“不忠诚”用户，近3月访问频率<2且近3月购买频率<2
        if acc_cnt < 2 and or_cnt < 2:
            userDic[k][2] = 1

        # 判断是否为“潜在忠诚”用户，近3月访问频率>=20且近3月访问购买转化率<=25%
        # if acc_cnt >= 20 and round(or_cnt * 1.0 / acc_cnt, 3) * 100 <= 25:
        #     userDic[k][2] = 2

        # 如果该用户不是生命周期模型中的潜力用户/活跃用户/忠实用户，则过滤
        if userDic[k][0] not in (4, 8, 16):
            continue

        # 判断是否为“雇佣型忠诚“用户，生命周期为忠实用户，近三月优惠订单占比>=80% 且近三月购买频率偏差(max-min)/min>=3 （如min=0,只需判断max>=3）
        max_cnt = max(cnt_1, cnt_2, cnt_3)
        min_cnt = min(cnt_1, cnt_2, cnt_3)
        if or_cnt != 0 and round(pre_cnt * 1.0 / or_cnt, 3) * 100 >= 73:
            #if min_cnt == 0 and max_cnt >= 3:
            #    userDic[k][2] = 4
            #elif min_cnt != 0 and (max_cnt - min_cnt) / min_cnt >= 3:
            #    userDic[k][2] = 4
            userDic[k][2] = 4

        # 如果该用户不是生命周期模型中的活跃用户/忠诚用户，则过滤
        if userDic[k][0] not in (8, 16):
            continue

        # 判断是否为“坚定型忠诚“用户，生命周期为活跃用户/忠实用户且近3月访问购买转化率>40%
        if round(or_cnt * 1.0 / acc_cnt, 3) * 100 >= 12:
            userDic[k][2] = 8

        # 如果该用户不是生命周期模型中的活跃用户/忠诚用户，则过滤
        if userDic[k][0] != 16:
            continue

        # 判断是否为“狂热型忠诚”用户，生命周期为忠诚用户且近3月连续购买且总购买频率>=6且有分享操作（暂时没有分享功能，先不实现）
        if (cnt_1 + cnt_2 + cnt_3) == 3 and or_cnt >= 6:
            userDic[k][2] = 16


# 把用户生命周期模型/用户忠诚度模型数据结构化
cyclePeriodList = []
loyalList = []
def userModelStrucProc():
    # 初始化值
    dt = yesDate
    year = yesDate.year

    for k, v in userDic.items():
        level = v[0]
        riskLevel = v[1]
        loyalLevel = v[2]
        levelName = ""
        liftCycle = ""
        riskLevelName = ""
        sortCnt = 0

        # 把risklevel转化为中文
        if riskLevel == 0:
            riskLevelName = "低风险"
        elif riskLevel == 1:
            riskLevelName = "中风险"
        else:
            riskLevelName = "高风险"

        # 把生命周期模型等级转化
        if level == 1:
            liftCycle = "新生期"
            levelName = "潜在用户"
            sortCnt = 1
        elif level == 2:
            liftCycle = "新生期"
            levelName = "新生用户"
            sortCnt = 2
        elif level == 4:
            liftCycle = "成长期"
            levelName = "潜力用户"
            sortCnt = 3
        elif level == 8:
            liftCycle = "成长期"
            levelName = "活跃用户"
            sortCnt = 4
        elif level == 16:
            liftCycle = "成熟期"
            levelName = "忠实用户"
            sortCnt = 5
        elif level == 32:
            liftCycle = "衰退期"
            levelName = "风险用户"
            sortCnt = 6
        elif level == 64:
            liftCycle = "衰退期"
            levelName = "沉睡用户"
            sortCnt = 7
        else:
            liftCycle = "流失期"
            levelName = "流失用户"
            sortCnt = 8
        cyclePeriodList.append([dt, year, k, liftCycle, riskLevelName, levelName, sortCnt])

        # 定义用户忠诚度模型等级名称
        loyalName = ""
        loyalSortCnt = 0

        # 把忠诚度模型等级转化
        if loyalLevel == 1:
            loyalName = "不忠诚"
            loyalSortCnt = 1
        elif loyalLevel == 2:
            loyalName = "潜在忠诚"
            loyalSortCnt = 2
        elif loyalLevel == 4:
            loyalName = "雇佣型忠诚"
            loyalSortCnt = 3
        elif loyalLevel == 8:
            loyalName = "坚定型忠诚"
            loyalSortCnt = 4
        else:
            loyalName = "狂热型忠诚"
            loyalSortCnt = 5

        loyalList.append([dt, year, k, loyalName, loyalSortCnt])

# 把数据插入到clickhouse中
def insert2CK(table, dataList):
    try:
        chClient.execute('insert into %s values' % table %(), dataList, types_check=True)
        print("插入%s表成功，条数为：%d" % (table, len(dataList)))
        return 1
    except Exception as e:
        print(e)
        return -1


if __name__ == "__main__":
    # 从用户轻度汇总表获取昨天的数据（以companyID去重，默认设置用户为"新生用户"），同时获取当年用户访问及订单数据
    userPreviousData()

    # 生命周期逻辑处理，获取对应用户所属用户类型（潜在/新生/潜力/活跃/忠实/风险/沉睡/流失）
    userLogicProc()

    # 用户忠诚度模型处理，获取对应用户所属忠诚度模型（不忠诚/潜在忠诚/雇佣型忠诚/坚定性忠诚/狂热型忠诚）
    loyaltyLogicProc()

    # 把得到的结果结构化，即和clickhouse表字段对应
    userModelStrucProc()

    # # 批量插入数据到clickhouse
    # insert2CK("bds_dw.ads_user_life_cycle_1y_loc", cyclePeriodList)
    # insert2CK("bds_dw.ads_user_loyal_1y_loc", loyalList)
