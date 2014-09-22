#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 字符串的I/O操作
Desc : 
"""
import io


def string_io():
    s = io.StringIO()
    s.write('Hello World\n')
    print('This is a test', file=s)
    # Get all of the data written so far
    print(s.getvalue())

    # Wrap a file interface around an existing string
    s = io.StringIO('Hello\nWorld\n')
    print(s.read(4))
    print(s.read())

if __name__ == '__main__':
    string_io()

