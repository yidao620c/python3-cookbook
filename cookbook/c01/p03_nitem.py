#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: collections.deque演示
Desc : deque有一个maxlen参数，当append的时候，如果超过，那么最前面的就被挤出队列。
"""
from collections import deque


def search(lines, pattern, history=5):
    previous_lines = deque(maxlen=history)
    for li in lines:
        if pattern in li:
            yield li, previous_lines
        previous_lines.append(li)

# Example use on a file
if __name__ == '__main__':
    with open(r'../../cookbook/somefile.txt') as f:
        for line, prevlines in search(f, 'Python', 5):
            for pline in prevlines:
                print(pline, end='')
            print(line, end='')
            print('-' * 20)



