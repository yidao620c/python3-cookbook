#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 忽略文件名编码
Desc : 
"""
import sys


def bypass_encoding():
    print(sys.getfilesystemencoding())

if __name__ == '__main__':
    bypass_encoding()

