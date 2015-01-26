#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 带状态值的回调函数
Desc : 
"""


def apply_async(func, args, *, callback):
    # Compute the result
    result = func(*args)

    # Invoke the callback with the result
    callback(result)


def add(x, y):
    return x + y


# 类方案
class ResultHandler:

    def __init__(self):
        self.sequence = 0

    def handler(self, result):
        self.sequence += 1
        print('[{}] Got: {}'.format(self.sequence, result))

r = ResultHandler()
apply_async(add, (2, 3), callback=r.handler)
apply_async(add, ('hello', 'world'), callback=r.handler)


# 闭包方案
def make_handler():
    sequence = 0
    def handler(result):
        nonlocal sequence
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))
    return handler

handler = make_handler()
apply_async(add, (2, 3), callback=handler)
apply_async(add, ('hello', 'world'), callback=handler)


# 协程方案
def make_handler():
    sequence = 0
    while True:
        result = yield
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))

handler = make_handler()
next(handler) # Advance to the yield
apply_async(add, (2, 3), callback=handler.send)
apply_async(add, ('hello', 'world'), callback=handler.send)

