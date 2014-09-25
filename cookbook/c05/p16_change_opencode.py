#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 增加/修改已打开文件的编码
Desc : 
"""
import urllib.request
import io
import sys


def change_open_encode():
    u = urllib.request.urlopen('http://www.python.org')
    f = io.TextIOWrapper(u, encoding='utf-8')
    text = f.read()

    print(sys.stdout.encoding)
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='latin-1')
    print(sys.stdout.encoding)

    f = open('sample.txt','w')
    print(f)
    print(f.buffer)
    print(f.buffer.raw)


if __name__ == '__main__':
    change_open_encode()
