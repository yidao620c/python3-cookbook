#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 模板方法模式
Desc : 
"""


class AbstractTemplate:
    # 基本方法1
    def do_something(self):
        pass

    # 基本方法2
    def do_anything(self):
        pass

    # 模板方法
    def template_method(self):
        # 调用基本方法，完成相关的业务逻辑
        self.do_something()
        self.do_anything()


class ConcreteClass1(AbstractTemplate):
    # 基本方法1
    def do_something(self):
        print('class1 doSomething...')

    # 基本方法2
    def do_anything(self):
        print('class1 doAnything...')


class ConcreteClass2(AbstractTemplate):
    # 基本方法1
    def do_something(self):
        print('class2 doSomething...')

    # 基本方法2
    def do_anything(self):
        print('class2 doAnything...')

if __name__ == '__main__':
    c1 = ConcreteClass1()
    c1.template_method()
    c2 = ConcreteClass2()
    c2.template_method()