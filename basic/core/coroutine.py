#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: 协程与yield表达式
    Desc : 
"""
import os
import fnmatch
import sys
from functools import wraps

__author__ = 'Xiong Neng'


def coroutine(func):
    """协程中很容易忘记调用__next__()，因此弄个装饰器"""
    @wraps(func)
    def start(*args, **kwargs):
        g = func(*args, **kwargs)
        g.__next__()
        return g

    return start


@coroutine
def receiver():
    print("ready to receive...")
    while True:
        n = (yield)
        print("got %s" % n)


@coroutine
def line_split(delimiter=None):
    """send()返回值：传递给下一个yield语句的值"""
    print("ready to split")
    result = None
    while True:
        line = (yield result)
        result = line.split(delimiter)


@coroutine
def find_files(target):
    while True:
        topdir, patternc = (yield)
        for path, dirname, filelist in os.walk(topdir):
            for name in filelist:
                if fnmatch.fnmatch(name, patternc):
                    target.send(os.path.join(path, name))


import gzip, bz2


@coroutine
def opener(target):
    while True:
        name = (yield)
        if name.endswith(".gz"):
            f = gzip.open(name)
        elif name.endswith(".bz2"):
            f = bz2.BZ2File(name)
        else:
            f = open(name, encoding='utf-8')
        target.send(f)


@coroutine
def cat(target):
    while True:
        f = (yield)
        for line in f:
            target.send(line)


@coroutine
def grep(pattern, target):
    while True:
        line = (yield)
        if pattern in line:
            target.send(line)


@coroutine
def printer():
    while True:
        line = (yield)
        sys.stdout.write(line)


def main():
    r = receiver()
    r.send("hello")

    s = line_split(",")
    print(s.send("A,B,C"))
    print(s.send("100,200,300"))

    # 协程实现管道流
    finder = find_files(opener(cat(grep("python", printer()))))
    finder.send(("D:/logs", "thinking*"))
    finder.send(("D:/errlogs", "thinking*"))


if __name__ == '__main__':
    main()
