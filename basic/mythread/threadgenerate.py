#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: 协程与微线程
    Desc : 
"""
from collections import deque

__author__ = 'Xiong Neng'


def foo():
    for n in range(5):
        print('I\'m foo %d' % n)
        yield


def bar():
    for n in range(10):
        print("I'm bar %d" % n)
        yield


def spam():
    for n in range(7):
        print("I'm spam %d" % n)


def demo():
    taskqueue = deque()
    taskqueue.append(foo())
    taskqueue.append(bar())
    taskqueue.append(spam())
    while taskqueue:
        task = taskqueue.pop()
        try:
            task.__next__()
            taskqueue.appendleft(task)
        except (StopIteration, AttributeError):
            pass


if __name__ == '__main__':
    demo()
