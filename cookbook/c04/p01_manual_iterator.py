#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 手动遍历迭代器
Desc : 
"""


def manual_iter():
    with open('/etc/passwd') as f:
        try:
            while True:
                line = next(f)
                print(line, end='')
        except StopIteration:
            pass

def manual_iter2():
    with open('/etc/passwd') as f:
        while True:
            line = next(f)
            if line is None:
                break
            print(line, end='')


if __name__ == '__main__':
    manual_iter()