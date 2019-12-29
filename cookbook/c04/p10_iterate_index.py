#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 迭代并跟踪索引
Desc : 
"""
from collections import defaultdict


def iterate_index():
    my_list = ['a', 'b', 'c']
    for idx, val in enumerate(my_list):
        print(idx, val)
    # 索引从1开始
    for idx, val in enumerate(my_list, 1):
        print(idx, val)

    # 序列中含有元组的解压
    data = [ (1, 2), (3, 4), (5, 6), (7, 8) ]
    for n, (x, y) in enumerate(data):
        print(n)
        print(x, y)


def parse_data(filename):
        with open(filename, 'rt') as f:
            for lineno, line in enumerate(f, 1):
                fields = line.split()
                try:
                    count = int(fields[1])
                    # ...
                except ValueError as e:
                    print('Line {}: Parse error: {}'.format(lineno, e))


def word_lines():
    word_summary = defaultdict(list)
    with open('myfile.txt', 'r') as f:
        lines = f.readlines()
    for idx, line in enumerate(lines):
        # Create a list of words in current line
        words = [w.strip().lower() for w in line.split()]
        for word in words:
            word_summary[word].append(idx)

if __name__ == '__main__':
    iterate_index()

