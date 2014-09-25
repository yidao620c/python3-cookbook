#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 在文本模式文件中写入字节
Desc : 
"""
import sys


def bytes_tofile():
    sys.stdout.buffer.write(b'Hello\n')

if __name__ == '__main__':
    bytes_tofile()

