#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 字符串合并
Desc : 
"""


def combine(source, maxsize):
    parts = []
    size = 0
    for part in source:
        parts.append(part)
        size += len(part)
        if size > maxsize:
            yield ''.join(parts)
            parts = []
            size = 0
        yield ' '.join(parts)


def sample():
    yield 'Is'
    yield 'Chicago'
    yield 'Not'
    yield 'Chicago?'


def join_str():
    parts = ['Is', 'Chicago', 'Not', 'Chicago?']
    print(' '.join(parts))
    print(','.join(parts))
    print(''.join(parts))

    # 使用+
    a = 'Is Chicago'
    b = 'Not Chicago?'
    c = 'ccc'
    print(a + ' ' + b)

    data = ['ACME', 50, 91.1]
    print(','.join(str(d) for d in data))


    print(a + ':' + b + ':' + c)  # Ugly
    print(':'.join([a, b, c]))  # Still ugly
    print(a, b, c, sep=':')  # Better

    # 混合方案
    # with open('filename', 'w') as f:
    #     for part in combine(sample(), 32768):
    #         f.write(part)
    for part in combine(sample(), 32768):
        print(part)

if __name__ == '__main__':
    join_str()

