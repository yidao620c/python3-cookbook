#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: Builder模式
Desc :
在Builder模式中，有如下3个角色：
1，Product产品类
通常是实现了模板方法模式，也就是有模板方法和基本方法
2，Builder类
可随时返回一个组建好的产品对象
3，Director导演类
负责安排已有模块的顺序，然后告诉Builder怎样建造产品对象
"""


class Product:
    def do_something(self):
        print('do_something')

    def do_otherthing(self):
        print('do_otherthing')


class Builder:
    def __init__(self, product):
        self.product = product

    def build_something(self):
        self.product.do_something()

    def build_otherthing(self):
        self.product.do_otherthing()

    def build_product(self):
        return self.product


class Director:
    def __init__(self):
        self.builder = Builder(Product())

    def get_product_a(self):
        self.builder.build_something()
        return self.builder.build_product()

    def get_product_b(self):
        self.builder.build_something()
        self.builder.build_otherthing()
        return self.builder.build_product()

if __name__ == '__main__':
    director = Director()
    director.get_product_a()
    print('-----------------')
    director.get_product_b()