# encoding: utf-8
"""
    Topic: sample
    Desc :
        Python生成器：生成器是一个带有yield语句的函数。
        一个生成器能暂停并返回一个中间结果，返回这个值给调用者并暂停执行。
        当生产器的next()方法被调用时，它会准确的从离开的那个地方继续
"""
from random import randint

__author__ = 'Xiong Neng'


# 生成器函数定义
def simpleGen():
    yield 1
    yield '2--->punch'


def gendemo():
    print(simpleGen().__next__())
    print(simpleGen().__next__())

    # 生成器对象的获取
    a = simpleGen()
    print(a.__next__())
    print(a.__next__())

    # Python的for循环有next()调用和对StopIteration的处理
    # 天生就是使用生成器的好手段
    for eachItem in simpleGen():
        print(eachItem)


# 序列的随机迭代器 pop index out of range ？？？？？？
def randGen(alist):
    while len(alist) > 0:
        yield alist.pop(randint(0, len(alist)))


def counter(start_at=0):
    print('new start...%d' % (start_at,))
    count = start_at
    while True:
        val = (yield count)
        print('count=%s, val=%s' % (count, val,))
        if val is not None:
            count = val
        else:
            count += 1


if __name__ == '__main__':
    count = counter(5)
    print(count.__next__())
    print(count.__next__())
    print(count.__next__())
    print(count.send(99))
    print(count.__next__())
    count.close()
    # print(count.next())  # ERROR


