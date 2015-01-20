#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: 基准测试
    Desc : 
"""
from timeit import timeit

__author__ = 'Xiong Neng'


class Stock():
    # 鼓励使用__slots__提升性能
    __slots__ = ["name", "shares", "price"]
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


def my_timeit():
    cdeque = """
import collections
s = collections.deque()
"""
    t1 = timeit("s.appendleft(37)", cdeque, number=100000)
    t2 = timeit("s.insert(0, 37)",
                "s=[]", number=100000)
    print("t1=", t1)
    print("t2=", t2)
    pass


def main():
    my_timeit()


if __name__ == '__main__':
    main()
