#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: sample
    Desc : 
"""
import sys, os

__author__ = 'Xiong Neng'


# def test_f(fmt, *args, exc_info, extra):
# return 2 if True else None

def aa():
    for x in range(1, 10):
        for y in range(1, x + 2):
            yield '%d * %d = %d\t' % (y, x, x * y) if y <= x else '\n'
            print('ddd')
b=1
def bb():
    a=b+2
    print(a)


if __name__ == '__main__':
    a = 1
    bb()

