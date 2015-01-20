#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 工厂方法
Desc : 抽象工厂中定义一个方法，其中会有参数输入，
       而实现类通过传入的参数判断该生产出哪种对象
"""


class ConcreteProduct1:
    def output(self):
        print('ConcreteProduct1')


class ConcreteProduct2:
    def output(self):
        print('ConcreteProduct2')


class Creator:
    def create_product(self, type):
        return {'1': ConcreteProduct1(), '2': ConcreteProduct2()}[type]

if __name__ == '__main__':
    creator = Creator()
    creator.create_product('1').output()
    creator.create_product('2').output()

