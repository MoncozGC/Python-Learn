"""
encoding: utf-8
Author: MoncozGC
Date  : 2021/12/29 15:40
Desc  : self在Python中的用途
self在定义时需要定义，但是在调用时会自动传入。
self总是指调用时的类的实例。
"""


class Person:
    def prf(self):
        # self代表的是类的实例
        print(self)
        # self.__class_才是指向类
        print(self.__class__)
        print("master 生产")

    def prf2(self):
        print(self)


# p = Person()
# p.prf()
# p.prf2()

class Parent:
    def pprt(self):
        print(self)


class Child(Parent):
    def cprt(self):
        print(self)


c = Child()
c.cprt()
c.pprt()
p = Parent()
p.pprt()

# x = open("./datas.txt", "a+")
# print("hellWord", file=x)
# x.close()

print("hello\bworld")

