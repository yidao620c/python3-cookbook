#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 检查字符串开始或结尾
Desc : 
"""
import re
import os
from urllib.request import urlopen


def start_end():
    filename = 'spam.txt'
    print(filename.endswith('.txt'))
    print(filename.startswith('file:'))
    url = 'http://www.python.org'
    print(url.startswith('http:'))

    filenames = os.listdir('.')
    print(filenames)
    print([name for name in filenames if name.endswith(('.py', '.c'))])
    print(any(name.endswith('.py') for name in filenames))

    choices = ['http:', 'ftp:']
    url = 'http://www.python.org'
    url.startswith(tuple(choices))

    # 切片实现，看上去不美
    filename = 'spam.txt'
    print(filename[-4:] == '.txt')
    url = 'http://www.python.org'
    print(url[:5] == 'http:' or url[:6] == 'https:' or url[:4] == 'ftp:')

    # 正则式实现
    url = 'http://www.python.org'
    print(re.match('http:|https:|ftp:', url))


def read_data(name):
        if name.startswith(('http:', 'https:', 'ftp:')):
            return urlopen(name).read()
        else:
            with open(name) as f:
                return f.read()

if __name__ == '__main__':
    start_end()

