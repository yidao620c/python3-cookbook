#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 跳过可迭代对象开始部分
Desc : 
"""
from itertools import dropwhile
from itertools import islice


def skip_iter():
    # with open('/etc/passwd') as f:
    #     for line in dropwhile(lambda line: not line.startswith('#'), f):
    #         print(line, end='')

    # 明确知道了要跳过的元素序号
    items = ['a', 'b', 'c', 1, 4, 10, 15]
    for x in islice(items, 3, None):
        print(x)

if __name__ == '__main__':
    skip_iter()


