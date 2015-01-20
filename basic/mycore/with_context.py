#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: 上下文管理与with
    Desc : 
"""
from contextlib import contextmanager

__author__ = 'Xiong Neng'


@contextmanager
def ListTransaction(thelist):
    """自定义上下文管理器，如果引发异常，
    将以异常形式出现在生成器函数中，如果需要可以捕获，否则传递出去了"""
    workcopy = list(thelist)
    yield workcopy

    # 仅在没有出现错误时才会修改原始列表
    thelist[:] = workcopy


def main():
    items = [1, 2, 3]
    try:
        with ListTransaction(items) as working:
            working.append(6)
            working.append(7)
            raise RuntimeError("We're hosed")
    except RuntimeError:
        pass
    print(items)


if __name__ == '__main__':
    main()
