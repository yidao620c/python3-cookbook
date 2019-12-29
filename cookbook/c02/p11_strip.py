#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 去除字符串中多余字符
Desc : 
"""
import re


def strip_str():
    s = ' hello world \n'
    print(s.strip())
    print(s.lstrip())
    print(s.rstrip())

    # Character stripping
    t = '-----hello====='
    print(t.lstrip('-'))
    print(t.strip('-='))

    # 对中间不会影响
    s = ' hello     world \n'
    print(s.strip())

    print(s.replace(' ', ''))
    print(re.sub('\s+', ' ', s))

    # 生成器表达式
    with open('filename') as f:
        lines = (line.strip() for line in f)
        for line in lines:
            pass


if __name__ == '__main__':
    strip_str()

