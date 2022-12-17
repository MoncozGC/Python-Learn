"""
encoding: utf-8
Author: MoncozGC
Date  : 2021/12/30 14:33
Desc  :
1. 求水仙花数
2. 数值反转
3. 白钱白鸡问题
"""


def NumberDaffodils():
    """
    求水仙花数
    :return:
    """
    for num in range(100, 1000):
        low = num % 10
        mid = num // 10 % 10
        high = num // 100
        if num == low ** 3 + mid ** 3 + high ** 3:
            return num


def ValueInversion(num):
    """
    数值反转
    :param num:
    :return:
    """
    reversed_num = 0
    while num > 0:
        reversed_num = reversed_num * 10 + num % 10
        num //= 10

    return reversed_num


def HundredChickens():
    """
    公鸡5元一只，母鸡3元一只，小鸡1元三只，用100块钱买一百只鸡，问公鸡、母鸡、小鸡各有多少只？
    :return:
    """
    for x in range(0, 20):
        for y in range(0, 33):
            z = 100 - x - y
            if 5 * x + 3 * y + z / 3 == 100:
                print('百钱白鸡问题: 公鸡: %d只, 母鸡: %d只, 小鸡: %d只' % (x, y, z))


def CrapsGame():
    """
    Craps赌博游戏
    我们设定玩家开始游戏时有1000元的赌注
    游戏结束的条件是玩家输光所有的赌注
    该游戏使用两粒骰子，玩家通过摇两粒骰子获得点数进行游戏。简单的规则是：
    1. 玩家第一次摇骰子如果摇出了7点或11点，玩家胜；玩家第一次如果摇出2点、3点或12点，庄家胜；
    2. 其他点数玩家继续摇骰子，如果玩家摇出了7点，庄家胜；如果玩家摇出了第一次摇的点数，玩家胜；
    3. 其他点数，玩家继续要骰子，直到分出胜负。
    :return:
    """
    from random import randint
    import time

    money = 1000
    while money > 0:
        print('你的总资产为:', money)
        needs_go_on = False
        while True:
            debt = int(input('请下注: '))
            if 0 < debt <= money:
                break
        first = randint(1, 6) + randint(1, 6)
        print('玩家摇出了%d点' % first)
        if first == 7 or first == 11:
            time.sleep(2)
            print('玩家胜!')
            money += debt
        elif first == 2 or first == 3 or first == 12:
            time.sleep(2)
            print('庄家胜!')
            money -= debt
        else:
            needs_go_on = True
        while needs_go_on:
            needs_go_on = False
            current = randint(1, 6) + randint(1, 6)
            time.sleep(2)
            print('玩家摇出了%d点' % current)
            if current == 7:
                time.sleep(2)
                print('庄家胜')
                money -= debt
            elif current == first:
                time.sleep(2)
                print('玩家胜')
                money += debt
            else:
                needs_go_on = True
    time.sleep(2)
    print('你破产了, 游戏结束!')


def PositiveInteger(num):
    """
    求阶乘
    :param num:
    :return:
    """
    result = 1
    for n in range(1, num + 1):
        result *= n
    return result


if __name__ == '__main__':
    # 求水仙花数
    print("水仙花数: %s" % NumberDaffodils())
    # 数值反转
    print("数值反转: %s" % ValueInversion(12345))
    # 百钱白鸡问题
    HundredChickens()
    # Craps游戏
    # CrapsGame()
    print(PositiveInteger(10) // PositiveInteger(20) // PositiveInteger(30))
