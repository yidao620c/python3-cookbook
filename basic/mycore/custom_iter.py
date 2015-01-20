#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: sample
    Desc : 自定义迭代器
"""
from random import choice
__author__ = 'Xiong Neng'


# 随机序列迭代器
class RandomSeq(object):
    def __init__(self, seq):
        self.seq = seq

    def __iter__(self):
        return self

    def next(self):
        return choice(self.seq)


# 任意项的迭代器
class AnyIter(object):
    def __init__(self, data, safe=False):
        self.safe = safe
        self.iter = iter(data)

    def __iter__(self):
        return self

    def next(self, howmany=1):
        retval = []
        for eachItem in range(howmany):
            try:
                retval.append(self.iter.next())
            except StopIteration:
                if self.safe:
                    break
                else:
                    raise
        return retval


def main():
    aa = AnyIter(range(10))
    myiter = iter(aa)  # 获取a的迭代器对象
    print(type(myiter))
    for j in range(1, 5):
        print('%02d : %s' % (j, myiter.next(j)))

    m = None
    n = ''
    k = ''
    print(id(m))
    print(id(n))
    print(id(k))

if __name__ == '__main__':
    main()