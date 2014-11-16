#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 抽象工厂模式
Desc : 为创建一组相关或相互依赖的对象提供一个借口，而且无需指定它们的具体类
"""


class ProductA1:
    def do_something(self):
        print('产品A1的实现方法')


class ProductA2:
    def do_something(self):
        print('产品A2的实现方法')


class ProductB1:
    def do_something(self):
        print('产品B1的实现方法')


class ProductB2:
    def do_something(self):
        print('产品B2的实现方法')


class Creator1:
    """生产系列1的产品"""
    def create_product_a(self):
        return ProductA1()

    def create_product_b(self):
        return ProductB1()


class Creator2:
    """生产系列2的产品"""
    def create_product_a(self):
        return ProductA2()

    def create_product_b(self):
        return ProductB2()
