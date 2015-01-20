#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: sample
    Desc : 包装对象简例
        引用一个属性时，python解释器试着在局部名称空间中查找那个名字，
        比如一个自定义的方法或局部实例属性，如果没有在局部字典中找到，
        则搜索类名称空间，以防一个类属性被访问（Class属性，类似于静态变量）
        如果两类搜索都失败了，搜索则对原对象开始授权请求，此时，__getattr__()被调用
    注：属性可以是数据属性，还可以是函数或方法
"""
from time import time, ctime

__author__ = 'Xiong Neng'


class WrapMe(object):
    def __init__(self, obj):
        self.__data = obj

    def get(self):
        return self.__data

    def __repr__(self):
        return repr(self.__data)

    def __str__(self):
        return str(self.__data)

    # 仅仅在属性找不到时调用
    def __getattr__(self, item):
        print('I call the __getattr__ method - '),
        return getattr(self.__data, item)

    # 无论何时都会调用
    def __getattribute__(self, item):
        print('I call the __getattribute__ method - '),
        return super(WrapMe, self).__getattribute__(item)

    def mymethod(self):
        print('hahaha')


wr = WrapMe(3.5 + 4.2j)
print(wr)
print(wr.real)
print(wr.imag)
ee = wr.get
wr.mymethod()


class TimeWrapMe(object):
    def __init__(self, obj):
        self.__data = obj
        self.__ctime = self.__mtime = self.__atime = time()

    def get(self):
        return self.__data

    def getTimeVal(self, tType):
        if not isinstance(tType, str) or tType[0] not in 'cma':
            raise (TypeError, "argument 'c', 'm', 'a'")
        return getattr(self, '_%s__%stime' %
                             (self.__class__.__name__, tType[0]))

    def getTimeStr(self, tType):
        return ctime(self.getTimeVal(tType))

    def set(self, obj):
        self.__data = obj
        self.__mtime = self.__atime = time()

    def __repr__(self):
        self.__atime = time()
        return repr(self.__data)

    def __str__(self):
        self.__atime = time()
        return str(self.__data)

    def __getattr__(self, item):  # delegate
        self.__atime = time()
        return getattr(self.__data, item)


class Haha(object):
    pass


def main():
    haha = Haha()
    haha.name = 'name'

    print(haha.__dict__)
    print(Haha.__dict__)

if __name__ == '__main__':
    main()

