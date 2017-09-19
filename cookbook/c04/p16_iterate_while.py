#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 使用迭代器重写while无限循环
Desc : 
"""
import sys


def reader(s, size):
    while True:
        data = s.recv(size)
        if data == b'':
            break
            # process_data(data)


def reader2(s, size):
    for data in iter(lambda: s.recv(size), b''):
        process_data(data)


def iterate_while():
    CHUNKSIZE = 8192
    with open('/etc/passwd') as f:
        for chunk in iter(lambda: f.read(10), ''):
            n = sys.stdout.write(chunk)


if __name__ == '__main__':
    iterate_while()
