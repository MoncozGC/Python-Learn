# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/1/12 16:41
# Desc  : python修改属性值

class Car(object):
    """模拟汽车的例子"""

    def __init__(self, make, model, year):
        """初始化描述汽车的属性"""
        self.make = make
        self.model = model
        self.year = year
        self.odometer_reading = 0

    def get_descriptive(self):
        """返回整洁的描述性信息"""
        long_name = f"{self.year} {self.make} {self.model}"
        return long_name.title()

    def read_odometer(self):
        """打印一条汽车里程信息"""
        print(f"This car has {self.odometer_reading} miles on it.")


my_car = Car('audi', 'a8', 2018)
print(my_car.get_descriptive())
my_car.read_odometer()

print("----------直接修改属性值----------")

my_car.odometer_reading = 100
my_car.read_odometer()

my_car.read_odometer()

if __name__ == '__main__':
    n = 2
    s = "pq"
    print(s * n)
