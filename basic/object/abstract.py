#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: python中的抽象基类
    Desc : 
"""
from abc import ABCMeta, abstractmethod, abstractproperty

__author__ = 'Xiong Neng'


class Foo(metaclass=ABCMeta):
    @abstractmethod
    def spam(self, a, b):
        """子类给我必须实现这个抽象方法"""
        pass

    @abstractproperty
    def name(self):
        """子类给我必须实现这个特性"""
        pass

class Grok():
    def spam(self, a, b):
        print("Grok...")

def main():
    Foo.register(Grok)  # 向抽象基类注册
    pass


if __name__ == '__main__':
    main()
