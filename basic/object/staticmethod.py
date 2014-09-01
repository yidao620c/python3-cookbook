#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: 对象的绑定和非绑定方法
    Desc : 
"""

__author__ = 'Xiong Neng'


class Foo():
    def ins_method(self, args):
        print("ins_method")

    @classmethod
    def class_method(cls, args):
        print("class_method")

    @staticmethod
    def static_method(args):
        print("static_method")


class Bar(Foo):
    pass


def subclass_instance():
    bar = Bar()
    print(issubclass(Bar, Foo))
    print(issubclass(Foo, object))
    print(issubclass(Bar, object))
    print(isinstance(bar, Bar))
    print(isinstance(bar, Foo))


def main():
    pass


if __name__ == '__main__':
    main()
