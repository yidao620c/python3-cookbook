#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 单例模式
Desc : 实际上python里面不需要单例模式，直接用模块就行了
"""


def singleton(cls, *args, **kw):
    """定义一个单例装饰器"""
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@singleton
class MyClass(object):
    a = 1

    def __init__(self, x=0):
        self.x = x

if __name__ == '__main__':
    one = MyClass()
    two = MyClass()
    print(one.a)
    one.a = 2
    print(two.a)
