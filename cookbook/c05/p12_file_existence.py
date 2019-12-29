#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 测试文件或目录是否存在
Desc : 
"""
import os
import time


def file_existence():
    print(os.path.exists('/etc/passwd'))
    print(os.path.exists('/tmp/spam'))

    print(os.path.isfile('/etc/passwd'))
    print(os.path.isdir('/etc/passwd'))
    print(os.path.islink('/usr/local/bin/python3'))
    print(os.path.realpath('/usr/local/bin/python3'))

    print(os.path.getsize('/etc/passwd'))
    print(os.path.getmtime('/etc/passwd'))
    print(time.ctime(os.path.getmtime('/etc/passwd')))


if __name__ == '__main__':
    file_existence()

