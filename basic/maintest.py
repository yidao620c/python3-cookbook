#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: main测试类
Desc : 
"""
import os


if __name__ == '__main__':
    print('----start----')
    print('abcd'[:-1])
    print(type('abcd'[:-1]))
    print(os.path.abspath(os.path.join(r'd:\tmp\work', '..', 'aaa.zip')))

