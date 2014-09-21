#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 输出重定向到文件
Desc : 
"""


def print_tofile():
    with open('somefile.txt', 'rt') as f:
        print('Hello World!', file=f)

if __name__ == '__main__':
    print_tofile()