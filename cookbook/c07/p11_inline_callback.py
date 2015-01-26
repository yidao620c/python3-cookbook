#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 内联回调函数
Desc : 
"""
from queue import Queue
from functools import wraps


def apply_async(func, args, *, callback):
    # Compute the result
    result = func(*args)

    # Invoke the callback with the result
    callback(result)


class Async:
    def __init__(self, func, args):
        self.func = func
        self.args = args


def inlined_async(func):
    @wraps(func)
    def wrapper(*args):
        f = func(*args)
        result_queue = Queue()
        result_queue.put(None)
        while True:
            print('1' * 15)
            result = result_queue.get()
            print('2' * 15)
            try:
                print('3' * 15)
                print('result={}'.format(result))
                a = f.send(result)
                print('4' * 15)
                apply_async(a.func, a.args, callback=result_queue.put)
                print('5' * 15)
            except StopIteration:
                break

    return wrapper


def add(x, y):
    return x + y


@inlined_async
def test():
    print('start'.center(20, '='))
    r = yield Async(add, (2, 3))
    print('last={}'.format(r))
    r = yield Async(add, ('hello', 'world'))
    print('last={}'.format(r))
    # for n in range(10):
    # r = yield Async(add, (n, n))
    # print(r)
    # print('Goodbye')
    print('end'.center(20, '='))


if __name__ == '__main__':
    test()