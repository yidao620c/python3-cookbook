#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc : 
"""


def read_demo():
    """读取文本文件"""
    with open(r'D:\work\readme.txt', 'r', encoding='utf-8') as f:
        for line in f:
            print(line, end='')  # 这里必须用end=''，因为line里有换行，而print也会加换行
    with open(r'D:\work\readme.txt', 'ab+') as f:
        pass


if __name__ == '__main__':
    read_demo()